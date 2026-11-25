package demo;

import java.io.UnsupportedEncodingException;
import java.net.URLEncoder;
import java.nio.charset.StandardCharsets;
import javax.servlet.http.Cookie;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.util.UriUtils;

// 탐지되면 안 되는 경우: CR·LF 를 둘 다 제거하거나(진단가이드 예) 인코딩·숫자 변환한 뒤 사용
@RestController
public class LoginCookieController {
    public void remember(HttpServletRequest request, HttpServletResponse response) {
        // ok: mois-1-13-http-response-splitting — 진단가이드 안전한 코드 예: \r 과 \n 이 모두 든 문자 클래스를 지움
        String lastLogin = request.getParameter("last_login").replaceAll("[\\r\\n]", "");
        Cookie c = new Cookie("LASTLOGIN", lastLogin);
        c.setSecure(true);
        c.setHttpOnly(true);
        response.addCookie(c);
    }

    public void download(HttpServletRequest request, HttpServletResponse res) throws UnsupportedEncodingException {
        // ok: mois-1-13-http-response-splitting — URL 인코딩하면 CR·LF 가 %0D%0A 가 된다
        String filename = URLEncoder.encode(request.getParameter("file"), "UTF-8");
        res.setHeader("Content-Disposition", "attachment;filename=" + filename);
    }

    public void downloadUtf8(HttpServletRequest request, HttpServletResponse res) {
        // ok: mois-1-13-http-response-splitting
        String filename = UriUtils.encode(request.getParameter("file"), StandardCharsets.UTF_8);
        res.setHeader("Content-Disposition", "attachment;filename*=UTF-8''" + filename);
    }

    @GetMapping("/lang")
    public void lang(@RequestParam String lang, HttpServletResponse response) {
        // ok: mois-1-13-http-response-splitting — \r 과 \n 을 이어서 각각 지움
        response.addHeader("Content-Language", lang.replace("\r", "").replace("\n", ""));
    }

    @GetMapping("/variants")
    public void variants(@RequestParam String v, HttpServletResponse response) {
        // ok: mois-1-13-http-response-splitting — 순서가 바뀌어도, replaceAll 로 써도 둘 다 지우면 된다
        response.setHeader("X-A", v.replaceAll("\\n", "").replaceAll("\\r", ""));
        // ok: mois-1-13-http-response-splitting — \r|\n
        response.setHeader("X-B", v.replaceAll("(\\r\\n|\\r|\\n)", " "));
        // ok: mois-1-13-http-response-splitting — 문자 클래스 안의 순서가 \n, \r 이어도 같다
        response.setHeader("X-E", v.replaceAll("[\\n\\r]", ""));
        // ok: mois-1-13-http-response-splitting — \n|\r
        response.setHeader("X-F", v.replaceAll("\\n|\\r", ""));
        // ok: mois-1-13-http-response-splitting — \R 은 모든 줄바꿈
        response.setHeader("X-C", v.replaceAll("\\R", ""));
        // ok: mois-1-13-http-response-splitting — \s 는 CR·LF 를 포함한 공백
        response.setHeader("X-D", v.replaceAll("\\s+", "_"));
        // ok: mois-1-13-http-response-splitting — replace 로 \n, \r 순서 (역슬래시 1개 = 개행 문자 자체), 빈칸으로 바꿈
        response.setHeader("X-G", v.replace("\n", " ").replace("\r", " "));
        // ok: mois-1-13-http-response-splitting — replaceAll 로 \r, \n 순서
        response.setHeader("X-H", v.replaceAll("\\r", "").replaceAll("\\n", ""));
        // ok: mois-1-13-http-response-splitting — 문자 클래스에 다른 글자(탭·빈칸)가 함께 있어도 \r 과 \n 이 모두 들어 있다
        response.setHeader("X-I", v.replaceAll("[\\r\\n\\t ]+", " "));
        // ok: mois-1-13-http-response-splitting — replaceAll 에 개행 문자 자체(역슬래시 1개)를 적어도 같다
        response.setHeader("X-J", v.replaceAll("\r|\n", ""));
    }

    public void paging(HttpServletRequest request, HttpServletResponse response) {
        // ok: mois-1-13-http-response-splitting — 숫자로 바꾼 값에는 개행이 들어갈 수 없다
        response.setHeader("X-Page", String.valueOf(Integer.parseInt(request.getParameter("page"))));
        long total = Long.parseLong(request.getParameter("total"));
        // ok: mois-1-13-http-response-splitting
        response.setHeader("X-Total-Count", "" + total);
    }
}
