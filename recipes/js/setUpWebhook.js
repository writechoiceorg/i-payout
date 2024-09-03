const base64 = require('base-64');
const axios = require('axios');
const crypto = require('crypto');

const baseUrl = "https://merchantapi.testewallet.com/api/v1";

const username = "<username>";
const password = "<password>";
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
        const merchantId = username;

        const webhookUrl = `${baseUrl}/webhook/Create`;
        const webhookBody = {
            "eventNames": ["PAYMENT.CREATED"],
            "url": "https://webhook.site/#!/view/94480622-0f4f-4b1c-bbf4-0d3071c0958a",
            "alias": "WebhookTest",
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
        const webhookData = webhookResponse.data;
        const webhookToken = webhookData.data.token;

        const activateWebhookUrl = `${baseUrl}/webhook/${webhookToken}/activate`;

        return axios.put(activateWebhookUrl, {}, { headers: headers });
    })
    .then(activateResponse => {
        console.log(activateResponse.data);
    })
    .catch(error => {
        console.error(error);
    });

function verifyWebhookSignature(publicKey, timestamp, notificationUrl, jsonBody, receivedSignature) {
    try {
        // Construct the signature body
        const signatureBody = `${timestamp}#${notificationUrl}#${jsonBody}`;
        const signatureHash = crypto.createHash('sha256').update(signatureBody).digest();

        // Verify the signature using the public key
        const hmacSignature = crypto.createHmac('sha256', publicKey).update(signatureHash).digest();
        const expectedSignature = base64.encode(hmacSignature);

        // Compare the received signature with the expected signature
        return crypto.timingSafeEqual(Buffer.from(receivedSignature), Buffer.from(expectedSignature));
    } catch (e) {
        console.error(`Signature verification failed: ${e.message}`);
        return false;
    }
}

// Example usage of the verification function
const publicKey = "<public_key>";
const timestamp = "<x-timestamp_value>";
const notificationUrl = "https://webhook.site/#!/view/94480622-0f4f-4b1c-bbf4-0d3071c0958a";
const jsonBody = '{"event":"PAYMENT.COMPLETED"}';  // Replace with the actual JSON payload
const receivedSignature = "<x-signature_value>";  // This is received from the triggered webhook

const isValid = verifyWebhookSignature(publicKey, timestamp, notificationUrl, jsonBody, receivedSignature);
if (isValid) {
    console.log("Webhook signature is valid.");
} else {
    console.log("Webhook signature is invalid.");
}
