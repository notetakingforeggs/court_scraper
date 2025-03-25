from requests import Session
import requests
from session import BASE_URL
import bs4 as bs

def get_court_links(session : Session) -> list[str] :
    """Retrieves all court links from the main court page."""
    print("getting court links")
    try:
        response = session.get(BASE_URL + "/courtlists/current/county/indexv2county.php")
        soup = bs(response.text, "html.parser")
        box = soup.find(id="box2a")
        if not box:
            print("No court links found.")
            return []
        links = box.find_all("a", string = lambda text: text and "daily" in text.lower())
        for link in links:
            print(link.get("href"))

            
        return [link.get("href") for link in box.find_all("a") if link.get("href")]
    except requests.RequestException as e:
        print(f"Failed to retrieve court links: {e}")
        return []


