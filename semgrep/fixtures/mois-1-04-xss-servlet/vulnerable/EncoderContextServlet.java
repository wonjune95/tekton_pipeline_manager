package demo;

import java.io.IOException;
import java.io.PrintWriter;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import org.apache.commons.text.StringEscapeUtils;
import org.owasp.encoder.Encode;
import org.springframework.web.util.HtmlUtils;

import egovframework.com.cmm.EgovWebUtil;

// 탐지돼야 하는 경우: HTML 인코더를 거쳤지만 그 인코더가 막지 못하는 위치에 출력 (v0.6.1 감사 4번)
// HTML 인코더가 증명하는 것은 "본문"과 "인코더가 바꾸는 따옴표로 감싼 일반 속성 값"뿐이다
public class EncoderContextServlet {
    // <script> 안: 엔티티는 풀리지 않지만 alert(1) 에는 바꿀 문자가 없다
    public void scriptBlock(HttpServletRequest request, HttpServletResponse response) throws IOException {
        String q = request.getParameter("q");
        PrintWriter out = response.getWriter();
        // ruleid: mois-1-04-xss-servlet
        out.println("<script>var id = " + HtmlUtils.htmlEscape(q) + ";</script>");
    }

    // 이벤트 속성: 브라우저가 &#39; 를 ' 로 푼 뒤 스크립트로 실행한다
    public void eventHandler(HttpServletRequest request, HttpServletResponse response) throws IOException {
        String q = request.getParameter("q");
        PrintWriter out = response.getWriter();
        // ruleid: mois-1-04-xss-servlet
        out.println("<img src=\"/logo.png\" onerror=\"report('" + HtmlUtils.htmlEscape(q) + "')\">");
    }

    // srcdoc 속성: 엔티티를 푼 결과가 다시 HTML 로 해석된다
    public void srcdoc(HttpServletRequest request, HttpServletResponse response) throws IOException {
        String q = request.getParameter("q");
        PrintWriter out = response.getWriter();
        // ruleid: mois-1-04-xss-servlet
        out.println("<iframe srcdoc='" + HtmlUtils.htmlEscape(q) + "'></iframe>");
    }

    // javascript: URL 안의 문자열: 이벤트 속성과 같다
    public void javascriptUrl(HttpServletRequest request, HttpServletResponse response) throws IOException {
        String q = request.getParameter("q");
        PrintWriter out = response.getWriter();
        // ruleid: mois-1-04-xss-servlet
        out.println("<a href=\"javascript:go('" + HtmlUtils.htmlEscape(q) + "')\">이동</a>");
    }

    // href 값 전체가 입력: javascript:alert(1) 은 이스케이프할 문자가 없다
    public void hrefStart(HttpServletRequest request, HttpServletResponse response) throws IOException {
        String q = request.getParameter("q");
        PrintWriter out = response.getWriter();
        // ruleid: mois-1-04-xss-servlet
        out.println("<a href=\"" + HtmlUtils.htmlEscape(q) + "\">이동</a>");
    }

    // src 값 전체가 입력 (작은따옴표)
    public void srcStart(HttpServletRequest request, HttpServletResponse response) throws IOException {
        String q = request.getParameter("q");
        PrintWriter out = response.getWriter();
        // ruleid: mois-1-04-xss-servlet
        out.println("<iframe src='" + HtmlUtils.htmlEscape(q) + "'></iframe>");
    }

    // form action 값 전체가 입력
    public void actionStart(HttpServletRequest request, HttpServletResponse response) throws IOException {
        String q = request.getParameter("q");
        PrintWriter out = response.getWriter();
        // ruleid: mois-1-04-xss-servlet
        out.println("<form method=\"post\" action=\"" + HtmlUtils.htmlEscape(q) + "\">");
    }

    // object data 값 전체가 입력
    public void objectData(HttpServletRequest request, HttpServletResponse response) throws IOException {
        String q = request.getParameter("q");
        PrintWriter out = response.getWriter();
        // ruleid: mois-1-04-xss-servlet
        out.println("<object data=\"" + HtmlUtils.htmlEscape(q) + "\"></object>");
    }

