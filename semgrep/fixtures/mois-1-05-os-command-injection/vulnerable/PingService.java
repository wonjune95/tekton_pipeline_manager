package demo;

import java.io.IOException;
import javax.servlet.http.HttpServletRequest;

// 탐지돼야 하는 경우: 외부 입력이 운영체제 명령어에 들어감
public class PingService {
    public Process ping(HttpServletRequest request) throws IOException {
        String host = request.getParameter("host");
        // ruleid: mois-1-05-os-command-injection
        return Runtime.getRuntime().exec("ping -c 1 " + host);
    }

    public Process run(HttpServletRequest request) throws IOException {
        String cmd = request.getParameter("cmd");
        // ruleid: mois-1-05-os-command-injection
        return new ProcessBuilder("sh", "-c", cmd).start();
    }
}
