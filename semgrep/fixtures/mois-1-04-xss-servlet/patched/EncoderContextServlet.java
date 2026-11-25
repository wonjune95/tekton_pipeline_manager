package demo;

import java.io.IOException;
import java.io.PrintWriter;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import org.apache.commons.text.StringEscapeUtils;
import org.owasp.encoder.Encode;
import org.springframework.web.util.HtmlUtils;

import egovframework.com.cmm.EgovWebUtil;

// 탐지되면 안 되는 경우: HTML 인코더가 실제로 막는 위치(본문, 따옴표로 감싼 일반 속성 값)에 출력
public class EncoderContextServlet {
    // 태그 사이의 본문
    public void body(HttpServletRequest request, HttpServletResponse response) throws IOException {
        String q = request.getParameter("q");
        PrintWriter out = response.getWriter();
        // ok: mois-1-04-xss-servlet
        out.println("<p>" + HtmlUtils.htmlEscape(q) + "</p>");
    }

    // 본문: commons escapeHtml4
    public void bodyCommons(HttpServletRequest request, HttpServletResponse response) throws IOException {
        String q = request.getParameter("q");
        PrintWriter out = response.getWriter();
        // ok: mois-1-04-xss-servlet
        out.println("<td>" + StringEscapeUtils.escapeHtml4(q) + "</td>");
    }

    // 본문: EgovWebUtil.clearXSS (& < > 만 바꾸지만 본문에서는 충분하다)
    public void bodyEgovClearXss(HttpServletRequest request, HttpServletResponse response) throws IOException {
        String q = request.getParameter("q");
        PrintWriter out = response.getWriter();
        // ok: mois-1-04-xss-servlet
        out.println("<td>" + EgovWebUtil.clearXSS(q) + "</td>");
    }

    // 본문: Encode.forHtmlContent
    public void bodyContentEncoder(HttpServletRequest request, HttpServletResponse response) throws IOException {
        String q = request.getParameter("q");
        PrintWriter out = response.getWriter();
        // ok: mois-1-04-xss-servlet
        out.println(String.format("<p>%s</p>", Encode.forHtmlContent(q)));
    }

    // 큰따옴표 속성 값 + 따옴표를 바꾸는 인코더
    public void attrDouble(HttpServletRequest request, HttpServletResponse response) throws IOException {
        String q = request.getParameter("q");
        PrintWriter out = response.getWriter();
        // ok: mois-1-04-xss-servlet
        out.println("<input type=\"text\" value=\"" + HtmlUtils.htmlEscape(q) + "\">");
    }

    // 작은따옴표 속성 값 + 따옴표를 바꾸는 인코더
    public void attrSingle(HttpServletRequest request, HttpServletResponse response) throws IOException {
        String q = request.getParameter("q");
        PrintWriter out = response.getWriter();
        // ok: mois-1-04-xss-servlet
        out.println("<input value='" + HtmlUtils.htmlEscape(q) + "'>");
    }

    // 큰따옴표 속성 값 + commons escapeHtml4 (" 는 바꾼다)
    public void attrDoubleCommons(HttpServletRequest request, HttpServletResponse response) throws IOException {
        String q = request.getParameter("q");
        PrintWriter out = response.getWriter();
        // ok: mois-1-04-xss-servlet
        out.println("<input value=\"" + StringEscapeUtils.escapeHtml4(q) + "\">");
    }

    // 형식 문자열의 일반 속성 자리
    public void attrFormat(HttpServletRequest request, HttpServletResponse response) throws IOException {
        String q = request.getParameter("q");
        PrintWriter out = response.getWriter();
        // ok: mois-1-04-xss-servlet
        out.println(String.format("<input name=\"q\" value=\"%s\">", HtmlUtils.htmlEscape(q)));
    }

    // URL 속성이지만 앞부분(경로)이 고정이라 스킴을 바꿀 수 없다
    public void urlFixedPrefix(HttpServletRequest request, HttpServletResponse response) throws IOException {
        String q = request.getParameter("q");
        PrintWriter out = response.getWriter();
        // ok: mois-1-04-xss-servlet
        out.println("<a href=\"/board/view?id=" + HtmlUtils.htmlEscape(q) + "\">보기</a>");
    }

