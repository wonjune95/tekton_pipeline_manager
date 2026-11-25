package demo;

import java.util.EnumMap;
import java.util.HashMap;
import java.util.LinkedHashMap;
import java.util.TreeMap;
import java.util.concurrent.ConcurrentHashMap;
import javax.servlet.http.HttpServletRequest;
import org.springframework.web.client.RestTemplate;

// 탐지되면 안 되는 경우: 허용 목록을 Map 인터페이스가 아닌 구현 클래스 타입의 final 필드로 둔 경우
public class ConcreteMapController {
    enum Api { STAT, CODE }

    private static final HashMap<String, String> APIS = new HashMap<>();
    private static final LinkedHashMap<String, String> ORDERED = new LinkedHashMap<>();
    private static final TreeMap<String, String> SORTED = new TreeMap<>();
    private static final EnumMap<Api, String> BY_API = new EnumMap<>(Api.class);
    private static final ConcurrentHashMap<String, String> SHARED = new ConcurrentHashMap<>();
    private final RestTemplate restTemplate = new RestTemplate();

    static {
        APIS.put("stat", "https://stat.example.go.kr/api");
        // 값에 이스케이프가 들어 있어도 리터럴이다
        APIS.put("search", "https://stat.example.go.kr/api/search?q=\"all\"");
        ORDERED.put("stat", "https://stat.example.go.kr/api");
        SORTED.put("stat", "https://stat.example.go.kr/api");
        BY_API.put(Api.STAT, "https://stat.example.go.kr/api");
        SHARED.put("stat", "https://stat.example.go.kr/api");
    }

    public String hashMap(HttpServletRequest request) {
        // ok: mois-1-12-ssrf
        return restTemplate.getForObject(APIS.get(request.getParameter("api")), String.class);
    }

    public String linkedHashMap(HttpServletRequest request) {
        // ok: mois-1-12-ssrf
        return restTemplate.getForObject(ORDERED.get(request.getParameter("api")), String.class);
    }

    public String treeMap(HttpServletRequest request) {
        // ok: mois-1-12-ssrf
        return restTemplate.getForObject(SORTED.get(request.getParameter("api")), String.class);
    }

    public String enumMap(HttpServletRequest request) {
        // ok: mois-1-12-ssrf
        return restTemplate.getForObject(BY_API.get(Api.valueOf(request.getParameter("api"))), String.class);
    }

    public String concurrentHashMap(HttpServletRequest request) {
        // ok: mois-1-12-ssrf
        return restTemplate.getForObject(SHARED.get(request.getParameter("api")), String.class);
    }
}
