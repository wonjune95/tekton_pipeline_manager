package demo;

import java.util.Calendar;
import javax.servlet.http.HttpServletRequest;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

// 탐지돼야 하는 경우: 외부 입력이 형식 문자열에 들어감
@RestController
public class GreetingFormat {
    // 진단가이드 예와 같은 형태: 입력값을 형식 문자열 앞에 이어 붙임
    @GetMapping("/check")
    public String check(@RequestParam String name) {
        Calendar validDate = Calendar.getInstance();
        validDate.set(2014, Calendar.OCTOBER, 14);
        // ruleid: mois-1-17-format-string
        return String.format(name + " did not match! HINT: It was issued on %1$terd of some month", validDate);
    }

    public String label(HttpServletRequest request) {
        // ruleid: mois-1-17-format-string
        return String.format(request.getParameter("fmt"), "value");
    }
}
