# import requests
# from bs4 import BeautifulSoup as bs
# from dotenv import load_dotenv
# import os

# # Load credentials from environment variables
# load_dotenv()
# USERNAME = os.getenv("COURT_USERNAME")
# PASSWORD = os.getenv("COURT_PASSWORD")

# BASE_URL = "https://www.courtserve.net"
# LOGIN_ROUTE = "/confirmation-pages/registration-confirm-request.php"
# HEADERS = {
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
# }

# def login():
#     """Logs into the court website and returns an authenticated session."""
#     session = requests.session()
#     login_payload = {"loginformused": 1, "username": USERNAME, "password": PASSWORD}
    
#     try:
#         response = session.post(BASE_URL + LOGIN_ROUTE, headers=HEADERS, data=login_payload)
#         if response.status_code == 200:
#             print("Login successful")
#             return session
#         else:
#             print(f"Login failed: {response.status_code}")
#             return None
#     except requests.RequestException as e:
#         print(f"Request failed: {e}")
#         return None

# def get_court_links(session):
#     """Retrieves all court links from the main court page."""
#     print("getting court links")
#     try:
#         response = session.get(BASE_URL + "/courtlists/current/county/indexv2county.php")
#         soup = bs(response.text, "html.parser")
#         box = soup.find(id="box2a")
#         if not box:
#             print("No court links found.")
#             return []
        
#         return [link.get("href") for link in box.find_all("a") if link.get("href")]
#     except requests.RequestException as e:
#         print(f"Failed to retrieve court links: {e}")
#         return []

# def search_cases(session, court_links, search_term="persons unknown"):
#     """Searches for a specific term in all available court cases."""
#     found_cases = []
#     total_links = len(court_links)

#     for i, link in enumerate(court_links):
#         try:
#             response = session.get(BASE_URL + link)
#             soup = bs(response.text, "html.parser")
#             box = soup.find("div", id="box2a")
#             if not box:
#                 continue

#             new_tab = box.find("a")
#             if not new_tab or not new_tab.get("href"):
#                 continue

#             # Open the case details page
#             case_url = BASE_URL + "/courtlists/viewcourtlist2014.php" + new_tab.get("href")
#             case_response = session.get(case_url)
#             case_soup = bs(case_response.text, "html.parser")

#             # Extract court name
#             court_name_elem = case_soup.find("b")
#             court_name = court_name_elem.get_text(strip=True) if court_name_elem else "Unknown Court"

#             # Extract and search case details
#             for span in case_soup.find_all("span"):
#                 text = span.get_text().strip().lower()
#                 if search_term in text:
#                     found_case = f"{text} - {court_name}"
#                     print(found_case)
#                     found_cases.append(found_case)

#             # Progress display
#             percent_done = int((i / total_links) * 100)
#             print(f"Progress: {percent_done}% done")

#         except requests.RequestException:
#             print(f"Failed to fetch details for {link}")
#         except AttributeError:
#             continue  # Skip if expected elements are missing

#     return found_cases

# def get_court_list(session):
#     """Retrieves a structured list of courts and their case links."""
#     try:
#         response = session.get(BASE_URL + "/courtlists/current/county/indexv2county.php")
#         soup = bs(response.text, "html.parser")
#         elements = soup.find_all("a", string=lambda text: text and "daily public" in text.lower())

#         for element in elements:
#             print(elements.get("href"), "::", element.text.strip)

#         courts = []
#         current_court = None
#         case_links = []

#         for elem in elements:
#             if elem.name == "strong":
#                 if current_court:
#                     courts.append((current_court, case_links))
#                 current_court = elem.get_text(strip=True)
#                 case_links = []
#             elif elem.name == "a" and elem.get("href"):
#                 case_links.append(elem.get("href"))

#         if current_court:
#             courts.append((current_court, case_links))

#         return courts
#     except requests.RequestException as e:
#         print(f"Failed to retrieve courts: {e}")
#         return []

# def search_court_by_name(court_name, courts):
#     """Finds a specific court by name in the list."""
#     for court in courts:
#         if court[0].lower() == court_name.lower():
#             return court
#     return None

# def list_courts(courts):
#     """Displays all available courts."""
#     for court in courts:
#         print(court[0])

# def search_names_in_court(session, court, search_term="HOUSING"):
#     """Searches for a specific term in cases of a single court."""
#     print(f"Searching cases in {court[0]}...")

