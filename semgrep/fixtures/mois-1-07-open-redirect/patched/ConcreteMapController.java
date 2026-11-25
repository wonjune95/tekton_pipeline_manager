package demo;

import java.io.IOException;
import java.util.EnumMap;
import java.util.HashMap;
import java.util.LinkedHashMap;
import java.util.TreeMap;
import java.util.concurrent.ConcurrentHashMap;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

// 탐지되면 안 되는 경우: 허용 목록을 Map 인터페이스가 아닌 구현 클래스 타입의 final 필드로 둔 경우
public class ConcreteMapController {
    enum Menu { NOTICE, FAQ }

    private static final HashMap<String, String> MENU = new HashMap<>();
    private static final LinkedHashMap<String, String> ORDERED = new LinkedHashMap<>();
    private static final TreeMap<String, String> SORTED = new TreeMap<>();
    private static final EnumMap<Menu, String> BY_MENU = new EnumMap<>(Menu.class);
    private static final ConcurrentHashMap<String, String> SHARED = new ConcurrentHashMap<>();

    static {
        MENU.put("notice", "/notice/list.do");
        // 값에 이스케이프가 들어 있어도 리터럴이다
        MENU.put("search", "/search.do?q=\"notice\"");
        ORDERED.put("notice", "/notice/list.do");
        SORTED.put("notice", "/notice/list.do");
        BY_MENU.put(Menu.NOTICE, "/notice/list.do");
        SHARED.put("notice", "/notice/list.do");
    }

    public void hashMap(HttpServletRequest request, HttpServletResponse response) throws IOException {
        // ok: mois-1-07-open-redirect
        response.sendRedirect(MENU.get(request.getParameter("menu")));
    }

    public void linkedHashMap(HttpServletRequest request, HttpServletResponse response) throws IOException {
        // ok: mois-1-07-open-redirect
        response.sendRedirect(ORDERED.get(request.getParameter("menu")));
    }

    public void treeMap(HttpServletRequest request, HttpServletResponse response) throws IOException {
        // ok: mois-1-07-open-redirect
        response.sendRedirect(SORTED.get(request.getParameter("menu")));
    }

    public void enumMap(HttpServletRequest request, HttpServletResponse response) throws IOException {
        // ok: mois-1-07-open-redirect
        response.sendRedirect(BY_MENU.get(Menu.valueOf(request.getParameter("menu"))));
    }

    public void concurrentHashMap(HttpServletRequest request, HttpServletResponse response) throws IOException {
        // ok: mois-1-07-open-redirect
        response.sendRedirect(SHARED.get(request.getParameter("menu")));
    }
}
