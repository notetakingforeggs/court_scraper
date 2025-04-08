from scraper.models import CourtCase
from scraper.session import BASE_URL, login, is_logged_in


from bs4 import BeautifulSoup as bs
import requests
import traceback
import re
from scraper.city_set import CITY_SET;

CASE_LIST_BASE_URL = "https://www.courtserve.net/courtlists/viewcourtlistv2.php"

# nb embedded html not coming through in soup, so must navigate to courtlist in new tab for each court.
def parse_cases(session, court_links): #-> list[CourtCase]:
    """ Get all the course case info from the list of links and put in db via objects."""
    print("IN parse_cases function")
    # print(session.cookies) # should have SITELOKPW to signify accss creds

    found_cases = []

    for link in court_links: #for each county court...
        
        try:
            url = BASE_URL + link                
            # get soup for content of daily causes page using session cookies from inital log in
            response = session.get(url)

            # convert html from request into soup
            soup = bs(response.text, "html.parser")

            # find box containing "open list in new tab" link and get path
            box2 = soup.find("div", id="box2")
            new_tab_anchor = box2.find("a")
            new_tab_url = new_tab_anchor["href"] # get url "open list..." link
            # print(new_tab_url)

       
            # get new page and make soup
            case_list_response = session.get(CASE_LIST_BASE_URL + new_tab_url)            
            soup2 = bs(case_list_response.text, "html.parser")
            # some pages have multiple tables of cases.
            rows = soup2.findAll("tr")
            rows_with_times = []

            for row in rows:
                span = row.find("span")
                if span:
                    text = span.text
                    if "AM" in text or "PM" in text:
                        rows_with_times.append(row)

           
                # for table in valid_tables:      
                #     court_name_elem = table.find("b")
                    
                #     court_name_string = court_name_elem.get_text(strip=True) if court_name_elem else "Unknown Court"
                #     # print(court_name_string)
                #     city= ""
                #     for c in CITY_SET:
                #         if c.lower() in court_name_string.lower():
                #             city = c
                #             print(f" extracted {city} from the court name")
                            

                    # # find valid rows
                    # rows = table.find_all("tr")
                    # valid_rows = []
                    

                # extract text content from valid rows
            case_count = 1
            
            for row in rows_with_times:
                spans = row.find_all("span")     
                texts = [span.text.strip() for span in spans]

                print(f"case nø {case_count}: {texts}")
                case_count += 1 

                # start_time_span, duration_span, case_details_span, hearing_type_span, hearing_channe_span = texts

                # case = CourtCase("id", "time", "duration", "claimant", "defendant", "hearing type", "channel")
                # found_cases.append(case)


                
            # go through each entry and get various variables

            # add all to an object

            # call a method which adds all object data to db    
            

        except requests.RequestException:
            print(f"Failed to fetch details for {link}")
        except AttributeError:
            print("AttributeError")
            continue  # Skip if expected elements are missing
        except :
            print("some other error")
            traceback.print_exc()
    return found_cases


