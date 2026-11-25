package demo;

import java.io.IOException;
import java.util.HashMap;
import java.util.Map;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

// 탐지돼야 하는 경우: 허용 목록·고정 주소처럼 보이지만 실제로는 이동 대상을 입력이 정하는 형태
public class NotAllowListController {
    private static final Map<String, String> ALLOWED = Map.of("main", "/main.do", "login", "/login.jsp");
    private static final Map<String, String> FROM_ENV = new HashMap<>();
    private Map<String, String> mutable = new HashMap<>();
    private final Map<String, String> recent = new HashMap<>();
    private final Map<String, String> history = new HashMap<>();
    private final Map<String, String> initial = new HashMap<>();
    private final Map<String, String> seeded = new HashMap<>();
    private final LinkStore store;

    static {
        FROM_ENV.put("partner", System.getenv("PARTNER_URL"));
    }

    public NotAllowListController(LinkStore store, Map<String, String> seed, String landing) {
        this.store = store;
        initial.put("landing", landing);
        this.seeded.putAll(seed);
    }

    // 기본값이 입력: 목록에 없으면 입력한 주소로 이동한다
    public void defaultFromInput(HttpServletRequest request, HttpServletResponse response) throws IOException {
        String next = request.getParameter("next");
        // ruleid: mois-1-07-open-redirect
        response.sendRedirect(ALLOWED.getOrDefault(request.getParameter("page"), next));
    }

    // final 이 아닌 Map: 다른 코드가 통째로 바꿀 수 있다
    public void notFinal(HttpServletRequest request, HttpServletResponse response) throws IOException {
        // ruleid: mois-1-07-open-redirect
        response.sendRedirect(mutable.get(request.getParameter("page")));
    }

    // final 이지만 요청 값을 넣는 Map
    public void filledFromRequest(HttpServletRequest request, HttpServletResponse response) throws IOException {
        recent.put(request.getParameter("page"), request.getParameter("url"));
        // ruleid: mois-1-07-open-redirect
        response.sendRedirect(recent.get(request.getParameter("page")));
    }

    public void remember(String page, String url) {
        if (url != null) {
            this.history.putIfAbsent(page, url);
        }
    }

    // 다른 메서드(this.history.putIfAbsent)에서 값을 넣는 Map
    public void filledElsewhere(HttpServletRequest request, HttpServletResponse response) throws IOException {
        // ruleid: mois-1-07-open-redirect
        response.sendRedirect(this.history.get(request.getParameter("page")));
    }

    // 생성자에서 리터럴이 아닌 값을 넣는 Map
    public void filledInConstructor(HttpServletRequest request, HttpServletResponse response) throws IOException {
        // ruleid: mois-1-07-open-redirect
        response.sendRedirect(initial.get(request.getParameter("page")));
    }

    public void filledInConstructorViaThis(HttpServletRequest request, HttpServletResponse response) throws IOException {
        // ruleid: mois-1-07-open-redirect
        response.sendRedirect(seeded.get(request.getParameter("page")));
    }

    // static 블록에서 리터럴이 아닌 값을 넣는 Map
    public void filledInStaticBlock(HttpServletRequest request, HttpServletResponse response) throws IOException {
        // ruleid: mois-1-07-open-redirect
        response.sendRedirect(FROM_ENV.get(request.getParameter("page")));
    }

    // Map 이 아닌 객체의 get(): 무엇을 돌려주는지 알 수 없다
    public void notMap(HttpServletRequest request, HttpServletResponse response) throws IOException {
        // ruleid: mois-1-07-open-redirect
        response.sendRedirect(store.get(request.getParameter("page")));
    }

    // "/" 뒤에 바로 입력: //evil.example 이 되어 다른 사이트로 간다
    public void slashOnly(HttpServletRequest request, HttpServletResponse response) throws IOException {
        // ruleid: mois-1-07-open-redirect
        response.sendRedirect("/" + request.getParameter("path"));
    }

    // 스킴만 고정
    public void schemeOnly(HttpServletRequest request, HttpServletResponse response) throws IOException {
        // ruleid: mois-1-07-open-redirect
        response.sendRedirect("https://" + request.getParameter("host") + "/main.do");
    }

    // 호스트 뒤에 / 가 없음: www.example.go.kr.evil.example, www.example.go.kr@evil.example
    public void hostNotTerminated(HttpServletRequest request, HttpServletResponse response) throws IOException {
        // ruleid: mois-1-07-open-redirect
        response.sendRedirect("https://www.example.go.kr" + request.getParameter("path"));
    }

    // 형식 문자열의 호스트 자리에 입력이 들어감
    public void formatHost(HttpServletRequest request, HttpServletResponse response) throws IOException {
        // ruleid: mois-1-07-open-redirect
        response.sendRedirect(String.format("https://%s/main.do", request.getParameter("host")));
    }

    // 리터럴의 호스트 자리를 입력으로 바꿔 넣는다: 식이 "https://…/" 로 시작해도 호스트는 고정이 아니다
    public void hostPlaceholderReplaced(HttpServletRequest request, HttpServletResponse response) throws IOException {
        // ruleid: mois-1-07-open-redirect
        response.sendRedirect("https://SITE.example.go.kr/".replace("SITE.example.go.kr", request.getParameter("site")) + request.getParameter("path"));
    }

    // 이어 붙인 뒤에 호스트 자리를 바꾼다
    public void replacedAfterConcat(HttpServletRequest request, HttpServletResponse response) throws IOException {
        String url = ("https://SITE.example.go.kr/" + "main.do").replace("SITE", request.getParameter("site"));
        // ruleid: mois-1-07-open-redirect
        response.sendRedirect(url);
    }

    // 고정 경로가 앞이 아니라 뒤에 붙음
    public void fixedSuffix(HttpServletRequest request, HttpServletResponse response) throws IOException {
        // ruleid: mois-1-07-open-redirect
        response.sendRedirect(request.getParameter("site") + "/board/list.do");
    }

    interface LinkStore {
        String get(String key);
    }
}
