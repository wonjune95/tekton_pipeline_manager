package demo;

import java.util.HashMap;
import java.util.Map;
import javax.servlet.http.HttpServletRequest;
import org.springframework.web.client.RestTemplate;

// 탐지돼야 하는 경우: 허용 목록·고정 주소처럼 보이지만 실제로는 요청 대상을 입력이 정하는 형태
public class NotAllowListController {
    private static final Map<String, String> ALLOWED = Map.of("stat", "https://stat.example.go.kr/api");
    private static final Map<String, String> FROM_ENV = new HashMap<>();
    private final RestTemplate restTemplate = new RestTemplate();
    private Map<String, String> mutable = new HashMap<>();
    private final Map<String, String> registered = new HashMap<>();
    private final Map<String, String> callbacks = new HashMap<>();
    private final Map<String, String> initial = new HashMap<>();
    private final Map<String, String> seeded = new HashMap<>();
    private final EndpointStore store;

    static {
        FROM_ENV.put("partner", System.getenv("PARTNER_API"));
    }

    public NotAllowListController(EndpointStore store, Map<String, String> seed, String fallback) {
        this.store = store;
        initial.put("fallback", fallback);
        this.seeded.putAll(seed);
    }

    // 기본값이 입력: 목록에 없으면 입력한 주소로 요청한다
    public String defaultFromInput(HttpServletRequest request) {
        String url = request.getParameter("url");
        // ruleid: mois-1-12-ssrf
        return restTemplate.getForObject(ALLOWED.getOrDefault(request.getParameter("api"), url), String.class);
    }

    // final 이 아닌 Map
    public String notFinal(HttpServletRequest request) {
        // ruleid: mois-1-12-ssrf
        return restTemplate.getForObject(mutable.get(request.getParameter("api")), String.class);
    }

    // final 이지만 요청 값을 넣는 Map
    public String filledFromRequest(HttpServletRequest request) {
        registered.put(request.getParameter("api"), request.getParameter("url"));
        // ruleid: mois-1-12-ssrf
        return restTemplate.getForObject(registered.get(request.getParameter("api")), String.class);
    }

    public void register(String name, String url) {
        if (url != null) {
            this.callbacks.putIfAbsent(name, url);
        }
    }

    // 다른 메서드(this.callbacks.putIfAbsent)에서 값을 넣는 Map
    public String filledElsewhere(HttpServletRequest request) {
        // ruleid: mois-1-12-ssrf
        return restTemplate.getForObject(this.callbacks.get(request.getParameter("api")), String.class);
    }

    // 생성자에서 리터럴이 아닌 값을 넣는 Map
    public String filledInConstructor(HttpServletRequest request) {
        // ruleid: mois-1-12-ssrf
        return restTemplate.getForObject(initial.get(request.getParameter("api")), String.class);
    }

    public String filledInConstructorViaThis(HttpServletRequest request) {
        // ruleid: mois-1-12-ssrf
        return restTemplate.getForObject(seeded.get(request.getParameter("api")), String.class);
    }

    // static 블록에서 리터럴이 아닌 값을 넣는 Map
    public String filledInStaticBlock(HttpServletRequest request) {
        // ruleid: mois-1-12-ssrf
        return restTemplate.getForObject(FROM_ENV.get(request.getParameter("api")), String.class);
    }

    // Map 이 아닌 객체의 get(): 무엇을 돌려주는지 알 수 없다
    public String notMap(HttpServletRequest request) {
        // ruleid: mois-1-12-ssrf
        return restTemplate.getForObject(store.get(request.getParameter("api")), String.class);
    }

    // 스킴만 고정
    public String schemeOnly(HttpServletRequest request) {
        // ruleid: mois-1-12-ssrf
        return restTemplate.getForObject("http://" + request.getParameter("host") + "/health", String.class);
    }

    // 호스트 뒤에 / 가 없음: api.example.go.kr.evil.example, api.example.go.kr@evil.example
    public String hostNotTerminated(HttpServletRequest request) {
        // ruleid: mois-1-12-ssrf
        return restTemplate.getForObject("https://api.example.go.kr" + request.getParameter("path"), String.class);
    }

    // 형식 문자열의 호스트 자리에 입력이 들어감
    public String formatHost(HttpServletRequest request) {
        // ruleid: mois-1-12-ssrf
        return restTemplate.getForObject(String.format("https://%s/health", request.getParameter("host")), String.class);
    }

    // 상대 경로처럼 보이는 접두는 서버 쪽 요청에서는 대상을 고정하지 못한다
    public String fixedSuffix(HttpServletRequest request) {
        // ruleid: mois-1-12-ssrf
        return restTemplate.getForObject(request.getParameter("base") + "/api/items", String.class);
    }

    interface EndpointStore {
        String get(String key);
    }
}
