package demo;

import java.io.IOException;
import java.net.URI;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.servlet.view.RedirectView;

// 탐지돼야 하는 경우: 외부 입력 URL 로 그대로 이동. sink 마다 한 줄씩
@Controller
public class RedirectController {
    // 진단가이드 예: 요청 파라미터 redirect 로 sendRedirect
    public void move(HttpServletRequest request, HttpServletResponse response) throws IOException {
        String rd = request.getParameter("redirect");
        // ruleid: mois-1-07-open-redirect
        response.sendRedirect(rd);
    }

    public void location(HttpServletRequest request, HttpServletResponse response) {
        response.setStatus(HttpServletResponse.SC_FOUND);
        // ruleid: mois-1-07-open-redirect
        response.setHeader("Location", request.getParameter("next"));
    }

    // "redirect:/" + 입력: 입력이 /evil.example 이면 redirect://evil.example (다른 사이트) 이 된다
    @GetMapping("/login/next")
    public String nextAfterLogin(@RequestParam String next) {
        // ruleid: mois-1-07-open-redirect
        return "redirect:/" + next;
    }

    @GetMapping("/login/next-view")
    public org.springframework.web.servlet.ModelAndView nextView(@RequestParam String next) {
        // ruleid: mois-1-07-open-redirect
        return new org.springframework.web.servlet.ModelAndView("redirect:/" + next);
    }

    // Spring 뷰 이름 "redirect:" + 입력
    @GetMapping("/login/success")
    public String afterLogin(@RequestParam("returnUrl") String returnUrl) {
        // ruleid: mois-1-07-open-redirect
        return "redirect:" + returnUrl;
    }

    @GetMapping("/go")
    public RedirectView go(@RequestParam String target) {
        // ruleid: mois-1-07-open-redirect
        return new RedirectView(target);
    }

    @GetMapping("/go2")
    public RedirectView go2(@RequestParam String target) {
        RedirectView view = new RedirectView();
        // ruleid: mois-1-07-open-redirect
        view.setUrl(target);
        return view;
    }

    @GetMapping("/go3")
    public ResponseEntity<Void> go3(@RequestParam String target) {
        HttpHeaders headers = new HttpHeaders();
        // ruleid: mois-1-07-open-redirect
        headers.setLocation(URI.create(target));
        return new ResponseEntity<>(headers, HttpStatus.FOUND);
    }
}
