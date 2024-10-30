package java;

import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.URL;
import java.nio.charset.StandardCharsets;
import java.util.Base64;

public class spendback {

  private static final String BASE_URL = "https://merchantapi.testewallet.com/api/v1";
  private static final String USERNAME = "<username>"; // Replace with your actual username
  private static final String PASSWORD = "<password>"; // Replace with your actual password
  private static String authStr = USERNAME + ":" + PASSWORD;
  private static String encodedAuthStr = Base64.getEncoder().encodeToString(authStr.getBytes(StandardCharsets.UTF_8));

  private static String apiToken;
  private static final String BENEFICIARY_TOKEN = "<beneficiaryToken>"; // Replace with actual beneficiary token
  private static final String CURRENCY_CODE = "USD"; // Replace with actual currency code if different

  public static void main(String[] args) throws Exception {
    authenticate();
    checkBalance();
    performSpendback();
  }

  // Authenticate the user and retrieve the API token
  private static void authenticate() throws Exception {
    URL url = new URL(BASE_URL + "/authentication/login");
    HttpURLConnection conn = (HttpURLConnection) url.openConnection();
    conn.setRequestMethod("GET");
    conn.setRequestProperty("Accept", "application/json");
    conn.setRequestProperty("Authorization", "Basic " + encodedAuthStr);
    conn.setRequestProperty("X-MerchantId", USERNAME);

    int responseCode = conn.getResponseCode();
    if (responseCode == HttpURLConnection.HTTP_OK) {
      String response = new String(conn.getInputStream().readAllBytes(), StandardCharsets.UTF_8);
      // Manually parse JSON to extract the token
      String tokenKey = "\"token\":\"";
      int tokenStart = response.indexOf(tokenKey) + tokenKey.length();
      int tokenEnd = response.indexOf("\"", tokenStart);
      apiToken = response.substring(tokenStart, tokenEnd);
    } else {
      throw new RuntimeException("Failed to authenticate: " + responseCode);
    }
    conn.disconnect();
  }

  // Check the balance of the beneficiary
  private static void checkBalance() throws Exception {
    URL url = new URL(BASE_URL + "/beneficiaries/" + BENEFICIARY_TOKEN + "/balances/" + CURRENCY_CODE);
    HttpURLConnection conn = (HttpURLConnection) url.openConnection();
    conn.setRequestMethod("GET");
    conn.setRequestProperty("Authorization", "Bearer " + apiToken);
    conn.setRequestProperty("X-MerchantId", USERNAME);
    conn.setRequestProperty("Accept", "application/json");

    int responseCode = conn.getResponseCode();
    String _response = conn.getResponseMessage();
    if (responseCode == HttpURLConnection.HTTP_OK) {
      String response = new String(conn.getInputStream().readAllBytes(), StandardCharsets.UTF_8);
      // Print the balance data
      System.out.println(response);
    } else {
      throw new RuntimeException("Failed to check balance: " + responseCode);
    }
    conn.disconnect();
  }

  // Perform the spendback operation
  private static void performSpendback() throws Exception {
    URL url = new URL(BASE_URL + "/payins/spendback");
    HttpURLConnection conn = (HttpURLConnection) url.openConnection();
    conn.setRequestMethod("POST");
    conn.setRequestProperty("Authorization", "Bearer " + apiToken);
    conn.setRequestProperty("X-MerchantId", USERNAME);
    conn.setRequestProperty("Accept", "application/json");
    conn.setRequestProperty("Content-Type", "application/*+json");

    // Manually create the JSON string for the request body
    String jsonBody = "{"
        + "\"amount\":100.00," // Replace with the amount you want to spend back
        + "\"currency\":\"USD\"," // Replace with actual currency if different
        + "\"reference\":\"spendback_001\""
        + "}";

    conn.setDoOutput(true);
    try (OutputStream os = conn.getOutputStream()) {
      os.write(jsonBody.getBytes(StandardCharsets.UTF_8));
      os.flush();
    }

    int responseCode = conn.getResponseCode();
    if (responseCode == HttpURLConnection.HTTP_OK) {
      String response = new String(conn.getInputStream().readAllBytes(), StandardCharsets.UTF_8);
      System.out.println(response);
    } else {
      throw new RuntimeException("Failed to perform spendback: " + responseCode);
    }
    conn.disconnect();
  }
}