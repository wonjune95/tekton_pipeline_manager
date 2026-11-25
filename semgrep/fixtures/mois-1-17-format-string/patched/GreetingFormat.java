package demo;

import java.text.MessageFormat;
import java.util.Calendar;
import java.util.Locale;
import javax.servlet.http.HttpServletRequest;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

// 탐지되면 안 되는 경우: 형식 문자열은 상수, 입력값은 인자로만 넘긴다 (진단가이드 안전한 코드 예)
@RestController
public class GreetingFormat {
    @GetMapping(value = "/check", produces = "text/plain;charset=UTF-8")
    public String check(@RequestParam String name) {
        Calendar validDate = Calendar.getInstance();
        validDate.set(2014, Calendar.OCTOBER, 14);
        // ok: mois-1-17-format-string — 형식은 상수, 입력은 인자
        return String.format("%s did not match! HINT: It was issued on %2$terd of some month", name, validDate);
    }

    public String label(HttpServletRequest request) {
        // ok: mois-1-17-format-string — 형식은 상수, 입력은 인자
        return MessageFormat.format("라벨: {0}", request.getParameter("label"));
    }

    // Locale 을 첫 인자로 받는 형태에서도 형식(두 번째 인자)이 상수면 안전하다
    @GetMapping(value = "/price", produces = "text/plain;charset=UTF-8")
    public String price(@RequestParam String item, HttpServletRequest request) {
        // ok: mois-1-17-format-string — Locale 뒤의 형식 문자열이 상수
        String line = String.format(Locale.KOREA, "%s: %,d원", item, 1000);
        // ok: mois-1-17-format-string — 입력이 첫 번째 "인자" 자리에 있을 뿐이다
        return line + String.format("%s (%s)", item, request.getLocale());
    }

    @GetMapping(value = "/hello", produces = "text/plain;charset=UTF-8")
    public String hello(@RequestParam String name) {
        // ok: mois-1-17-format-string — 형식은 상수, 입력은 인자
        return "안녕하세요, %s 님".formatted(name);
    }
}
