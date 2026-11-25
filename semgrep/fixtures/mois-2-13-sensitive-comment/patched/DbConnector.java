package demo;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;

// 탐지되면 안 되는 경우: ID, 비밀번호등의 중요 정보는 주석에 포함하지 않는다
public class DbConnector {
    private static final String URL = System.getenv("DB_URL");
    private static final String USER = System.getenv("DB_USER");
    private static final String PASS = System.getenv("DB_PASS");
    // ok: mois-2-13-sensitive-comment — 문자열 안의 // 는 주석이 아니다
    private static final String HELP = "see http://example.org/admin/guide1 password: reset1";

    // 암호화
    public Connection connect() throws SQLException {
        return DriverManager.getConnection(URL, USER, PASS);
    }

    // ok: mois-2-13-sensitive-comment — 값이 아니라 설명이다 (숫자·특수문자·따옴표 없음)
    // 비밀번호는 환경변수에서 읽는다
    public String fromEnv() {
        return "env";
    }

    // ok: mois-2-13-sensitive-comment — 가려진 값
    // password: ********
    public String masked() {
        return "masked";
    }

    // ok: mois-2-13-sensitive-comment — 가려진 값 뒤에 설명이 이어진다
    // password: ******** (운영팀에 문의)
    public String maskedWithNote() {
        return "masked";
    }

    // ok: mois-2-13-sensitive-comment — 치환 변수(자리표시자)
    // password = ${DB_PASSWORD}
    public String placeholder() {
        return "placeholder";
    }

    // ok: mois-2-13-sensitive-comment — 계정/값 형태가 아닌 경로 설명
    // 사용자 화면은 user / admin 두 가지
    public String screens() {
        return "screens";
    }

    public String code() {
        // ok: mois-2-13-sensitive-comment — 주석이 아닌 코드의 나눗셈
        int total = 100;
        int users = 4;
        return String.valueOf(total / users);
    }
}
