import requests
from utils.index import save_response
from headers import headers, url, username


def create_payment_method():
    method_url = f"{url}/paymentmethod"
    data = {
        "merchantIdentifier": username,
        "customerReference": "154564559",
        "paymentMethodIdentifier": "",
        "card": {
            "cardNumber": "4780155230947580",
            "expiryMonth": 11,
            "expiryYear": 2026,
            "cardHolderName": "Mitesh",
            "cvv": "111",
        },
        "billingInformation": {
            "firstLine": "540 NE 4th st",
            "secondLine": "Second Floor",
            "city": "FLL",
            "region": "FL",
            "zipCode": "33091",
            "countryAlpha3Code": "USA",
        },
    }
    response = requests.post(method_url, json=data, headers=headers)
    save_response(response, "create_payment_method")


if __name__ == "__main__":
    create_payment_method()
