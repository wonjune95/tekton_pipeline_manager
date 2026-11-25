package demo;

import jakarta.servlet.http.HttpServlet;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import java.io.IOException;
import java.net.Socket;

// 탐지돼야 하는 경우: jakarta 네임스페이스의 서블릿에서 소켓 직접 사용
public class JakartaProbe extends HttpServlet {
    @Override
    public void doGet(HttpServletRequest request, HttpServletResponse response) throws IOException {
        // ruleid: mois-7-02-dangerous-api
        try (Socket socket = new Socket("kisa.or.kr", 8080)) {
            response.setStatus(socket.isConnected() ? 200 : 503);
        }
    }
}
