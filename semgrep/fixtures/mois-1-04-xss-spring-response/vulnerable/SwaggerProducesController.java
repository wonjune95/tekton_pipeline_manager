package demo;

import io.swagger.annotations.ApiOperation;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

// 탐지돼야 하는 경우: produces 가 Spring 매핑이 아닌 다른 애너테이션에만 적혀 있다 (v0.6.1 감사 12번)
@RestController
public class SwaggerProducesController {
    // Swagger 의 produces 는 API 문서용이다. 실제 응답 형식은 @GetMapping 이 정하고, 여기에는 지정이 없다
    @ApiOperation(value = "검색", produces = "application/json")
    @GetMapping("/swagger/search")
    public String search(@RequestParam String q) {
        // ruleid: mois-1-04-xss-spring-response
        return "<b>" + q + "</b>";
    }
}
