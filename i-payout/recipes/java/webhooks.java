package java;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.Base64;
import javax.crypto.Mac;
import javax.crypto.spec.SecretKeySpec;
import org.json.JSONObject;

public class webhooks {

  private static final String BASE_URL = "https://merchantapi.testewallet.com/api/v1";
  private static final String USERNAME = "<username>"; // Replace with your username
  private static final String PASSWORD = "<password>"; // Replace with your password

  public static void main(String[] args) {
    try {
      // Encode the username:password in Base64 for Basic Authentication
      String authStr = USERNAME + ":" + PASSWORD;
      String encodedAuthStr = Base64.getEncoder().encodeToString(authStr.getBytes());

      // Login and obtain the API token
      String tokenUrl = BASE_URL + "/authentication/login";
      HttpURLConnection tokenConnection = (HttpURLConnection) new URL(tokenUrl).openConnection();
      tokenConnection.setRequestMethod("GET");
      tokenConnection.setRequestProperty("accept", "application/json");
      tokenConnection.setRequestProperty("authorization", "Basic " + encodedAuthStr);
      tokenConnection.setRequestProperty("X-MerchantId", USERNAME);

      // Parse the response to get the API token
      String apiToken = getResponseData(tokenConnection).getJSONObject("data").getString("token");
      String merchantId = USERNAME;

      // Create a webhook
      String webhookUrl = BASE_URL + "/webhooks";
      JSONObject webhookBody = new JSONObject();
      webhookBody.put("eventNames", new org.json.JSONArray().put("PAYMENT.CREATED"));
      webhookBody.put("url", "https://webhook.site/#!/view/94480622-0f4f-4b1c-bbf4-0d3071c0958a");
      webhookBody.put("alias", "WebhookTest");

      HttpURLConnection webhookConnection = (HttpURLConnection) new URL(webhookUrl).openConnection();
      webhookConnection.setRequestMethod("POST");
      webhookConnection.setRequestProperty("Authorization", "Bearer " + apiToken);
      webhookConnection.setRequestProperty("X-MerchantId", merchantId);
      webhookConnection.setRequestProperty("accept", "application/json");
      webhookConnection.setRequestProperty("content-type", "application/*+json");
      sendRequestBody(webhookConnection, webhookBody.toString());

      // Parse the response to get the webhook token
      JSONObject webhookData = getResponseData(webhookConnection);
      String webhookToken = webhookData.getJSONObject("data").getString("token");

      // Activate the webhook
      String activateWebhookUrl = BASE_URL + "/webhooks/" + webhookToken + "/activate";
      HttpURLConnection activateConnection = (HttpURLConnection) new URL(activateWebhookUrl).openConnection();
      activateConnection.setRequestMethod("POST");
      activateConnection.setRequestProperty("Authorization", "Bearer " + apiToken);
      activateConnection.setRequestProperty("X-MerchantId", merchantId);
      activateConnection.setRequestProperty("accept", "application/json");
      getResponseData(activateConnection); // Activation response

    } catch (Exception e) {
      e.printStackTrace();
    }
  }

  // Helper method to read the response from the connection and parse it as a JSON
  // object
  private static JSONObject getResponseData(HttpURLConnection connection) throws Exception {
    BufferedReader in = new BufferedReader(new InputStreamReader(connection.getInputStream()));
    String inputLine;
    StringBuilder content = new StringBuilder();
    while ((inputLine = in.readLine()) != null) {
      content.append(inputLine);
    }
    in.close();
    return new JSONObject(content.toString());
  }

  // Helper method to send a JSON body with the request
  private static void sendRequestBody(HttpURLConnection connection, String body) throws Exception {
    connection.setDoOutput(true);
    try (OutputStream os = connection.getOutputStream()) {
      byte[] input = body.getBytes("utf-8");
      os.write(input, 0, input.length);
    }
  }

  // Method to verify the webhook signature
  public static boolean verifyWebhookSignature(String publicKey, String timestamp, String notificationUrl,
      String jsonBody, String receivedSignature) {
    try {
      // Create the signature body by concatenating timestamp, URL, and JSON body
      String signatureBody = timestamp + "#" + notificationUrl + "#" + jsonBody;

      // Hash the signature body using SHA-256
      Mac sha256Hmac = Mac.getInstance("HmacSHA256");
      SecretKeySpec secretKey = new SecretKeySpec(publicKey.getBytes(), "HmacSHA256");
      sha256Hmac.init(secretKey);
      byte[] signatureHash = sha256Hmac.doFinal(signatureBody.getBytes());

      // Encode the hash to Base64
      String expectedSignature = Base64.getEncoder().encodeToString(signatureHash);

      // Compare the received signature with the expected one
      return receivedSignature.equals(expectedSignature);
    } catch (Exception e) {
      System.out.println("Signature verification failed: " + e.getMessage());
      return false;
    }
  }

  // Example usage of the signature verification function
  public static void exampleVerification() {
    String publicKey = "<public_key>"; // Replace with your actual public key
    String timestamp = "<x-timestamp_value>"; // Replace with the timestamp from the webhook header
    String notificationUrl = "https://webhook.site/#!/view/94480622-0f4f-4b1c-bbf4-0d3071c0958a"; // Replace with the
                                                                                                  // actual notification
                                                                                                  // URL
    String jsonBody = "{\"event\":\"PAYMENT.COMPLETED\"}"; // Replace with the actual JSON payload
    String receivedSignature = "<x-signature_value>"; // Replace with the actual signature from the webhook header

    // Verify the signature
    boolean isValid = verifyWebhookSignature(publicKey, timestamp, notificationUrl, jsonBody, receivedSignature);
    if (isValid) {
      System.out.println("Webhook signature is valid.");
    } else {
      System.out.println("Webhook signature is invalid.");
    }
  }
}