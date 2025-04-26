import pytest
from scraper.parsers.daily_cause_list_parser import DailyCauseListParser
from scraper.factories.court_case_factory import CourtCaseFactory
from pprint import pprint



def create_parser_with_html(html):
    parser = DailyCauseListParser(html)
    return parser

def create_court_case_factory(list_of_court_case_strings, date, city):
    factory = CourtCaseFactory(list_of_court_case_strings, date, city)
    return factory

def test_integration_no_minors(daily_cause_list_no_minors):
    date = "12/12/25"

    parser = create_parser_with_html(daily_cause_list_no_minors)   

    city = parser.extract_city()
    print(city)
    rows = parser.extract_case_rows()
    factory = create_court_case_factory(rows, date, city)
   
    court_cases = factory.process_rows_to_cases()
    assert len(court_cases) == 20
    
    
def test_integration_mixed(daily_cause_list_mixed):
    date = "12/12/25"
    # print(f"0000000000000000000000 {daily_cause_list_mixed}")

    parser = create_parser_with_html(daily_cause_list_mixed)   

    city = parser.extract_city()
    print(city)
    rows = parser.extract_case_rows()
    pprint(rows)
    factory = create_court_case_factory(rows, date, city)
   
    court_cases = factory.process_rows_to_cases()
    assert len(court_cases) == 24
    