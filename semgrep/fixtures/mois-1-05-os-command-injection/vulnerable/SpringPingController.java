package demo;

import java.io.IOException;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.context.request.WebRequest;
import org.springframework.web.multipart.MultipartFile;
import org.springframework.web.multipart.MultipartHttpServletRequest;

// 탐지돼야 하는 경우: Spring 으로 들어온 요청 값이 셸 명령어에 들어감 (입력 지점 형태별)
@RestController
public class SpringPingController {
    @GetMapping("/ping")
    public Process ping(@RequestParam String host) throws IOException {
        // ruleid: mois-1-05-os-command-injection
        return Runtime.getRuntime().exec(new String[] {"sh", "-c", "ping -c 1 " + host});
    }

    // 애너테이션이 없는 핸들러 매개변수도 요청 파라미터로 채워진다
    @GetMapping("/trace")
    public Process trace(String host) throws IOException {
        // ruleid: mois-1-05-os-command-injection
        return Runtime.getRuntime().exec("traceroute " + host);
    }

    // 요청을 감싼 객체: 멀티파트 요청, WebRequest
    @PostMapping("/convert")
    public Process convert(MultipartHttpServletRequest request) throws IOException {
        // ruleid: mois-1-05-os-command-injection
        return Runtime.getRuntime().exec("convert " + request.getParameter("options"));
    }

    @GetMapping("/lookup")
    public Process lookup(WebRequest request) throws IOException {
        // ruleid: mois-1-05-os-command-injection
        return Runtime.getRuntime().exec("nslookup " + request.getParameter("name"));
    }

    // 업로드 파일의 원본 이름
    @PostMapping("/scan")
    public Process scan(MultipartFile file) throws IOException {
        // ruleid: mois-1-05-os-command-injection
        return new ProcessBuilder("sh", "-c", "clamscan " + file.getOriginalFilename()).start();
    }
}
