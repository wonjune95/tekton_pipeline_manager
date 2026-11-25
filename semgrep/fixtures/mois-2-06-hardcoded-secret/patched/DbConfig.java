package demo;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;

// 탐지되면 안 되는 경우: 환경변수에서 읽음, 파라미터 이름 상수는 비밀번호가 아님
public class DbConfig {
    // ok: mois-2-06-hardcoded-secret — 환경변수에서 읽는다
    private static final String DB_PASSWORD = System.getenv("DB_PASSWORD");
    // ok: mois-2-06-hardcoded-secret — 값이 파라미터 이름 그 자체
    private static final String PASSWORD_FIELD = "password";
    // ok: mois-2-06-hardcoded-secret — 값이 헤더·키 이름일 뿐 (apiKey 라는 단어 그 자체)
    private static final String API_KEY_PARAM = "api_key";
    // ok: mois-2-06-hardcoded-secret — 아래 넷도 요청 파라미터·헤더·JSON 필드의 "이름"이다
    private static final String PASSWD_PARAM = "passwd";
    private static final String CLIENT_SECRET_FIELD = "secret";
    private static final String TOKEN_PARAM = "token";
    private static final String ACCESS_KEY_HEADER = "accessKey";
    // ok: mois-2-06-hardcoded-secret — 비어 있는 초기값
    private String password = "";
    // ok: mois-2-06-hardcoded-secret — 이름이 비밀정보가 아니다
    private static final String DB_URL = "jdbc:mysql://db/app";

    public Connection connect(String url, String user) throws SQLException {
        // ok: mois-2-06-hardcoded-secret — 세 번째 인자가 문자열 리터럴이 아니다
        return DriverManager.getConnection(url, user, DB_PASSWORD);
    }

    public void setPassword(String value) {
        // ok: mois-2-06-hardcoded-secret — 리터럴이 아닌 값의 대입
        this.password = value;
    }
}
