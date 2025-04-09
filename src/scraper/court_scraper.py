class CourtScraper:
    def __init__(self, session, court_url):
        self.session = session
        self.court_url = court_url
        self.city = None
        self.court_name = None
        self.case_rows = None

    def load_case_page(self):
        #load page of cases from url
        pass

    def extract_city_and_court_name(self):
        pass

    def extract_case_rows(self):
        pass
    def to_court_case_objects(self):
        pass
