import requests
from dotenv import load_dotenv
import os
from bs4 import BeautifulSoup as bs

# Load credentials from environment variables
load_dotenv()
USERNAME = os.getenv("COURT_USERNAME")
PASSWORD = os.getenv("COURT_PASSWORD")

BASE_URL = "https://www.courtserve.net"
LOGIN_ROUTE = "/confirmation-pages/registration-confirm-request.php"
HEADERS = {
"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
"Referer": "https://www.courtserve.net/",
"Origin": "https://www.courtserve.net"
}

def login():
    """Logs into the court website and returns an authenticated session."""
    session = requests.session()
    # login_payload = {"loginformused": 1, "username": USERNAME, "password": PASSWORD}
    session.headers.update(HEADERS)
    login_payload = {
        "loginformused": "1",
        "forgotpassword": "",
        "username": USERNAME,
        "password": PASSWORD,
        "remember": "1",
        "login": "Sign In"
    }
    
    try:
        response = session.post(BASE_URL + LOGIN_ROUTE, data=login_payload)
        if response.status_code == 200:
            print("Login successful, text below!")
            # print(response.text)
            print(f"session cookies: {session.cookies}")
            return session
        else:
            print(f"Login failed: {response.status_code}")
            return None
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return None
    
def is_logged_in(soup : bs) -> bool:
    return soup.find("div", id="login")
