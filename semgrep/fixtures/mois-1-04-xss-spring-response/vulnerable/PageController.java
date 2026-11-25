package demo;

import org.springframework.http.MediaType;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.ResponseBody;
import org.springframework.web.util.HtmlUtils;

// 탐지돼야 하는 경우: @Controller 의 @ResponseBody 핸들러, HTML 로 응답한다고 적은 핸들러, 이스케이프가 적용되지 않은 값
@Controller
public class PageController {

    @GetMapping("/banner")
    @ResponseBody
    public String banner(@RequestParam String text) {
        // ruleid: mois-1-04-xss-spring-response
        return "<div class=\"banner\">" + text + "</div>";
    }

    // produces 가 HTML: 브라우저가 그대로 해석한다
    @GetMapping(value = "/preview", produces = MediaType.TEXT_HTML_VALUE)
    @ResponseBody
    public String preview(@RequestParam String body) {
        // ruleid: mois-1-04-xss-spring-response
        return body;
    }

    @GetMapping(value = "/preview2", produces = "text/html;charset=UTF-8")
    @ResponseBody
    public String previewUtf8(@RequestParam String body) {
        // ruleid: mois-1-04-xss-spring-response
        return body;
    }

    // 여러 형식을 나열: 요청의 Accept 에 따라 text/html 로 응답한다
    @GetMapping(value = "/preview3", produces = {"text/plain", "text/html"})
    @ResponseBody
    public String previewNegotiated(@RequestParam String body) {
        // ruleid: mois-1-04-xss-spring-response
        return body;
    }

    // 모든 형식 허용은 형식을 지정하지 않은 것과 같다
    @GetMapping(value = "/preview4", produces = MediaType.ALL_VALUE)
    @ResponseBody
    public String previewAny(@RequestParam String body) {
        // ruleid: mois-1-04-xss-spring-response
        return body;
    }

    // 이스케이프 결과를 쓰지 않음 (String 은 바뀌지 않는다)
    @GetMapping("/title")
    @ResponseBody
    public String resultIgnored(@RequestParam String title) {
        HtmlUtils.htmlEscape(title);
        // ruleid: mois-1-04-xss-spring-response
        return "<h1>" + title + "</h1>";
    }

    // 다른 변수만 이스케이프
    @GetMapping("/article")
    @ResponseBody
    public String otherVariable(@RequestParam String title, @RequestParam String body) {
        String safeTitle = HtmlUtils.htmlEscape(title);
        // ruleid: mois-1-04-xss-spring-response
        return "<h1>" + safeTitle + "</h1><div>" + body + "</div>";
    }
}
