package demo;

import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import java.io.IOException;

// 탐지돼야 하는 경우: jakarta.servlet (Spring Boot 3·Tomcat 10 이상)
public class JakartaRedirectServlet {
    public void move(HttpServletRequest request, HttpServletResponse response) throws IOException {
        // ruleid: mois-1-07-open-redirect
        response.sendRedirect(request.getParameter("redirect"));
    }

    public void location(HttpServletRequest request, HttpServletResponse response) {
        response.setStatus(HttpServletResponse.SC_FOUND);
        // ruleid: mois-1-07-open-redirect
        response.setHeader("Location", request.getParameter("next"));
    }
}
