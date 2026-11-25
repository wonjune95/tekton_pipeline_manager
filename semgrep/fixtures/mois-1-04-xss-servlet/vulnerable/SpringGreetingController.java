package demo;

import java.io.IOException;
import javax.servlet.http.HttpServletResponse;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;

// 탐지돼야 하는 경우: Spring 요청 파라미터를 이스케이프 없이 응답에 출력
@Controller
public class SpringGreetingController {
    @GetMapping("/hello")
    public void hello(@RequestParam String name, HttpServletResponse response) throws IOException {
        // ruleid: mois-1-04-xss-servlet
        response.getWriter().write("<p>Hello " + name + "</p>");
    }
}
