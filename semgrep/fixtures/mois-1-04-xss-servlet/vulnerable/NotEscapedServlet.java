package demo;

import java.io.IOException;
import java.io.PrintWriter;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import org.springframework.web.util.HtmlUtils;

// 탐지돼야 하는 경우: 이스케이프가 있어 보이지만 출력되는 값에는 적용되지 않는 형태
public class NotEscapedServlet {
    // 이스케이프 결과를 쓰지 않음 (String 은 바뀌지 않는다)
    public void resultIgnored(HttpServletRequest request, HttpServletResponse response) throws IOException {
        String name = request.getParameter("name");
        HtmlUtils.htmlEscape(name);
        // ruleid: mois-1-04-xss-servlet
        response.getWriter().print(name);
    }

    // 다른 변수만 이스케이프
    public void otherVariable(HttpServletRequest request, HttpServletResponse response) throws IOException {
        String title = HtmlUtils.htmlEscape(request.getParameter("title"));
        String body = request.getParameter("body");
        PrintWriter out = response.getWriter();
        out.print("<h1>" + title + "</h1>");
        // ruleid: mois-1-04-xss-servlet
        out.print("<div>" + body + "</div>");
    }

    // 이스케이프한 값에 원래 입력을 다시 이어 붙임
    public void mixed(HttpServletRequest request, HttpServletResponse response) throws IOException {
        String name = request.getParameter("name");
        // ruleid: mois-1-04-xss-servlet
        response.getWriter().print(HtmlUtils.htmlEscape(name) + " (" + name + ")");
    }

    // 일부 문자열만 지우는 치환은 이스케이프가 아니다: <scr<script>ipt> 로 우회된다
    public void partialReplace(HttpServletRequest request, HttpServletResponse response) throws IOException {
        String name = request.getParameter("name").replace("<script>", "");
        // ruleid: mois-1-04-xss-servlet
        response.getWriter().print(name);
    }
}
