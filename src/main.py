import sys
sys.path.append('../src/')  
from scraper.session import login, BASE_URL
from scraper.fetch import get_court_links_and_dates
from scraper.court_scraper import CourtScraper

from db.db_methods import get_connection, get_court_id_by_city, insert_court_case


def main():
    # getting court links doesnt need session as no log in... but it does want you to log in to view the deetts..
    links_and_dates = get_court_links_and_dates()

    # logging in
    session = login()      

    # get db connection
    get_connection()

    # scrape cases and add to db
    for i, (link, date) in enumerate (links_and_dates):
        if i < 2:
            continue
        try:
            court_scraper = CourtScraper(session, BASE_URL + link)
            court_scraper.load_case_page()
            court_scraper.get_case_list_soup()
            court_scraper.extract_city_and_court_name()
            court_cases = court_scraper.rows_to_objects(date)
            if not court_cases:
                continue
            for case in court_cases: # iterate through scraped court cases and add to db
                court_id = get_court_id_by_city(case.city)
                if not court_id:
                    continue 
                insert_court_case(case, court_id)
        except Exception as e:
            print(f"Exception during court_scraper logic on link - {link}:\n {e.with_traceback}")

if __name__ == "__main__":
    main()