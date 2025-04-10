import requests
from dotenv import load_dotenv
import os
from bs4 import BeautifulSoup as bs

# Load credentials from environment variables (may have to change depending on where this is being called from, setting up for nb)
load_dotenv(dotenv_path="../.env")

USERNAME = os.getenv("COURT_USERNAME")
PASSWORD = os.getenv("COURT_PASSWORD")

BASE_URL = "https://www.courtserve.net"
# LOGIN_ROUTE = "/confirmation-pages/registration-confirm-request.php"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
    "Referer": "https://www.courtserve.net/",
    "Origin": "https://www.courtserve.net",
    "Content-Type": "application/x-www-form-urlencoded"
    }
login_payload = {
    "loginformused": "1",
    "forgotpassword": "",
    "username": USERNAME,
    "password": PASSWORD,
    "remember": "1",
    "login": "Sign In"
    }


def login():
    # url = BASE_URL+"/"

    url = "https://courtserve.net/"

    """Logs into the court website and returns an authenticated session."""
    session = requests.session()
    session.headers.update(HEADERS)
    # print(f"username: {USERNAME}, password: {PASSWORD}")
    
    try:
        login_response = session.post(url, data=login_payload, allow_redirects=False)
        
        # 200 response is failed login, returning login page, 302 is redirection, which is what we want to get.
        print(f"Status Code: {login_response.status_code}")
        print(f"Final URL: {login_response.url}")
        print(f"session cookies: {session.cookies}")
        if login_response.status_code == 302:
            redirect_url = login_response.headers.get("Location", "/")
            home_response = session.get("https://courtserve.net" + redirect_url)
        else:
            home_response = session.get("https://courtserve.net/")
        
        soup = bs(home_response.text, "html.parser")

        if(not is_logged_in(soup)):
            print(f"Login probs failed ")
            return None
        else:
            print("probs logged in")
            return session #, response   
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return None
    
def is_logged_in(soup : bs) -> bool:
    return not (soup.find("form", id="login-form") or soup.find("form", id="signin-form"))
