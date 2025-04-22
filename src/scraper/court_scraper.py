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
        court_name_elem = self.case_soup.find("b")
        
        court_name_string = court_name_elem.get_text(strip=True) if court_name_elem else "Unknown Court"

        print(court_name_string)
        for c in CITY_SET:
            city_pattern = rf"\b{re.escape(c.lower())}\b"
            if re.search(city_pattern, court_name_string.lower()):
                self.city = c    

        return self.city # returning city name for easier debugging in main/nb

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
                pattern = r"\bAM|PM\b"
                if re.search(pattern, text):
                    rows_with_times.append(row)


        case_count = 1       
        row_texts_messy = []
        for row in rows_with_times:
            spans = row.find_all("span")     
            texts = [span.text.strip() for span in spans]
            row_texts_messy.append(texts)
            case_count += 1 
        print(f"{self.city}: number of rows of messy texts containing regex pattern (pre-cases): {case_count}")
        return row_texts_messy
       


    def _process_rows_to_cases(self, messy_texts, date):
        """Converts each row into a court case object."""
        court_cases = []
    
        
        for row in messy_texts:   

            try:
                if len(row)>8:
                    print(f"row lenght longer than 8, this may introduce bad data/None values") #TODO fix this, leaving them out for now
                    continue
                    try:
                        start_time_span, duration_span, case_details_span, hearing_type_span, hearing_channel_span = row[2:7]
                    except Exception as e:
                        print(f"tried to unpack, and got exception: {e}")
                        continue
                elif len(row) == 8:
                    print("88888888888888")
                    start_time_span, duration_span, case_details_span_1, case_details_span_2, hearing_type_span, hearing_channel_span = row[2:8]
                    case_details_span = case_details_span_1 + case_details_span_2
                elif len(row) == 7:
                    print("77777777777")
                    start_time_span, duration_span, case_details_span, hearing_type_span, hearing_channel_span = row[2:7]
                elif len(row) == 6: # No rows have six?
                    print("66666666666")
                    _, start_time_span, duration_span, case_details_span, hearing_type_span, hearing_channel_span = row
                elif len(row) == 5:
                    print("5555555555")
                    start_time_span, duration_span, case_details_span, hearing_type_span, hearing_channel_span = row
                else:
                    print(f"unexpected row size, skipping this one {row}")
                    continue
            
                # TODO some of the case details td cells have two spans in, use the re.search for v to find these cells and conditional
                # for two spans, consequently joining the inner text into one case details var... maybe can do this before then feeding the rows in?
           
                start_time_span = (" ".join(start_time_span.split()))
                hearing_channel_span = " ".join(hearing_channel_span.split())
                hearing_type_span = " ".join(hearing_type_span.split())

                case_details_list = case_details_span.split(" ")
                case_id = case_details_list[0]

                print(case_details_span)
                print(case_details_list)

                details_span_less_case_id = (" ").join(case_details_list[1:])


                if re.search(r' v |vs|-v-|-V-', case_details_span): 
                 
                    match = re.search(r"(.+?)\s*(?:v|vs|-v-|-V-|-V-)\s*(.+)", details_span_less_case_id) 
                    if match: # maybe there is a bug where the first research passes and the second one doesnt?
                        claimant = match.group(1).strip()
                        defendant = match.group(2).strip()
                        court_case = CourtCase(
                            case_id,
                            start_time_span,
                            date,
                            duration_span,
                            case_details_span,
                            claimant,
                            defendant,
                            False,
                            hearing_type_span,
                            hearing_channel_span,
                            self.city
                        )
                        court_cases.append(court_case)
                # TODO this is not being reached... only effs in the db.
                elif re.search(r"a minor", details_span_less_case_id.lower()):
                    print("ppowoiewpoiepwi")
                    if len(case_details_list) == 5:  # TODO think about this... why am i doing this if else clause? there was a case where it made sense I think? length 5??/
                        court_case = CourtCase(
                        case_id,
                        start_time_span,
                        date,
                        duration_span,
                        case_details_span,
                        None,
                        None,
                        True,
                        hearing_type_span,
                        hearing_channel_span,
                        self.city
                        )
                        court_cases.append(court_case)


                    else: 
                            court_case = CourtCase(
                            case_id,
                            start_time_span,
                            date,
                            duration_span,
                            case_details_span,
                            None,
                            None,
                            True,
                            hearing_type_span,
                            hearing_channel_span,
                            self.city
                        )
                            court_cases.append(court_case)

                
            except (IndexError, ValueError)  as e:
                print(f"issue with unpacking {e}\n Row: {row}") # this may now be redundant due to the elif chain?     
        return court_cases
        
            

    def rows_to_objects(self, date):
        
        raw_row_texts = self._extract_case_rows()
        court_cases = self._process_rows_to_cases(raw_row_texts, date)
        return court_cases
