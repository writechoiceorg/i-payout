const axios = require('axios');
const dotenv = require('dotenv');
dotenv.config();

const base_url = "https://merchantapi.testewallet.com/api/v1";

const username = process.env.IPAYOUT_USERNAME;
const password = process.env.IPAYOUT_PASSWORD;
const merchant_id = process.env.IPAYOUT_MERCHANT_ID;

const auth_str = `${username}:${password}`;
const encoded_auth_str = Buffer.from(auth_str).toString('base64');

const token_url = `${base_url}/authentication/login`;
let headers = {
    'accept': 'application/json',
    'authorization': `Basic ${encoded_auth_str}`,
    'X-MerchantId': merchant_id,
};

axios.get(token_url, { headers })
    .then(response => {
        const api_token = response.data.data.token;

        // Create beneficiary
        const customer_url = `${base_url}/beneficiaries`;
        const body = {
            username: "john_doe",
            firstName: "John",
            lastName: "Doe",
            emailAddress: "johndoe@mail.com",
        };
        headers = {
            'Authorization': `Bearer ${api_token}`,
            'X-MerchantId': merchant_id,
            'accept': 'application/json',
            'content-type': 'application/*+json',
        };

        axios.post(customer_url, body, { headers })
            .then(response => {
                const customer_token = response.data.data.beneficiaryToken;

                // Create payout
                const payout_url = `${base_url}/payouts`;
                const payout_body = {
                    partnerBatchId: "batch_002",
                    poolId: "pool_123",
                    allowDuplicates: true,
                    autoLoad: true,
                    currencyCode: "USD",
                    arrAccounts: [
                        {
                            username: "john_doe",
                            amount: 200,
                            merchantReferenceId: "929019",
                        },
                    ],
                };
                headers = {
                    'Authorization': `Bearer ${api_token}`,
                    'X-MerchantId': merchant_id,
                    'Content-Type': 'application/json',
                };

                axios.post(payout_url, payout_body, { headers })
                    .then(response => {
                        console.log(response.data);
                    })
                    .catch(error => {
                        console.error(error.response ? error.response.data : error.message);
                    });
            })
            .catch(error => {
                console.error(error.response ? error.response.data : error.message);
            });
    })
    .catch(error => {
        console.error(error.response ? error.response.data : error.message);
    });
