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


customer_url = f"{base_url}/beneficiaries"
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

customer_token = response.json()["data"]["beneficiaryToken"]

transfer_method_url = (
    f"{base_url}/transfermethods/beneficiaries/{customer_token}/credit-cards"
)
body = {
    "beneficiaryFirstName": "John",
    "beneficiaryLastName": "Doe",
    "creditCardNumber": "4111111111111111",
    "expiryMonth": "12",
    "expiryYear": "2026",
    "beneficiaryAddress1": "123 Elm St",
    "beneficiaryCity": "Los Angeles",
    "beneficiaryState": "CA",
    "beneficiaryZipCode": "90001",
    "beneficiaryCountry": "US",
    "beneficiaryPhoneNumber": "+1 555-1234",
    "cardType": "CreditCard",
}

headers = {
    "Authorization": f"Bearer {api_token}",
    "X-MerchantId": merchant_id,
    "Content-Type": "application/json",
}

response = requests.post(transfer_method_url, headers=headers, json=body)

transfer_url = f"{base_url}/transfers"
body = {
    "merchantTransactionId": "TX123456",
    "beneficiaryToken": customer_token,
    "autoApprove": True,
    "comments": "Payment for services",
    "dateExpire": "2024-12-31T23:59:59.999Z",
    "destinationAmount": 100.00,
    "destinationCurrency": "USD",
    "destinationType": "CreditCard",
}
headers = {
    "Authorization": f"Bearer {api_token}",
    "X-MerchantId": merchant_id,
    "Content-Type": "application/json",
}

response = requests.post(transfer_method_url, headers=headers, json=body)

print(response.json())
