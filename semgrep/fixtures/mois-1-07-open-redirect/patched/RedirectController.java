package demo;

import java.io.IOException;
import java.util.HashMap;
import java.util.Map;
import com.google.common.collect.ImmutableMap;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.servlet.view.RedirectView;

// 탐지되면 안 되는 경우: 허용 목록에서 고르거나, 고정된 주소 뒤에만 붙인다
@Controller
public class RedirectController {
    private static final Map<String, String> ALLOWED = Map.of("main", "/main.do", "login", "/login.jsp");
    private static final Map<String, String> LEGACY = new HashMap<>();
    // 값에 이스케이프가 들어 있어도 리터럴이다
    private static final Map<String, String> SEARCH = Map.of("notice", "/search.do?q=\"notice\"");
    private static final Map<String, String> PORTAL = Map.ofEntries(
            Map.entry("minwon", "https://minwon.example.go.kr/main"),
            Map.entry("help", "/help/index.do"));
    private static final ImmutableMap<String, String> BOARDS = ImmutableMap.of("free", "/board/free.do");
    private final Map<String, String> menus = Map.of("home", "/home.do");
    private final Map<String, String> tabs = new HashMap<>();
    private final Map<String, String> footers = new HashMap<>();

    static {
        LEGACY.put("notice", "/notice/list.do");
        LEGACY.put("faq", "/faq/list.do");
    }

    {
        // 초기화 블록에서 리터럴 값만 넣는다
        footers.put("privacy", "/policy/privacy.do");
        this.footers.put("terms", "/policy/terms.do");
    }

    public RedirectController() {
        // 생성자에서 리터럴 값만 넣는다
        tabs.put("my", "/my/main.do");
        this.tabs.put("cart", "/my/cart.do");
    }

    // 진단가이드 안전한 코드 예처럼 이동할 수 있는 URL 범위를 제한
    public void move(HttpServletRequest request, HttpServletResponse response) throws IOException {
        // ok: mois-1-07-open-redirect — final Map 에서 고르고 기본값은 리터럴
        response.sendRedirect(ALLOWED.getOrDefault(request.getParameter("redirect"), "/main.do"));
    }

    public void moveOrFail(HttpServletRequest request, HttpServletResponse response) throws IOException {
        // ok: mois-1-07-open-redirect — final Map 의 값만 쓴다
        String target = ALLOWED.get(request.getParameter("redirect"));
        if (target == null) {
            response.sendError(HttpServletResponse.SC_BAD_REQUEST);
            return;
        }
        response.sendRedirect(target);
    }

    public void legacy(HttpServletRequest request, HttpServletResponse response) throws IOException {
        // ok: mois-1-07-open-redirect — static 블록에서 리터럴 값만 넣은 final Map
        response.sendRedirect(LEGACY.get(request.getParameter("menu")));
    }

    public void menu(HttpServletRequest request, HttpServletResponse response) throws IOException {
        // ok: mois-1-07-open-redirect — Map.of 로 만든 final Map (this. 접근)
        response.sendRedirect(this.menus.get(request.getParameter("menu")));
    }

    public void menuOrMain(HttpServletRequest request, HttpServletResponse response) throws IOException {
        // ok: mois-1-07-open-redirect
        response.sendRedirect(this.menus.getOrDefault(request.getParameter("menu"), "/main.do"));
    }

    public void search(HttpServletRequest request, HttpServletResponse response) throws IOException {
        // ok: mois-1-07-open-redirect — 이스케이프가 든 리터럴 값
        response.sendRedirect(SEARCH.get(request.getParameter("menu")));
    }

    public void portal(HttpServletRequest request, HttpServletResponse response) throws IOException {
        // ok: mois-1-07-open-redirect — Map.ofEntries(Map.entry("k", "v"), …) 로 만든 final Map
        response.sendRedirect(PORTAL.get(request.getParameter("site")));
    }

    public void board(HttpServletRequest request, HttpServletResponse response) throws IOException {
        // ok: mois-1-07-open-redirect — ImmutableMap.of 로 만든 final Map
        response.sendRedirect(BOARDS.get(request.getParameter("board")));
    }

    public void tab(HttpServletRequest request, HttpServletResponse response) throws IOException {
        // ok: mois-1-07-open-redirect — 빈 Map 으로 만들고 생성자에서 리터럴만 넣은 final Map
        response.sendRedirect(tabs.get(request.getParameter("tab")));
    }

    public void footer(HttpServletRequest request, HttpServletResponse response) throws IOException {
        // ok: mois-1-07-open-redirect — 빈 Map 으로 만들고 초기화 블록에서 리터럴만 넣은 final Map
        response.sendRedirect(footers.get(request.getParameter("link")));
    }

    @GetMapping("/board/list")
    public String list(@RequestParam("page") String page) {
        // ok: mois-1-07-open-redirect — 같은 사이트의 고정 경로 뒤에 붙인다
        return "redirect:/board/list.do?page=" + page;
    }

    @GetMapping("/board/view")
    public RedirectView view(@RequestParam String id, @RequestParam String page) {
        // ok: mois-1-07-open-redirect — 여러 값을 이어 붙여도 맨 앞이 고정 경로
        return new RedirectView("/board/view.do?id=" + id + "&page=" + page);
    }

    public void filtered(HttpServletRequest request, HttpServletResponse response) throws IOException {
        // ok: mois-1-07-open-redirect — 고정 경로 리터럴에 이스케이프(\")가 들어 있어도 리터럴이 닫힌 뒤에 붙인다
        response.sendRedirect("/board/list.do?filter=title eq \"" + request.getParameter("keyword") + "\"");
    }

    public void sso(HttpServletRequest request, HttpServletResponse response) throws IOException {
        // ok: mois-1-07-open-redirect — 스킴과 호스트가 고정되고 / 로 끝난 뒤에 붙인다
        response.sendRedirect("https://sso.example.go.kr/login?returnUrl=" + request.getParameter("returnUrl"));
    }

    public void formatted(HttpServletRequest request, HttpServletResponse response) throws IOException {
        // ok: mois-1-07-open-redirect — 형식 문자열의 앞부분이 고정 경로
        response.sendRedirect(String.format("/board/%s/list.do", request.getParameter("board")));
    }

    public void formattedSso(HttpServletRequest request, HttpServletResponse response) throws IOException {
        // ok: mois-1-07-open-redirect — 형식 문자열의 스킴과 호스트가 고정되고 / 로 끝난 뒤에 넣는다
        response.sendRedirect(String.format("https://sso.example.go.kr/login?returnUrl=%s", request.getParameter("returnUrl")));
    }

    public void paged(HttpServletRequest request, HttpServletResponse response) throws IOException {
        // ok: mois-1-07-open-redirect — 숫자로 바꾼 값은 주소를 바꿀 수 없다
        response.sendRedirect(request.getContextPath() + "?page=" + Integer.parseInt(request.getParameter("page")));
    }

    public void article(HttpServletRequest request, HttpServletResponse response) throws IOException {
        long id = Long.parseLong(request.getParameter("id"));
        // ok: mois-1-07-open-redirect
        response.sendRedirect(request.getContextPath() + "?id=" + id);
    }

    // 진단가이드 오탐 예: 컨텍스트 경로 + 고정 경로
    public void back(HttpServletRequest request, HttpServletResponse response) throws IOException {
        // ok: mois-1-07-open-redirect — 입력이 들어가지 않는다
        response.sendRedirect(request.getContextPath() + "/login.do");
    }
}
