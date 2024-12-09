import base64
import requests
import os
from dotenv import load_dotenv

load_dotenv()

base_url = "https://merchantapi.testewallet.com/api/v1"

username = os.environ.get("IPAYOUT_USERNAME")  # Replace with your username
password = os.environ.get("IPAYOUT_PASSWORD")  # Replace with your password
merchant_id = os.environ.get("IPAYOUT_MERCHANT_ID")  # Replace with your merchant ID

auth_str = f"{username}:{password}"
encoded_auth_str = base64.b64encode(auth_str.encode()).decode()

# Step 1: Get API Token
token_url = f"{base_url}/authentication/login"
headers = {
    "accept": "application/json",
    "authorization": f"Basic {encoded_auth_str}",
    "X-MerchantId": merchant_id,
}

response = requests.get(token_url, headers=headers)
api_token = response.json()["data"]["token"]

# Step 2: Create Beneficiary
customer_url = f"{base_url}/beneficiaries"
body = {
    "username": "<USERNAME>",  # Replace with beneficiary's username
    "firstName": "<FIRST_NAME>",  # Replace with beneficiary's first name
    "lastName": "<LAST_NAME>",  # Replace with beneficiary's last name
    "emailAddress": "<EMAIL_ADDRESS>",  # Replace with beneficiary's email address
}
headers = {
    "Authorization": f"Bearer {api_token}",
    "X-MerchantId": merchant_id,
    "accept": "application/json",
    "content-type": "application/*+json",
}

response = requests.post(customer_url, headers=headers, json=body)
customer_token = response.json()["data"]["beneficiaryToken"]

# Step 3: Add Wire Transfer Method
transfer_method_url = f"{base_url}/transfermethods/beneficiaries/{customer_token}/wires"
body = {
    "accountNickName": "<ACCOUNT_NICKNAME>",  # Replace with account nickname
    "beneficiaryCountry": "<BENEFICIARY_COUNTRY>",  # Replace with beneficiary's country
    "accountType1": "<ACCOUNT_TYPE_1>",  # Replace with 'personal' or 'business'
    "beneficiaryAddress1": "<BENEFICIARY_ADDRESS>",  # Replace with beneficiary's address
    "beneficiaryCity": "<BENEFICIARY_CITY>",  # Replace with beneficiary's city
    "beneficiaryState": "<BENEFICIARY_STATE>",  # Replace with beneficiary's state
    "beneficiaryZipCode": "<BENEFICIARY_ZIP_CODE>",  # Replace with beneficiary's ZIP code
    "bankCountry": "<BANK_COUNTRY>",  # Replace with bank's country
    "accountNumber": "<ACCOUNT_NUMBER>",  # Replace with account number
    "bankName": "<BANK_NAME>",  # Replace with bank name
    "bankAddress1": "<BANK_ADDRESS>",  # Replace with bank address
    "bankCity": "<BANK_CITY>",  # Replace with bank city
    "bankState": "<BANK_STATE>",  # Replace with bank state
    "bankZipCode": "<BANK_ZIP_CODE>",  # Replace with bank ZIP code
}
headers = {
    "Authorization": f"Bearer {api_token}",
    "X-MerchantId": merchant_id,
    "Content-Type": "application/json",
}

response = requests.post(transfer_method_url, headers=headers, json=body)

# Step 4: Create Wire Transfer
transfer_url = f"{base_url}/transfers"
body = {
    "merchantTransactionId": "<TRANSACTION_ID>",  # Replace with transaction ID
    "beneficiaryToken": customer_token,
    "autoApprove": True,
    "comments": "<COMMENTS>",  # Replace with comments about the transaction
    "dateExpire": "<EXPIRATION_DATE>",  # Replace with expiration date in ISO format
    "destinationAmount": <AMOUNT>,  # Replace with transfer amount
    "destinationCurrency": "<DESTINATION_CURRENCY>",  # Replace with destination currency
    "destinationType": "<DESTINATION_TYPE>",  # Replace with destination type (e.g., "Wire")
    "wireProfile": {
        "accountNickName": "<ACCOUNT_NICKNAME>",  # Replace with account nickname
        "beneficiaryCountry": "<BENEFICIARY_COUNTRY>",  # Replace with beneficiary's country
        "accountType1": "<ACCOUNT_TYPE_1>",  # Replace with 'personal' or 'business'
        "beneficiaryAddress1": "<BENEFICIARY_ADDRESS>",  # Replace with beneficiary's address
        "beneficiaryCity": "<BENEFICIARY_CITY>",  # Replace with beneficiary's city
        "beneficiaryState": "<BENEFICIARY_STATE>",  # Replace with beneficiary's state
        "beneficiaryZipCode": "<BENEFICIARY_ZIP_CODE>",  # Replace with beneficiary's ZIP code
        "bankCountry": "<BANK_COUNTRY>",  # Replace with bank's country
        "routingNumber": "<ROUTING_NUMBER>",  # Replace with routing number
        "accountNumber": "<ACCOUNT_NUMBER>",  # Replace with account number
        "bankName": "<BANK_NAME>",  # Replace with bank name
        "bankAddress1": "<BANK_ADDRESS>",  # Replace with bank address
        "bankCity": "<BANK_CITY>",  # Replace with bank city
        "bankState": "<BANK_STATE>",  # Replace with bank state
        "bankZipCode": "<BANK_ZIP_CODE>",  # Replace with bank ZIP code
    },
}
headers = {
    "Authorization": f"Bearer {api_token}",
    "X-MerchantId": merchant_id,
    "Content-Type": "application/json",
}

response = requests.post(transfer_url, headers=headers, json=body)

print(response.json())