package demo;

import java.sql.Connection;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import javax.servlet.http.HttpServletRequest;

// 탐지돼야 하는 경우: 외부 입력을 SQL 문에 이어 붙임
public class UserDao {
    private Connection conn;

    // 외부 입력을 문자열로 이어 붙여 Statement 로 실행
    public ResultSet findByName(HttpServletRequest request) throws SQLException {
        String name = request.getParameter("name");
        Statement stmt = conn.createStatement();
        // ruleid: mois-1-01-sql-injection-jdbc
        return stmt.executeQuery("SELECT * FROM users WHERE name = '" + name + "'");
    }

    // PreparedStatement 를 써도 SQL 문을 이어 붙이면 SQL 삽입
    public ResultSet findByEmail(HttpServletRequest request) throws SQLException {
        String email = request.getParameter("email");
        // ruleid: mois-1-01-sql-injection-jdbc
        return conn.prepareStatement("SELECT * FROM users WHERE email = '" + email + "'").executeQuery();
    }
}
