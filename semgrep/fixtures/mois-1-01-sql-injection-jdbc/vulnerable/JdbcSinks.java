package demo;

import java.sql.Connection;
import java.sql.SQLException;
import java.sql.Statement;
import javax.servlet.http.HttpServletRequest;
import javax.sql.DataSource;

// sink 가지마다 한 줄씩: JDBC 전용 메서드 이름(수신 객체 타입 무관)과, 타입이 확인될 때만 보는 execute·nativeSQL
public class JdbcSinks {
    private Connection conn;
    private Statement stmt;
    private DataSource dataSource;

    // java.sql.Statement — execute 는 타입으로, 나머지는 메서드 이름으로 잡힌다
    public void typedStatement(HttpServletRequest request) throws SQLException {
        String sql = "DELETE FROM users WHERE name = '" + request.getParameter("name") + "'";
        // ruleid: mois-1-01-sql-injection-jdbc
        stmt.executeQuery(sql);
        // ruleid: mois-1-01-sql-injection-jdbc
        stmt.executeUpdate(sql);
        // ruleid: mois-1-01-sql-injection-jdbc
        stmt.executeLargeUpdate(sql);
        // ruleid: mois-1-01-sql-injection-jdbc
        stmt.execute(sql);
        // ruleid: mois-1-01-sql-injection-jdbc
        stmt.execute(sql, Statement.RETURN_GENERATED_KEYS);
        // ruleid: mois-1-01-sql-injection-jdbc
        stmt.addBatch(sql);
    }

    // java.sql.Connection — nativeSQL 은 타입으로, 나머지는 메서드 이름으로 잡힌다
    public void typedConnection(HttpServletRequest request) throws SQLException {
        String sql = "{call find_user('" + request.getParameter("name") + "')}";
        // ruleid: mois-1-01-sql-injection-jdbc
        conn.prepareStatement(sql);
        // ruleid: mois-1-01-sql-injection-jdbc
        conn.prepareCall(sql);
        // ruleid: mois-1-01-sql-injection-jdbc
        conn.nativeSQL(sql);
    }

    // 타입을 알 수 없는 수신 객체: 메서드 이름으로 잡는다
    public void untypedReceiver(HttpServletRequest request) throws SQLException {
        String sql = "UPDATE users SET grade = 'A' WHERE name = '" + request.getParameter("name") + "'";
        // ruleid: mois-1-01-sql-injection-jdbc
        dataSource.getConnection().prepareStatement(sql);
        // ruleid: mois-1-01-sql-injection-jdbc
        dataSource.getConnection().prepareCall(sql);
        // ruleid: mois-1-01-sql-injection-jdbc
        dataSource.getConnection().createStatement().executeQuery(sql);
        // ruleid: mois-1-01-sql-injection-jdbc
        currentStatement().executeUpdate(sql);
        // ruleid: mois-1-01-sql-injection-jdbc
        currentStatement().executeLargeUpdate(sql);
        // ruleid: mois-1-01-sql-injection-jdbc
        currentStatement().addBatch(sql);
    }

    // 숫자로 변환하긴 했지만 변환한 값을 쓰지 않는다
    public void conversionResultIgnored(HttpServletRequest request) throws SQLException {
        String id = request.getParameter("id");
        Integer.parseInt(id);
        // ruleid: mois-1-01-sql-injection-jdbc
        stmt.executeQuery("SELECT * FROM users WHERE id = " + id);
        String seq = request.getParameter("seq");
        Long.parseLong(seq);
        // ruleid: mois-1-01-sql-injection-jdbc
        stmt.executeQuery("SELECT * FROM users WHERE seq = " + seq);
    }

    // 바인딩을 쓰면서도 질의문 일부(정렬 기준)는 이어 붙인다
    public void boundButConcatenated(HttpServletRequest request) throws SQLException {
        String name = request.getParameter("name");
        String order = request.getParameter("order");
        // ruleid: mois-1-01-sql-injection-jdbc
        java.sql.PreparedStatement ps = conn.prepareStatement("SELECT * FROM users WHERE name = ? ORDER BY " + order);
        ps.setString(1, name);
        ps.executeQuery();
    }

    // 숫자 변환의 "인자 안"에서 실행되는 질의문: 변환 결과가 숫자라는 것은 안쪽 질의문이 안전하다는 증명이 아니다
    public boolean sinkInsideConversion(HttpServletRequest request) throws SQLException {
        String table = request.getParameter("table");
        // ruleid: mois-1-01-sql-injection-jdbc
        int max = Integer.parseInt(conn.prepareStatement("SELECT MAX(id) FROM " + table).executeQuery().getString(1));
        // ruleid: mois-1-01-sql-injection-jdbc
        long count = Long.parseLong(stmt.executeQuery("SELECT COUNT(*) FROM " + table).getString(1));
        // ruleid: mois-1-01-sql-injection-jdbc
        return max > count || Integer.parseInt(stmt.executeQuery("SELECT MIN(id) FROM " + table).getString(1)) > 0;
    }

    // 변환 식의 인자 안에서 대입한 변수는 문자열 그대로다 (숫자인 것은 변환 "결과"뿐)
    public void assignedInsideConversion(HttpServletRequest request) throws SQLException {
        String id;
        int n = Integer.parseInt(id = request.getParameter("id"));
        // ruleid: mois-1-01-sql-injection-jdbc
        stmt.executeQuery("SELECT * FROM users WHERE id = " + id);
    }

    private Statement currentStatement() {
        return stmt;
    }
}
