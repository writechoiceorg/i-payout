package java;

import java.net.HttpURLConnection;
import java.net.URL;
import java.util.Base64;
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.OutputStream;
import org.json.JSONObject;

public class collectReceivableHostedSolutionBeneficiary {

  public static void main(String[] args) throws Exception {
    String baseUrl = "https://merchantapi.testewallet.com/api/v1";

    String username = "<username>"; // Replace with your actual username
    String password = "<password>"; // Replace with your actual password
    String authStr = username + ":" + password;
    String encodedAuthStr = Base64.getEncoder().encodeToString(authStr.getBytes());

    // Step 1: Authenticate and get API token
    String tokenUrl = baseUrl + "/authentication/login";
    HttpURLConnection tokenConnection = (HttpURLConnection) new URL(tokenUrl).openConnection();
    tokenConnection.setRequestMethod("GET");
    tokenConnection.setRequestProperty("accept", "application/json");
    tokenConnection.setRequestProperty("authorization", "Basic " + encodedAuthStr);
    tokenConnection.setRequestProperty("X-MerchantId", username);

    BufferedReader in = new BufferedReader(new InputStreamReader(tokenConnection.getInputStream()));
    String inputLine;
    StringBuilder tokenResponse = new StringBuilder();
    while ((inputLine = in.readLine()) != null) {
      tokenResponse.append(inputLine);
    }
    in.close();

    JSONObject tokenJson = new JSONObject(tokenResponse.toString());
    String apiToken = tokenJson.getJSONObject("data").getString("token");
    String merchantId = username;

    // Step 2: Create a beneficiary
    String beneficiaryUrl = baseUrl + "/beneficiaries";
    JSONObject beneficiaryBody = new JSONObject();
    beneficiaryBody.put("username", "john_doe52");
    beneficiaryBody.put("firstName", "John");
    beneficiaryBody.put("lastName", "Doe");
    beneficiaryBody.put("emailAddress", "johndoe@email.com");

    HttpURLConnection beneficiaryConnection = (HttpURLConnection) new URL(beneficiaryUrl).openConnection();
    beneficiaryConnection.setRequestMethod("POST");
    beneficiaryConnection.setRequestProperty("Authorization", "Bearer " + apiToken);
    beneficiaryConnection.setRequestProperty("X-MerchantId", merchantId);
    beneficiaryConnection.setRequestProperty("accept", "application/json");
    beneficiaryConnection.setRequestProperty("content-type", "application/*+json");
    beneficiaryConnection.setDoOutput(true);

    OutputStream os = beneficiaryConnection.getOutputStream();
    os.write(beneficiaryBody.toString().getBytes());
    os.flush();
    os.close();

    BufferedReader beneficiaryIn = new BufferedReader(new InputStreamReader(beneficiaryConnection.getInputStream()));
    StringBuilder beneficiaryResponse = new StringBuilder();
    while ((inputLine = beneficiaryIn.readLine()) != null) {
      beneficiaryResponse.append(inputLine);
    }
    beneficiaryIn.close();

    beneficiaryData = new JSONObject(beneficiaryResponse.toString());

    // Step 3: Create payment items
    String paymentItemsUrl = baseUrl + "/payins";
    JSONObject paymentItemsBody = new JSONObject();
    paymentItemsBody.put("items", new JSONObject[] {
        new JSONObject().put("description", "Service Fee").put("amount", 50.00).put("currency", "USD"),
        new JSONObject().put("description", "Product Purchase").put("amount", 150.00).put("currency", "USD")
    });
    paymentItemsBody.put("beneficiaryToken", beneficiaryData.getJSONObject("data").getString("beneficiaryToken"));
    paymentItemsBody.put("username", "john_doe");

    HttpURLConnection paymentItemsConnection = (HttpURLConnection) new URL(paymentItemsUrl).openConnection();
    paymentItemsConnection.setRequestMethod("POST");
    paymentItemsConnection.setRequestProperty("Authorization", "Bearer " + apiToken);
    paymentItemsConnection.setRequestProperty("X-MerchantId", merchantId);
    paymentItemsConnection.setRequestProperty("accept", "application/json");
    paymentItemsConnection.setRequestProperty("content-type", "application/*+json");
    paymentItemsConnection.setDoOutput(true);

    os = paymentItemsConnection.getOutputStream();
    os.write(paymentItemsBody.toString().getBytes());
    os.flush();
    os.close();

    BufferedReader paymentItemsIn = new BufferedReader(new InputStreamReader(paymentItemsConnection.getInputStream()));
    StringBuilder paymentItemsResponse = new StringBuilder();
    while ((inputLine = paymentItemsIn.readLine()) != null) {
      paymentItemsResponse.append(inputLine);
    }
    paymentItemsIn.close();

    JSONObject paymentItemsData = new JSONObject(paymentItemsResponse.toString());

    // Step 4: Create a webhook
    String webhookUrl = baseUrl + "/webhooks";
    JSONObject webhookBody = new JSONObject();
    webhookBody.put("alias", "PAYMENT.COMPLETED");
    webhookBody.put("eventNames", new String[] { "PAYMENT.COMPLETED" });
    webhookBody.put("url", "https://yourwebhookurl.com/notification");
    webhookBody.put("description", "Webhook for payment completion");

    HttpURLConnection webhookConnection = (HttpURLConnection) new URL(webhookUrl).openConnection();
    webhookConnection.setRequestMethod("POST");
    webhookConnection.setRequestProperty("Authorization", "Bearer " + apiToken);
    webhookConnection.setRequestProperty("X-MerchantId", merchantId);
    webhookConnection.setRequestProperty("accept", "application/json");
    webhookConnection.setRequestProperty("content-type", "application/*+json");
    webhookConnection.setDoOutput(true);

    os = webhookConnection.getOutputStream();
    os.write(webhookBody.toString().getBytes());
    os.flush();
    os.close();

    BufferedReader webhookIn = new BufferedReader(new InputStreamReader(webhookConnection.getInputStream()));
    StringBuilder webhookResponse = new StringBuilder();
    while ((inputLine = webhookIn.readLine()) != null) {
      webhookResponse.append(inputLine);
    }
    webhookIn.close();

    JSONObject webhookData = new JSONObject(webhookResponse.toString());

    // Print the webhook response
    System.out.println(webhookData.toString(4));
  }
}