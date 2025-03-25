# from requests import Session
import requests
# from scraper.session import BASE_URL
import pandas as pd


def get_court_links(session) -> list[str] :
    """Retrieves all court links from the main court page."""
    print("getting court links")
    try:
        BASE_URL = "https://www.courtserve.net"
        url = BASE_URL + "/courtlists/current/county/indexv2county.php"
        response = session.get(url)
        tables = pd.read_html(response.text)

        first_table_df = tables[0]
        print(first_table_df.head())   

        return first_table_df
        
        
        
        # response = session.get(BASE_URL + "/courtlists/current/county/indexv2county.php")
        # soup = bs(response.text, "html.parser")
        # box = soup.find(id="box2a")
        # if not box:
        #     print("No court links found.")
        #     return []
        # links = box.find_all("a", string = lambda text: text and "daily" in text.lower())
        # for link in links:
        #     print(link.get("href"))
        # return [link.get("href") for link in box.find_all("a") if link.get("href")]

    except requests.RequestException as e:
        print(f"Failed to retrieve court links: {e}")
        return []

