from scraper.models import CourtCase
from scraper.session import BASE_URL
from bs4 import BeautifulSoup as bs

def parse_cases(session, court_links)-> list[CourtCase]:
    """ Get all the course case info from the list of links and put in db via objects."""
    print("in parser")

    found_cases = []
    total_links = len(court_links)

    for i, link in enumerate(court_links):
        try:
            # get soup for content of daily causes page
            response = session.get(BASE_URL + link)
            soup = bs(response.text, "html.parser")
            box = soup.find("div", id="box2a")
            
            # are there cases where there is no box?
            if not box:
                print("NOBOXNOXBOBXBX DO NOT CONTINUE")
                continue        

            # Extract court name
            court_name_elem = box.find("b")
            court_name = court_name_elem.get_text(strip=True) if court_name_elem else "Unknown Court"
            print(court_name)
            #TODO find specific court name from court name string?
            # scrape from court lists and store in memory as set, and then iterate through to figure out which court each is in


            # Extract and search case details
            for span in box.find_all("span"):
                text = span.get_text().strip().lower()
                if search_term in text:
                    found_case = f"{text} - {court_name}"
                    print(found_case)
                    found_cases.append(found_case)

            # Progress display
            percent_done = int((i / total_links) * 100)
            print(f"Progress: {percent_done}% done")

        except requests.RequestException:
            print(f"Failed to fetch details for {link}")
        except AttributeError:
            continue  # Skip if expected elements are missing

    return found_cases
