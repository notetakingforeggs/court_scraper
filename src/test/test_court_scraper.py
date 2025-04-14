import pytest
from bs4 import BeautifulSoup as bs
from scraper.court_scraper import CourtScraper

class DummySession:
        def get(self, url):
                return None
        
def test_extract_city_and_court_name():
    html = '''
    <html>
        <body>
            <b>Manchester Crown Court - Civil Division</b>
        </body>
    </html>
    '''

    scraper = CourtScraper(session=DummySession(), court_url = "fake_url")
    scraper.case_soup = bs(html, "html.parser")
    scraper.extract_city_and_court_name()
    print(f"city: {scraper.city}")

    assert scraper.city == "Manchester"