    // 따옴표 없는 속성 값: "x onfocus=alert(1) autofocus" 로 속성이 추가된다
    public void unquoted(HttpServletRequest request, HttpServletResponse response) throws IOException {
        String q = request.getParameter("q");
        PrintWriter out = response.getWriter();
        // ruleid: mois-1-04-xss-servlet
        out.println("<input value=" + HtmlUtils.htmlEscape(q) + ">");
    }

    // 따옴표 없는 속성 값 (앞 속성은 큰따옴표로 닫힘)
    public void unquotedAfterDq(HttpServletRequest request, HttpServletResponse response) throws IOException {
        String q = request.getParameter("q");
        PrintWriter out = response.getWriter();
        // ruleid: mois-1-04-xss-servlet
        out.println("<input type=\"text\" value=" + HtmlUtils.htmlEscape(q) + ">");
    }

    // 따옴표 없는 속성 값 (앞 속성은 작은따옴표로 닫힘)
    public void unquotedAfterSq(HttpServletRequest request, HttpServletResponse response) throws IOException {
        String q = request.getParameter("q");
        PrintWriter out = response.getWriter();
        // ruleid: mois-1-04-xss-servlet
        out.println("<input type='text' value=" + HtmlUtils.htmlEscape(q) + ">");
    }

    // 태그 안의 속성 이름 자리: onmouseover=alert(1) 에는 바꿀 문자가 없다
    public void inTag(HttpServletRequest request, HttpServletResponse response) throws IOException {
        String q = request.getParameter("q");
        PrintWriter out = response.getWriter();
        // ruleid: mois-1-04-xss-servlet
        out.println("<div class=\"box\" " + HtmlUtils.htmlEscape(q) + ">");
    }

    // 형식 문자열의 자리표시(%s)가 이벤트 속성 안
    public void formatEvent(HttpServletRequest request, HttpServletResponse response) throws IOException {
        String q = request.getParameter("q");
        PrintWriter out = response.getWriter();
        // ruleid: mois-1-04-xss-servlet
        out.println(String.format("<button onclick=\"select('%s')\">선택</button>", HtmlUtils.htmlEscape(q)));
    }

    // 형식 문자열의 자리표시가 href 값의 시작
    public void formatHref(HttpServletRequest request, HttpServletResponse response) throws IOException {
        String q = request.getParameter("q");
        PrintWriter out = response.getWriter();
        // ruleid: mois-1-04-xss-servlet
        out.println(String.format("<a href=\"%s\">이동</a>", HtmlUtils.htmlEscape(q)));
    }

    // 메서드로 이어 붙임 (앞 글자가 수신 객체)
    public void concatMethod(HttpServletRequest request, HttpServletResponse response) throws IOException {
        String q = request.getParameter("q");
        PrintWriter out = response.getWriter();
        // ruleid: mois-1-04-xss-servlet
        out.println("<a href=\"".concat(HtmlUtils.htmlEscape(q)));
    }

    // 인코더가 삼항식 안에 있어도 위치는 같다
    public void ternary(HttpServletRequest request, HttpServletResponse response) throws IOException {
        String q = request.getParameter("q");
        PrintWriter out = response.getWriter();
        // ruleid: mois-1-04-xss-servlet
        out.println("<a href=\"" + (q.isEmpty() ? "#" : HtmlUtils.htmlEscape(q)) + "\">이동</a>");
    }

    // commons escapeHtml4 는 ' 를 바꾸지 않는다: x' onfocus='alert(1) 로 속성이 추가된다
    public void singleQuoteCommons(HttpServletRequest request, HttpServletResponse response) throws IOException {
        String q = request.getParameter("q");
        PrintWriter out = response.getWriter();
        // ruleid: mois-1-04-xss-servlet
        out.println("<input value='" + StringEscapeUtils.escapeHtml4(q) + "'>");
    }

    // commons escapeHtml4 + 작은따옴표 속성 (형식 문자열)
    public void singleQuoteCommonsFormat(HttpServletRequest request, HttpServletResponse response) throws IOException {
        String q = request.getParameter("q");
        PrintWriter out = response.getWriter();
        // ruleid: mois-1-04-xss-servlet
        out.println(String.format("<input value='%s'>", StringEscapeUtils.escapeHtml4(q)));
    }

