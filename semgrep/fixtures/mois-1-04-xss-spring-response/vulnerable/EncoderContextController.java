package demo;

import org.apache.commons.text.StringEscapeUtils;
import org.owasp.encoder.Encode;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.util.HtmlUtils;

import egovframework.com.cmm.EgovWebUtil;

// 탐지돼야 하는 경우: HTML 인코더를 거쳤지만 그 인코더가 막지 못하는 위치에 넣어 응답 (v0.6.1 감사 4번)
// HTML 인코더가 증명하는 것은 "본문"과 "인코더가 바꾸는 따옴표로 감싼 일반 속성 값"뿐이다
@RestController
public class EncoderContextController {
    private final String contextPath = "/app";

    // <script> 안: 엔티티는 풀리지 않지만 alert(1) 에는 바꿀 문자가 없다
    @GetMapping("/ctx/1")
    public String scriptBlock(@RequestParam String q) {
        // ruleid: mois-1-04-xss-spring-response
        return "<script>var id = " + HtmlUtils.htmlEscape(q) + ";</script>";
    }

    // 이벤트 속성: 브라우저가 &#39; 를 ' 로 푼 뒤 스크립트로 실행한다
    @GetMapping("/ctx/2")
    public String eventHandler(@RequestParam String q) {
        // ruleid: mois-1-04-xss-spring-response
        return "<img src=\"/logo.png\" onerror=\"report('" + HtmlUtils.htmlEscape(q) + "')\">";
    }

    // srcdoc 속성: 엔티티를 푼 결과가 다시 HTML 로 해석된다
    @GetMapping("/ctx/3")
    public String srcdoc(@RequestParam String q) {
        // ruleid: mois-1-04-xss-spring-response
        return "<iframe srcdoc='" + HtmlUtils.htmlEscape(q) + "'></iframe>";
    }

    // javascript: URL 안의 문자열: 이벤트 속성과 같다
    @GetMapping("/ctx/4")
    public String javascriptUrl(@RequestParam String q) {
        // ruleid: mois-1-04-xss-spring-response
        return "<a href=\"javascript:go('" + HtmlUtils.htmlEscape(q) + "')\">이동</a>";
    }

    // href 값 전체가 입력: javascript:alert(1) 은 이스케이프할 문자가 없다
    @GetMapping("/ctx/5")
    public String hrefStart(@RequestParam String q) {
        // ruleid: mois-1-04-xss-spring-response
        return "<a href=\"" + HtmlUtils.htmlEscape(q) + "\">이동</a>";
    }

    // src 값 전체가 입력 (작은따옴표)
    @GetMapping("/ctx/6")
    public String srcStart(@RequestParam String q) {
        // ruleid: mois-1-04-xss-spring-response
        return "<iframe src='" + HtmlUtils.htmlEscape(q) + "'></iframe>";
    }

    // form action 값 전체가 입력
    @GetMapping("/ctx/7")
    public String actionStart(@RequestParam String q) {
        // ruleid: mois-1-04-xss-spring-response
        return "<form method=\"post\" action=\"" + HtmlUtils.htmlEscape(q) + "\">";
    }

    // object data 값 전체가 입력
    @GetMapping("/ctx/8")
    public String objectData(@RequestParam String q) {
        // ruleid: mois-1-04-xss-spring-response
        return "<object data=\"" + HtmlUtils.htmlEscape(q) + "\"></object>";
    }

    // 따옴표 없는 속성 값: "x onfocus=alert(1) autofocus" 로 속성이 추가된다
    @GetMapping("/ctx/9")
    public String unquoted(@RequestParam String q) {
        // ruleid: mois-1-04-xss-spring-response
        return "<input value=" + HtmlUtils.htmlEscape(q) + ">";
    }

    // 따옴표 없는 속성 값 (앞 속성은 큰따옴표로 닫힘)
    @GetMapping("/ctx/10")
    public String unquotedAfterDq(@RequestParam String q) {
        // ruleid: mois-1-04-xss-spring-response
        return "<input type=\"text\" value=" + HtmlUtils.htmlEscape(q) + ">";
    }

    // 따옴표 없는 속성 값 (앞 속성은 작은따옴표로 닫힘)
    @GetMapping("/ctx/11")
    public String unquotedAfterSq(@RequestParam String q) {
        // ruleid: mois-1-04-xss-spring-response
        return "<input type='text' value=" + HtmlUtils.htmlEscape(q) + ">";
    }

    // 태그 안의 속성 이름 자리: onmouseover=alert(1) 에는 바꿀 문자가 없다
    @GetMapping("/ctx/12")
    public String inTag(@RequestParam String q) {
        // ruleid: mois-1-04-xss-spring-response
        return "<div class=\"box\" " + HtmlUtils.htmlEscape(q) + ">";
    }

    // 형식 문자열의 자리표시(%s)가 이벤트 속성 안
    @GetMapping("/ctx/13")
    public String formatEvent(@RequestParam String q) {
        // ruleid: mois-1-04-xss-spring-response
        return String.format("<button onclick=\"select('%s')\">선택</button>", HtmlUtils.htmlEscape(q));
    }

    // 형식 문자열의 자리표시가 href 값의 시작
    @GetMapping("/ctx/14")
    public String formatHref(@RequestParam String q) {
        // ruleid: mois-1-04-xss-spring-response
        return String.format("<a href=\"%s\">이동</a>", HtmlUtils.htmlEscape(q));
    }

