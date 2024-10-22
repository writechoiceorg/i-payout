import requests
from utils.index import save_response
from headers import headers, url, username


def create_payment_method():
    method_url = f"{url}/paymentmethod"
    data = {
        "merchantIdentifier": username,
        "card": {
            "cardNumber": "1234567890123456",
            "expiryMonth": 12,
            "expiryYear": 2025,
            "cardHolderName": "John Doe",
            "cvv": "123",
            "creditCardBrand": "Visa",
        },
    }
    response = requests.post(method_url, json=data, headers=headers)
    save_response(response, "create_payment_method")


if __name__ == "__main__":
    create_payment_method()
