from bs4 import BeautifulSoup as bs
class EntryPageParser:
    def __init__(self, html):
        self.html = html


    def parse_for_new_tab_url(self)->str:
        # convert html from request into soup
            soup = bs(self.html, "html.parser")

            # find box containing "open list in new tab" link and get path
            box2 = soup.find("div", id="box2")
            if not box2:
                print(f"no box2 at{self.court_url}")
                return None
            new_tab_anchor = box2.find("a")
            if not new_tab_anchor:
                print(f"no new tab link at {self.court_url}")
                return None
                
            new_tab_url = new_tab_anchor["href"] # get url "open list..." link
            self.new_tab_url = new_tab_url

            # returns the url to allow for conditional continuation
            return new_tab_url
