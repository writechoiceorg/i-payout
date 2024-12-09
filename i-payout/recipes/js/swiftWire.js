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
    emailAddress: "<EMAIL_ADDRESS>", // Replace with beneficiary's email
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

// Step 3: Add Wire Transfer Method
const addWireTransferMethod = async (apiToken, beneficiaryToken) => {
  const body = {
    accountNickName: "<ACCOUNT_NICKNAME>", // Replace with account nickname
    beneficiaryCountry: "<BENEFICIARY_COUNTRY>", // Replace with beneficiary's country
    accountType1: "<ACCOUNT_TYPE_1>", // Replace with 'personal' or 'business'
    beneficiaryAddress1: "<BENEFICIARY_ADDRESS>", // Replace with beneficiary's address
    beneficiaryCity: "<BENEFICIARY_CITY>", // Replace with beneficiary's city
    beneficiaryState: "<BENEFICIARY_STATE>", // Replace with beneficiary's state
    beneficiaryZipCode: "<BENEFICIARY_ZIP_CODE>", // Replace with beneficiary's ZIP code
    bankCountry: "<BANK_COUNTRY>", // Replace with bank's country
    accountNumber: "<ACCOUNT_NUMBER>", // Replace with account number
    bankName: "<BANK_NAME>", // Replace with bank name
    bankAddress1: "<BANK_ADDRESS>", // Replace with bank address
    bankCity: "<BANK_CITY>", // Replace with bank city
    bankState: "<BANK_STATE>", // Replace with bank state
    bankZipCode: "<BANK_ZIP_CODE>", // Replace with bank ZIP code
  };
  const headers = {
    Authorization: `Bearer ${apiToken}`,
    "X-MerchantId": merchantId,
    "Content-Type": "application/json",
  };
  await axios.post(
    `${baseUrl}/transfermethods/beneficiaries/${beneficiaryToken}/wires`,
    body,
    { headers }
  );
};

// Step 4: Create Wire Transfer
const createWireTransfer = async (apiToken, beneficiaryToken) => {
  const body = {
    merchantTransactionId: "<TRANSACTION_ID>", // Replace with transaction ID
    beneficiaryToken: beneficiaryToken,
    autoApprove: true,
    comments: "<COMMENTS>", // Replace with comments about the transaction
    dateExpire: "<EXPIRATION_DATE>", // Replace with expiration date in ISO format
    destinationAmount: <AMOUNT>, // Replace with transfer amount
    destinationCurrency: "<DESTINATION_CURRENCY>", // Replace with destination currency
    destinationType: "<DESTINATION_TYPE>", // Replace with destination type
    wireProfile: {
      accountNickName: "<ACCOUNT_NICKNAME>", // Replace with account nickname
      beneficiaryCountry: "<BENEFICIARY_COUNTRY>", // Replace with beneficiary's country
      accountType1: "<ACCOUNT_TYPE_1>", // Replace with 'personal' or 'business'
      beneficiaryAddress1: "<BENEFICIARY_ADDRESS>", // Replace with beneficiary's address
      beneficiaryCity: "<BENEFICIARY_CITY>", // Replace with beneficiary's city
      beneficiaryState: "<BENEFICIARY_STATE>", // Replace with beneficiary's state
      beneficiaryZipCode: "<BENEFICIARY_ZIP_CODE>", // Replace with beneficiary's ZIP code
      bankCountry: "<BANK_COUNTRY>", // Replace with bank's country
      routingNumber: "<ROUTING_NUMBER>", // Replace with routing number
      accountNumber: "<ACCOUNT_NUMBER>", // Replace with account number
      bankName: "<BANK_NAME>", // Replace with bank name
      bankAddress1: "<BANK_ADDRESS>", // Replace with bank address
      bankCity: "<BANK_CITY>", // Replace with bank city
      bankState: "<BANK_STATE>", // Replace with bank state
      bankZipCode: "<BANK_ZIP_CODE>", // Replace with bank ZIP code
    },
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
    await addWireTransferMethod(apiToken, beneficiaryToken);
    await createWireTransfer(apiToken, beneficiaryToken);
  } catch (error) {
    console.error(error);
  }
};

main();
