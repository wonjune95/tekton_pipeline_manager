package demo;

import javax.servlet.http.Cookie;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import org.springframework.http.HttpHeaders;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

// 탐지돼야 하는 경우: 개행 문자를 걸러내지 않은 입력이 응답 헤더·쿠키에 들어감. sink 마다 한 줄씩
@RestController
public class LoginCookieController {
    // 진단가이드 예: 요청 파라미터를 그대로 쿠키 값에 사용
    public void remember(HttpServletRequest request, HttpServletResponse response) {
        String lastLogin = request.getParameter("last_login");
        // ruleid: mois-1-13-http-response-splitting
        Cookie c = new Cookie("LASTLOGIN", lastLogin);
        c.setSecure(true);
        response.addCookie(c);
    }

    public void update(HttpServletRequest request, HttpServletResponse response) {
        Cookie c = new Cookie("THEME", "light");
        // ruleid: mois-1-13-http-response-splitting
        c.setValue(request.getParameter("theme"));
        response.addCookie(c);
    }

    // 진단가이드 정탐 예: 파일 이름을 Content-Disposition 헤더에 그대로 사용
    public void download(HttpServletRequest request, HttpServletResponse res) {
        String filename = request.getParameter("file");
        // ruleid: mois-1-13-http-response-splitting
        res.setHeader("Content-Disposition", "attachment;filename=" + filename);
    }

    @GetMapping("/lang")
    public void lang(@RequestParam String lang, HttpServletResponse response) {
        // ruleid: mois-1-13-http-response-splitting
        response.addHeader("Content-Language", lang);
    }

    @GetMapping(value = "/trace", produces = "text/plain")
    public ResponseEntity<String> trace(@RequestParam String traceId, @RequestParam String tag) {
        HttpHeaders headers = new HttpHeaders();
        // ruleid: mois-1-13-http-response-splitting
        headers.add("X-Trace-Id", traceId);
        // ruleid: mois-1-13-http-response-splitting
        headers.set("X-Tag", tag);
        return ResponseEntity.ok().headers(headers).body("ok");
    }
}
