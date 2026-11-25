package demo;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;

// 탐지돼야 하는 경우: 주석에 DB 계정과 비밀번호가 남아 있음
public class DbConnector {
    private static final String URL = System.getenv("DB_URL");
    private static final String USER = System.getenv("DB_USER");
    private static final String PASS = System.getenv("DB_PASS");

    // ruleid: mois-2-13-sensitive-comment
    // DB연결 root / a1q2w3r3f2!@
    public Connection connect() throws SQLException {
        return DriverManager.getConnection(URL, USER, PASS);
    }

    /*
     // ruleid: mois-2-13-sensitive-comment
     * Password for administrator is "tiger."
     */
    public Connection admin() throws SQLException {
        return DriverManager.getConnection(URL, "admin", PASS);
    }

    // ruleid: mois-2-13-sensitive-comment
    // 암호화 전, 후 : 1365ADMIN_01, aa84c40031d808196537ad3dcf81f9af
    public String sample() {
        return "sample";
    }

    // ruleid: mois-2-13-sensitive-comment
    // TODO 운영 반영 전 삭제: password=Qwer1234!
    public String todo() {
        return "todo";
    }

    public String inline() {
        // ruleid: mois-2-13-sensitive-comment
        return "inline"; // 테스트 계정 비밀번호는 test1234
    }

    // ruleid: mois-2-13-sensitive-comment
    /* 관리자 pwd = 'admin' 초기값 그대로 */
    public String block() {
        return "block";
    }

    /**
     * 운영 DB 접속 정보.
     // ruleid: mois-2-13-sensitive-comment
     * 패스워드: Oper#2024
     */
    public String javadoc() {
        return "javadoc";
    }

    // ruleid: mois-2-13-sensitive-comment
    /* 개발 서버 scott/tiger1 로 접속 */
    public String slashPair() {
        return "pair";
    }
}
