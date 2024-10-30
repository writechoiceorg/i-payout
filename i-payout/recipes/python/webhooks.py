import base64
import requests
import hashlib
import hmac

base_url = "https://merchantapi.testewallet.com/api/v1"

username = "<username>"
password = "<password>"
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

webhook_url = f"{base_url}/webhooks"
webhook_body = {
    "eventNames": ["PAYMENT.CREATED"],
    "url": "https://webhook.site/#!/view/94480622-0f4f-4b1c-bbf4-0d3071c0958a",
    "alias": "WebhookTest",
}

headers = {
    "Authorization": f"Bearer {api_token}",
    "X-MerchantId": merchant_id,
    "accept": "application/json",
    "content-type": "application/*+json",
}

webhook_response = requests.post(webhook_url, headers=headers, json=webhook_body)
webhook_data = webhook_response.json()

webhook_token = webhook_data["data"]["token"]

activate_webhook_url = f"{base_url}/webhooks/{webhook_token}/activate"

activate_response = requests.post(activate_webhook_url, headers=headers)
activate_data = activate_response.json()


def verify_webhook_signature(
    public_key, timestamp, notification_url, json_body, received_signature
):
    # Construct the signature body
    signature_body = f"{timestamp}#{notification_url}#{json_body}"
    signature_hash = hashlib.sha256(signature_body.encode()).digest()

    # Verify the signature using the public key
    try:
        hmac_signature = hmac.new(
            public_key.encode(), signature_hash, hashlib.sha256
        ).digest()
        expected_signature = base64.b64encode(hmac_signature).decode()

        # Compare the received signature with the expected signature
        return hmac.compare_digest(received_signature, expected_signature)
    except Exception as e:
        print(f"Signature verification failed: {e}")
        return False


# # Example usage of the verification function
public_key = "<public_key>"
timestamp = "<x-timestamp_value>"
notification_url = "https://webhook.site/#!/view/94480622-0f4f-4b1c-bbf4-0d3071c0958a"
json_body = '{"event":"PAYMENT.COMPLETED"}'  # Replace with the actual JSON payload
received_signature = (
    "<x-signature_value>"  # This is received from the triggered webhook
)

is_valid = verify_webhook_signature(
    public_key, timestamp, notification_url, json_body, received_signature
)
if is_valid:
    print("Webhook signature is valid.")
else:
    print("Webhook signature is invalid.")
