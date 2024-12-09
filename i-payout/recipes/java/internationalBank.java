import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.net.URI;
import java.util.Base64;
import org.json.JSONObject;

public class internationalBank {
    private static final String BASE_URL = "https://merchantapi.testewallet.com/api/v1";
    private static final String USERNAME = "<USERNAME>"; // Replace with your username
    private static final String PASSWORD = "<PASSWORD>"; // Replace with your password
    private static final String MERCHANT_ID = "<MERCHANT_ID>"; // Replace with your merchant ID

    public static void main(String[] args) {
        try {
            String apiToken = getApiToken();
            String beneficiaryToken = createBeneficiary(apiToken);
            addTransferMethod(apiToken, beneficiaryToken);
            createTransfer(apiToken, beneficiaryToken);
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

    private static void addTransferMethod(String apiToken, String beneficiaryToken) throws Exception {
        JSONObject body = new JSONObject();
        body.put("beneficiaryToken", beneficiaryToken);
        body.put("accountHolderName", "<ACCOUNT_HOLDER_NAME>");
        body.put("accountNickName", "<ACCOUNT_NICKNAME>");
        body.put("accountCurrency", "<CURRENCY>");
        body.put("accountNumber", "<ACCOUNT_NUMBER>");
        body.put("accountType1", "<ACCOUNT_TYPE_1>");
        body.put("accountType2", "<ACCOUNT_TYPE_2>");
        body.put("bankName", "<BANK_NAME>");
        body.put("bankCode", "<BANK_CODE>");
        body.put("bankCountry", "<BANK_COUNTRY>");
        body.put("swiftCode", "<SWIFT_CODE>");
        body.put("routingNumber", "<ROUTING_NUMBER>");
        body.put("branchAddress", "<BRANCH_ADDRESS>");
        body.put("beneficiaryFirstName", "<BENEFICIARY_FIRST_NAME>");
        body.put("beneficiaryLastName", "<BENEFICIARY_LAST_NAME>");
        body.put("beneficiaryCountry", "<BENEFICIARY_COUNTRY>");
        body.put("beneficiaryAddress1", "<BENEFICIARY_ADDRESS>");
        body.put("beneficiaryState", "<BENEFICIARY_STATE>");
        body.put("beneficiaryCity", "<BENEFICIARY_CITY>");
        body.put("beneficiaryZipCode", "<BENEFICIARY_ZIP_CODE>");

        HttpClient client = HttpClient.newHttpClient();
        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create(BASE_URL + "/transfermethods/beneficiaries/" + beneficiaryToken + "/bank-accounts"))
                .header("Authorization", "Bearer " + apiToken)
                .header("X-MerchantId", MERCHANT_ID)
                .header("Content-Type", "application/json")
                .POST(HttpRequest.BodyPublishers.ofString(body.toString()))
                .build();

        client.send(request, HttpResponse.BodyHandlers.ofString());
    }

    private static void createTransfer(String apiToken, String beneficiaryToken) throws Exception {
        JSONObject body = new JSONObject();
        body.put("merchantTransactionId", "<TRANSACTION_ID>");
        body.put("beneficiaryToken", beneficiaryToken);
        body.put("autoApprove", true);
        body.put("comments", "<COMMENTS>");
        body.put("dateExpire", "<EXPIRATION_DATE>");
        body.put("destinationAmount", "<AMOUNT>");
        body.put("destinationCurrency", "<CURRENCY>");
        body.put("destinationType", "<DESTINATION_TYPE>");
        JSONObject bankAccount = new JSONObject();
        bankAccount.put("accountNickName", "<ACCOUNT_NICKNAME>");
        bankAccount.put("accountCurrency", "<CURRENCY>");
        bankAccount.put("accountNumber", "<ACCOUNT_NUMBER>");
        bankAccount.put("accountType1", "<ACCOUNT_TYPE_1>");
        bankAccount.put("accountType2", "<ACCOUNT_TYPE_2>");
        bankAccount.put("bankName", "<BANK_NAME>");
        bankAccount.put("bankCountry", "<BANK_COUNTRY>");
        bankAccount.put("routingNumber", "<ROUTING_NUMBER>");
        bankAccount.put("branchAddress", "<BRANCH_ADDRESS>");
        bankAccount.put("beneficiaryFirstName", "<BENEFICIARY_FIRST_NAME>");
        bankAccount.put("beneficiaryLastName", "<BENEFICIARY_LAST_NAME>");
        bankAccount.put("beneficiaryDateOfBirth", "<DATE_OF_BIRTH>");
        bankAccount.put("beneficiaryGovernmentID", "<GOVERNMENT_ID>");
        bankAccount.put("beneficiaryCountry", "<BENEFICIARY_COUNTRY>");
        bankAccount.put("beneficiaryAddress1", "<BENEFICIARY_ADDRESS>");
        bankAccount.put("beneficiaryState", "<BENEFICIARY_STATE>");
        bankAccount.put("beneficiaryCity", "<BENEFICIARY_CITY>");
        bankAccount.put("beneficiaryZipCode", "<BENEFICIARY_ZIP_CODE>");
        body.put("bankAccount", bankAccount);

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