    // EgovWebUtil.clearXSS 는 & < > 만 바꾼다: 큰따옴표 속성에서 " 로 빠져나온다
    public void egovClearXssAttr(HttpServletRequest request, HttpServletResponse response) throws IOException {
        String q = request.getParameter("q");
        PrintWriter out = response.getWriter();
        // ruleid: mois-1-04-xss-servlet
        out.println("<input type=\"text\" value=\"" + EgovWebUtil.clearXSS(q) + "\">");
    }

    // EgovWebUtil.clearXSS + 작은따옴표 속성
    public void egovClearXssSingle(HttpServletRequest request, HttpServletResponse response) throws IOException {
        String q = request.getParameter("q");
        PrintWriter out = response.getWriter();
        // ruleid: mois-1-04-xss-servlet
        out.println("<input value='" + EgovWebUtil.clearXSS(q) + "'>");
    }

    // Encode.forHtmlContent 는 본문 전용이다 (따옴표를 바꾸지 않음)
    public void contentEncoderAttr(HttpServletRequest request, HttpServletResponse response) throws IOException {
        String q = request.getParameter("q");
        PrintWriter out = response.getWriter();
        // ruleid: mois-1-04-xss-servlet
        out.println("<input value=\"" + Encode.forHtmlContent(q) + "\">");
    }

    // Encode.forHtmlContent + 큰따옴표 속성 (형식 문자열)
    public void contentEncoderFormat(HttpServletRequest request, HttpServletResponse response) throws IOException {
        String q = request.getParameter("q");
        PrintWriter out = response.getWriter();
        // ruleid: mois-1-04-xss-servlet
        out.println(String.format("<input value=\"%s\">", Encode.forHtmlContent(q)));
    }

    // 인코딩한 값을 변수에 담았다가 <script> 안에 씀
    public void viaVariable(HttpServletRequest request, HttpServletResponse response) throws IOException {
        String q = request.getParameter("q");
        PrintWriter out = response.getWriter();
        String safe = HtmlUtils.htmlEscape(q);
        // ruleid: mois-1-04-xss-servlet
        out.println("<script>var keyword = '" + safe + "';</script>");
    }

    // 변수가 삼항식 안에 있어도 위치는 같다
    public void viaVariableTernary(HttpServletRequest request, HttpServletResponse response) throws IOException {
        String q = request.getParameter("q");
        PrintWriter out = response.getWriter();
        String safe = HtmlUtils.htmlEscape(q);
        // ruleid: mois-1-04-xss-servlet
        out.println("<a href=\"" + (safe.isEmpty() ? "#" : safe) + "\">이동</a>");
    }

    // 변수에 담았다가 href 값으로 이어 붙임 (변수에 메서드를 한 번 더 부름)
    public void viaVariableConcatMethod(HttpServletRequest request, HttpServletResponse response) throws IOException {
        String q = request.getParameter("q");
        PrintWriter out = response.getWriter();
        String safe = HtmlUtils.htmlEscape(q);
        // ruleid: mois-1-04-xss-servlet
        out.println("<a href=\"".concat(safe.trim()));
    }

    // 변수에 담았다가 형식 문자열의 src 자리에 씀
    public void viaVariableFormat(HttpServletRequest request, HttpServletResponse response) throws IOException {
        String q = request.getParameter("q");
        PrintWriter out = response.getWriter();
        String safe = HtmlUtils.htmlEscape(q);
        // ruleid: mois-1-04-xss-servlet
        out.println(String.format("<img src=\"%s\">", safe.trim()));
    }

    // 바로 앞 문장에서 href=" 까지 출력하고 이어서 값을 출력
    public void splitOutput(HttpServletRequest request, HttpServletResponse response) throws IOException {
        String q = request.getParameter("q");
        PrintWriter out = response.getWriter();
        out.print("<a href=\"");
        // ruleid: mois-1-04-xss-servlet
        out.print(HtmlUtils.htmlEscape(q));
        out.println("\">이동</a>");
    }

    // 변수에 담았다가 바로 앞 문장의 href=' 뒤에 출력
    public void splitOutputViaVariable(HttpServletRequest request, HttpServletResponse response) throws IOException {
        String q = request.getParameter("q");
        PrintWriter out = response.getWriter();
        String safe = HtmlUtils.htmlEscape(q);
        out.print("<a href='");
        // ruleid: mois-1-04-xss-servlet
        out.print(safe);
        out.println("'>이동</a>");
    }
}
