import base64
import requests

base_url = "https://merchantapi.testewallet.com/api/v1"

username = "<username>"  # Replace with your actual username
password = "<password>"  # Replace with your actual password
auth_str = f"{username}:{password}"
encoded_auth_str = base64.b64encode(auth_str.encode()).decode()

token_url = f"{base_url}/authentication/login"
headers = {
    "accept": "application/json",
    "authorization": f"Basic {encoded_auth_str}",
    "X-MerchantId": username,
}

response = requests.get(token_url, headers=headers)
api_token = response.json()["data"]["token"]
merchant_id = username

beneficiary_token = "<beneficiaryToken>"  # Replace with actual beneficiary token
currency_code = "USD"  # Replace with actual currency code if different
balance_url = f"{base_url}/beneficiaries/{beneficiary_token}/balances/{currency_code}"

headers = {
    "Authorization": f"Bearer {api_token}",
    "X-MerchantId": merchant_id,
    "accept": "application/json",
}

balance_response = requests.get(balance_url, headers=headers)
balance_data = balance_response.json()

spendback_url = f"{base_url}/payins/spendback"
spendback_body = {
    "amount": 100.00,  # Replace with the amount you want to spend back
    "currency": "USD",  # Replace with actual currency if different
    "reference": "spendback_001",
}

headers = {
    "Authorization": f"Bearer {api_token}",
    "X-MerchantId": merchant_id,
    "accept": "application/json",
    "content-type": "application/*+json",
}

spendback_response = requests.post(spendback_url, headers=headers, json=spendback_body)
spendback_data = spendback_response.json()

print(spendback_data.json())
