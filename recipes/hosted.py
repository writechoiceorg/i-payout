import base64
import requests

base_url = "https://merchantapi.testewallet.com/api/v1"

username = "6d099995-e2f9-4a01-bef1-258eb99c1b77"
password = "Ys=LYgysz0s+tZPC"
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


beneficiary_url = f"{base_url}/beneficiary/create"
body = {
    "username": "john_doe",
    "firstName": "John",
    "lastName": "Doe",
    "emailAddress": "johndoe@gmail.com",
}
headers = {
    "Authorization": f"Bearer {api_token}",
    "X-MerchantId": username,
    "accept": "application/json",
    "content-type": "application/*+json",
}

response = requests.post(beneficiary_url, headers=headers, json=body)

payout_url = f"{base_url}/PayOut/create"
body = {
    "partnerBatchId": "batch_001",
    "allowDuplicates": True,
    "autoLoad": True,
    "currencyCode": "USD",
    "arrAccounts": [
        {"username": "john_doe", "amount": 200, "merchantReferenceId": "789012"}
    ],
}
headers = {
    "Authorization": f"Bearer {api_token}",
    "X-MerchantId": username,
    "Content-Type": "application/json",
}

response = requests.post(payout_url, headers=headers, json=body)

print(response.json())
