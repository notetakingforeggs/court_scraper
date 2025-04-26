import pytest
from scraper.parsers.daily_cause_list_parser import DailyCauseListParser
from scraper.factories.court_case_factory import CourtCaseFactory




def create_parser_with_html(html):
    parser = DailyCauseListParser(html)
    return parser

def create_court_case_factory(list_of_court_case_strings, date, city):
    factory = CourtCaseFactory(list_of_court_case_strings, date, city )
    return factory

def test_aldershot_parse_obj(daily_cause_list_aldershot_test):
    date = "12/12/25"

    parser = create_parser_with_html(daily_cause_list_aldershot_test)   

    city = parser.extract_city()
    print(city)
    rows = parser.extract_case_rows()
    print(rows)


    factory = create_court_case_factory(rows, date, city)
    print("factory created")
    if factory == None:
        print("but it is None")
    court_cases = factory.process_rows_to_cases()
    assert len(court_cases) == 20
    
    