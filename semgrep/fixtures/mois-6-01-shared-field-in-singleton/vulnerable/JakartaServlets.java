package demo;

import jakarta.servlet.GenericServlet;
import jakarta.servlet.ServletRequest;
import jakarta.servlet.ServletResponse;
import jakarta.servlet.http.HttpServlet;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;

// 탐지돼야 하는 경우: jakarta 네임스페이스의 서블릿
public class JakartaServlets extends HttpServlet {
    private String name;

    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response) {
        // ruleid: mois-6-01-shared-field-in-singleton
        name = request.getParameter("name");
    }
}

class JakartaLegacyServlet extends GenericServlet {
    private String lastUser;

    @Override
    public void service(ServletRequest req, ServletResponse res) {
        // ruleid: mois-6-01-shared-field-in-singleton
        lastUser = req.getParameter("user");
    }
}
