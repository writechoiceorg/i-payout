package java;

import java.io.IOException;
import java.util.Base64;
import java.util.HashMap;
import java.util.Map;
import java.util.Arrays;
import java.nio.charset.StandardCharsets;

import okhttp3.*;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.JsonNode;

public class eWalletPayout {
  public static void main(String[] args) throws IOException {
    String base_url = "https://merchantapi.testewallet.com/api/v1";

    String username = System.getenv("IPAYOUT_USERNAME");
    String password = System.getenv("IPAYOUT_PASSWORD");
    String merchant_id = System.getenv("IPAYOUT_MERCHANT_ID");

    String auth_str = username + ":" + password;
    String encoded_auth_str = Base64.getEncoder().encodeToString(auth_str.getBytes(StandardCharsets.UTF_8));

    String token_url = base_url + "/authentication/login";
    OkHttpClient client = new OkHttpClient();
    ObjectMapper mapper = new ObjectMapper();

    // Authentication
    Request tokenRequest = new Request.Builder()
        .url(token_url)
        .addHeader("accept", "application/json")
        .addHeader("authorization", "Basic " + encoded_auth_str)
        .addHeader("X-MerchantId", merchant_id)
        .build();

    Response response = client.newCall(tokenRequest).execute();
    String responseBody = response.body().string();
    JsonNode jsonNode = mapper.readTree(responseBody);
    String api_token = jsonNode.get("data").get("token").asText();

    // Create Beneficiary
    String customer_url = base_url + "/beneficiaries";
    Map<String, String> beneficiary = new HashMap<>();
    beneficiary.put("username", "john_doe");
    beneficiary.put("firstName", "John");
    beneficiary.put("lastName", "Doe");
    beneficiary.put("emailAddress", "johndoe@mail.com");

    String beneficiaryJson = mapper.writeValueAsString(beneficiary);

    Request customerRequest = new Request.Builder()
        .url(customer_url)
        .addHeader("Authorization", "Bearer " + api_token)
        .addHeader("X-MerchantId", merchant_id)
        .addHeader("accept", "application/json")
        .addHeader("content-type", "application/*+json")
        .post(RequestBody.create(beneficiaryJson, MediaType.parse("application/json")))
        .build();

    response = client.newCall(customerRequest).execute();
    responseBody = response.body().string();
    jsonNode = mapper.readTree(responseBody);
    String customer_token = jsonNode.get("data").get("beneficiaryToken").asText();

    // Create Payout
    String payout_url = base_url + "/payouts";
    Map<String, Object> payout = new HashMap<>();
    payout.put("partnerBatchId", "batch_002");
    payout.put("poolId", "pool_123");
    payout.put("allowDuplicates", true);
    payout.put("autoLoad", true);
    payout.put("currencyCode", "USD");
    Map<String, Object> account = new HashMap<>();
    account.put("username", "john_doe");
    account.put("amount", 200);
    account.put("merchantReferenceId", "929019");
    payout.put("arrAccounts", Arrays.asList(account));

    String payoutJson = mapper.writeValueAsString(payout);

    Request payoutRequest = new Request.Builder()
        .url(payout_url)
        .addHeader("Authorization", "Bearer " + api_token)
        .addHeader("X-MerchantId", merchant_id)
        .addHeader("Content-Type", "application/json")
        .post(RequestBody.create(payoutJson, MediaType.parse("application/json")))
        .build();

    response = client.newCall(payoutRequest).execute();
    responseBody = response.body().string();
    System.out.println(responseBody);
  }
}
