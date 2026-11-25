package egovframework.demo.cmm;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

// EgovWebUtil 을 같은 패키지로 옮겨 쓰는 프로젝트 (import 없이 짧은 이름으로 부른다)
@RestController
public class EgovXssControllerLocal {
    @GetMapping("/local/a")
    public String a(@RequestParam String q) {
        // ok: mois-1-04-xss-spring-response
        return "<p>" + EgovWebUtil.clearXSSMinimum(q) + "</p>";
    }

    @GetMapping("/local/b")
    public String b(@RequestParam String q) {
        // ok: mois-1-04-xss-spring-response
        return "<p>" + EgovWebUtil.clearXSSMaximum(q) + "</p>";
    }

    @GetMapping("/local/c")
    public String c(@RequestParam String q) {
        // ok: mois-1-04-xss-spring-response
        return "<p>" + EgovWebUtil.clearXSS(q) + "</p>";
    }

    @GetMapping("/local/d")
    public String d(@RequestParam String q) {
        // ok: mois-1-04-xss-spring-response
        return "<p>" + EgovWebUtil.escapeXml(q) + "</p>";
    }
}
