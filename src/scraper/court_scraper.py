# TODO duration needs cleaned but tbh im not really going to use that so can do it later.

from db.models import CourtCase
from bs4 import BeautifulSoup as bs
from utils.city_set import CITY_SET
from utils.time_converter import parse_duration
from scraper.clients.court_client import CourtClient
from scraper.parsers.entry_page_parser import EntryPageParser
from scraper.parsers.court_list_parser import DailyCauseListParser
from db.db_methods import get_court_id_by_city
from factories.court_case_factory import CourtCaseFactory
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

        self.court_client = CourtClient(self.session, CASE_LIST_BASE_URL)

    # passing session from main where it is returned from the session/login call. BASE URL in main also?
    def run(self, links_and_dates, session, BASE_URL): # this function orchestrates the scraping process, and should be called from main and takes the links and dates list from the county court list scrape (change this at some point maybe?)
        # Most methods below are from this class, but i now need to move them elsewhere and call them from here.
        for i, (link, date) in enumerate (links_and_dates):
            if i < 1:
                continue
            
            # can pass sesion and base url from main for now...
            courtScraper = CourtScraper(session, BASE_URL + link) # for each link, initialise a court scraper obj
            
            # this is parsing logic? and http logic? "Entry Page" as it is the page that contains the new tab url that leads to the content thta is visible but as embedded html
            entry_page_response_text = courtScraper.court_client.fetch_list_page(link) # TODO lost conditional check for new tab url here.

            entry_page_parser =  EntryPageParser(entry_page_response_text)

            new_tab_url = entry_page_parser.parse_for_new_tab_url()

            # TODO  courtScraper.get_case_list_soup()
            case_list_response_text = courtScraper.court_client.fetch_list_page(CASE_LIST_BASE_URL + new_tab_url)            
            
            
            # self.case_soup = bs(case_list_response_text, "html.parser")
            # if not self.case_soup:
            #     print("no soup")         

            court_list_parser  = DailyCauseListParser(case_list_response_text)

            city = court_list_parser.extract_city()

            row_texts_messy  = court_list_parser.extract_case_rows()


            
            # TODO rows to objects become factory
            court_case_factory = CourtCaseFactory(date, row_texts_messy)
            court_cases = court_case_factory.process_rows_to_cases()


            if not court_cases:
                print(f"failure to get court cases for: {city}")
                continue
            for case in court_cases: # iterate through scraped court cases and add to db
                court_id = get_court_id_by_city(case.city)

            if not court_id and case.city:
                print(f"no court id for {case.city}")
                continue 
            
            # insert_court_case(case, court_id)
            print(f"{city} has {len(court_cases)} court cases")
            return(case, court_id)



        





    # def load_case_page(self):
    #     """ Gets new tab urls from each court listing. """
    #     #load page of cases from url
    #     # get soup for content of daily causes page using session cookies from inital log in
    #     response = self.session.get(self.court_url)

    #     # convert html from request into soup
    #     soup = bs(response.text, "html.parser")

    #     # find box containing "open list in new tab" link and get path
    #     box2 = soup.find("div", id="box2")
    #     if not box2:
    #         print(f"no box2 at{self.court_url}")
    #         return None
    #     new_tab_anchor = box2.find("a")
    #     if not new_tab_anchor:
    #         print(f"no new tab link at {self.court_url}")
    #         return None
            
    #     new_tab_url = new_tab_anchor["href"] # get url "open list..." link
    #     self.new_tab_url = new_tab_url


    #     # returns the url to allow for conditional continuation
    #     return new_tab_url

    # def get_case_list_soup(self):
    #     """Gets case list soup from case list page."""

        
    #     case_list_response = self.session.get(CASE_LIST_BASE_URL + self.new_tab_url)            
    #     self.case_soup = bs(case_list_response.text, "html.parser")
    #     if not self.case_soup:
    #         print("no soup")
        

    # def extract_city_and_court_name(self):
    #     """Extracts city and court name from the soup and stores inside the court_scraper object."""

    #     court_name_elem = self.case_soup.find("b")
        
    #     court_name_string = court_name_elem.get_text(strip=True) if court_name_elem else "Unknown Court"

    #     print(court_name_string)
    #     for c in CITY_SET:
    #         city_pattern = rf"\b{re.escape(c.lower())}\b"
    #         if re.search(city_pattern, court_name_string.lower()):
    #             self.city = c    

    #     if self.city == None:
    #         print("Issue finding city for this court")# TODO better logging here
    #     return self.city # returning city name for easier debugging in main/nb

    # def _extract_case_rows(self):
    #     '''Extract all text from table data tahs in rows.'''

    #     # select only rows with times in
    #     rows = self.case_soup.findAll("tr") 
    #     rows_with_times = []
        
    #     for row in rows:
    #         if row.find("tr"): # ignore rows that contain other rows, as only the most deeply nested are desired to avoid duplication
    #             continue
    #         spans = row.find_all("span") # check for AM or PM in the span childs of the row and add to rows with times if found, all desired data has a time associated with it.
    #         for span in spans:
    #             text = span.text
    #             pattern = r"\bAM|PM\b"
    #             if re.search(pattern, text):
    #                 rows_with_times.append(row)


    #     case_count = 1       
    #     row_texts_messy = []
    #     for row in rows_with_times:
    #         spans = row.find_all("span")     
    #         texts = [span.text.strip() for span in spans]
    #         row_texts_messy.append(texts)
    #         case_count += 1 
    #     print(f"{self.city}: number of rows of messy texts containing regex pattern (pre-cases): {case_count}")
    #     return row_texts_messy
       


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
                    # print("88888888888888")
                    start_time_span, duration_span, case_details_span_1, case_details_span_2, hearing_type_span, hearing_channel_span = row[2:8]
                    case_details_span = case_details_span_1 + case_details_span_2
                elif len(row) == 7:
                    # print("77777777777")
                    start_time_span, duration_span, case_details_span, hearing_type_span, hearing_channel_span = row[2:7]
                elif len(row) == 6: # No rows have six?
                    # print("66666666666")
                    _, start_time_span, duration_span, case_details_span, hearing_type_span, hearing_channel_span = row
                elif len(row) == 5:
                    # print("5555555555")
                    start_time_span, duration_span, case_details_span, hearing_type_span, hearing_channel_span = row
                else:
                    print(f"unexpected row size, skipping this one {row}")
                    continue
            
                # TODO some of the case details d cells have two spans in, use the re.search for v to find these cells and conditional
                # for two spans, consequently joining the inner text into one case details var... maybe can do this before then feeding the rows in?
           
                start_time_span = (" ".join(start_time_span.split()))
                duration_span = parse_duration(duration_span)
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
                elif re.search(r"a minor", details_span_less_case_id.lower()):
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

