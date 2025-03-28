from scraper.models import CourtCase
from scraper.session import BASE_URL, login


from bs4 import BeautifulSoup as bs
import requests
from scraper.city_set import CITY_SET;

def parse_cases(session, court_links): #-> list[CourtCase]:
    """ Get all the course case info from the list of links and put in db via objects."""
    print("in parser")
    

    found_cases = []
    for link in court_links:
        
        try:
            print("trying to access link and get court case page html")
            url = BASE_URL + link
            
            print(f"this is the url:{url}")
            
            #TODO the issue is session is not valid?
            print("these are the headers")
            print(session.headers)
            
            # get soup for content of daily causes page
            response = session.get(url)

            print("Response Debug Print")
            print(response.status_code)
            print(response.url)
            print(response.headers.get("Content-Type"))
            print(response.text)
        

            soup = bs(response.text, "html.parser")
            # print("this is the text of the soup for the parser")
            box = soup.find("table", class_="MsoNormalTable")
            
            # are there cases where there is no box?
            if not box:
                print("couldnt find what im looking for?")
                continue        

            # Extract court name + city
            court_name_elem = box.find("b")
            court_name_string = court_name_elem.get_text(strip=True) if court_name_elem else "Unknown Court"
            print(court_name_string)
            city= ""
            for c in CITY_SET:
                if c.lower() in court_name_string.lower():
                    city = c
                    break

            # print(city)

            # struggling to find good class selectors for desired rows, thinking to check cells and select for containgin AM/PM
            # find valid rows
            rows = box.find_all("tr")
            valid_rows = []
            for row in rows:
                span = row.find("span")
                if span:
                    text = span.text
                    if "AM" in text or "PM" in text:
                        valid_rows.append(row)

            spans = row.find_all("span")     
            texts = [span.text.strip() for span in spans]
            print(texts)
            start_time_span, duration_span, case_details_span, hearing_type_span, hearing_channe_span = texts

            case = CourtCase("id", "time", "duration", "claimant", "defendant", "hearing type", "channel")
            found_cases.append(case)


            
        # go through each entry and get various variables

        # add all to an object

        # call a method which adds all object data to db    
           

        except requests.RequestException:
            print(f"Failed to fetch details for {link}")
        except AttributeError:
            continue  # Skip if expected elements are missing
    return found_cases


