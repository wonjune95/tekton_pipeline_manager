package demo;

import java.io.IOException;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

// 탐지돼야 하는 경우: final Map 이지만 put 이 아닌 메서드로 값을 바꿔 넣는다 (고정된 허용 목록이 아니다)
public class MutatedMapController {
    private final Map<String, String> lastVisited = new ConcurrentHashMap<>();
    private final Map<String, String> resolved = new ConcurrentHashMap<>();
    private final Map<String, String> refreshed = new ConcurrentHashMap<>();
    private final Map<String, String> trail = new ConcurrentHashMap<>();
    private final Map<String, String> swapped = new ConcurrentHashMap<>();
    private final Map<String, String> rewritten = new ConcurrentHashMap<>();
    private final LinkResolver resolver;

    public MutatedMapController(LinkResolver resolver) {
        this.resolver = resolver;
    }

    public void visit(String user, String url) {
        lastVisited.compute(user, (k, old) -> url);
    }

    public void compute(HttpServletRequest request, HttpServletResponse response) throws IOException {
        // ruleid: mois-1-07-open-redirect
        response.sendRedirect(lastVisited.get(request.getParameter("user")));
    }

    // 없는 키는 외부 조회 결과로 채운다
    public void computeIfAbsent(HttpServletRequest request, HttpServletResponse response) throws IOException {
        String page = request.getParameter("page");
        resolved.computeIfAbsent(page, resolver::resolve);
        // ruleid: mois-1-07-open-redirect
        response.sendRedirect(resolved.get(page));
    }

    public void refresh(String page, String url) {
        refreshed.computeIfPresent(page, (k, old) -> url);
    }

    public void computeIfPresent(HttpServletRequest request, HttpServletResponse response) throws IOException {
        // ruleid: mois-1-07-open-redirect
        response.sendRedirect(refreshed.get(request.getParameter("page")));
    }

    public void append(String user, String url) {
        trail.merge(user, url, (old, added) -> added);
    }

    public void merge(HttpServletRequest request, HttpServletResponse response) throws IOException {
        // ruleid: mois-1-07-open-redirect
        response.sendRedirect(trail.get(request.getParameter("user")));
    }

    public void swap(String page, String url) {
        swapped.replace(page, url);
    }

    public void replace(HttpServletRequest request, HttpServletResponse response) throws IOException {
        // ruleid: mois-1-07-open-redirect
        response.sendRedirect(swapped.get(request.getParameter("page")));
    }

    public void rebase(String host) {
        rewritten.replaceAll((page, url) -> host + url);
    }

    public void replaceAll(HttpServletRequest request, HttpServletResponse response) throws IOException {
        // ruleid: mois-1-07-open-redirect
        response.sendRedirect(rewritten.get(request.getParameter("page")));
    }

    interface LinkResolver {
        String resolve(String page);
    }
}
