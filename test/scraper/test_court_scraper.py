import pytest
from bs4 import BeautifulSoup as bs
from scraper.court_scraper import CourtScraper

class DummySession:
        def get(self, url):
                return None
        

def create_scraper_with_html(html):
    scraper = CourtScraper(session=DummySession(), court_url = "fake_url")
    scraper.case_soup = bs(html, "html.parser")
    return scraper


def test_extract_city_normal():
    html = '''
    <html>
        <body>
            <b>Manchester Crown Court - Civil Division</b>
        </body>
    </html>
    '''
    scraper = create_scraper_with_html(html)
    scraper.extract_city_and_court_name()
    assert scraper.city == "Manchester"

def test_city_case_insensitive():
    html =  '''
    <html>
        <body>
            <b>manchester crown court - Civil Division</b>
        </body>
    </html>
    '''
    scraper = create_scraper_with_html(html)
    scraper.extract_city_and_court_name()
    assert scraper.city == "Manchester"
def test_no_city_name():
    html =  '''
    <html>
        <body>
            <b>blimpt lompts largdne</b>
        </body>
    </html>
    '''
    scraper = create_scraper_with_html(html)
    scraper.extract_city_and_court_name()
    assert scraper.city == None
def test_no_b_tag():
    html =  '''
    <html>
        <body>
            <p>Manchester</p>
        </body>
    </html>
    '''
    scraper = create_scraper_with_html(html)
    scraper.extract_city_and_court_name()
    assert scraper.city == None
def test_no_html():
    html =  ""
    scraper = create_scraper_with_html(html)
    scraper.extract_city_and_court_name()
    assert scraper.city == None
def multiple_b_tags():
    html =  '''
    <html>
        <body>
            <b>Manchester</b>
            <b>Chester</b>
        </body>
    </html>
    '''
    scraper = create_scraper_with_html(html)
    scraper.extract_city_and_court_name()
    assert scraper.city == "Manchester"