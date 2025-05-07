class CourtClient:
    def __init__(self, session, base_url):
        self.session = session
        self.base_url = base_url

    def fetch_entry_page(self, court_url)-> str:
        print("---------------------------------------------")
        print(f"url for following court:{self.base_url + court_url}")
        response = self.session.get(self.base_url + court_url)
        response.raise_for_status()
        return response.text
    
    def fetch_case_list(self, new_tab_url)->str:
        response = self.session.get(new_tab_url)
        response.raise_for_status()
        return response.text