package demo;

import java.io.IOException;
import java.io.PrintWriter;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

// 탐지돼야 하는 경우: 외부 입력을 이스케이프 없이 응답 HTML 에 출력. 출력 메서드마다 한 줄씩
public class GreetingServlet {
    public void hello(HttpServletRequest request, HttpServletResponse response) throws IOException {
        String name = request.getParameter("name");
        // ruleid: mois-1-04-xss-servlet
        response.getWriter().println("<p>Hello " + name + "</p>");
    }

    public void echo(HttpServletRequest request, HttpServletResponse response) throws IOException {
        PrintWriter out = response.getWriter();
        // ruleid: mois-1-04-xss-servlet
        out.print(request.getParameter("q"));
    }

    public void writerMethods(HttpServletRequest request, HttpServletResponse response) throws IOException {
        String q = request.getParameter("q");
        PrintWriter out = response.getWriter();
        out.println("<html><body>");
        // ruleid: mois-1-04-xss-servlet
        out.println("<h1>" + q + "</h1>");
        // ruleid: mois-1-04-xss-servlet
        out.write(q);
        // ruleid: mois-1-04-xss-servlet
        out.printf("<p>%s 검색 결과</p>", q);
        // ruleid: mois-1-04-xss-servlet
        out.format("<input value=\"%s\">", q);
        // ruleid: mois-1-04-xss-servlet
        out.append(q);
        out.println("</body></html>");
    }

    // writer 를 나중에 대입하는 형태
    public void assigned(HttpServletRequest request, HttpServletResponse response) throws IOException {
        PrintWriter out;
        out = response.getWriter();
        // ruleid: mois-1-04-xss-servlet
        out.print(request.getParameter("q"));
    }

    // try-with-resources 로 연 writer
    public void resource(HttpServletRequest request, HttpServletResponse response) throws IOException {
        try (PrintWriter out = response.getWriter()) {
            // ruleid: mois-1-04-xss-servlet
            out.print(request.getHeader("User-Agent"));
        }
    }
}
