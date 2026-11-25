package demo;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;

// 탐지돼야 하는 경우: 비밀번호를 소스에 직접 적음
public class DbConfig {
    // ruleid: mois-2-06-hardcoded-secret
    private static final String DB_PASSWORD = "P@ssw0rd!";
    private String apiKey;
    private String jwtSecret;

    public Connection connect() throws SQLException {
        // ruleid: mois-2-06-hardcoded-secret
        return DriverManager.getConnection("jdbc:mysql://db/app", "app", "s3cretValue");
    }

    // 선언이 아닌 대입
    public void init() {
        // ruleid: mois-2-06-hardcoded-secret
        this.apiKey = "AKIA1234567890EXAMPLE";
        // ruleid: mois-2-06-hardcoded-secret
        jwtSecret = "change-me-please";
    }

    // 지역 변수, 이름 중간에 pwd·token
    public String local() {
        // ruleid: mois-2-06-hardcoded-secret
        String adminPwdDefault = "admin1234";
        // ruleid: mois-2-06-hardcoded-secret
        String accessToken = "eyJhbGciOiJIUzI1NiJ9.e30.abc";
        return adminPwdDefault + accessToken;
    }

    // 클라우드 접근 키, 서명용 개인키
    public String[] cloud() {
        // ruleid: mois-2-06-hardcoded-secret
        String awsAccessKey = "AKIAIOSFODNN7EXAMPLE";
        // ruleid: mois-2-06-hardcoded-secret
        String signingPrivateKey = "MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQC7";
        return new String[] {awsAccessKey, signingPrivateKey};
    }

    // 값이 이름과 같은 단어로 "시작"할 뿐 실제 비밀번호인 경우
    public Connection weak(String url) throws SQLException {
        // ruleid: mois-2-06-hardcoded-secret
        String dbPasswd = "password123";
        // ruleid: mois-2-06-hardcoded-secret
        return DriverManager.getConnection(url, "app", dbPasswd);   // 상수 전파: 위의 리터럴이 그대로 쓰인다
    }
}
