package demo;

import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import java.io.IOException;

// 탐지돼야 하는 경우: jakarta.servlet (Spring Boot 3·Tomcat 10 이상)
public class JakartaGreetingServlet {
    public void hello(HttpServletRequest request, HttpServletResponse response) throws IOException {
        // ruleid: mois-1-04-xss-servlet
        response.getWriter().print("<p>Hello " + request.getParameter("name") + "</p>");
    }
}
