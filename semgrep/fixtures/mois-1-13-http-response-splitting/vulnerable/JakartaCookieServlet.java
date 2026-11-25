package demo;

import jakarta.servlet.http.Cookie;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;

// 탐지돼야 하는 경우: jakarta.servlet (Spring Boot 3·Tomcat 10 이상)
public class JakartaCookieServlet {
    public void remember(HttpServletRequest request, HttpServletResponse response) {
        // ruleid: mois-1-13-http-response-splitting
        Cookie c = new Cookie("LASTLOGIN", request.getParameter("last_login"));
        // ruleid: mois-1-13-http-response-splitting
        c.setValue(request.getParameter("theme"));
        response.addCookie(c);
    }

    public void headers(HttpServletRequest request, HttpServletResponse response) {
        // ruleid: mois-1-13-http-response-splitting
        response.setHeader("Content-Disposition", "attachment;filename=" + request.getParameter("file"));
        // ruleid: mois-1-13-http-response-splitting
        response.addHeader("Content-Language", request.getParameter("lang"));
    }

    // 헤더 이름 자리
    public void headerName(HttpServletRequest request, HttpServletResponse response) {
        // ruleid: mois-1-13-http-response-splitting
        response.addHeader(request.getParameter("name"), "1");
    }
}
