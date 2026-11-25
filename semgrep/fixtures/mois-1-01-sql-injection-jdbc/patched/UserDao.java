package demo;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import javax.servlet.http.HttpServletRequest;

// 탐지되면 안 되는 경우: 값은 바인딩으로 넘기거나 숫자로 변환해서 쓴다
public class UserDao {
    private Connection conn;

    // 바인딩 변수 사용: 질의문은 상수, 입력값은 setString 으로만 전달
    public ResultSet findByName(HttpServletRequest request) throws SQLException {
        String name = request.getParameter("name");
        // ok: mois-1-01-sql-injection-jdbc — 질의문이 상수
        PreparedStatement ps = conn.prepareStatement("SELECT * FROM users WHERE name = ?");
        // ok: mois-1-01-sql-injection-jdbc — 바인딩 값은 질의문 인자가 아니다
        ps.setString(1, name);
        return ps.executeQuery();
    }

    // 여러 값을 바인딩하고 배치로 실행
    public int[] rename(HttpServletRequest request) throws SQLException {
        PreparedStatement ps = conn.prepareStatement("UPDATE users SET name = ? WHERE email = ?");
        ps.setString(1, request.getParameter("name"));
        ps.setString(2, request.getParameter("email"));
        // ok: mois-1-01-sql-injection-jdbc — 인자 없는 addBatch() 는 바인딩한 값을 묶을 뿐이다
        ps.addBatch();
        return ps.executeBatch();
    }

    // 정수로 변환해 검증
    public ResultSet findById(HttpServletRequest request) throws SQLException {
        int id = Integer.parseInt(request.getParameter("id"));
        Statement stmt = conn.createStatement();
        // ok: mois-1-01-sql-injection-jdbc — int 로 변환한 값
        return stmt.executeQuery("SELECT * FROM users WHERE id = " + id);
    }

    public ResultSet findBySeq(HttpServletRequest request) throws SQLException {
        long seq = Long.parseLong(request.getParameter("seq"));
        Statement stmt = conn.createStatement();
        // ok: mois-1-01-sql-injection-jdbc — long 으로 변환한 값
        return stmt.executeQuery("SELECT * FROM users WHERE seq = " + seq);
    }

    // 변환 식을 질의문에 바로 이어 붙여도 들어가는 것은 숫자(변환 결과)뿐이다
    public ResultSet findInline(HttpServletRequest request) throws SQLException {
        Statement stmt = conn.createStatement();
        // ok: mois-1-01-sql-injection-jdbc — 변환 결과만 질의문에 들어간다
        return stmt.executeQuery("SELECT * FROM users WHERE id = " + Integer.parseInt(request.getParameter("id")) + " AND seq = " + Long.parseLong(request.getParameter("seq")));
    }

    // 선언과 대입을 나눠 써도 같다 (변환 실패 시 기본값)
    public ResultSet findPage(HttpServletRequest request) throws SQLException {
        int page;
        long last;
        try {
            page = Integer.parseInt(request.getParameter("page"));
            last = Long.parseLong(request.getParameter("last"));
        } catch (NumberFormatException e) {
            page = 1;
            last = 0L;
        }
        Statement stmt = conn.createStatement();
        // ok: mois-1-01-sql-injection-jdbc — 어느 경로로 와도 숫자
        return stmt.executeQuery("SELECT * FROM users WHERE seq > " + last + " LIMIT 20 OFFSET " + (page - 1) * 20);
    }
}
