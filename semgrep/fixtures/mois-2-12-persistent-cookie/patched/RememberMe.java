package demo;

import javax.servlet.http.Cookie;
import javax.servlet.http.HttpServletResponse;

// 탐지되면 안 되는 경우: 만료시간을 기능에 맞춰 최소(1일 이하)로 설정
public class RememberMe {
    public void remember(HttpServletResponse response) {
        Cookie loginCookie = new Cookie("rememberme", "YES");
        // ok: mois-2-12-persistent-cookie — 1일 (진단가이드 안전한 예, 경계값)
        loginCookie.setMaxAge(60 * 60 * 24);
        response.addCookie(loginCookie);
    }

    public void session(HttpServletResponse response) {
        Cookie c = new Cookie("view", "list");
        // ok: mois-2-12-persistent-cookie — 음수 = 브라우저를 닫으면 사라지는 세션 쿠키
        c.setMaxAge(-1);
        response.addCookie(c);
    }

    public void logout(HttpServletResponse response) {
        Cookie c = new Cookie("rememberme", "");
        // ok: mois-2-12-persistent-cookie — 0 = 즉시 삭제
        c.setMaxAge(0);
        response.addCookie(c);
    }

    public void shortLived(HttpServletResponse response) {
        Cookie c = new Cookie("popup", "hide");
        // ok: mois-2-12-persistent-cookie — 30분
        c.setMaxAge(1800);
        response.addCookie(c);
    }
}
