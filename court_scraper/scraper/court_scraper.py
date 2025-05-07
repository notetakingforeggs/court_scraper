
from court_scraper.scraper.clients.court_client import CourtClient
from court_scraper.scraper.parsers.entry_page_parser import EntryPageParser
from court_scraper.db.db_methods import get_court_id_by_city, insert_court_case
from court_scraper.scraper.session import BASE_URL
from court_scraper.scraper.flavours import flavours

CASE_LIST_BASE_URL = "https://www.courtserve.net/courtlists/viewcourtlistv2.php"

class CourtScraper:
    def __init__(self, session, links_and_dates):

        self.session = session
        self.links_and_dates = links_and_dates
        self.new_tab_url = None
        self.city = None
        self.court_name = None # am i just going to collapse city and court name? so far unused i think
        self.case_rows = None
        self.case_soup = None

        self.court_client = CourtClient(self.session, BASE_URL)

    # passing session from main where it is returned from the session/login call. BASE URL in main also?
    def run(self): # this function orchestrates the scraping process, and should be called from main and takes the links and dates list from the county court list scrape (change this at some point maybe?)
        # Most methods below are from this class, but i now need to move them elsewhere and call them from here.

    
        for i, (link, date) in enumerate (self.links_and_dates):
            if i < 1:
                continue
            
            # use http client to get html for entry page
            entry_page_response_text = self.court_client.fetch_entry_page(link) # TODO lost conditional check for new tab url here.

            # initialise a parser for the entry page and find the new tab url
            entry_page_parser =  EntryPageParser(entry_page_response_text)
            new_tab_url = entry_page_parser.parse_for_new_tab_url()

            # use the http client to get the text from the daily cause list page
            case_list_response_text = self.court_client.fetch_case_list(CASE_LIST_BASE_URL + new_tab_url)            
      
            # check case list page for flavor
            flavour = flavours.detect_Flavour(case_list_response_text)
           
            # init another parser, specifically for daily cause list pages and use it to get the city
            court_list_parser  = flavour.parser_class(case_list_response_text)

            # debug line to work with specific flavours only - uncomment as needed
            # if isinstance(court_list_parser, Flavour1DailyCauseListParser):
            #     print("Flavour x SKIPPING")
            #     continue

            self.city = court_list_parser.extract_city()

            # use the same parser to extract the rows with desired info in them
            row_texts_messy  = court_list_parser.extract_case_rows()
          
            # init a court case factory and use it to process the rows to a list of court cases
            court_case_factory = flavour.factory_class(row_texts_messy, date, self.city)
            court_cases = court_case_factory.process_rows_to_cases()

            # check list not null, and that each city has a corresponding id in the db (second check could be phased out later maybe?)
            if not court_cases:

                print(f"failure to get court cases for: {self.city}")
                continue
            for case in court_cases: # iterate through scraped court cases and add to db
                court_id = get_court_id_by_city(case.city)

                if not court_id and case.city:
                    print(f"no court id for {case.city}")
                    continue 

                # insert court case into db
                insert_court_case(case, court_id)
            print(f"{self.city} has {len(court_cases)} court cases")

     
