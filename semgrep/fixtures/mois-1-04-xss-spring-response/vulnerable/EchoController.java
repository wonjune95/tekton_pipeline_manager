package demo;

import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PatchMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

// 탐지돼야 하는 경우: @RestController 핸들러가 외부 입력으로 만든 문자열을 그대로 응답. 매핑 애너테이션마다 한 줄씩
@RestController
public class EchoController {

    // 외부 입력을 응답 본문으로 그대로 반환 (애너테이션 없는 매개변수도 요청 값이다)
    @GetMapping("/echo")
    public String echo(String message) {
        // ruleid: mois-1-04-xss-spring-response
        return message;
    }

    @GetMapping("/hello")
    public String hello(@RequestParam("name") String name) {
        // ruleid: mois-1-04-xss-spring-response
        return "<p>안녕하세요 " + name + "</p>";
    }

    @RequestMapping("/search")
    public String search(@RequestParam String keyword) {
        StringBuilder html = new StringBuilder("<h1>");
        html.append(keyword).append("</h1>");
        // ruleid: mois-1-04-xss-spring-response
        return html.toString();
    }

    @PostMapping("/comments")
    public String create(@RequestBody String comment) {
        // ruleid: mois-1-04-xss-spring-response
        return "<li>" + comment + "</li>";
    }

    @PutMapping("/comments/{id}")
    public String update(@PathVariable String id, @RequestBody String comment) {
        // ruleid: mois-1-04-xss-spring-response
        return String.format("<li id=\"%s\">%s</li>", id, comment);
    }

    @PatchMapping("/comments/{id}")
    public String patch(@PathVariable String id) {
        if (id.isEmpty()) {
            return "<p>없음</p>";
        }
        // ruleid: mois-1-04-xss-spring-response
        return "<p>" + id + " 수정됨</p>";
    }

    @DeleteMapping("/comments/{id}")
    public String delete(@PathVariable String id) {
        // ruleid: mois-1-04-xss-spring-response
        return "<p>" + id + " 삭제됨</p>";
    }
}
