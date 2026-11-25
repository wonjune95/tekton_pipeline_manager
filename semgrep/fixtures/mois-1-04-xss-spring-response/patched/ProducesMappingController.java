package demo;

import io.swagger.annotations.ApiOperation;
import org.springframework.http.MediaType;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.PatchMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

// 탐지되면 안 되는 경우: Spring 매핑 애너테이션의 produces 가 HTML 로 해석되지 않는 형식. 매핑 애너테이션마다 한 줄씩
// (@GetMapping 은 StatusController 에 있다)
@RestController
public class ProducesMappingController {
    @RequestMapping(value = "/p/echo", produces = "text/plain")
    public String request(@RequestParam String q) {
        // ok: mois-1-04-xss-spring-response
        return "q=" + q;
    }

    @PostMapping(value = "/p/notes", produces = MediaType.TEXT_PLAIN_VALUE)
    public String post(@RequestBody String note) {
        // ok: mois-1-04-xss-spring-response
        return "saved: " + note;
    }

    @PutMapping(value = "/p/notes/{id}", produces = "text/plain;charset=UTF-8")
    public String put(@PathVariable String id) {
        // ok: mois-1-04-xss-spring-response
        return "updated: " + id;
    }

    @PatchMapping(value = "/p/notes/{id}", produces = "text/plain")
    public String patch(@PathVariable String id) {
        // ok: mois-1-04-xss-spring-response
        return "patched: " + id;
    }

    @DeleteMapping(value = "/p/notes/{id}", produces = "text/plain")
    public String delete(@PathVariable String id) {
        // ok: mois-1-04-xss-spring-response
        return "deleted: " + id;
    }

    // Swagger 애너테이션이 함께 있어도 Spring 매핑의 produces 가 text/plain 이면 제외된다
    @ApiOperation(value = "상태", produces = "text/html")
    @RequestMapping(value = "/p/status", produces = "text/plain")
    public String documented(@RequestParam String job) {
        // ok: mois-1-04-xss-spring-response
        return "job=" + job;
    }
}
