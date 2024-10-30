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

customer_token = response.json()["data"]["beneficiaryToken"]

payout_url = f"{base_url}/PayOut/create"
body = {
    "partnerBatchId": "batch_002",
    "poolId": "pool_123",
    "allowDuplicates": True,
    "autoLoad": True,
    "currencyCode": "USD",
    "arrAccounts": [
        {"username": "john_doe", "amount": 200, "merchantReferenceId": "929019"}
    ],
}
headers = {
    "Authorization": f"Bearer {api_token}",
    "X-MerchantId": merchant_id,
    "Content-Type": "application/json",
}

response = requests.post(payout_url, headers=headers, json=body)

print(response.json())
