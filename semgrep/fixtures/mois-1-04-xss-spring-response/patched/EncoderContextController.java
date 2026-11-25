package demo;

import org.apache.commons.text.StringEscapeUtils;
import org.owasp.encoder.Encode;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.util.HtmlUtils;

import egovframework.com.cmm.EgovWebUtil;

// 탐지되면 안 되는 경우: HTML 인코더가 실제로 막는 위치(본문, 따옴표로 감싼 일반 속성 값)에 넣어 응답
@RestController
public class EncoderContextController {
    private final String contextPath = "/app";

    // 태그 사이의 본문
    @GetMapping("/ctx/1")
    public String body(@RequestParam String q) {
        // ok: mois-1-04-xss-spring-response
        return "<p>" + HtmlUtils.htmlEscape(q) + "</p>";
    }

    // 본문: commons escapeHtml4
    @GetMapping("/ctx/2")
    public String bodyCommons(@RequestParam String q) {
        // ok: mois-1-04-xss-spring-response
        return "<td>" + StringEscapeUtils.escapeHtml4(q) + "</td>";
    }

    // 본문: EgovWebUtil.clearXSS (& < > 만 바꾸지만 본문에서는 충분하다)
    @GetMapping("/ctx/3")
    public String bodyEgovClearXss(@RequestParam String q) {
        // ok: mois-1-04-xss-spring-response
        return "<td>" + EgovWebUtil.clearXSS(q) + "</td>";
    }

    // 본문: Encode.forHtmlContent
    @GetMapping("/ctx/4")
    public String bodyContentEncoder(@RequestParam String q) {
        // ok: mois-1-04-xss-spring-response
        return String.format("<p>%s</p>", Encode.forHtmlContent(q));
    }

    // 큰따옴표 속성 값 + 따옴표를 바꾸는 인코더
    @GetMapping("/ctx/5")
    public String attrDouble(@RequestParam String q) {
        // ok: mois-1-04-xss-spring-response
        return "<input type=\"text\" value=\"" + HtmlUtils.htmlEscape(q) + "\">";
    }

    // 작은따옴표 속성 값 + 따옴표를 바꾸는 인코더
    @GetMapping("/ctx/6")
    public String attrSingle(@RequestParam String q) {
        // ok: mois-1-04-xss-spring-response
        return "<input value='" + HtmlUtils.htmlEscape(q) + "'>";
    }

    // 큰따옴표 속성 값 + commons escapeHtml4 (" 는 바꾼다)
    @GetMapping("/ctx/7")
    public String attrDoubleCommons(@RequestParam String q) {
        // ok: mois-1-04-xss-spring-response
        return "<input value=\"" + StringEscapeUtils.escapeHtml4(q) + "\">";
    }

    // 형식 문자열의 일반 속성 자리
    @GetMapping("/ctx/8")
    public String attrFormat(@RequestParam String q) {
        // ok: mois-1-04-xss-spring-response
        return String.format("<input name=\"q\" value=\"%s\">", HtmlUtils.htmlEscape(q));
    }

    // URL 속성이지만 앞부분(경로)이 고정이라 스킴을 바꿀 수 없다
    @GetMapping("/ctx/9")
    public String urlFixedPrefix(@RequestParam String q) {
        // ok: mois-1-04-xss-spring-response
        return "<a href=\"/board/view?id=" + HtmlUtils.htmlEscape(q) + "\">보기</a>";
    }

    // href·onclick 이 있지만 닫힌 뒤의 본문
    @GetMapping("/ctx/10")
    public String afterClosedAttrs(@RequestParam String q) {
        // ok: mois-1-04-xss-spring-response
        return "<a href=\"/home\" onclick=\"track()\">" + HtmlUtils.htmlEscape(q) + "</a>";
    }

    // <script> 가 닫힌 뒤의 본문
    @GetMapping("/ctx/11")
    public String afterClosedScript(@RequestParam String q) {
        // ok: mois-1-04-xss-spring-response
        return "<script src=\"/js/app.js\"></script><h1>" + HtmlUtils.htmlEscape(q) + "</h1>";
    }

    // content= 는 이벤트 속성(on…=)이 아니다
    @GetMapping("/ctx/12")
    public String contentAttr(@RequestParam String q) {
        // ok: mois-1-04-xss-spring-response
        return "<meta name=\"description\" content=\"" + HtmlUtils.htmlEscape(q) + "\">";
    }

    // 100% 의 % 는 형식 문자열의 자리표시가 아니다 (속성은 닫혀 있고 값은 본문)
    @GetMapping("/ctx/13")
    public String percentWidth(@RequestParam String q) {
        // ok: mois-1-04-xss-spring-response
        return "<td width=\"100%\">" + EgovWebUtil.clearXSS(q) + "</td>";
    }

    // data-id= 는 URL 속성(data=)이 아니다
    @GetMapping("/ctx/14")
    public String dataAttr(@RequestParam String q) {
        // ok: mois-1-04-xss-spring-response
        return "<li data-id=\"" + HtmlUtils.htmlEscape(q) + "\"></li>";
    }

    // 변수에 담았다가 본문에 씀
    @GetMapping("/ctx/15")
    public String viaVariable(@RequestParam String q) {
        String safe = HtmlUtils.htmlEscape(q);
        // ok: mois-1-04-xss-spring-response
        return "<td>" + safe + "</td>";
    }

    // 변수에 담았다가 일반 속성 값에 씀
    @GetMapping("/ctx/16")
    public String viaVariableAttr(@RequestParam String q) {
        String safe = HtmlUtils.htmlEscape(q);
        // ok: mois-1-04-xss-spring-response
        return String.format("<input value=\"%s\">", safe);
    }

    // 바로 앞 문장에서 본문 태그를 붙임
    @GetMapping("/ctx/17")
    public String splitOutput(@RequestParam String q) {
        StringBuilder html = new StringBuilder();
        html.append("<td>");
        html.append(HtmlUtils.htmlEscape(q));
        html.append("</td>");
        // ok: mois-1-04-xss-spring-response
        return html.toString();
    }

    // 앞 문장이 href 값을 열었지만 다음 문장이 값을 닫은 뒤(본문)에 인코딩한 값을 쓴다
    @GetMapping("/ctx/18")
    public String splitOutputAfterUrl(@RequestParam String q) {
        StringBuilder html = new StringBuilder();
        html.append("<a href=\"" + contextPath);
        html.append("/board/list\">" + HtmlUtils.htmlEscape(q) + "</a>");
        // ok: mois-1-04-xss-spring-response
        return html.toString();
    }
}