    // href·onclick 이 있지만 닫힌 뒤의 본문
    public void afterClosedAttrs(HttpServletRequest request, HttpServletResponse response) throws IOException {
        String q = request.getParameter("q");
        PrintWriter out = response.getWriter();
        // ok: mois-1-04-xss-servlet
        out.println("<a href=\"/home\" onclick=\"track()\">" + HtmlUtils.htmlEscape(q) + "</a>");
    }

    // <script> 가 닫힌 뒤의 본문
    public void afterClosedScript(HttpServletRequest request, HttpServletResponse response) throws IOException {
        String q = request.getParameter("q");
        PrintWriter out = response.getWriter();
        // ok: mois-1-04-xss-servlet
        out.println("<script src=\"/js/app.js\"></script><h1>" + HtmlUtils.htmlEscape(q) + "</h1>");
    }

    // content= 는 이벤트 속성(on…=)이 아니다
    public void contentAttr(HttpServletRequest request, HttpServletResponse response) throws IOException {
        String q = request.getParameter("q");
        PrintWriter out = response.getWriter();
        // ok: mois-1-04-xss-servlet
        out.println("<meta name=\"description\" content=\"" + HtmlUtils.htmlEscape(q) + "\">");
    }

    // 100% 의 % 는 형식 문자열의 자리표시가 아니다 (속성은 닫혀 있고 값은 본문)
    public void percentWidth(HttpServletRequest request, HttpServletResponse response) throws IOException {
        String q = request.getParameter("q");
        PrintWriter out = response.getWriter();
        // ok: mois-1-04-xss-servlet
        out.println("<td width=\"100%\">" + EgovWebUtil.clearXSS(q) + "</td>");
    }

    // data-id= 는 URL 속성(data=)이 아니다
    public void dataAttr(HttpServletRequest request, HttpServletResponse response) throws IOException {
        String q = request.getParameter("q");
        PrintWriter out = response.getWriter();
        // ok: mois-1-04-xss-servlet
        out.println("<li data-id=\"" + HtmlUtils.htmlEscape(q) + "\"></li>");
    }

    // 변수에 담았다가 본문에 씀
    public void viaVariable(HttpServletRequest request, HttpServletResponse response) throws IOException {
        String q = request.getParameter("q");
        PrintWriter out = response.getWriter();
        String safe = HtmlUtils.htmlEscape(q);
        // ok: mois-1-04-xss-servlet
        out.println("<td>" + safe + "</td>");
    }

    // 변수에 담았다가 일반 속성 값에 씀
    public void viaVariableAttr(HttpServletRequest request, HttpServletResponse response) throws IOException {
        String q = request.getParameter("q");
        PrintWriter out = response.getWriter();
        String safe = HtmlUtils.htmlEscape(q);
        // ok: mois-1-04-xss-servlet
        out.println(String.format("<input value=\"%s\">", safe));
    }

    // 바로 앞 문장에서 본문 태그를 출력
    public void splitOutput(HttpServletRequest request, HttpServletResponse response) throws IOException {
        String q = request.getParameter("q");
        PrintWriter out = response.getWriter();
        out.print("<td>");
        // ok: mois-1-04-xss-servlet
        out.print(HtmlUtils.htmlEscape(q));
        out.println("</td>");
    }

    // 앞 문장이 href 값을 열었지만 다음 문장이 값을 닫은 뒤(본문)에 인코딩한 값을 쓴다
    public void splitOutputAfterUrl(HttpServletRequest request, HttpServletResponse response) throws IOException {
        String q = request.getParameter("q");
        PrintWriter out = response.getWriter();
        out.print("<a href=\"" + request.getContextPath());
        // ok: mois-1-04-xss-servlet
        out.println("/board/list\">" + HtmlUtils.htmlEscape(q) + "</a>");
    }
}
