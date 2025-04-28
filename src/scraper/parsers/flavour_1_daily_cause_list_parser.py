from bs4 import BeautifulSoup as bs
from utils import city_set, time_converter
from scraper.parsers.base import BaseDailyCauseListParser
import re


class Flavour1DailyCauseListParser(BaseDailyCauseListParser):     

    def extract_city(self):
        """Extracts city / court name from the court case cause list."""
        if not self.case_soup:
            print("no soup")

        court_name_elem = self.case_soup.find("title")
        
        page_title = court_name_elem.get_text(strip=True) if court_name_elem else "Unknown Court"
        print(f"page title: {page_title}")
        for c in CITY_SET:
            city_pattern = rf"\b{re.escape(c.lower())}\b"
            if re.search(city_pattern, page_title.lower()):
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
                pattern = r"\bAM|PM\b|\dam\b|\dpm\b"
                if re.search(pattern, text):
                    rows_with_times.append(row)
            
            # case for second style of court list, exemplified by brighton.html in test resources.
            if not spans:
                # print("no spans in this row")
                b_tags = row.find_all("b")
                for b in b_tags:
                    text = b.text
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
            else:
                # print("no spans in the row... getting text other ways")
                td_tags = row.find_all("td")

                texts = [
                    td.get_text(separator = " ", strip = True) for td in td_tags
                ]
                
                (start_time, duration) = time_converter.calculate_duration(texts[0])
                texts[1] = start_time
                texts[2] = duration
                print(texts)
                row_texts_messy.append(texts)

              

                continue
        print(f"{self.city}: has the following no of rows selected for (pre-cases): {case_count}")
        return row_texts_messy