from bs4 import BeautifulSoup as bs
from utils import city_set
import re

CITY_SET = city_set.CITY_SET

class DailyCauseListParser:
    def __init__(self, html):
        self.html = html
        self.CITY_SET = CITY_SET
        self.case_soup = bs(self.html, "html.parser")
        self.city = None # just for debugging with print statements


    def extract_city(self):
        """Extracts city / court name from the court case cause list."""
        if not self.case_soup:
            print("no soup")

        court_name_elem = self.case_soup.find("title")
        
        court_name_string = court_name_elem.get_text(strip=True) if court_name_elem else "Unknown Court"
        print(court_name_string)
        for c in CITY_SET:
            city_pattern = rf"\b{re.escape(c.lower())}\b"
            if re.search(city_pattern, court_name_string.lower()):
                self.city = c    

        if self.city == None:
            print("Issue finding city for this court")# TODO better logging here
        return self.city # returning city name for easier debugging in main/nb
    
    def extract_case_rows(self)->list[str]:
        '''Extract all text from td cells in rows that have court cases in .'''

        # select only rows with times in
        rows = self.case_soup.find_all("tr") 
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