#     found_cases = search_cases(session, court[1], search_term)

#     if found_cases:
#         print("Cases found:")
#         for case in found_cases:
#             print(case)
#     else:
#         print(f"No cases found for '{search_term}' in {court[0]}.")

# def user_interface():
#     """Handles user interaction and flow control."""
#     session = login()
#     if not session:
#         return

#     while True:
#         option = input("Check all courts or one court? (all/one/exit): ").strip().lower()
        
#         if option == "all":
#             # get links
#             court_links = get_court_links(session)
#             print(court_links)
#             if not court_links:
#                 print("No court links found.")
#             else:
#                 # search within links for keyword
#                 search_cases(session, court_links)

#         elif option == "one":
#             courts = get_court_list(session)
#             if not courts:
#                 print("No courts available.")
#                 continue

#             court_name = input("Enter the court name: ").strip()
#             court = search_court_by_name(court_name, courts)
            
#             if court:
#                 search_names_in_court(session, court)
#             else:
#                 print("Court not found. Available courts:")
#                 list_courts(courts)

#         elif option == "exit":
#             print("Exiting...")
#             break

#         else:
#             print("Invalid option. Please choose 'all', 'one', or 'exit'.")

# if __name__ == "__main__":
#     user_interface()



import requests
from bs4 import BeautifulSoup as bs
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

def get_court_links(session):
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

def search_cases(session, court_links, search_term="persons unknown"):
    """Searches for a specific term in all available court cases."""
    print("in search cases")
    found_cases = []
    total_links = len(court_links)

    for i, link in enumerate(court_links):
        try:
            response = session.get(BASE_URL + link)
            soup = bs(response.text, "html.parser")
            box = soup.find("div", id="box2a")
            if not box:
                continue

            new_tab = box.find("a")
            if not new_tab or not new_tab.get("href"):
                continue

            # Open the case details page
            case_url = BASE_URL + "/courtlists/viewcourtlist2014.php" + new_tab.get("href")
            case_response = session.get(case_url)
            case_soup = bs(case_response.text, "html.parser")

            # Extract court name
            court_name_elem = case_soup.find("b")
            court_name = court_name_elem.get_text(strip=True) if court_name_elem else "Unknown Court"

            # Extract and search case details
            for span in case_soup.find_all("span"):
                text = span.get_text().strip().lower()
                if search_term in text:
                    found_case = f"{text} - {court_name}"
                    print(found_case)
                    found_cases.append(found_case)

            # Progress display
            percent_done = int((i / total_links) * 100)
            print(f"Progress: {percent_done}% done")

        except requests.RequestException:
            print(f"Failed to fetch details for {link}")
        except AttributeError:
            continue  # Skip if expected elements are missing

    return found_cases

# put back if needed! def get_court_list(session):

def search_court_by_name(court_name, courts):
    """Finds a specific court by name in the list."""
    for court in courts:
        if court[0].lower() == court_name.lower():
            return court
    return None

def list_courts(courts):
    """Displays all available courts."""
    for court in courts:
        print(court[0])

def search_names_in_court(session, court, search_term="HOUSING"):
    """Searches for a specific term in cases of a single court."""
    print(f"Searching cases in {court[0]}...")

    found_cases = search_cases(session, court[1], search_term)

    if found_cases:
        print("Cases found:")
        for case in found_cases:
            print(case)
    else:
        print(f"No cases found for '{search_term}' in {court[0]}.")

def user_interface():
    """Handles user interaction and flow control."""
    session = login()
    if not session:
        return

    while True:
        option = input("Check all courts or one court? (all/one/exit): ").strip().lower()
        
        if option == "all":
            # get links
            court_links = get_court_links(session)
            if not court_links:
                print("No court links found.")
            else:
                # search within links for keyword
                search_cases(session, court_links)

        elif option == "one":
            courts = get_court_list(session)
            if not courts:
                print("No courts available.")
                continue

            court_name = input("Enter the court name: ").strip()
            court = search_court_by_name(court_name, courts)
            
            if court:
                search_names_in_court(session, court)
            else:
                print("Court not found. Available courts:")
                list_courts(courts)

        elif option == "exit":
            print("Exiting...")
            break

        else:
            print("Invalid option. Please choose 'all', 'one', or 'exit'.")

if __name__ == "__main__":
    user_interface()
