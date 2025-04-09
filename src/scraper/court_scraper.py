from scraper.models import CourtCase
from scraper.session import BASE_URL

from bs4 import BeautifulSoup as bs
from scraper.city_set import CITY_SET;

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
        #load page of cases from url
        # get soup for content of daily causes page using session cookies from inital log in
        response = self.session.get(self.court_url)

        # convert html from request into soup
        soup = bs(response.text, "html.parser")

        # find box containing "open list in new tab" link and get path
        box2 = soup.find("div", id="box2")
        new_tab_anchor = box2.find("a")
        new_tab_url = new_tab_anchor["href"] # get url "open list..." link
        self.new_tab_url = new_tab_url

    def get_case_list_soup(self):
        case_list_response = self.session.get(CASE_LIST_BASE_URL + self.new_tab_url)            
        self.case_soup = bs(case_list_response.text, "html.parser")
        

    def extract_city_and_court_name(self):
            
        # assuming first bold element contains court name, does it always? TODO 
        court_name_elem = self.case_soup.find("b")
        
        court_name_string = court_name_elem.get_text(strip=True) if court_name_elem else "Unknown Court"
        city= ""
        for c in CITY_SET:
            if c.lower() in court_name_string.lower():
                city = c
                print(f" extracted {city} from the court name")  
        self.city = city

        

    def _extract_case_rows(self):


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
            print(f"case nø {case_count}: {texts}")
            case_count += 1 
        return row_texts_messy
       


    def _clean_row_texts(self, messy_texts):
        try:
            for row in messy_texts:          
                _, _, start_time_span, duration_span, case_details_span, hearing_type_span, hearing_channe_span = row
            # case nø 1: ['', '', '10:00 AM', '1 hour', 'AF24P00035 Re A Minor', 'First Hearing and Dispute Resolution Appointment (FHDRA)     (Private Law)', 'In Person']
                print(" ".join(start_time_span.split()))
        except IndexError as e:
            print(f"index error: {e}")

    def get_cleaned_row_texts(self):
        raw = self._extract_case_rows()
        clean = self._clean_row_texts(raw)
        # return clean
        pass

    def to_court_case_objects(self):
        pass



                # case = CourtCase("id", "time", "duration", "claimant", "defendant", "hearing type", "channel")
                # found_cases.append(case)


                
            # go through each entry and get various variables

            # add all to an object

            # call a method which adds all object data to db    