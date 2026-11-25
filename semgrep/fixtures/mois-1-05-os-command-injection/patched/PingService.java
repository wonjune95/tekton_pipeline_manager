package demo;

import java.io.IOException;
import javax.servlet.http.HttpServletRequest;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

// 탐지되면 안 되는 경우: 입력값은 허용 목록 선택에만 쓰고 명령어는 고정
@RestController
public class PingService {
    public Process ping(HttpServletRequest request) throws IOException {
        String target = "127.0.0.1";
        if ("gateway".equals(request.getParameter("host"))) {
            target = "10.0.0.1";
        }
        // ok: mois-1-05-os-command-injection — 명령어 인자는 코드에 적힌 상수 중에서만 고른다
        return new ProcessBuilder("ping", "-c", "1", target).start();
    }

    public Process uptime() throws IOException {
        // ok: mois-1-05-os-command-injection — 입력이 없다
        return Runtime.getRuntime().exec(new String[] {"uptime"});
    }

    // 숫자형 파라미터는 명령어를 끼워 넣을 수 없다
    @GetMapping("/ping/count")
    public Process pingCount(@RequestParam int count) throws IOException {
        // ok: mois-1-05-os-command-injection — int 는 외부 입력(문자열)으로 보지 않는다
        return new ProcessBuilder("ping", "-c", String.valueOf(count), "127.0.0.1").start();
    }

    // 입력값으로는 분기만 하고, 실행할 명령어는 상수로 정한다
    @GetMapping("/report")
    public Process report(@RequestParam String kind) throws IOException {
        String script;
        switch (kind) {
            case "daily":
                script = "/opt/report/daily.sh";
                break;
            case "weekly":
                script = "/opt/report/weekly.sh";
                break;
            default:
                throw new IllegalArgumentException("unknown report");
        }
        // ok: mois-1-05-os-command-injection — 실행 파일은 상수
        return new ProcessBuilder(script).start();
    }
}
