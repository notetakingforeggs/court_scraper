from court_scraper.scraper.parsers.base import BaseDailyCauseListParser
import re


class Flavour1DailyCauseListParser(BaseDailyCauseListParser):     

    def __init__(self, html):
        super().__init__(html)
    
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
                pattern = r"\bAM|PM\b|\dam\b|\dpm\b"
                if re.search(pattern, text):
                    rows_with_times.append(row)
    
        case_count = 0       
        row_texts_messy = []
        for row in rows_with_times:
            if (spans := row.find_all("span")):
                texts = [span.text.strip() for span in spans]
                row_texts_messy.append(texts)
                case_count += 1 
          
        print(f"{self.city}: has the following no of rows selected for (pre-cases): {case_count}")
        return row_texts_messy