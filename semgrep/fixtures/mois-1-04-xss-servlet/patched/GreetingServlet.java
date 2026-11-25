package demo;

import java.io.IOException;
import java.io.PrintWriter;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import org.owasp.encoder.Encode;
import org.owasp.esapi.ESAPI;
import org.owasp.esapi.Encoder;
import org.springframework.web.util.HtmlUtils;

// 탐지되면 안 되는 경우: HTML 이스케이프 후 출력. 이스케이프 함수마다 한 줄씩
public class GreetingServlet {
    private final Encoder encoder = ESAPI.encoder();

    public void hello(HttpServletRequest request, HttpServletResponse response) throws IOException {
        String name = request.getParameter("name");
        // ok: mois-1-04-xss-servlet — Spring HtmlUtils
        response.getWriter().println("<p>Hello " + HtmlUtils.htmlEscape(name) + "</p>");
    }

    public void echo(HttpServletRequest request, HttpServletResponse response) throws IOException {
        PrintWriter out = response.getWriter();
        // ok: mois-1-04-xss-servlet — OWASP Java Encoder
        out.print(Encode.forHtml(request.getParameter("q")));
    }

    public void springHtmlUtils(HttpServletRequest request, HttpServletResponse response) throws IOException {
        String q = request.getParameter("q");
        PrintWriter out = response.getWriter();
        // ok: mois-1-04-xss-servlet
        out.write(HtmlUtils.htmlEscapeDecimal(q));
        // ok: mois-1-04-xss-servlet
        out.append(HtmlUtils.htmlEscapeHex(q));
        // ok: mois-1-04-xss-servlet — 앞에서 append 한 값이 이스케이프됐으므로 writer 는 오염되지 않는다
        out.println("</body></html>");
    }

    public void owaspEncoder(HttpServletRequest request, HttpServletResponse response) throws IOException {
        String q = request.getParameter("q");
        try (PrintWriter out = response.getWriter()) {
            // ok: mois-1-04-xss-servlet
            out.printf("<p>%s 검색 결과</p>", Encode.forHtmlContent(q));
        }
    }

    public void esapi(HttpServletRequest request, HttpServletResponse response) throws IOException {
        String q = request.getParameter("q");
        PrintWriter out;
        out = response.getWriter();
        // ok: mois-1-04-xss-servlet
        out.print(ESAPI.encoder().encodeForHTML(q));
        // ok: mois-1-04-xss-servlet
        out.format("<input value=\"%s\">", ESAPI.encoder().encodeForHTMLAttribute(q));
        // ok: mois-1-04-xss-servlet — Encoder 를 필드로 둔 경우
        out.print(encoder.encodeForHTML(q));
        // ok: mois-1-04-xss-servlet
        out.format("<input value=\"%s\">", encoder.encodeForHTMLAttribute(q));
    }

    public void commons(HttpServletRequest request, HttpServletResponse response) throws IOException {
        String q = request.getParameter("q");
        PrintWriter out = response.getWriter();
        // ok: mois-1-04-xss-servlet — commons-text
        out.print(org.apache.commons.text.StringEscapeUtils.escapeHtml4(q));
        // ok: mois-1-04-xss-servlet
        out.print(org.apache.commons.text.StringEscapeUtils.escapeHtml3(q));
        // ok: mois-1-04-xss-servlet — commons-lang3
        out.print(org.apache.commons.lang3.StringEscapeUtils.escapeHtml4(q));
        // ok: mois-1-04-xss-servlet
        out.print(org.apache.commons.lang3.StringEscapeUtils.escapeHtml3(q));
        // ok: mois-1-04-xss-servlet — commons-lang 2 (전자정부 구버전)
        out.print(org.apache.commons.lang.StringEscapeUtils.escapeHtml(q));
    }

    public void constant(HttpServletRequest request, HttpServletResponse response) throws IOException {
        String theme = "dark".equals(request.getParameter("theme")) ? "dark" : "light";
        // ok: mois-1-04-xss-servlet — 입력은 선택에만 쓰고 출력은 상수
        response.getWriter().print("<body class=\"" + theme + "\">");
    }
}