    // 메서드로 이어 붙임 (앞 글자가 수신 객체)
    @GetMapping("/ctx/15")
    public String concatMethod(@RequestParam String q) {
        // ruleid: mois-1-04-xss-spring-response
        return "<a href=\"".concat(HtmlUtils.htmlEscape(q));
    }

    // 인코더가 삼항식 안에 있어도 위치는 같다
    @GetMapping("/ctx/16")
    public String ternary(@RequestParam String q) {
        // ruleid: mois-1-04-xss-spring-response
        return "<a href=\"" + (q.isEmpty() ? "#" : HtmlUtils.htmlEscape(q)) + "\">이동</a>";
    }

    // commons escapeHtml4 는 ' 를 바꾸지 않는다: x' onfocus='alert(1) 로 속성이 추가된다
    @GetMapping("/ctx/17")
    public String singleQuoteCommons(@RequestParam String q) {
        // ruleid: mois-1-04-xss-spring-response
        return "<input value='" + StringEscapeUtils.escapeHtml4(q) + "'>";
    }

    // commons escapeHtml4 + 작은따옴표 속성 (형식 문자열)
    @GetMapping("/ctx/18")
    public String singleQuoteCommonsFormat(@RequestParam String q) {
        // ruleid: mois-1-04-xss-spring-response
        return String.format("<input value='%s'>", StringEscapeUtils.escapeHtml4(q));
    }

    // EgovWebUtil.clearXSS 는 & < > 만 바꾼다: 큰따옴표 속성에서 " 로 빠져나온다
    @GetMapping("/ctx/19")
    public String egovClearXssAttr(@RequestParam String q) {
        // ruleid: mois-1-04-xss-spring-response
        return "<input type=\"text\" value=\"" + EgovWebUtil.clearXSS(q) + "\">";
    }

    // EgovWebUtil.clearXSS + 작은따옴표 속성
    @GetMapping("/ctx/20")
    public String egovClearXssSingle(@RequestParam String q) {
        // ruleid: mois-1-04-xss-spring-response
        return "<input value='" + EgovWebUtil.clearXSS(q) + "'>";
    }

    // Encode.forHtmlContent 는 본문 전용이다 (따옴표를 바꾸지 않음)
    @GetMapping("/ctx/21")
    public String contentEncoderAttr(@RequestParam String q) {
        // ruleid: mois-1-04-xss-spring-response
        return "<input value=\"" + Encode.forHtmlContent(q) + "\">";
    }

    // Encode.forHtmlContent + 큰따옴표 속성 (형식 문자열)
    @GetMapping("/ctx/22")
    public String contentEncoderFormat(@RequestParam String q) {
        // ruleid: mois-1-04-xss-spring-response
        return String.format("<input value=\"%s\">", Encode.forHtmlContent(q));
    }

    // 인코딩한 값을 변수에 담았다가 <script> 안에 씀
    @GetMapping("/ctx/23")
    public String viaVariable(@RequestParam String q) {
        String safe = HtmlUtils.htmlEscape(q);
        // ruleid: mois-1-04-xss-spring-response
        return "<script>var keyword = '" + safe + "';</script>";
    }

    // 변수가 삼항식 안에 있어도 위치는 같다
    @GetMapping("/ctx/24")
    public String viaVariableTernary(@RequestParam String q) {
        String safe = HtmlUtils.htmlEscape(q);
        // ruleid: mois-1-04-xss-spring-response
        return "<a href=\"" + (safe.isEmpty() ? "#" : safe) + "\">이동</a>";
    }

    // 변수에 담았다가 href 값으로 이어 붙임 (변수에 메서드를 한 번 더 부름)
    @GetMapping("/ctx/25")
    public String viaVariableConcatMethod(@RequestParam String q) {
        String safe = HtmlUtils.htmlEscape(q);
        // ruleid: mois-1-04-xss-spring-response
        return "<a href=\"".concat(safe.trim());
    }

    // 변수에 담았다가 형식 문자열의 src 자리에 씀
    @GetMapping("/ctx/26")
    public String viaVariableFormat(@RequestParam String q) {
        String safe = HtmlUtils.htmlEscape(q);
        // ruleid: mois-1-04-xss-spring-response
        return String.format("<img src=\"%s\">", safe.trim());
    }

    // 바로 앞 문장에서 href=" 까지 붙이고 이어서 값을 붙임
    @GetMapping("/ctx/27")
    public String splitOutput(@RequestParam String q) {
        StringBuilder html = new StringBuilder();
        html.append("<a href=\"");
        html.append(HtmlUtils.htmlEscape(q));
        html.append("\">이동</a>");
        // ruleid: mois-1-04-xss-spring-response
        return html.toString();
    }

    // 변수에 담았다가 바로 앞 문장의 href=' 뒤에 붙임
    @GetMapping("/ctx/28")
    public String splitOutputViaVariable(@RequestParam String q) {
        String safe = HtmlUtils.htmlEscape(q);
        StringBuilder html = new StringBuilder();
        html.append("<a href='");
        html.append(safe);
        html.append("'>이동</a>");
        // ruleid: mois-1-04-xss-spring-response
        return html.toString();
    }
}
