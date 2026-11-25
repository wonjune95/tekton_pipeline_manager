package demo;

import java.io.IOException;
import java.util.Collections;
import java.util.HashMap;
import java.util.Map;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

// 탐지돼야 하는 경우: final Map 이지만 내용이 리터럴뿐이라고 확인할 수 없다 (값이 밖에서 들어온다)
public class UnprovenMapController {
    private static final Map<String, String> FROM_DB = loadFromDb();
    private static final Map<String, String> MIXED = Map.of("main", "/main.do", "partner", System.getenv("PARTNER_URL"));
    private static final Map<String, String> ENTRIES = Map.ofEntries(Map.entry("partner", System.getenv("PARTNER_URL")));
    private final Map<String, String> targets;
    private final Map<String, String> copied = new HashMap<>(Registry.shared);
    private final Map<String, String> fromConfig = Registry.config.getTargets();
    private final Map<String, String> wrapped = Collections.unmodifiableMap(Registry.shared);
    private final Map<String, String> assignedInBlock;
    private final Map<String, String> filledInBlock = new HashMap<>();
    private final Map<String, String> filledInBlockViaThis = new HashMap<>();
    private final Map<String, String> filledByLambda = new HashMap<>();
    private final Map<String, String> doubleBrace = new HashMap<>() {{
        put("partner", System.getenv("PARTNER_URL"));
    }};

    {
        assignedInBlock = Registry.shared;
    }

    {
        filledInBlock.put("partner", System.getenv("PARTNER_URL"));
    }

    {
        this.filledInBlockViaThis.put("partner", System.getenv("PARTNER_URL"));
    }

    // 생성자 인자를 그대로 받는다: 호출하는 쪽이 무엇을 넣었는지 이 클래스에서는 알 수 없다
    public UnprovenMapController(Map<String, String> supplied) {
        this.targets = supplied;
        supplied.forEach((page, url) -> filledByLambda.put(page, url));
    }

    public void constructorArgument(HttpServletRequest request, HttpServletResponse response) throws IOException {
        // ruleid: mois-1-07-open-redirect
        response.sendRedirect(targets.get(request.getParameter("key")));
    }

    public void constructorArgumentViaThis(HttpServletRequest request, HttpServletResponse response) throws IOException {
        // ruleid: mois-1-07-open-redirect
        response.sendRedirect(this.targets.getOrDefault(request.getParameter("key"), "/main.do"));
    }

    // 메서드가 돌려준 Map
    public void methodResult(HttpServletRequest request, HttpServletResponse response) throws IOException {
        // ruleid: mois-1-07-open-redirect
        response.sendRedirect(FROM_DB.get(request.getParameter("key")));
    }

    public void getterResult(HttpServletRequest request, HttpServletResponse response) throws IOException {
        // ruleid: mois-1-07-open-redirect
        response.sendRedirect(fromConfig.get(request.getParameter("key")));
    }

    // 다른 Map 을 복사하거나 감싼 Map
    public void copyOfOther(HttpServletRequest request, HttpServletResponse response) throws IOException {
        // ruleid: mois-1-07-open-redirect
        response.sendRedirect(copied.get(request.getParameter("key")));
    }

    public void wrapperOfOther(HttpServletRequest request, HttpServletResponse response) throws IOException {
        // ruleid: mois-1-07-open-redirect
        response.sendRedirect(wrapped.get(request.getParameter("key")));
    }

    // Map.of·Map.ofEntries 이지만 값 하나가 리터럴이 아니다
    public void mapOfWithVariable(HttpServletRequest request, HttpServletResponse response) throws IOException {
        // ruleid: mois-1-07-open-redirect
        response.sendRedirect(MIXED.get(request.getParameter("key")));
    }

    public void entriesWithVariable(HttpServletRequest request, HttpServletResponse response) throws IOException {
        // ruleid: mois-1-07-open-redirect
        response.sendRedirect(ENTRIES.get(request.getParameter("key")));
    }

    // 초기화 블록에서 대입하거나 리터럴이 아닌 값을 넣는 Map
    public void assignedInInitializer(HttpServletRequest request, HttpServletResponse response) throws IOException {
        // ruleid: mois-1-07-open-redirect
        response.sendRedirect(assignedInBlock.get(request.getParameter("key")));
    }

    public void filledInInitializer(HttpServletRequest request, HttpServletResponse response) throws IOException {
        // ruleid: mois-1-07-open-redirect
        response.sendRedirect(filledInBlock.get(request.getParameter("key")));
    }

    public void filledInInitializerViaThis(HttpServletRequest request, HttpServletResponse response) throws IOException {
        // ruleid: mois-1-07-open-redirect
        response.sendRedirect(filledInBlockViaThis.get(request.getParameter("key")));
    }

    // 람다 안에서 넣는다
    public void filledByLambda(HttpServletRequest request, HttpServletResponse response) throws IOException {
        // ruleid: mois-1-07-open-redirect
        response.sendRedirect(filledByLambda.get(request.getParameter("key")));
    }

    // 익명 하위 클래스의 초기화 블록에서 넣는다 ({{ put(...) }})
    public void doubleBraceInit(HttpServletRequest request, HttpServletResponse response) throws IOException {
        // ruleid: mois-1-07-open-redirect
        response.sendRedirect(doubleBrace.get(request.getParameter("key")));
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
