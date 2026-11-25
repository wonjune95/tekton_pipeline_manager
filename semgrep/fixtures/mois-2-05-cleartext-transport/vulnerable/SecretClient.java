package demo;

import java.io.IOException;
import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.URI;
import java.net.URISyntaxException;
import java.net.URL;

// 탐지돼야 하는 경우: 중요정보를 암호화되지 않은 http:// 로 전송
public class SecretClient {
    private static final String LOGIN_API = "http://auth.example.org/login";

    public void put(byte[] body) throws IOException {
        // ruleid: mois-2-05-cleartext-transport
        URL u = new URL("http://www.secret.example.org/");
        HttpURLConnection hu = (HttpURLConnection) u.openConnection();
        hu.setRequestMethod("PUT");
        hu.setDoOutput(true);
        try (OutputStream os = hu.getOutputStream()) {
            os.write(body);
        }
        hu.disconnect();
    }

    public URI uri() throws URISyntaxException {
        // ruleid: mois-2-05-cleartext-transport
        return new URI("HTTP://api.example.org/members");
    }

    public URI created() {
        // ruleid: mois-2-05-cleartext-transport
        return URI.create("http://10.0.0.5:8080/pay");
    }

    // 상수로 둔 주소
    public URL constant() throws IOException {
        // ruleid: mois-2-05-cleartext-transport
        return new URL(LOGIN_API);
    }

    // localhost 로 시작하지만 다른 호스트
    public URL lookalike() throws IOException {
        // ruleid: mois-2-05-cleartext-transport
        return new URL("http://localhost.example.org/");
    }
}
