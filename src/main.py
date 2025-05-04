import sys
sys.path.append('../src/')  
from scraper.session import login
from scraper.fetch import get_court_links_and_dates
from scraper.court_scraper import CourtScraper

from db.db_methods import get_connection


def main():
    # getting court links doesnt need session as no log in... but it does want you to log in to view the deetts..
    links_and_dates = get_court_links_and_dates()

    # logging in
    session = login()      

    # get db connection
    get_connection()

    # scrape cases
    courtScraper = CourtScraper(session, links_and_dates)
    courtScraper.run()  

if __name__ == "__main__":
    main()