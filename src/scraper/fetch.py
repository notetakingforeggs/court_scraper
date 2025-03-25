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

        table = soup.find_all("table")[0]

        if not table:
            print("No tables found.")
            return []
        
        links = table.find_all("a", string = lambda text: text and "daily" in text.lower())

        for link in links:
            print(link.get("href"))
        # return [link.get("href") for link in box.find_all("a") if link.get("href")]
        return[]

    except requests.RequestException as e:
        print(f"Failed to retrieve court links: {e}")
        return []

