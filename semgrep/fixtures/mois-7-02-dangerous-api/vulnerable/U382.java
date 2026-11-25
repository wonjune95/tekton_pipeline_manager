package demo;

import java.io.IOException;
import java.net.DatagramSocket;
import java.net.ServerSocket;
import java.net.Socket;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Component;
import org.springframework.stereotype.Controller;
import org.springframework.stereotype.Repository;
import org.springframework.stereotype.Service;
import org.springframework.web.bind.annotation.RestController;

// 탐지돼야 하는 경우 (진단가이드 7-2: J2EE 에서 System.exit() 사용, 소켓 직접 사용)
public class U382 extends HttpServlet {
    private static final Logger LOG = LoggerFactory.getLogger(U382.class);

    @Override
    public void doPost(HttpServletRequest request, HttpServletResponse response) {
        // ruleid: mois-7-02-dangerous-api
        try (Socket socket = new Socket("kisa.or.kr", 8080)) {
            response.setStatus(socket.isConnected() ? 200 : 503);
        } catch (IOException ase) {
            LOG.info("ERROR");
            // J2EE 프로그램에서 System.exit() 으로 서비스가 종료될 수 있다
            // ruleid: mois-7-02-dangerous-api
            System.exit(1);
        }
    }

    // ── 프로세스 종료 3종 ──

    void shutdown(int code) {
        // ruleid: mois-7-02-dangerous-api
        Runtime.getRuntime().exit(code);
    }

    void kill() {
        // ruleid: mois-7-02-dangerous-api
        Runtime.getRuntime().halt(1);
    }

    // 전체 이름으로 쓴 경우
    void shutdownQualified(int code) {
        // ruleid: mois-7-02-dangerous-api
        java.lang.System.exit(code);
        // ruleid: mois-7-02-dangerous-api
        java.lang.Runtime.getRuntime().exit(code);
        // ruleid: mois-7-02-dangerous-api
        java.lang.Runtime.getRuntime().halt(code);
    }

    // (독립 실행 main() 안의 System.exit() 는 이 규칙으로 표시하지 않는다 — main() 자체는 6-2 디버그 코드 규칙이 맡는다)
    public static void main(String[] args) {
        System.exit(args.length == 0 ? 1 : 0);
    }

    // 이름만 main 이고 프로그램 시작점이 아니다
    public void main(String command) {
        // ruleid: mois-7-02-dangerous-api
        System.exit(0);
    }
}

// ── Spring 빈(스테레오타입 5종)에서 소켓 직접 사용: Socket · ServerSocket · DatagramSocket ──

@Controller
class ProbeController {
    boolean probe(String host) throws IOException {
        // ruleid: mois-7-02-dangerous-api
        try (Socket s = new Socket(host, 80)) {
            return s.isConnected();
        }
    }
}

@RestController
class ListenerApi {
    int listen() throws IOException {
        // ruleid: mois-7-02-dangerous-api
        try (ServerSocket server = new ServerSocket(0)) {
            return server.getLocalPort();
        }
    }
}

@Service("udpService")
class UdpService {
    int open() throws IOException {
        // ruleid: mois-7-02-dangerous-api
        try (DatagramSocket socket = new DatagramSocket()) {
            return socket.getLocalPort();
        }
    }
}

@Component
class Pinger {
    boolean ping(String host) throws IOException {
        // ruleid: mois-7-02-dangerous-api
        try (Socket s = new Socket(host, 7)) {
            return s.isConnected();
        }
    }
}

@Repository
class RemoteStore {
    boolean reachable(String host) throws IOException {
        // ruleid: mois-7-02-dangerous-api
        try (Socket s = new Socket(host, 5432)) {
            return s.isConnected();
        }
    }
}
