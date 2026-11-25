package demo;

import jakarta.servlet.http.HttpServletRequest;
import java.sql.Connection;
import java.sql.SQLException;
import java.sql.Statement;

// 탐지돼야 하는 경우 (jakarta 네임스페이스)
public class OrderDao {
    private Connection conn;

    public int cancel(HttpServletRequest request) throws SQLException {
        String orderId = request.getParameter("orderId");
        Statement stmt = conn.createStatement();
        // ruleid: mois-1-01-sql-injection-jdbc
        return stmt.executeUpdate("UPDATE orders SET status = 'CANCEL' WHERE id = " + orderId);
    }
}
