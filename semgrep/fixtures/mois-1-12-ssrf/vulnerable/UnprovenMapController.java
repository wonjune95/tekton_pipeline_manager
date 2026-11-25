package demo;

import java.io.IOException;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.Collections;
import java.util.HashMap;
import java.util.Map;
import javax.servlet.http.HttpServletRequest;
import org.springframework.web.client.RestTemplate;

// 탐지돼야 하는 경우: final Map 이지만 내용이 리터럴뿐이라고 확인할 수 없다 (값이 밖에서 들어온다)
public class UnprovenMapController {
    private final RestTemplate restTemplate = new RestTemplate();
    private static final Map<String, String> FROM_DB = loadFromDb();
    private static final Map<String, String> MIXED = Map.of("main", "https://stat.example.go.kr/api", "partner", System.getenv("PARTNER_API"));
    private static final Map<String, String> ENTRIES = Map.ofEntries(Map.entry("partner", System.getenv("PARTNER_API")));
    private final Map<String, String> targets;
    private final Map<String, URL> urlMap;
    private final Map<String, String> copied = new HashMap<>(Registry.shared);
    private final Map<String, String> fromConfig = Registry.config.getTargets();
    private final Map<String, String> wrapped = Collections.unmodifiableMap(Registry.shared);
    private final Map<String, String> assignedInBlock;
    private final Map<String, String> filledInBlock = new HashMap<>();
    private final Map<String, String> filledInBlockViaThis = new HashMap<>();
    private final Map<String, String> filledByLambda = new HashMap<>();
    private final Map<String, String> doubleBrace = new HashMap<>() {{
        put("partner", System.getenv("PARTNER_API"));
    }};

    {
        assignedInBlock = Registry.shared;
    }

    {
        filledInBlock.put("partner", System.getenv("PARTNER_API"));
    }

    {
        this.filledInBlockViaThis.put("partner", System.getenv("PARTNER_API"));
    }

    // 생성자 인자를 그대로 받는다: 호출하는 쪽이 무엇을 넣었는지 이 클래스에서는 알 수 없다
    public UnprovenMapController(Map<String, String> supplied, Map<String, URL> urlMap) {
        this.targets = supplied;
        this.urlMap = urlMap;
        supplied.forEach((api, url) -> filledByLambda.put(api, url));
    }

    public String constructorArgument(HttpServletRequest request) {
        // ruleid: mois-1-12-ssrf
        return restTemplate.getForObject(targets.get(request.getParameter("key")), String.class);
    }

    public String constructorArgumentViaThis(HttpServletRequest request) {
        // ruleid: mois-1-12-ssrf
        return restTemplate.getForObject(this.targets.getOrDefault(request.getParameter("key"), "https://stat.example.go.kr/api"), String.class);
    }

    // 진단가이드 안전한 코드 예와 같은 모양이지만 urlMap 을 생성자 인자로 받는다.
    // Map 의 내용을 이 클래스에서 확인할 수 없으므로 탐지한다 (주입하는 쪽이 고정 목록인지는 수동 확인)
    public HttpURLConnection connect(HttpServletRequest req) throws IOException {
        URL url = urlMap.get(req.getParameter("url"));
        // ruleid: mois-1-12-ssrf
        return (HttpURLConnection) url.openConnection();
    }

    // 메서드가 돌려준 Map
    public String methodResult(HttpServletRequest request) {
        // ruleid: mois-1-12-ssrf
        return restTemplate.getForObject(FROM_DB.get(request.getParameter("key")), String.class);
    }

    public String getterResult(HttpServletRequest request) {
        // ruleid: mois-1-12-ssrf
        return restTemplate.getForObject(fromConfig.get(request.getParameter("key")), String.class);
    }

    // 다른 Map 을 복사하거나 감싼 Map
    public String copyOfOther(HttpServletRequest request) {
        // ruleid: mois-1-12-ssrf
        return restTemplate.getForObject(copied.get(request.getParameter("key")), String.class);
    }

    public String wrapperOfOther(HttpServletRequest request) {
        // ruleid: mois-1-12-ssrf
        return restTemplate.getForObject(wrapped.get(request.getParameter("key")), String.class);
    }

    // Map.of·Map.ofEntries 이지만 값 하나가 리터럴이 아니다
    public String mapOfWithVariable(HttpServletRequest request) {
        // ruleid: mois-1-12-ssrf
        return restTemplate.getForObject(MIXED.get(request.getParameter("key")), String.class);
    }

    public String entriesWithVariable(HttpServletRequest request) {
        // ruleid: mois-1-12-ssrf
        return restTemplate.getForObject(ENTRIES.get(request.getParameter("key")), String.class);
    }

    // 초기화 블록에서 대입하거나 리터럴이 아닌 값을 넣는 Map
    public String assignedInInitializer(HttpServletRequest request) {
        // ruleid: mois-1-12-ssrf
        return restTemplate.getForObject(assignedInBlock.get(request.getParameter("key")), String.class);
    }

    public String filledInInitializer(HttpServletRequest request) {
        // ruleid: mois-1-12-ssrf
        return restTemplate.getForObject(filledInBlock.get(request.getParameter("key")), String.class);
    }

    public String filledInInitializerViaThis(HttpServletRequest request) {
        // ruleid: mois-1-12-ssrf
        return restTemplate.getForObject(filledInBlockViaThis.get(request.getParameter("key")), String.class);
    }

    // 람다 안에서 넣는다
    public String filledByLambda(HttpServletRequest request) {
        // ruleid: mois-1-12-ssrf
        return restTemplate.getForObject(filledByLambda.get(request.getParameter("key")), String.class);
    }

    // 익명 하위 클래스의 초기화 블록에서 넣는다 ({{ put(...) }})
    public String doubleBraceInit(HttpServletRequest request) {
        // ruleid: mois-1-12-ssrf
        return restTemplate.getForObject(doubleBrace.get(request.getParameter("key")), String.class);
    }

    static Map<String, String> loadFromDb() {
        return Registry.shared;
    }

    static class Registry {
        static Map<String, String> shared = new HashMap<>();
        static Config config;
    }

    interface Config {
        Map<String, String> getTargets();
    }
}
