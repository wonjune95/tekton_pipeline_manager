package demo;

import org.owasp.encoder.Encode;
import org.owasp.esapi.ESAPI;
import org.owasp.esapi.Encoder;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.util.HtmlUtils;

// 탐지되면 안 되는 경우: HTML 이스케이프한 값만 응답. 이스케이프 함수마다 한 줄씩
@RestController
public class EchoController {
    private final Encoder encoder = ESAPI.encoder();

    @GetMapping("/echo")
    public String echo(String message) {
        // ok: mois-1-04-xss-spring-response — Spring HtmlUtils
        return HtmlUtils.htmlEscape(message);
    }

    @GetMapping("/hello")
    public String hello(@RequestParam("name") String name) {
        // ok: mois-1-04-xss-spring-response
        return "<p>안녕하세요 " + HtmlUtils.htmlEscape(name) + "</p>";
    }

    @GetMapping("/e1")
    public String decimal(@RequestParam String q) {
        // ok: mois-1-04-xss-spring-response
        return HtmlUtils.htmlEscapeDecimal(q);
    }

    @GetMapping("/e2")
    public String hex(@RequestParam String q) {
        // ok: mois-1-04-xss-spring-response
        return HtmlUtils.htmlEscapeHex(q);
    }

    @GetMapping("/e3")
    public String owaspHtml(@RequestParam String q) {
        // ok: mois-1-04-xss-spring-response — OWASP Java Encoder
        return Encode.forHtml(q);
    }

    @GetMapping("/e4")
    public String owaspHtmlContent(@RequestParam String q) {
        // ok: mois-1-04-xss-spring-response
        return "<p>" + Encode.forHtmlContent(q) + "</p>";
    }

    @GetMapping("/e5")
    public String esapiHtml(@RequestParam String q) {
        // ok: mois-1-04-xss-spring-response — ESAPI
        return ESAPI.encoder().encodeForHTML(q);
    }

    @GetMapping("/e6")
    public String esapiAttribute(@RequestParam String q) {
        // ok: mois-1-04-xss-spring-response
        return "<input value=\"" + ESAPI.encoder().encodeForHTMLAttribute(q) + "\">";
    }

    @GetMapping("/e7")
    public String esapiField(@RequestParam String q) {
        // ok: mois-1-04-xss-spring-response — Encoder 를 필드로 둔 경우
        return encoder.encodeForHTML(q);
    }

    @GetMapping("/e8")
    public String esapiFieldAttribute(@RequestParam String q) {
        // ok: mois-1-04-xss-spring-response
        return "<input value=\"" + encoder.encodeForHTMLAttribute(q) + "\">";
    }

    @GetMapping("/e9")
    public String commonsText(@RequestParam String q) {
        // ok: mois-1-04-xss-spring-response — commons-text
        return org.apache.commons.text.StringEscapeUtils.escapeHtml4(q);
    }

    @GetMapping("/e10")
    public String commonsText3(@RequestParam String q) {
        // ok: mois-1-04-xss-spring-response
        return org.apache.commons.text.StringEscapeUtils.escapeHtml3(q);
    }

    @GetMapping("/e11")
    public String commonsLang3(@RequestParam String q) {
        // ok: mois-1-04-xss-spring-response — commons-lang3
        return org.apache.commons.lang3.StringEscapeUtils.escapeHtml4(q);
    }

    @GetMapping("/e12")
    public String commonsLang3Html3(@RequestParam String q) {
        // ok: mois-1-04-xss-spring-response
        return org.apache.commons.lang3.StringEscapeUtils.escapeHtml3(q);
    }

    @GetMapping("/e13")
    public String commonsLang2(@RequestParam String q) {
        // ok: mois-1-04-xss-spring-response — commons-lang 2 (전자정부 구버전)
        return org.apache.commons.lang.StringEscapeUtils.escapeHtml(q);
    }
}
