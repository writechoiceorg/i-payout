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

public_invoice_url = f"{base_url}/payins/public-invoice"
public_invoice_body = {
    "currencyCode": "USD",
    "merchantReferenceId": "your-reference-id",
    "arrItems": [
        {"amount": 50.00, "description": "Payment for Service", "quantity": 1}
    ],
}

headers = {
    "Authorization": f"Bearer {api_token}",
    "X-MerchantId": merchant_id,
    "accept": "application/json",
    "content-type": "application/json",
}

invoice_response = requests.post(
    public_invoice_url, headers=headers, json=public_invoice_body
)
invoice_data = invoice_response.json()

transaction_ref_number = invoice_data["data"]

test_payment_url = f"https://merchant.testewallet.com/PublicCheckout/Checkout.aspx?PaymentGuid={transaction_ref_number}"
prod_payment_url = f"https://merchant.globalewallet.com/PublicCheckout/Checkout.aspx?PaymentGuid={transaction_ref_number}"

webhook_url = f"{base_url}/webhooks"
webhook_body = {
    "eventNames": ["PAYMENT.STATUS.UPDATED"],
    "url": "https://webhook.site/#!/view/94480622-0f4f-4b1c-bbf4-0d3071c0958a",
    "alias": "Payment_status_update",
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
