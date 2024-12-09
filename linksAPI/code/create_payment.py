import requests
from utils.index import save_response
from headers import headers, url, username, create_headers_with_token


def create_payment():
    method_url = f"{url}/payments"
    data = {
        "merchantIdentifier": username,
        "currencyCode": "USD",
        "amount": 100,
        "merchantOrderId": "order_1234567893",
    }
    response = requests.post(method_url, json=data, headers=headers)
    save_response(response, "create_payment")
    if response.status_code == 201:
        return response.json()


def authorize_payment():
    payment = create_payment()
    payment_identifier = payment["paymentIdentifier"]
    token = payment["token"]
    method_url = f"{url}/payments/{payment_identifier}/authorize"
    data = {
        "paymentMethodType": "CreditCard",
        "card": {
            "cardNumber": "4111111111111111",
            "cardExpiryMonth": 12,
            "cardExpiryYear": 2025,
            "cardHolderName": "Jane Doe",
            "cardCvv": "123",
        },
        "billingInformation": {
            "firstLine": "123 Test Street",
            "secondLine": "Suite 200",
            "city": "Test City",
            "region": "Test Region",
            "zipCode": "54321",
            "countryAlpha3Code": "USA",
        },
        "autoCapture": False,
    }

    response = requests.post(
        method_url, json=data, headers=create_headers_with_token(token)
    )
    save_response(response, "authorize_payment")
    return payment_identifier


def capture_payment():
    payment_identifier = authorize_payment()
    method_url = f"{url}/payments/{payment_identifier}/capture"

    response = requests.post(method_url, headers=headers)
    save_response(response, "capture_payment")


if __name__ == "__main__":
    capture_payment()
