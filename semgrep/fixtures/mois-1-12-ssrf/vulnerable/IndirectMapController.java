package demo;

import java.io.IOException;
import java.util.HashMap;
import java.util.Map;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

// 탐지돼야 하는 경우: 빈 Map 으로 시작했지만 메서드 참조나 다른 호출에 넘겨 채운다 (값이 어디서 왔는지 알 수 없다)
public class IndirectMapController {
    private final Map<String, String> byMethodRef = new HashMap<>();
    private final Map<String, String> byCtorMethodRef = new HashMap<>();
    private final Map<String, String> byHelper = new HashMap<>();
    private final Map<String, String> byCtorHelper = new HashMap<>();

    IndirectMapController(Map<String, String> supplied) {
        supplied.forEach(byCtorMethodRef::put);
        Registry.fill(byCtorHelper);
    }

    void reload(Map<String, String> supplied) {
        supplied.forEach(byMethodRef::put);
        Registry.fill(byHelper);
    }

    void methodRef(HttpServletRequest req) throws IOException {
        // ruleid: mois-1-12-ssrf
        new java.net.URL(byMethodRef.get(req.getParameter("key"))).openStream();
    }

    void ctorMethodRef(HttpServletRequest req) throws IOException {
        // ruleid: mois-1-12-ssrf
        new java.net.URL(byCtorMethodRef.get(req.getParameter("key"))).openStream();
    }

    void helper(HttpServletRequest req) throws IOException {
        // ruleid: mois-1-12-ssrf
        new java.net.URL(byHelper.get(req.getParameter("key"))).openStream();
    }

    void ctorHelper(HttpServletRequest req) throws IOException {
        // ruleid: mois-1-12-ssrf
        new java.net.URL(byCtorHelper.get(req.getParameter("key"))).openStream();
    }
}
