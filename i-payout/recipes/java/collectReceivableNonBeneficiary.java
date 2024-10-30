package java;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.Base64;
import org.json.JSONObject;

public class collectReceivableNonBeneficiary {

  private static final String BASE_URL = "https://merchantapi.testewallet.com/api/v1";
  private static final String USERNAME = "<username>"; // replace with your username
  private static final String PASSWORD = "<password>"; // Replace with your password

  public static void main(String[] args) {
    try {
      // Autenticação Base64
      String authStr = USERNAME + ":" + PASSWORD;
      String encodedAuthStr = Base64.getEncoder().encodeToString(authStr.getBytes());

      // Get the authentication token
      String tokenUrl = BASE_URL + "/authentication/login";
      HttpURLConnection tokenConnection = (HttpURLConnection) new URL(tokenUrl).openConnection();
      tokenConnection.setRequestMethod("GET");
      tokenConnection.setRequestProperty("accept", "application/json");
      tokenConnection.setRequestProperty("authorization", "Basic " + encodedAuthStr);
      tokenConnection.setRequestProperty("X-MerchantId", USERNAME);

      String apiToken = getResponseData(tokenConnection).getJSONObject("data").getString("token");
      String merchantId = USERNAME;

      // Create a Public Invoice
      String publicInvoiceUrl = BASE_URL + "/payins/public-invoice";
      JSONObject publicInvoiceBody = new JSONObject();
      publicInvoiceBody.put("currencyCode", "USD");
      publicInvoiceBody.put("merchantReferenceId", "your-reference-id");
      publicInvoiceBody.put("arrItems", new org.json.JSONArray()
          .put(new JSONObject().put("amount", 50.00)
              .put("description", "Payment for Service")
              .put("quantity", 1)));

      HttpURLConnection invoiceConnection = (HttpURLConnection) new URL(publicInvoiceUrl).openConnection();
      invoiceConnection.setRequestMethod("POST");
      invoiceConnection.setRequestProperty("Authorization", "Bearer " + apiToken);
      invoiceConnection.setRequestProperty("X-MerchantId", merchantId);
      invoiceConnection.setRequestProperty("accept", "application/json");
      invoiceConnection.setRequestProperty("content-type", "application/json");
      sendRequestBody(invoiceConnection, publicInvoiceBody.toString());

      JSONObject invoiceData = getResponseData(invoiceConnection);
      String transactionRefNumber = invoiceData.getJSONObject("data").toString();

      String testPaymentUrl = "https://merchant.testewallet.com/PublicCheckout/Checkout.aspx?PaymentGuid="
          + transactionRefNumber;
      String prodPaymentUrl = "https://merchant.globalewallet.com/PublicCheckout/Checkout.aspx?PaymentGuid="
          + transactionRefNumber;

      // Subscribe to Webhook
      String webhookUrl = BASE_URL + "/webhooks";
      JSONObject webhookBody = new JSONObject();
      webhookBody.put("eventNames", new org.json.JSONArray().put("PAYMENT.STATUS.UPDATED"));
      webhookBody.put("url", "https://webhook.site/#!/view/94480622-0f4f-4b1c-bbf4-0d3071c0958a");
      webhookBody.put("alias", "Payment_status_update");

      HttpURLConnection webhookConnection = (HttpURLConnection) new URL(webhookUrl).openConnection();
      webhookConnection.setRequestMethod("POST");
      webhookConnection.setRequestProperty("Authorization", "Bearer " + apiToken);
      webhookConnection.setRequestProperty("X-MerchantId", merchantId);
      webhookConnection.setRequestProperty("accept", "application/json");
      webhookConnection.setRequestProperty("content-type", "application/*+json");
      sendRequestBody(webhookConnection, webhookBody.toString());

      JSONObject webhookData = getResponseData(webhookConnection);
      System.out.println(webhookData.toString());

    } catch (Exception e) {
      e.printStackTrace();
    }
  }

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

  private static void sendRequestBody(HttpURLConnection connection, String body) throws Exception {
    connection.setDoOutput(true);
    try (OutputStream os = connection.getOutputStream()) {
      byte[] input = body.getBytes("utf-8");
      os.write(input, 0, input.length);
    }
  }
}