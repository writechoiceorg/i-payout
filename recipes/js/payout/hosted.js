const base64 = require('base-64');
const axios = require('axios');

const baseUrl = "https://merchantapi.testewallet.com/api/v1";

const username = "<username>";  // Replace with your actual username
const password = "<password>";  // Replace with your actual password
const authStr = `${username}:${password}`;
const encodedAuthStr = base64.encode(authStr);

const tokenUrl = `${baseUrl}/Authentication/Login`;
let headers = {
    "accept": "application/json",
    "authorization": `Basic ${encodedAuthStr}`,
    "X-MerchantId": username,
};

axios.get(tokenUrl, { headers: headers })
    .then(response => {
        const apiToken = response.data.data.token;

        const beneficiaryUrl = `${baseUrl}/beneficiary/create`;
        const beneficiaryBody = {
            "username": "john_doe",
            "firstName": "John",
            "lastName": "Doe",
            "emailAddress": "johndoe@gmail.com",
        };
        headers = {
            "Authorization": `Bearer ${apiToken}`,
            "X-MerchantId": username,
            "accept": "application/json",
            "content-type": "application/*+json",
        };

        return axios.post(beneficiaryUrl, beneficiaryBody, { headers: headers });
    })
    .then(() => {
        const payoutUrl = `${baseUrl}/PayOut/create`;
        const payoutBody = {
            "partnerBatchId": "batch_001",
            "allowDuplicates": true,
            "autoLoad": true,
            "currencyCode": "USD",
            "arrAccounts": [
                { "username": "john_doe", "amount": 200, "merchantReferenceId": "789012" }
            ],
        };
        headers = {
            "Authorization": `Bearer ${apiToken}`,
            "X-MerchantId": username,
            "Content-Type": "application/json",
        };

        return axios.post(payoutUrl, payoutBody, { headers: headers });
    })
    .then(response => {
        console.log(response.data);
    })
    .catch(error => {
        console.error(error);
    });
