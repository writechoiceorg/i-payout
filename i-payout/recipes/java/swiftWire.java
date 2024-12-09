import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.net.URI;
import java.util.Base64;
import org.json.JSONObject;

public class swiftWire {
  private static final String BASE_URL = "https://merchantapi.testewallet.com/api/v1";
  private static final String USERNAME = "<USERNAME>"; // Replace with your username
  private static final String PASSWORD = "<PASSWORD>"; // Replace with your password
  private static final String MERCHANT_ID = "<MERCHANT_ID>"; // Replace with your merchant ID

  public static void main(String[] args) {
    try {
      String apiToken = getApiToken();
      String beneficiaryToken = createBeneficiary(apiToken);
      addWireTransferMethod(apiToken, beneficiaryToken);
      createWireTransfer(apiToken, beneficiaryToken);
    } catch (Exception e) {
      e.printStackTrace();
    }
  }

  private static String getApiToken() throws Exception {
    String authStr = USERNAME + ":" + PASSWORD;
    String encodedAuthStr = Base64.getEncoder().encodeToString(authStr.getBytes());

    HttpClient client = HttpClient.newHttpClient();
    HttpRequest request = HttpRequest.newBuilder()
        .uri(URI.create(BASE_URL + "/authentication/login"))
        .header("accept", "application/json")
        .header("authorization", "Basic " + encodedAuthStr)
        .header("X-MerchantId", MERCHANT_ID)
        .build();

    HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());
    JSONObject jsonResponse = new JSONObject(response.body());
    return jsonResponse.getJSONObject("data").getString("token");
  }

  private static String createBeneficiary(String apiToken) throws Exception {
    JSONObject body = new JSONObject();
    body.put("username", "<USERNAME>");
    body.put("firstName", "<FIRST_NAME>");
    body.put("lastName", "<LAST_NAME>");
    body.put("emailAddress", "<EMAIL_ADDRESS>");

    HttpClient client = HttpClient.newHttpClient();
    HttpRequest request = HttpRequest.newBuilder()
        .uri(URI.create(BASE_URL + "/beneficiaries"))
        .header("Authorization", "Bearer " + apiToken)
        .header("X-MerchantId", MERCHANT_ID)
        .header("Content-Type", "application/json")
        .POST(HttpRequest.BodyPublishers.ofString(body.toString()))
        .build();

    HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());
    JSONObject jsonResponse = new JSONObject(response.body());
    return jsonResponse.getJSONObject("data").getString("beneficiaryToken");
  }

  private static void addWireTransferMethod(String apiToken, String beneficiaryToken) throws Exception {
    JSONObject body = new JSONObject();
    body.put("accountNickName", "<ACCOUNT_NICKNAME>");
    body.put("beneficiaryCountry", "<BENEFICIARY_COUNTRY>");
    body.put("accountType1", "<ACCOUNT_TYPE_1>");
    body.put("beneficiaryAddress1", "<BENEFICIARY_ADDRESS>");
    body.put("beneficiaryCity", "<BENEFICIARY_CITY>");
    body.put("beneficiaryState", "<BENEFICIARY_STATE>");
    body.put("beneficiaryZipCode", "<BENEFICIARY_ZIP_CODE>");
    body.put("bankCountry", "<BANK_COUNTRY>");
    body.put("accountNumber", "<ACCOUNT_NUMBER>");
    body.put("bankName", "<BANK_NAME>");
    body.put("bankAddress1", "<BANK_ADDRESS>");
    body.put("bankCity", "<BANK_CITY>");
    body.put("bankState", "<BANK_STATE>");
    body.put("bankZipCode", "<BANK_ZIP_CODE>");

    HttpClient client = HttpClient.newHttpClient();
    HttpRequest request = HttpRequest.newBuilder()
        .uri(URI.create(BASE_URL + "/transfermethods/beneficiaries/" + beneficiaryToken + "/wires"))
        .header("Authorization", "Bearer " + apiToken)
        .header("X-MerchantId", MERCHANT_ID)
        .header("Content-Type", "application/json")
        .POST(HttpRequest.BodyPublishers.ofString(body.toString()))
        .build();

    client.send(request, HttpResponse.BodyHandlers.ofString());
  }

  private static void createWireTransfer(String apiToken, String beneficiaryToken) throws Exception {
    JSONObject body = new JSONObject();
    body.put("merchantTransactionId", "<TRANSACTION_ID>");
    body.put("beneficiaryToken", beneficiaryToken);
    body.put("autoApprove", true);
    body.put("comments", "<COMMENTS>");
    body.put("dateExpire", "<EXPIRATION_DATE>");
    body.put("destinationAmount", "<AMOUNT>");
    body.put("destinationCurrency", "<DESTINATION_CURRENCY>");
    body.put("destinationType", "<DESTINATION_TYPE>");

    JSONObject wireProfile = new JSONObject();
    wireProfile.put("accountNickName", "<ACCOUNT_NICKNAME>");
    wireProfile.put("beneficiaryCountry", "<BENEFICIARY_COUNTRY>");
    wireProfile.put("accountType1", "<ACCOUNT_TYPE_1>");
    wireProfile.put("beneficiaryAddress1", "<BENEFICIARY_ADDRESS>");
    wireProfile.put("beneficiaryCity", "<BENEFICIARY_CITY>");
    wireProfile.put("beneficiaryState", "<BENEFICIARY_STATE>");
    wireProfile.put("beneficiaryZipCode", "<BENEFICIARY_ZIP_CODE>");
    wireProfile.put("bankCountry", "<BANK_COUNTRY>");
    wireProfile.put("routingNumber", "<ROUTING_NUMBER>");
    wireProfile.put("accountNumber", "<ACCOUNT_NUMBER>");
    wireProfile.put("bankName", "<BANK_NAME>");
    wireProfile.put("bankAddress1", "<BANK_ADDRESS>");
    wireProfile.put("bankCity", "<BANK_CITY>");
    wireProfile.put("bankState", "<BANK_STATE>");
    wireProfile.put("bankZipCode", "<BANK_ZIP_CODE>");
    body.put("wireProfile", wireProfile);

    HttpClient client = HttpClient.newHttpClient();
    HttpRequest request = HttpRequest.newBuilder()
        .uri(URI.create(BASE_URL + "/transfers"))
        .header("Authorization", "Bearer " + apiToken)
        .header("X-MerchantId", MERCHANT_ID)
        .header("Content-Type", "application/json")
        .POST(HttpRequest.BodyPublishers.ofString(body.toString()))
        .build();

    HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());
    System.out.println(response.body());
  }
}
