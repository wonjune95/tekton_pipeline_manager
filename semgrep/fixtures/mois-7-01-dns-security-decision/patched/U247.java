package demo;

import java.io.IOException;
import java.net.InetAddress;
import java.util.Set;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

// 탐지되면 안 되는 경우 (진단가이드 7-1 안전한 코드: DNS 조회 없이 IP 주소를 직접 비교)
public class U247 extends HttpServlet {
    private static final Logger LOG = LoggerFactory.getLogger(U247.class);
    private static final String TRUSTED_ADDR = "127.0.0.1";
    private static final Set<String> TRUSTED_ADDRS = Set.of("127.0.0.1", "10.0.0.5");

    @Override
    public void doGet(HttpServletRequest req, HttpServletResponse res) throws IOException {
        // ok: mois-7-01-dns-security-decision — getRemoteAddr() 는 DNS 조회 없이 IP 주소를 돌려준다
        String ip = req.getRemoteAddr();
        if (ip == null || "".equals(ip)) {
            res.setStatus(400);
            return;
        }
        res.setStatus(ip.equals(TRUSTED_ADDR) ? 200 : 403);
    }

    // ok: mois-7-01-dns-security-decision — InetAddress 의 IP 주소(getHostAddress)로 판단한다
    boolean trusted(InetAddress addr) {
        String ip = addr.getHostAddress();
        return TRUSTED_ADDRS.contains(ip) || TRUSTED_ADDR.equals(addr.getHostAddress());
    }

    // ok: mois-7-01-dns-security-decision — 호스트 이름을 기록만 하고 판단에는 쓰지 않는다
    void audit(InetAddress addr) {
        String name = addr.getHostName();
        LOG.info("ERROR-70: 접속 호스트 길이 {}", Integer.valueOf(name.length()));
    }
}
