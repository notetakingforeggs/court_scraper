from court_scraper.utils import time_converter
from court_scraper.scraper.parsers.base import BaseDailyCauseListParser
import re


class Flavour2DailyCauseListParser(BaseDailyCauseListParser):     

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

            # case for second style of court list, exemplified by brighton.html in test resources.
            b_tags = row.find_all("b")
            for b in b_tags:
                text = b.text
                pattern = r"\bAM|PM\b|\dam\b|\dpm\b"
                if re.search(pattern, text):
                    rows_with_times.append(row)



        case_count = 0       
        row_texts_messy = []
        for row in rows_with_times:
            
                td_tags = row.find_all("td")

                texts = [
                    td.get_text(separator = " ", strip = True) for td in td_tags
                ]
                
                (start_time, duration) = time_converter.calculate_duration(texts[0])
                texts[0] = start_time
                texts.insert(1,duration)
                row_texts_messy.append(texts)            
                continue
        print(f"{self.city}: has the following no of rows selected for (pre-cases): {case_count} - printing from flavour 2 dclp")
        return row_texts_messy