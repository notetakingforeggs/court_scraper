import requests
from dotenv import load_dotenv
import os

# Load credentials from environment variables
load_dotenv()
USERNAME = os.getenv("COURT_USERNAME")
PASSWORD = os.getenv("COURT_PASSWORD")

BASE_URL = "https://www.courtserve.net"
LOGIN_ROUTE = "/confirmation-pages/registration-confirm-request.php"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
}

def login():
    """Logs into the court website and returns an authenticated session."""
    session = requests.session()
    login_payload = {"loginformused": 1, "username": USERNAME, "password": PASSWORD}
    
    try:
        response = session.post(BASE_URL + LOGIN_ROUTE, headers=HEADERS, data=login_payload)
        if response.status_code == 200:
            print("Login successful")
            return session
        else:
            print(f"Login failed: {response.status_code}")
            return None
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return None
    
login()