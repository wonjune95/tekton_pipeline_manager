package demo;

import com.google.common.collect.ImmutableMap;
import java.io.IOException;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.HashMap;
import java.util.Map;
import javax.servlet.http.HttpServletRequest;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.client.RestTemplate;

// 탐지되면 안 되는 경우: 허용 목록(Map)에서 URL 을 고르거나, 스킴·호스트가 고정된 주소에 경로만 붙인다
@RestController
public class ProxyController {
    private static final Map<String, String> ENDPOINTS = Map.of("stat", "https://stat.example.go.kr/api");
    private static final Map<String, String> LEGACY = new HashMap<>();
    private final RestTemplate restTemplate = new RestTemplate();
    // 값에 이스케이프가 들어 있어도 리터럴이다
    private static final Map<String, String> SEARCH = Map.of("all", "https://stat.example.go.kr/api/search?q=\"all\"");
    private static final Map<String, String> PARTNERS = Map.ofEntries(
            Map.entry("code", "https://code.example.go.kr/api"),
            Map.entry("addr", "https://addr.example.go.kr/api"));
    private static final ImmutableMap<String, String> MIRRORS = ImmutableMap.of("kr", "https://kr.example.go.kr/api");
    private final Map<String, String> urlMap = Map.of("stat", "https://stat.example.go.kr/api");
    private final Map<String, String> routes = new HashMap<>();
    private final Map<String, String> backups = new HashMap<>();

    @Value("${backend.base-url}")
    private String backendBaseUrl;

    static {
        LEGACY.put("code", "https://code.example.go.kr/api");
    }

    {
        // 초기화 블록에서 리터럴 값만 넣는다
        backups.put("stat", "https://stat-backup.example.go.kr/api");
        this.backups.put("code", "https://code-backup.example.go.kr/api");
    }

    public ProxyController() {
        // 생성자에서 리터럴 값만 넣는다
        routes.put("stat", "https://stat.example.go.kr/api");
        this.routes.put("code", "https://code.example.go.kr/api");
    }

    // 진단가이드 안전한 코드 예처럼 입력값은 urlMap 의 키로만 쓴다 (urlMap 의 내용은 이 클래스에서 리터럴로 정한다)
    public HttpURLConnection connect(HttpServletRequest req) throws IOException {
        // ok: mois-1-12-ssrf — Map.of 로 만든 final Map 에서 꺼낸 주소
        URL url = new URL(urlMap.get(req.getParameter("url")));
        return (HttpURLConnection) url.openConnection();
    }

    public HttpURLConnection connectViaThis(HttpServletRequest req) throws IOException {
        // ok: mois-1-12-ssrf
        URL url = new URL(this.urlMap.get(req.getParameter("url")));
        return (HttpURLConnection) url.openConnection();
    }

    public String search(HttpServletRequest request) {
        // ok: mois-1-12-ssrf — 이스케이프가 든 리터럴 값
        return restTemplate.getForObject(SEARCH.get(request.getParameter("api")), String.class);
    }

    public String partner(HttpServletRequest request) {
        // ok: mois-1-12-ssrf — Map.ofEntries(Map.entry("k", "v"), …) 로 만든 final Map
        return restTemplate.getForObject(PARTNERS.get(request.getParameter("api")), String.class);
    }

    public String mirror(HttpServletRequest request) {
        // ok: mois-1-12-ssrf — ImmutableMap.of 로 만든 final Map
        return restTemplate.getForObject(MIRRORS.get(request.getParameter("region")), String.class);
    }

    public String backup(HttpServletRequest request) {
        // ok: mois-1-12-ssrf — 빈 Map 으로 만들고 초기화 블록에서 리터럴만 넣은 final Map
        return restTemplate.getForObject(backups.get(request.getParameter("api")), String.class);
    }

    public String endpoint(HttpServletRequest request) {
        // ok: mois-1-12-ssrf — final Map 에서 고르고 기본값은 리터럴
        String url = ENDPOINTS.getOrDefault(request.getParameter("api"), "https://stat.example.go.kr/api");
        return restTemplate.getForObject(url, String.class);
    }

    public String route(HttpServletRequest request) {
        // ok: mois-1-12-ssrf — 빈 Map 으로 만들고 생성자에서 리터럴만 넣은 final Map
        String url = this.routes.getOrDefault(request.getParameter("api"), "https://stat.example.go.kr/api");
        return restTemplate.getForObject(url, String.class);
    }

    public String legacy(HttpServletRequest request) {
        // ok: mois-1-12-ssrf — static 블록에서 리터럴 값만 넣은 final Map
        return restTemplate.getForObject(LEGACY.get(request.getParameter("api")), String.class);
    }

    @GetMapping(value = "/items", produces = "application/json")
    public String item(@RequestParam String itemId) {
        // ok: mois-1-12-ssrf — 스킴과 호스트가 고정되고 / 로 끝난 뒤에 붙인다
        return restTemplate.getForObject("https://api.example.com/items/" + itemId, String.class);
    }

    @GetMapping(value = "/items/search", produces = "application/json")
    public String search(@RequestParam String keyword, @RequestParam String sort) {
        // ok: mois-1-12-ssrf — 여러 값을 이어 붙여도 맨 앞이 고정 주소
        return restTemplate.getForObject("https://api.example.com/items?q=" + keyword + "&sort=" + sort, String.class);
    }

    @GetMapping(value = "/items/detail", produces = "application/json")
    public String detail(@RequestParam String itemId) {
        // ok: mois-1-12-ssrf — 형식 문자열의 스킴·호스트가 고정
        return restTemplate.getForObject(String.format("https://api.example.com/items/%s/detail", itemId), String.class);
    }

    @GetMapping(value = "/pages", produces = "application/json")
    public String page(@RequestParam String page) {
        // ok: mois-1-12-ssrf — 숫자로 바꾼 값은 요청 대상을 바꿀 수 없다
        return restTemplate.getForObject(backendBaseUrl + "?page=" + Integer.parseInt(page), String.class);
    }

    @GetMapping(value = "/pages/next", produces = "application/json")
    public String nextPage(@RequestParam String page) {
        int next = Integer.parseInt(page);
        // ok: mois-1-12-ssrf — 숫자로 바꿔 변수에 받은 값
        return restTemplate.getForObject(backendBaseUrl + "?page=" + next, String.class);
    }

    @GetMapping(value = "/comments", produces = "application/json")
    public String comment(@RequestParam String id) {
        // ok: mois-1-12-ssrf — 숫자로 바꾼 값을 바로 붙인다
        return restTemplate.getForObject(backendBaseUrl + "/comments/" + Long.parseLong(id), String.class);
    }

    @GetMapping(value = "/items/named", produces = "application/json")
    public String named(@RequestParam String name) {
        // ok: mois-1-12-ssrf — 고정 주소 리터럴에 이스케이프(\")가 들어 있어도 리터럴이 닫힌 뒤에 붙인다
        return restTemplate.getForObject("https://api.example.com/items?filter=name eq \"" + name + "\"", String.class);
    }

    @GetMapping(value = "/articles", produces = "application/json")
    public String article(@RequestParam String id) {
        long articleId = Long.parseLong(id);
        // ok: mois-1-12-ssrf
        return restTemplate.getForObject(backendBaseUrl + "/articles/" + articleId, String.class);
    }
}
