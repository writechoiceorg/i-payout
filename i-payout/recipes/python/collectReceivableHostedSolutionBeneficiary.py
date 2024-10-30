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

beneficiary_url = f"{base_url}/beneficiaries"
beneficiary_body = {"username": "john_doe", "firstName": "John", "lastName": "Doe"}

headers = {
    "Authorization": f"Bearer {api_token}",
    "X-MerchantId": merchant_id,
    "accept": "application/json",
    "content-type": "application/*+json",
}

beneficiary_response = requests.post(
    beneficiary_url, headers=headers, json=beneficiary_body
)
beneficiary_data = beneficiary_response.json()

payment_items_url = f"{base_url}/payins"
payment_items_body = {
    "items": [
        {"description": "Service Fee", "amount": 50.00, "currency": "USD"},
        {"description": "Product Purchase", "amount": 150.00, "currency": "USD"},
    ],
    "beneficiaryToken": beneficiary_data["data"]["beneficiaryToken"],
    "username": "john_doe",
}

headers = {
    "Authorization": f"Bearer {api_token}",
    "X-MerchantId": merchant_id,
    "accept": "application/json",
    "content-type": "application/*+json",
}

payment_items_response = requests.post(
    payment_items_url, headers=headers, json=payment_items_body
)
payment_items_data = payment_items_response.json()

webhook_url = f"{base_url}/webhooks"
webhook_body = {
    "alias": "PAYMENT.COMPLETED",
    "eventNames": ["PAYMENT.COMPLETED"],
    "url": "https://yourwebhookurl.com/notification",
    "description": "Webhook for payment completion",
}

headers = {
    "Authorization": f"Bearer {api_token}",
    "X-MerchantId": merchant_id,
    "accept": "application/json",
    "content-type": "application/*+json",
}

webhook_response = requests.post(webhook_url, headers=headers, json=webhook_body)
webhook_data = webhook_response.json()

print(webhook_response.json())
