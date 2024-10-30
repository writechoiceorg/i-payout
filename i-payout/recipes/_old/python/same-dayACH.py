import base64
import requests
import os
from dotenv import load_dotenv

load_dotenv()

base_url = "https://merchantapi.testewallet.com/api/v1"

username = os.environ.get("IPAYOUT_USERNAME")
password = os.environ.get("IPAYOUT_PASSWORD")
merchant_id = os.environ.get("IPAYOUT_MERCHANT_ID")

auth_str = f"{username}:{password}"
encoded_auth_str = base64.b64encode(auth_str.encode()).decode()

token_url = f"{base_url}/authentication/login"
headers = {
    "accept": "application/json",
    "authorization": f"Basic {encoded_auth_str}",
    "X-MerchantId": merchant_id,
}

response = requests.get(token_url, headers=headers)
api_token = response.json()["data"]["token"]


customer_url = f"{base_url}/beneficiaries/create"
body = {
    "username": "john_doe",
    "firstName": "John",
    "lastName": "Doe",
    "emailAddress": "johndoe@mail.com",
}
headers = {
    "Authorization": f"Bearer {api_token}",
    "X-MerchantId": merchant_id,
    "accept": "application/json",
    "content-type": "application/*+json",
}

response = requests.post(customer_url, headers=headers, json=body)

# customer_token = response.json()["data"]["beneficiaryToken"]
customer_token = "e6252377-e999-46fd-bb70-3c4bdb83edf8"

transfer_method_url = f"{base_url}/transfer/beneficiaries/{customer_token}/bankaccount"
body = {
    "beneficiaryToken": customer_token,
    "accountHolderName": "John Doe",
    "accountNickName": "John's Personal Account",
    "accountCurrency": "USD",
    "accountNumber": "123456789",
    "accountType1": "personal",  # can be either 'personal' or 'business'
    "accountType2": "checking",  # can be either 'checking' or 'savings'
    "bankName": "Bank of America",
    "bankCountry": "US",
    "routingNumber": "987654321",
    "branchAddress": "1234 Bank Street, Suite 567",
    "beneficiaryFirstName": "John",
    "beneficiaryLastName": "Doe",
    "beneficiaryCountry": "US",
    "beneficiaryAddress1": "1234 Elm St",
    "beneficiaryState": "CA",
    "beneficiaryCity": "Los Angeles",
    "beneficiaryZipCode": "90001",
}

headers = {
    "Authorization": f"Bearer {api_token}",
    "X-MerchantId": merchant_id,
    "Content-Type": "application/json",
}

response = requests.post(transfer_method_url, headers=headers, json=body)
# print(response.json())  # RETURNS A 404 WITHOUT DATA

transfer_url = f"{base_url}/transfer/create"
body = {
    "merchantTransactionId": "TX123456",
    "beneficiaryToken": customer_token,
    "autoApprove": True,
    "comments": "Payment for services",
    "dateExpire": "2024-12-31T23:59:59.999Z",
    "destinationAmount": 100.00,
    "destinationCurrency": "USD",
    "destinationType": "SameDayACH",
    "bankAccount": {
        "accountNickName": "John's Personal Account",
        "accountCurrency": "USD",
        "accountNumber": "123456789",
        "accountType1": "personal",
        "accountType2": "checking",
        "bankName": "Bank of America",
        "bankCountry": "US",
        "routingNumber": "987654321",
        "branchAddress": "1234 Bank Street, Suite 567",
        "beneficiaryCountry": "US",
        "beneficiaryAddress1": "1234 Elm St",
        "beneficiaryState": "CA",
        "beneficiaryCity": "Los Angeles",
        "beneficiaryZipCode": "90001",
    },
}
headers = {
    "Authorization": f"Bearer {api_token}",
    "X-MerchantId": merchant_id,
    "Content-Type": "application/json",
}

response = requests.post(transfer_method_url, headers=headers, json=body)

print(response.json())

# ERROR RETURNS A 404 WITHOUT DATA
