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

        const publicInvoiceUrl = `${baseUrl}/payins/public-invoice`;
        const publicInvoiceBody = {
            "currencyCode": "USD",
            "merchantReferenceId": "your-reference-id",
            "arrItems": [
                { "amount": 50.00, "description": "Payment for Service", "quantity": 1 }
            ]
        };

        headers = {
            "Authorization": `Bearer ${apiToken}`,
            "X-MerchantId": merchantId,
            "accept": "application/json",
            "content-type": "application/json",
        };

        return axios.post(publicInvoiceUrl, publicInvoiceBody, { headers: headers });
    })
    .then(invoiceResponse => {
        const invoiceData = invoiceResponse.data.data;

        const testPaymentUrl = `https://merchant.testewallet.com/PublicCheckout/Checkout.aspx?PaymentGuid=${invoiceData}`;
        const prodPaymentUrl = `https://merchant.globalewallet.com/PublicCheckout/Checkout.aspx?PaymentGuid=${invoiceData}`;

        console.log(`Test Payment URL: ${testPaymentUrl}`);
        console.log(`Production Payment URL: ${prodPaymentUrl}`);

        const webhookUrl = `${baseUrl}/webhooks`;
        const webhookBody = {
            "eventNames": ["PAYMENT.STATUS.UPDATED"],
            "url": "https://webhook.site/#!/view/94480622-0f4f-4b1c-bbf4-0d3071c0958a",
            "alias": "Payment_status_update",
        };

        headers = {
            "Authorization": `Bearer ${apiToken}`,
            "X-MerchantId": merchantId,
            "accept": "application/json",
            "content-type": "application/*+json",
        };

        return axios.post(webhookUrl, webhookBody, { headers: headers });
    })
    .then(webhookResponse => {
        console.log(webhookResponse.data);
    })
    .catch(error => {
        console.error(error);
    });
