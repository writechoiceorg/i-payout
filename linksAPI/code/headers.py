import base64
import os
from dotenv import load_dotenv

load_dotenv()

url = "https://testapi.linksmerchantservices.com/api"
username = os.environ.get("LINKS_USERNAME")
password = os.environ.get("LINKS_PASSWORD")


def create_headers():
    auth_str = f"{username}:{password}"
    encoded_auth_str = base64.b64encode(auth_str.encode()).decode()
    return {
        "accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Basic {encoded_auth_str}",
    }


headers = create_headers()


def create_headers_with_token(token):
    return {
        "accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"X-Api-Key {token}",
    }
