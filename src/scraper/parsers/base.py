from typing import Optional 
from scraper.utils import city_set



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

    def extract_city(self) -> Optional[str]:
        raise NotImplementedError
    
    def extract_case_rows(self)-> list[list[str]]:
        raise NotImplementedError
        