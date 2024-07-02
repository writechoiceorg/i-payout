import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

url = "https://merchantapi.testewallet.com/api/v1"


def save_response(response, file_name):
    response_data = response.json()
    status = response.status_code
    print(status)
    if status == 204:
        return True

    main_path = f"./responses/{file_name}"
    os.makedirs(main_path, exist_ok=True)
    file_path = f"{main_path}/{file_name}_{status}.json"

    if file_name == "token":
        file_path = file_name

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


def create_customer():
    customer_url = f"{url}/customer/create"
    data = {
        "username": "gabriel_raeder",
        "firstName": "Gabriel",
        "lastName": "Raeder",
        "companyName": "Raeder Enterprises",
        "address": "123 Main Street",
        "address2": "Suite 400",
        "city": "Metropolis",
        "state": "NY",
        "zipCode": "12345",
        "country": "US",
        "phoneNumber": "+1-555-123-4567",
        "cellPhoneNumber": "+1-555-765-4321",
        "emailAddress": "gabrielraeder@writechoice.io",
        "dateOfBirth": "1985-07-02T16:33:04.299Z",
        "preferredLanguage": "en",
        "kyc": [{"idType": 0, "idNumber": "103-45-6789"}],
    }
    headers = create_headers()
    response = requests.post(customer_url, json=data, headers=headers)
    response.raise_for_status()
    save_response(response, "create_customer")


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
    headers = create_headers()
    response = requests.post(url, json=data, headers=headers)
    response.raise_for_status()
    save_response(response, "create_payout")


if __name__ == "__main__":
    create_customer()
