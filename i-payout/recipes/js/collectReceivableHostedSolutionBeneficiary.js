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
        const merchantId = username;

        const beneficiaryUrl = `${baseUrl}/beneficiaries`;
        const beneficiaryBody = {
            "username": "john_doe55",
            "firstName": "John",
            "lastName": "Doe",
            "emailAddress": "johndoe@gmail.com",
        };

        headers = {
            "Authorization": `Bearer ${apiToken}`,
            "X-MerchantId": merchantId,
            "accept": "application/json",
            "content-type": "application/*+json",
        };

        return axios.post(beneficiaryUrl, beneficiaryBody, { headers: headers })
            .then(beneficiaryResponse => {
                const beneficiaryData = beneficiaryResponse.data;

                const paymentItemsUrl = `${baseUrl}/payins`;
                const paymentItemsBody = {
                    "items": [
                        { "description": "Service Fee", "amount": 50.00, "currency": "USD" },
                        { "description": "Product Purchase", "amount": 150.00, "currency": "USD" },
                    ],
                    "beneficiaryToken": beneficiaryData.data.beneficiaryToken,
                    "username": "john_doe"
                };

                headers = {
                    "Authorization": `Bearer ${apiToken}`,
                    "X-MerchantId": merchantId,
                    "accept": "application/json",
                    "content-type": "application/*+json",
                };

                return axios.post(paymentItemsUrl, paymentItemsBody, { headers: headers });
            })
            .then(() => {
                const webhookUrl = `${baseUrl}/webhooks`;
                const webhookBody = {
                    "alias": "PAYMENT.COMPLETED",
                    "eventNames": ["PAYMENT.COMPLETED"],
                    "url": "https://yourwebhookurl.com/notification",
                    "description": "Webhook for payment completion",
                };

                headers = {
                    "Authorization": `Bearer ${apiToken}`,
                    "X-MerchantId": merchantId,
                    "accept": "application/json",
                    "content-type": "application/*+json",
                };

                return axios.post(webhookUrl, webhookBody, { headers: headers });
            });
    })
    .then(webhookResponse => {
        console.log(webhookResponse.data);
    })
    .catch(error => {
        console.error(error.response.data);
    });