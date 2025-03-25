# from requests import Session
import requests
# from scraper.session import BASE_URL
from bs4 import BeautifulSoup as bs

def get_court_links(session) -> list[str] :
    """Retrieves all court links from the main court page."""
    print("getting court links")
    try:
        BASE_URL = "https://www.courtserve.net"
        url = BASE_URL + "/courtlists/current/county/indexv2county.php"  
            
        response = session.get(url)
        soup = bs(response.text, "html.parser")

        # get the table with all the links in
        table = soup.find_all("table")[0]

        if not table:
            print("No tables found.")
            return []
        # find all anchor elements that have "daily" in their text field.
        link_tags = table.find_all("a", string = lambda text: text and "daily" in text.lower())

        links = []
        for link in link_tags:
            links.append(link.get("href"))
        
        print (links)
        return links

    except requests.RequestException as e:
        print(f"Failed to retrieve court links: {e}")
        return []

