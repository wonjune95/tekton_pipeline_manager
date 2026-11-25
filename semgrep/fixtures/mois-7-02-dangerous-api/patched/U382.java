package demo;

import java.io.IOException;
import java.net.Socket;
import java.net.URL;
import java.net.URLConnection;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

// 탐지되면 안 되는 경우 (진단가이드 7-2 안전한 코드: 프레임워크 API(URLConnection) 사용, System.exit() 미사용)
public class U382 extends HttpServlet {
    private static final Logger LOG = LoggerFactory.getLogger(U382.class);
    private static final String DATA_URL = "https://data.internal.example/DataServlet";

    @Override
    public void doPost(HttpServletRequest request, HttpServletResponse response) {
        try {
            // ok: mois-7-02-dangerous-api — 소켓 대신 URLConnection 을 쓴다
            URLConnection urlConn = new URL(DATA_URL).openConnection();
            urlConn.setDoOutput(true);
            response.setStatus(200);
        } catch (IOException ase) {
            // ok: mois-7-02-dangerous-api — 프로세스를 끝내지 않고 오류 응답을 준다
            LOG.info("ERROR");
            response.setStatus(503);
        }
    }
}

// ok: mois-7-02-dangerous-api — 서블릿도 Spring 빈도 아닌 일반 클래스의 소켓 사용은 이 규칙의 대상이 아니다
class PortChecker {
    static boolean open(String host, int port) {
        try (Socket socket = new Socket(host, port)) {
            return socket.isConnected();
        } catch (IOException e) {
            return false;
        }
    }
}
