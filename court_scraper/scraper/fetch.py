import requests
from bs4 import BeautifulSoup as bs
from court_scraper.scraper.session import BASE_URL
import re


def get_court_links_and_dates() -> list[str] :
    """Retrieves all court links from the main court page."""
    print("getting court links")
    try:
        url = BASE_URL + "/courtlists/current/county/indexv2county.php"  
            
        # response = session.get(url) Don't need to use session here as the court list is not behind login
        response = requests.get(url)

        soup = bs(response.text, "html.parser")
        
        # get the table with all the links in
        table = soup.find_all("table")[0]

        if not table:
            print("No tables found.")
            return []
        
        rows = table.find_all("tr")
        pattern = r'\b(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[0-2])/\d{2}\b'
        if not rows:
            print("no rows")
        links_and_dates = []

        for row in rows:
            date = ""
            link_tag = None
            td_tags = row.find_all("td")
            for td in td_tags:
                match =  re.search(pattern, td.get_text(strip=True))
                if match:
                    date = td.text
                    link_tag = row.find("a")   
                    break
            if date and link_tag and link_tag.get("href"):
                links_and_dates.append((link_tag.get("href"), date))
        
        return links_and_dates

    except requests.RequestException as e:
        print(f"Failed to retrieve court links: {e}")
        return []

