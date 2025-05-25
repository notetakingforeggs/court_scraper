from typing import Optional 
from court_scraper.utils import city_set
from bs4 import BeautifulSoup as bs
import re



class BaseDailyCauseListParser:
    """
    A daily cause parser must accept `html: str` in its constructor, then implement:

      - extract_city() -> Optional[str]
      - extract_case_rows() -> List[List[str]]

    Both methods should never hit the network or DB—just HTML → data.
    """

    def __init__(self, html:str):
        self.html = html
        self.city_set = city_set.CITY_SET
        self.case_soup = bs(self.html, "html.parser")
        self.city = None # just for debugging with print statements


    def extract_city(self):
        """Extracts city / court name from the court case cause list."""
        if not self.case_soup:
            print("no soup")

        court_name_elem = self.case_soup.find("title")
        
        page_title = court_name_elem.get_text(strip=True) if court_name_elem else "Unknown Court"
        # print(f"page title: {page_title}")
        for c in self.city_set:
            city_pattern = rf"\b{re.escape(c.lower())}\b"
            if re.search(city_pattern, page_title.lower()):
                self.city = c    

        if self.city == None:
            print("Issue finding city for this court")# TODO better logging here
        return self.city # returning city name for easier debugging in main/nb
    

    # def extract_city(self) -> Optional[str]:
    #     raise NotImplementedError
    
    def extract_case_rows(self)-> list[list[str]]:
        raise NotImplementedError
        