package egovframework.demo;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import egovframework.com.cmm.EgovWebUtil;

// 전자정부 표준프레임워크의 XSS 필터를 거친 값만 응답에 넣는다
@RestController
public class EgovXssController {
    @GetMapping("/egov/a")
    public String a(@RequestParam String q) {
        // ok: mois-1-04-xss-spring-response
        return "<p>" + EgovWebUtil.clearXSSMinimum(q) + "</p>";
    }

    @GetMapping("/egov/b")
    public String b(@RequestParam String q) {
        // ok: mois-1-04-xss-spring-response
        return "<p>" + EgovWebUtil.clearXSSMaximum(q) + "</p>";
    }

    @GetMapping("/egov/c")
    public String c(@RequestParam String q) {
        // ok: mois-1-04-xss-spring-response
        return "<p>" + EgovWebUtil.clearXSS(q) + "</p>";
    }

    @GetMapping("/egov/d")
    public String d(@RequestParam String q) {
        // ok: mois-1-04-xss-spring-response
        return "<p>" + EgovWebUtil.escapeXml(q) + "</p>";
    }

    // 패키지 전체 이름으로 부른 경우
    @GetMapping("/egov/full/a")
    public String fullA(@RequestParam String q) {
        // ok: mois-1-04-xss-spring-response
        return egovframework.com.cmm.EgovWebUtil.clearXSSMinimum(q);
    }

    @GetMapping("/egov/full/b")
    public String fullB(@RequestParam String q) {
        // ok: mois-1-04-xss-spring-response
        return egovframework.com.cmm.EgovWebUtil.clearXSSMaximum(q);
    }

    @GetMapping("/egov/full/c")
    public String fullC(@RequestParam String q) {
        // ok: mois-1-04-xss-spring-response
        return egovframework.com.cmm.EgovWebUtil.clearXSS(q);
    }

    @GetMapping("/egov/full/d")
    public String fullD(@RequestParam String q) {
        // ok: mois-1-04-xss-spring-response
        return egovframework.com.cmm.EgovWebUtil.escapeXml(q);
    }
}
