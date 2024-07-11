import requests
from requests import Response
import json
import os
from dotenv import load_dotenv

load_dotenv()

url = "https://merchantapi.testewallet.com/api/v1"


def save_response(response: Response, file_name):
    status = response.status_code
    print(status)
    if status == 204:
        return True

    try:
        response_data = response.json()
    except json.JSONDecodeError:
        response_data = {"content": response.content.decode("utf-8")}

    if file_name == "token":
        file_path = f"./code/{file_name}.json"
        with open(file_path, "w") as json_file:
            json.dump(response_data, json_file, indent=4)
        return

    main_path = f"./code/responses/{file_name}"
    os.makedirs(main_path, exist_ok=True)
    file_path = f"{main_path}/{file_name}_{status}.json"

    existing_data = []
    if os.path.exists(file_path):
        with open(file_path, "r") as json_file:
            try:
                existing_data = json.load(json_file)
                if not isinstance(existing_data, list):
                    existing_data = [existing_data]
            except json.JSONDecodeError:
                existing_data = []

    if not isinstance(existing_data, list):
        existing_data = []

    existing_data.append(response_data)

    with open(file_path, "w") as json_file:
        json.dump(existing_data, json_file, indent=4)


def read_json(file_path):
    try:
        with open(file_path, "r") as json_file:
            data = json.load(json_file)
            return data
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except json.JSONDecodeError:
        print(f"Error decoding JSON from file: {file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")


def create_headers():
    return {
        "accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": os.getenv("TOKEN"),
        "X-MerchantId": os.getenv("MERCHANT_ID"),
    }


def generate_token():
    token_url = f"{url}/Authentication/Login"
    data = {
        "username": "6d099995-e2f9-4a01-bef1-258eb99c1b77",
        "password": "Dp4xF2MYysp$0g!1",
    }

    headers = create_headers()
    response = requests.post(token_url, json=data, headers=headers)
    save_response(response, "generate_token")


def create_beneficiary():
    beneficiary_url = f"{url}/beneficiary/create"
    data = {
        "username": "bruna_salgado",
        "firstName": "Bruna",
        "lastName": "Salgado",
        "companyName": "Doe Enterprises",
        "address": "123 Main Street",
        "address2": "Suite 400",
        "city": "Metropolis",
        "state": "NY",
        "zipCode": "12345",
        "country": "US",
        "phoneNumber": "+1-555-123-4567",
        "cellPhoneNumber": "+1-555-765-4321",
        "emailAddress": "bruna@writechoice.io",
        "dateOfBirth": "1985-07-02T16:33:04.299Z",
        "preferredLanguage": "en",
        "kyc": [{"idType": 0, "idNumber": "223-45-6789"}],
    }
    headers = create_headers()
    response = requests.post(beneficiary_url, json=data, headers=headers)
    save_response(response, "create_beneficiary")


def create_payout():
    data = {
        "partnerBatchId": "batch_001",
        "poolId": "pool_123",
        "allowDuplicates": True,
        "autoLoad": True,
        "currencyCode": "USD",
        "arrAccounts": [
            {
                "username": "bruna_salgado",
                "amount": 100,
                "comments": "Test payment",
                "merchantReferenceId": "123456",
            }
        ],
    }

    payout_url = f"{url}/PayOut/create"
    headers = create_headers()
    response = requests.post(payout_url, json=data, headers=headers)
    save_response(response, "create_payout")


if __name__ == "__main__":
    generate_token()
