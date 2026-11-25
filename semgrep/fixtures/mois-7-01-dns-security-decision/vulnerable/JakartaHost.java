package demo;

import jakarta.servlet.http.HttpServlet;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;

// 탐지돼야 하는 경우: jakarta 네임스페이스의 getRemoteHost()
public class JakartaHost extends HttpServlet {
    @Override
    public void doGet(HttpServletRequest req, HttpServletResponse res) {
        // ruleid: mois-7-01-dns-security-decision
        res.setStatus(req.getRemoteHost().endsWith(".trustme.com") ? 200 : 403);
    }
}
