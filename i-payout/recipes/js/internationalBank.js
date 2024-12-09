const axios = require("axios");
const base64 = require("base64");

// Replace with your credentials and base URL
const baseUrl = "https://merchantapi.testewallet.com/api/v1";
const username = process.env.IPAYOUT_USERNAME; // Replace with your username
const password = process.env.IPAYOUT_PASSWORD; // Replace with your password
const merchantId = process.env.IPAYOUT_MERCHANT_ID; // Replace with your merchant ID

const encodedAuthStr = Buffer.from(`${username}:${password}`).toString("base64");

// Get API token
const getToken = async () => {
  const response = await axios.get(`${baseUrl}/authentication/login`, {
    headers: {
      accept: "application/json",
      authorization: `Basic ${encodedAuthStr}`,
      "X-MerchantId": merchantId,
    },
  });
  return response.data.data.token;
};

// Create a new beneficiary
const createBeneficiary = async (apiToken) => {
  const body = {
    username: "<USERNAME>",
    firstName: "<FIRST_NAME>",
    lastName: "<LAST_NAME>",
    emailAddress: "<EMAIL_ADDRESS>",
  };

  const response = await axios.post(`${baseUrl}/beneficiaries`, body, {
    headers: {
      Authorization: `Bearer ${apiToken}`,
      "X-MerchantId": merchantId,
      "Content-Type": "application/json",
    },
  });
  return response.data.data.beneficiaryToken;
};

// Add transfer method
const addTransferMethod = async (apiToken, beneficiaryToken) => {
  const body = {
    beneficiaryToken: beneficiaryToken,
    accountHolderName: "<ACCOUNT_HOLDER_NAME>",
    accountNickName: "<ACCOUNT_NICKNAME>",
    accountCurrency: "<CURRENCY>",
    accountNumber: "<ACCOUNT_NUMBER>",
    accountType1: "<ACCOUNT_TYPE_1>",
    accountType2: "<ACCOUNT_TYPE_2>",
    bankName: "<BANK_NAME>",
    bankCode: "<BANK_CODE>",
    bankCountry: "<BANK_COUNTRY>",
    swiftCode: "<SWIFT_CODE>",
    routingNumber: "<ROUTING_NUMBER>",
    branchAddress: "<BRANCH_ADDRESS>",
    beneficiaryFirstName: "<BENEFICIARY_FIRST_NAME>",
    beneficiaryLastName: "<BENEFICIARY_LAST_NAME>",
    beneficiaryCountry: "<BENEFICIARY_COUNTRY>",
    beneficiaryAddress1: "<BENEFICIARY_ADDRESS>",
    beneficiaryState: "<BENEFICIARY_STATE>",
    beneficiaryCity: "<BENEFICIARY_CITY>",
    beneficiaryZipCode: "<BENEFICIARY_ZIP_CODE>",
  };

  await axios.post(
    `${baseUrl}/transfermethods/beneficiaries/${beneficiaryToken}/bank-accounts`,
    body,
    {
      headers: {
        Authorization: `Bearer ${apiToken}`,
        "X-MerchantId": merchantId,
        "Content-Type": "application/json",
      },
    }
  );
};

// Create a transfer
const createTransfer = async (apiToken, beneficiaryToken) => {
  const body = {
    merchantTransactionId: "<TRANSACTION_ID>",
    beneficiaryToken: beneficiaryToken,
    autoApprove: true,
    comments: "<COMMENTS>",
    dateExpire: "<EXPIRATION_DATE>",
    destinationAmount: <AMOUNT>,
    destinationCurrency: "<CURRENCY>",
    destinationType: "<DESTINATION_TYPE>",
    sourceCurrency: "<SOURCE_CURRENCY>",
    bankAccount: {
      accountNickName: "<ACCOUNT_NICKNAME>",
      accountCurrency: "<CURRENCY>",
      accountNumber: "<ACCOUNT_NUMBER>",
      accountType1: "<ACCOUNT_TYPE_1>",
      accountType2: "<ACCOUNT_TYPE_2>",
      bankName: "<BANK_NAME>",
      bankCountry: "<BANK_COUNTRY>",
      routingNumber: "<ROUTING_NUMBER>",
      branchAddress: "<BRANCH_ADDRESS>",
      beneficiaryFirstName: "<BENEFICIARY_FIRST_NAME>",
      beneficiaryLastName: "<BENEFICIARY_LAST_NAME>",
      beneficiaryDateOfBirth: "<DATE_OF_BIRTH>",
      beneficiaryGovernmentID: "<GOVERNMENT_ID>",
      beneficiaryCountry: "<BENEFICIARY_COUNTRY>",
      beneficiaryAddress1: "<BENEFICIARY_ADDRESS>",
      beneficiaryState: "<BENEFICIARY_STATE>",
      beneficiaryCity: "<BENEFICIARY_CITY>",
      beneficiaryZipCode: "<BENEFICIARY_ZIP_CODE>",
    },
  };

  const response = await axios.post(`${baseUrl}/transfers`, body, {
    headers: {
      Authorization: `Bearer ${apiToken}`,
      "X-MerchantId": merchantId,
      "Content-Type": "application/json",
    },
  });

  console.log(response.data);
};

const main = async () => {
  const apiToken = await getToken();
  const beneficiaryToken = await createBeneficiary(apiToken);
  await addTransferMethod(apiToken, beneficiaryToken);
  await createTransfer(apiToken, beneficiaryToken);
};

main().catch((error) => console.error(error));
