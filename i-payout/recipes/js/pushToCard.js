const axios = require("axios");
const base64 = require("base-64");
require("dotenv").config();

const baseUrl = "https://merchantapi.testewallet.com/api/v1";

const username = process.env.IPAYOUT_USERNAME; // Replace with your username
const password = process.env.IPAYOUT_PASSWORD; // Replace with your password
const merchantId = process.env.IPAYOUT_MERCHANT_ID; // Replace with your merchant ID

const encodedAuthStr = base64.encode(`${username}:${password}`);

// Step 1: Get API Token
const getToken = async () => {
  const headers = {
    accept: "application/json",
    authorization: `Basic ${encodedAuthStr}`,
    "X-MerchantId": merchantId,
  };
  const response = await axios.get(`${baseUrl}/authentication/login`, { headers });
  return response.data.data.token;
};

// Step 2: Create Beneficiary
const createBeneficiary = async (apiToken) => {
  const body = {
    username: "<USERNAME>", // Replace with beneficiary's username
    firstName: "<FIRST_NAME>", // Replace with beneficiary's first name
    lastName: "<LAST_NAME>", // Replace with beneficiary's last name
    emailAddress: "<EMAIL_ADDRESS>", // Replace with beneficiary's email address
  };
  const headers = {
    Authorization: `Bearer ${apiToken}`,
    "X-MerchantId": merchantId,
    accept: "application/json",
    "Content-Type": "application/*+json",
  };
  const response = await axios.post(`${baseUrl}/beneficiaries`, body, { headers });
  return response.data.data.beneficiaryToken;
};

// Step 3: Add Credit Card as Transfer Method
const addCreditCard = async (apiToken, beneficiaryToken) => {
  const body = {
    beneficiaryFirstName: "<BENEFICIARY_FIRST_NAME>", // Replace with beneficiary's first name
    beneficiaryLastName: "<BENEFICIARY_LAST_NAME>", // Replace with beneficiary's last name
    creditCardNumber: "<CREDIT_CARD_NUMBER>", // Replace with credit card number
    expiryMonth: "<EXPIRY_MONTH>", // Replace with expiry month (MM)
    expiryYear: "<EXPIRY_YEAR>", // Replace with expiry year (YYYY)
    beneficiaryAddress1: "<BENEFICIARY_ADDRESS>", // Replace with beneficiary's address
    beneficiaryCity: "<BENEFICIARY_CITY>", // Replace with beneficiary's city
    beneficiaryState: "<BENEFICIARY_STATE>", // Replace with beneficiary's state
    beneficiaryZipCode: "<BENEFICIARY_ZIP_CODE>", // Replace with beneficiary's ZIP code
    beneficiaryCountry: "<BENEFICIARY_COUNTRY>", // Replace with beneficiary's country code
    beneficiaryPhoneNumber: "<BENEFICIARY_PHONE_NUMBER>", // Replace with beneficiary's phone number
    cardType: "<CARD_TYPE>", // Replace with card type (e.g., "CreditCard")
  };
  const headers = {
    Authorization: `Bearer ${apiToken}`,
    "X-MerchantId": merchantId,
    "Content-Type": "application/json",
  };
  await axios.post(
    `${baseUrl}/transfermethods/beneficiaries/${beneficiaryToken}/credit-cards`,
    body,
    { headers }
  );
};

// Step 4: Create Transfer
const createTransfer = async (apiToken, beneficiaryToken) => {
  const body = {
    merchantTransactionId: "<TRANSACTION_ID>", // Replace with transaction ID
    beneficiaryToken: beneficiaryToken,
    autoApprove: true,
    comments: "<COMMENTS>", // Replace with comments about the transaction
    dateExpire: "<EXPIRATION_DATE>", // Replace with expiration date in ISO format
    destinationAmount: <AMOUNT>, // Replace with transfer amount
    destinationCurrency: "<DESTINATION_CURRENCY>", // Replace with destination currency
    destinationType: "<DESTINATION_TYPE>", // Replace with destination type (e.g., "CreditCard")
  };
  const headers = {
    Authorization: `Bearer ${apiToken}`,
    "X-MerchantId": merchantId,
    "Content-Type": "application/json",
  };
  const response = await axios.post(`${baseUrl}/transfers`, body, { headers });
  console.log(response.data);
};

// Main Function
const main = async () => {
  try {
    const apiToken = await getToken();
    const beneficiaryToken = await createBeneficiary(apiToken);
    await addCreditCard(apiToken, beneficiaryToken);
    await createTransfer(apiToken, beneficiaryToken);
  } catch (error) {
    console.error(error);
  }
};

main();
