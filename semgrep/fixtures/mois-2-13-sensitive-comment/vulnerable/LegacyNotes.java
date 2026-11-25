package demo;

// 탐지돼야 하는 경우: 인수인계용으로 남긴 주석에 계정·비밀번호가 그대로 있다 (표현별)
public class LegacyNotes {
    // 값에 숫자·특수문자가 있는 경우 (따옴표 없음)
    // ruleid: mois-2-13-sensitive-comment
    /* 임시 passwd = Temp#2023 */
    private String ftpHost;
    // ruleid: mois-2-13-sensitive-comment
    // FTP pwd: ftp!2345
    private String ftpUser;
    // ruleid: mois-2-13-sensitive-comment
    // default password is admin1234
    private String adminId;
    // ruleid: mois-2-13-sensitive-comment
    // 비밀번호 초기값은 init#01
    private String initValue;

    // 값을 따옴표로 감싼 경우 (숫자·특수문자 없음)
    // ruleid: mois-2-13-sensitive-comment
    // 관리자 비밀번호: "qwerty"
    private String managerId;
    // ruleid: mois-2-13-sensitive-comment
    // passwd 값은 'changeme'
    private String batchUser;
    // ruleid: mois-2-13-sensitive-comment
    // 패스워드는 "welcome"
    private String guestId;
    // ruleid: mois-2-13-sensitive-comment
    // 접속 암호: 'guest'
    private String kioskId;

    // 계정/비밀번호 쌍 (DB·서버의 흔한 계정 이름)
    // ruleid: mois-2-13-sensitive-comment
    // MSSQL 접속: sa / P@ssw0rd
    private String mssqlUrl;
    // ruleid: mois-2-13-sensitive-comment
    // Oracle 관리 계정 sys/oracle12 as sysdba
    private String oracleUrl;
    // ruleid: mois-2-13-sensitive-comment
    /* 설치 직후 계정 system/manager1 그대로 사용 중 */
    private String oracleSid;
    // ruleid: mois-2-13-sensitive-comment
    // 관리 콘솔 admin / admin123
    private String consoleUrl;
    // ruleid: mois-2-13-sensitive-comment
    // 시험 서버 test/test1234
    private String stagingUrl;
    // ruleid: mois-2-13-sensitive-comment
    // 파일 서버 user / ftp#2020
    private String fileServer;
}
