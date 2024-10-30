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

transfer_method_url = f"{base_url}/transfermethod/beneficiaries/{customer_token}/wire"
body = {
    "accountNickName": "John US Wire Account",
    "beneficiaryCountry": "US",
    "accountType1": "personal",
    "routingNumber": "12345",
    "beneficiaryAddress1": "123 Elm St",
    "beneficiaryCity": "Los Angeles",
    "beneficiaryState": "CA",
    "beneficiaryZipCode": "90001",
    "bankCountry": "US",
    "accountNumber": "987654321",
    "bankName": "Bank of America",
    "bankAddress1": "123 Bank St",
    "bankCity": "New York",
    "bankState": "New York",
    "bankZipCode": "10001",
}

headers = {
    "Authorization": f"Bearer {api_token}",
    "X-MerchantId": merchant_id,
    "Content-Type": "application/json",
}

response = requests.post(transfer_method_url, headers=headers, json=body)
print(response.json())

# THE CALL ABOVE RETURNS THE FOLLOWING ERROR:
# {
#     "statusCode": -72,
#     "isSuccess": False,
#     "logIdentifier": "76a947c990e24c76b2a62f26ebf48639",
#     "message": "400: Bad request. The inputs supplied to the API are invalid",
#     "errors": {
#         "": [
#             "Invalid state! (Ex. BeneficiaryState allows 2 characters for BeneficiaryCountry US only.)"
#         ]
#     },
# }
# Im currently using "beneficiaryState": "CA" and it still gives the error above. I added beneficiaryCountry and it didn't made a difference

transfer_url = f"{base_url}/transfer/create"
body = {
    "merchantTransactionId": "TX123456",
    "beneficiaryToken": customer_token,
    "autoApprove": True,
    "comments": "Payment for services",
    "dateExpire": "2024-12-31T23:59:59.999Z",
    "destinationAmount": 100.00,
    "destinationCurrency": "USD",
    "destinationType": "Wire",
    "wireProfile": {
        "accountNickName": "John's Wire Account",
        "beneficiaryCountry": "US",
        "accountType1": "personal",
        "beneficiaryAddress1": "123 Elm St",
        "beneficiaryCity": "Los Angeles",
        "beneficiaryState": "CA",
        "beneficiaryZipCode": "90001",
        "bankCountry": "US",
        "routingNumber": "123456789",
        "accountNumber": "987654321",
        "bankName": "Bank of America",
        "bankAddress1": "123 Bank St",
        "bankCity": "New York",
        "bankState": "New York",
        "bankZipCode": "10001",
    },
}
headers = {
    "Authorization": f"Bearer {api_token}",
    "X-MerchantId": merchant_id,
    "Content-Type": "application/json",
}

response = requests.post(transfer_method_url, headers=headers, json=body)

print(response.json())
