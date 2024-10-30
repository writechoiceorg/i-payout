const base64 = require('base-64');
const axios = require('axios');

const baseUrl = "https://merchantapi.testewallet.com/api/v1";

const username = "<username>";  // Replace with your actual username
const password = "<password>";  // Replace with your actual password
const authStr = `${username}:${password}`;
const encodedAuthStr = base64.encode(authStr);

const tokenUrl = `${baseUrl}/authentication/login`;
let headers = {
    "accept": "application/json",
    "authorization": `Basic ${encodedAuthStr}`,
    "X-MerchantId": username,
};

axios.get(tokenUrl, { headers: headers })
    .then(response => {
        const apiToken = response.data.data.token;

        const customerUrl = `${baseUrl}/beneficiaries/create`;
        const customerBody = {
            "username": "john_doe3",
            "firstName": "Johne",
            "lastName": "Doee",
            "emailAddress": "johndoe1@gmail.com",
        };
        headers = {
            "Authorization": `Bearer ${apiToken}`,
            "X-MerchantId": username,
            "accept": "application/json",
            "content-type": "application/*+json",
        };

        return axios.post(customerUrl, customerBody, { headers: headers })
            .then(response => {
                const customerToken = response.data.data.beneficiaryToken;

                const transferMethodUrl = `${baseUrl}/transfer/beneficiaries/${customerToken}/bankaccount`;
                const transferMethodBody = {
                    "beneficiaryToken": customerToken,
                    "accountHolderName": "John Doe",
                    "accountNumber": "123456789",
                    "bankName": "Bank of the World",
                    "routingNumber": "987654321",
                    "countryCode": "US",
                    "currencyCode": "USD",
                };
                headers = {
                    "Authorization": `Bearer ${apiToken}`,
                    "X-MerchantId": username,
                    "Content-Type": "application/json",
                };

                return axios.post(transferMethodUrl, transferMethodBody, { headers: headers });
            })
            .then(() => {
                const createTransferUrl = `${baseUrl}/transfer/create`;
                const createTransferBody = {
                    "merchantTransactionId": "TX123456",
                    "beneficiaryToken": customerToken,
                    "autoApprove": true,
                    "comments": "Payment for services",
                    "dateExpire": "2024-12-31T23:59:59.999Z",
                    "sourceAmount": 100.00,
                    "sourceCurrency": "USD",
                    "destinationAmount": 95.00,
                    "destinationCurrency": "USD",
                    "destinationType": 1,
                };
                headers = {
                    "Authorization": `Bearer ${apiToken}`,
                    "X-MerchantId": username,
                    "Content-Type": "application/json",
                    "accept": "application/json",
                };

                return axios.post(createTransferUrl, createTransferBody, { headers: headers });
            });
    })
    .then(response => {
        console.log(response.data);
    })
    .catch(error => {
        console.error(error);
    });
