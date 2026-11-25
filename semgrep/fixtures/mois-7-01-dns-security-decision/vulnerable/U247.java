package demo;

import java.io.IOException;
import java.net.InetAddress;
import java.util.Map;
import java.util.Set;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

// 탐지돼야 하는 경우 (진단가이드 7-1: DNS 이름으로 요청의 신뢰 여부를 판단)
public class U247 extends HttpServlet {
    private static final Set<String> TRUSTED = Set.of("admin.trustme.com");
    private static final Map<String, String> ROLES = Map.of("admin.trustme.com", "admin");

    @Override
    public void doGet(HttpServletRequest req, HttpServletResponse res) throws IOException {
        String ip = req.getRemoteAddr();
        InetAddress addr = InetAddress.getByName(ip);
        // 호스트의 DNS 이름이 신뢰할 수 있는 도메인에 속하는지 검사한다
        // ruleid: mois-7-01-dns-security-decision
        if (addr.getCanonicalHostName().endsWith("trustme.com")) {
            res.setStatus(200);
            return;
        }
        String host = req.getRemoteHost();
        // ruleid: mois-7-01-dns-security-decision
        res.setStatus(host.equals("admin.trustme.com") ? 200 : 403);
    }

    // ── (가) 호스트 이름을 얻는 방법 × 바로 비교 (비교 메서드 6종) ──

    boolean direct(HttpServletRequest req, InetAddress addr, String ip) throws IOException {
        // ruleid: mois-7-01-dns-security-decision
        boolean a = addr.getHostName().equalsIgnoreCase("admin.trustme.com");
        // ruleid: mois-7-01-dns-security-decision
        boolean b = InetAddress.getByName(ip).getCanonicalHostName().startsWith("admin.");
        // ruleid: mois-7-01-dns-security-decision
        boolean c = InetAddress.getByName(ip).getHostName().contains("trustme");
        // ruleid: mois-7-01-dns-security-decision
        boolean d = req.getRemoteHost().matches(".*\\.trustme\\.com");
        // ruleid: mois-7-01-dns-security-decision
        boolean e = req.getRemoteHost().equals("admin.trustme.com");
        return a || b || c || d || e;
    }

    // ── (나) 변수에 담아 비교 (선언·대입) ──

    boolean viaVariable(HttpServletRequest req, InetAddress addr) {
        String name = addr.getCanonicalHostName();
        // ruleid: mois-7-01-dns-security-decision
        boolean a = name.equalsIgnoreCase("admin.trustme.com");
        String host;
        host = req.getRemoteHost();
        // ruleid: mois-7-01-dns-security-decision
        boolean b = host.startsWith("admin.");
        // ruleid: mois-7-01-dns-security-decision
        boolean c = host.contains("trustme");
        // ruleid: mois-7-01-dns-security-decision
        boolean d = host.matches(".*\\.trustme\\.com");
        // ruleid: mois-7-01-dns-security-decision
        boolean e = host.endsWith(".kr");
        return a || b || c || d || e;
    }

    // ── (다) 상수·허용 목록 쪽에서 비교 ──

    boolean reversed(HttpServletRequest req, InetAddress addr) {
        // ruleid: mois-7-01-dns-security-decision
        boolean a = "admin.trustme.com".equals(req.getRemoteHost());
        // ruleid: mois-7-01-dns-security-decision
        boolean b = "ADMIN.TRUSTME.COM".equalsIgnoreCase(addr.getHostName());
        // ruleid: mois-7-01-dns-security-decision
        boolean c = TRUSTED.contains(addr.getCanonicalHostName());
        // ruleid: mois-7-01-dns-security-decision
        boolean d = ROLES.containsKey(req.getRemoteHost());
        return a || b || c || d;
    }

    boolean reversedViaVariable(HttpServletRequest req) {
        String host = req.getRemoteHost();
        // ruleid: mois-7-01-dns-security-decision
        boolean a = "admin.trustme.com".equals(host);
        // ruleid: mois-7-01-dns-security-decision
        boolean b = "ADMIN.TRUSTME.COM".equalsIgnoreCase(host);
        // ruleid: mois-7-01-dns-security-decision
        boolean c = TRUSTED.contains(host);
        // ruleid: mois-7-01-dns-security-decision
        boolean d = ROLES.containsKey(host);
        return a || b || c || d;
    }
}
