import base64
import requests
import os
from dotenv import load_dotenv

load_dotenv()

base_url = "https://merchantapi.testewallet.com/api/v1"

username = os.environ.get("USERNAME")
password = os.environ.get("PASSWORD")
merchant_id = os.environ.get("MERCHANT_ID")

auth_str = f"{username}:{password}"
encoded_auth_str = base64.b64encode(auth_str.encode()).decode()

token_url = f"{base_url}/Authentication/Login"
headers = {
    "accept": "application/json",
    "authorization": f"Basic {encoded_auth_str}",
    "X-MerchantId": username,
}

response = requests.get(token_url, headers=headers)
api_token = response.json()["data"]["token"]


customer_url = f"{base_url}/beneficiary/create"
body = {
    "username": "john_doe3",
    "firstName": "Johne",
    "lastName": "Doee",
    "emailAddress": "johndoe1@gmail.com",
}
headers = {
    "Authorization": f"Bearer {api_token}",
    "X-MerchantId": username,
    "accept": "application/json",
    "content-type": "application/*+json",
}

response = requests.post(customer_url, headers=headers, json=body)

# customer_token = response.json()["data"]["beneficiaryToken"]
customer_token = "e6252377-e999-46fd-bb70-3c4bdb83edf8"

transfer_method_url = f"{base_url}/transfer/beneficiary/{customer_token}/bankaccount"
body = {
    "beneficiaryToken": customer_token,
    "accountHolderName": "John Doe",
    "accountNumber": "123456789",
    "bankName": "Bank of the World",
    "routingNumber": "987654321",
    "countryCode": "US",
    "currencyCode": "USD",
}
headers = {
    "Authorization": f"Bearer {api_token}",
    "X-MerchantId": username,
    "Content-Type": "application/json",
}

response = requests.post(transfer_method_url, headers=headers, json=body)

create_transfer_url = f"{base_url}/transfer/create"
body = {
    "merchantTransactionId": "TX123456",
    "beneficiaryToken": customer_token,
    "autoApprove": True,
    "comments": "Payment for services",
    "dateExpire": "2024-12-31T23:59:59.999Z",
    "sourceAmount": 100.00,
    "sourceCurrency": "USD",
    "destinationAmount": 95.00,
    "destinationCurrency": "USD",
    "destinationType": 1,
}
headers = {
    "Authorization": f"Bearer {api_token}",
    "X-MerchantId": username,
    "Content-Type": "application/json",
    "accept": "application/json",
}

response = requests.post(transfer_method_url, headers=headers, json=body)

print(response.json())
