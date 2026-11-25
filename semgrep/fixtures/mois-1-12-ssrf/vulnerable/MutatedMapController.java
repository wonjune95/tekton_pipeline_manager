package demo;

import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;
import javax.servlet.http.HttpServletRequest;
import org.springframework.web.client.RestTemplate;

// 탐지돼야 하는 경우: final Map 이지만 put 이 아닌 메서드로 값을 바꿔 넣는다 (고정된 허용 목록이 아니다)
public class MutatedMapController {
    private final RestTemplate restTemplate = new RestTemplate();
    private final Map<String, String> webhooks = new ConcurrentHashMap<>();
    private final Map<String, String> discovered = new ConcurrentHashMap<>();
    private final Map<String, String> refreshed = new ConcurrentHashMap<>();
    private final Map<String, String> mirrors = new ConcurrentHashMap<>();
    private final Map<String, String> swapped = new ConcurrentHashMap<>();
    private final Map<String, String> rewritten = new ConcurrentHashMap<>();
    private final EndpointResolver resolver;

    public MutatedMapController(EndpointResolver resolver) {
        this.resolver = resolver;
    }

    public void subscribe(String tenant, String url) {
        webhooks.compute(tenant, (k, old) -> url);
    }

    public String compute(HttpServletRequest request) {
        // ruleid: mois-1-12-ssrf
        return restTemplate.getForObject(webhooks.get(request.getParameter("tenant")), String.class);
    }

    // 없는 키는 외부 조회 결과로 채운다
    public String computeIfAbsent(HttpServletRequest request) {
        String api = request.getParameter("api");
        discovered.computeIfAbsent(api, resolver::resolve);
        // ruleid: mois-1-12-ssrf
        return restTemplate.getForObject(discovered.get(api), String.class);
    }

    public void refresh(String api, String url) {
        refreshed.computeIfPresent(api, (k, old) -> url);
    }

    public String computeIfPresent(HttpServletRequest request) {
        // ruleid: mois-1-12-ssrf
        return restTemplate.getForObject(refreshed.get(request.getParameter("api")), String.class);
    }

    public void addMirror(String api, String url) {
        mirrors.merge(api, url, (old, added) -> added);
    }

    public String merge(HttpServletRequest request) {
        // ruleid: mois-1-12-ssrf
        return restTemplate.getForObject(mirrors.get(request.getParameter("api")), String.class);
    }

    public void swap(String api, String url) {
        swapped.replace(api, url);
    }

    public String replace(HttpServletRequest request) {
        // ruleid: mois-1-12-ssrf
        return restTemplate.getForObject(swapped.get(request.getParameter("api")), String.class);
    }

    public void rebase(String host) {
        rewritten.replaceAll((api, url) -> host + url);
    }

    public String replaceAll(HttpServletRequest request) {
        // ruleid: mois-1-12-ssrf
        return restTemplate.getForObject(rewritten.get(request.getParameter("api")), String.class);
    }

    interface EndpointResolver {
        String resolve(String api);
    }
}
