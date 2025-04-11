import sys
sys.path.append('../src/')  
from scraper.session import login, BASE_URL
from scraper.fetch import get_court_links_and_dates
from scraper.court_scraper import CourtScraper
from db.db_methods import get_connection, get_court_id_by_city, insert_court_case


if __name__ == "__main__":

    # getting links to different courts
    links = get_court_links_and_dates()

    # logging in
    session = login()      

    # get db connection
    get_connection()

    # iterating through each court link TODO currently selecting for 'daily' which i think is sub optimal
    for link in links:
        courtScraoer = CourtScraper(session, BASE_URL + link)
        courtScraoer.load_case_page()
        courtScraoer.get_case_list_soup()
        courtScraoer.extract_city_and_court_name()
        court_cases = courtScraoer.rows_to_objects()
        if not court_cases:
            continue
        for case in court_cases: # iterate through scraped court cases and add to db
            court_id = get_court_id_by_city(case.city)
            if not court_id:
                continue 
            insert_court_case(case, court_id)




