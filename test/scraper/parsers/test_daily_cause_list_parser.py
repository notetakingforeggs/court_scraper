import pytest
from bs4 import BeautifulSoup as bs
from scraper.parsers.daily_cause_list_parser import DailyCauseListParser
class DummySession:
        def get(self, url):
                return None
        

def create_parser_with_html(html):
    parser = DailyCauseListParser(html)
    return parser


def test_extract_city_normal():
    html = '''
    <html>
        <body>
            <b>Manchester Crown Court - Civil Division</b>
        </body>
    </html>
    '''
    parser = create_parser_with_html(html)
    parser.extract_city()
    assert parser.city == "Manchester"

def test_city_case_insensitive():
    html =  '''
    <html>
        <body>
            <b>manchester crown court - Civil Division</b>
        </body>
    </html>
    '''
    parser = create_parser_with_html(html)
    parser.extract_city()
    assert parser.city == "Manchester"

def test_no_city_name():
    html =  '''
    <html>
        <body>
            <b>blimpt lompts largdne</b>
        </body>
    </html>
    '''
    parser = create_parser_with_html(html)
    parser.extract_city()
    assert parser.city == None
    
def test_no_b_tag():
    html =  '''
    <html>
        <body>
            <p>Manchester</p>
        </body>
    </html>
    '''
    parser = create_parser_with_html(html)
    parser.extract_city()
    assert parser.city == None

def test_no_html():
    html =  ""
    parser = create_parser_with_html(html)
    parser.extract_city()
    assert parser.city == None

def multiple_b_tags():
    html =  '''
    <html>
        <body>
            <b>Manchester</b>
            <b>Chester</b>
        </body>
    </html>
    '''
    parser = create_parser_with_html(html)
    parser.extract_city()
    assert parser.city == "Manchester"