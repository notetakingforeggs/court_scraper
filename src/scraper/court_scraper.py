# TODO duration needs cleaned but tbh im not really going to use that so can do it later.

from db.models import CourtCase
from bs4 import BeautifulSoup as bs
from utils.city_set import CITY_SET
import re


CASE_LIST_BASE_URL = "https://www.courtserve.net/courtlists/viewcourtlistv2.php"


class CourtScraper:
    def __init__(self, session, court_url):
        self.session = session
        self.court_url = court_url
        self.new_tab_url = None
        self.city = None
        self.court_name = None # am i just going to collapse city and court name? so far unused i think
        self.case_rows = None
        self.case_soup = None

    def load_case_page(self):
        """ Gets new tab urls from each court listing. """
        #load page of cases from url
        # get soup for content of daily causes page using session cookies from inital log in
        response = self.session.get(self.court_url)

        # convert html from request into soup
        soup = bs(response.text, "html.parser")

        # find box containing "open list in new tab" link and get path
        box2 = soup.find("div", id="box2")
        if not box2:
            print(f"no box2 at{self.court_url}")
            return None
        new_tab_anchor = box2.find("a")
        if not new_tab_anchor:
            print(f"no new tab link at {self.court_url}")
            return None
            
        new_tab_url = new_tab_anchor["href"] # get url "open list..." link
        self.new_tab_url = new_tab_url


        # returns the url to allow for conditional continuation
        return new_tab_url

    def get_case_list_soup(self):
        """Gets case list soup from case list page."""

        
        case_list_response = self.session.get(CASE_LIST_BASE_URL + self.new_tab_url)            
        self.case_soup = bs(case_list_response.text, "html.parser")
        

    def extract_city_and_court_name(self):
        """Extracts city and court name from the soup and stores inside the court_scraper object."""
        # assuming first bold element contains court name, does it always? TODO 
        court_name_elem = self.case_soup.find("b")
        
        court_name_string = court_name_elem.get_text(strip=True) if court_name_elem else "Unknown Court"
        city= ""
        print(court_name_string)

        for c in CITY_SET:
            city_pattern = rf"\b{re.escape(c.lower())}\b"
            if re.search(city_pattern, court_name_string.lower()):
                self.city = c    
            if self.city == "Barrow":
                print("barrrooooooooow")
        print(self.city)

        

    def _extract_case_rows(self):
        '''Extract all text from table data tahs in rows.'''

        # select only rows with times in
        rows = self.case_soup.findAll("tr") 
        rows_with_times = []

        for row in rows:
            if row.find("tr"): # ignore rows that contain other rows, as only the most deeply nested are desired to avoid duplication
                continue
            spans = row.find_all("span") # check for AM or PM in the span childs of the row and add to rows with times if found, all desired data has a time associated with it.
            for span in spans:
                text = span.text
                if "AM" in text or "PM" in text:
                    rows_with_times.append(row)

        
        case_count = 1       
        row_texts_messy = []
        for row in rows_with_times:
            spans = row.find_all("span")     
            texts = [span.text.strip() for span in spans]
            row_texts_messy.append(texts)
            case_count += 1 
        return row_texts_messy
       


    def _process_rows_to_cases(self, messy_texts, date):
        """Converts each row into a court case object."""
        court_cases = []
        try:
            
            for row in messy_texts:          
                _, _, start_time_span, duration_span, case_details_span, hearing_type_span, hearing_channel_span = row
                start_time_span = (" ".join(start_time_span.split()))
                hearing_channel_span = " ".join(hearing_channel_span.split())
                hearing_type_span = " ".join(hearing_type_span.split())

                if re.search(r' v |vs|-v-', case_details_span): #TODO ignoring situations in which there is no claimant vs defendant for now, do i need that though?
                    case_details_list = case_details_span.split(" ")
                    case_id = case_details_list[0]

                    parties_string = (" ").join(case_details_list[1:])

                    match = re.search(r"(.+?)\s*(?:v|vs|-v-)\s*(.+)", parties_string) 
                    if match:
                        claimant = match.group(1).strip()
                        defendant = match.group(2).strip()
                    court_case = CourtCase(
                        case_id,
                        start_time_span,
                        date,
                        duration_span,
                        claimant,
                        defendant,
                        hearing_type_span,
                        hearing_channel_span,
                        self.city
                    )
               
                    court_cases.append(court_case)
                    
            return court_cases
        except (IndexError, ValueError) as e:
            # print(f"index error: {e}, likely an issue with the number of items in the row not being the same as the number of values expected for unpacking")
            pass

    def rows_to_objects(self, date):
        
        raw_row_texts = self._extract_case_rows()
        court_cases = self._process_rows_to_cases(raw_row_texts, date)
        return court_cases
