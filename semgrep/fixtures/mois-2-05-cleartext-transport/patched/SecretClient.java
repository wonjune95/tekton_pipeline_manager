package demo;

import java.net.MalformedURLException;
import java.net.URI;
import java.net.URL;

// 탐지되면 안 되는 경우: https 보안 채널 사용
public class SecretClient {
    public URL endpoint() throws MalformedURLException {
        // ok: mois-2-05-cleartext-transport — https
        return new URL("https://www.secret.example.org/");
    }

    public URI api() {
        // ok: mois-2-05-cleartext-transport — https
        return URI.create("https://api.example.org/members");
    }

    public URL local() throws MalformedURLException {
        // ok: mois-2-05-cleartext-transport — 같은 장비 안의 통신(localhost)은 대상이 아니다
        return new URL("http://localhost:8080/health");
    }

    public URI localBase() {
        // ok: mois-2-05-cleartext-transport — 포트·경로 없이 localhost 만 적은 기준 주소
        return URI.create("http://localhost");
    }

    public URI loopback() {
        // ok: mois-2-05-cleartext-transport — 루프백 주소
        return URI.create("http://127.0.0.1/health");
    }
}
