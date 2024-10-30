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

        const beneficiaryToken = "<beneficiaryToken>";  // Replace with actual beneficiary token
        const currencyCode = "USD";  // Replace with actual currency code if different
        const balanceUrl = `${baseUrl}/beneficiaries/${beneficiaryToken}/balances/${currencyCode}`;

        headers = {
            "Authorization": `Bearer ${apiToken}`,
            "X-MerchantId": merchantId,
            "accept": "application/json",
        };

        return axios.get(balanceUrl, { headers: headers });
    })
    .then(balanceResponse => {
        const balanceData = balanceResponse.data;

        const spendbackUrl = `${baseUrl}/payins/spendback`;
        const spendbackBody = {
            "amount": 100.00,  // Replace with the amount you want to spend back
            "currency": "USD",  // Replace with actual currency if different
            "reference": "spendback_001"
        };

        headers = {
            "Authorization": `Bearer ${apiToken}`,
            "X-MerchantId": merchantId,
            "accept": "application/json",
            "content-type": "application/*+json",
        };

        return axios.post(spendbackUrl, spendbackBody, { headers: headers });
    })
    .then(spendbackResponse => {
        console.log(spendbackResponse.data);
    })
    .catch(error => {
        console.error(error);
    });
