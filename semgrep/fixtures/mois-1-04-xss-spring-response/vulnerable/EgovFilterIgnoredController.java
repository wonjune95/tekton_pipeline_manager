package egovframework.demo;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import egovframework.com.cmm.EgovWebUtil;

@RestController
public class EgovFilterIgnoredController {
    // 필터를 부르기만 하고 결과를 쓰지 않으면 원래 값이 그대로 응답에 들어간다
    @GetMapping("/egov/ignored")
    public String ignored(@RequestParam String q) {
        EgovWebUtil.clearXSS(q);
        // ruleid: mois-1-04-xss-spring-response
        return "<p>" + q + "</p>";
    }
}
