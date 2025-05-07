from typing import NamedTuple
from court_scraper.scraper.parsers.flavour_1_daily_cause_list_parser import Flavour1DailyCauseListParser
from court_scraper.scraper.parsers.flavour_2_daily_cause_list_parser import Flavour2DailyCauseListParser
from court_scraper.scraper.factories.flavour_1_court_case_factory import Flavour1CourtCaseFactory
from court_scraper.scraper.factories.flavour_2_court_case_factory import Flavour2CourtCaseFactory

from bs4 import BeautifulSoup as bs

class Flavour(NamedTuple):
    parser_class : type
    factory_class: type

FLAVOURS: dict[str, Flavour] = {
    "flavour1": Flavour(Flavour1DailyCauseListParser, Flavour1CourtCaseFactory),
    "flavour2": Flavour(Flavour2DailyCauseListParser, Flavour2CourtCaseFactory),
}

def detect_Flavour(html:str) -> Flavour:
    soup = bs(html, "html.parser")
    if soup.find("meta", {"name": "Generator"}):
        return FLAVOURS["flavour1"]
    else:
        return FLAVOURS ["flavour2"]