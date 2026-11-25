package demo;

import javax.servlet.http.Cookie;
import javax.servlet.http.HttpServletResponse;

// 탐지돼야 하는 경우: 쿠키 만료시간을 하루보다 길게 설정
public class RememberMe {
    private static final int THIRTY_DAYS = 60 * 60 * 24 * 30;

    public void remember(HttpServletResponse response) {
        Cookie loginCookie = new Cookie("rememberme", "YES");
        // ruleid: mois-2-12-persistent-cookie
        loginCookie.setMaxAge(60 * 60 * 24 * 365);
        response.addCookie(loginCookie);
    }

    public void literal(HttpServletResponse response) {
        Cookie c = new Cookie("uid", "1001");
        // ruleid: mois-2-12-persistent-cookie
        c.setMaxAge(31536000);
        response.addCookie(c);
    }

    // 상수로 둔 만료시간
    public void constant(HttpServletResponse response) {
        Cookie c = new Cookie("uid", "1001");
        // ruleid: mois-2-12-persistent-cookie
        c.setMaxAge(THIRTY_DAYS);
        response.addCookie(c);
    }

    // 하루를 1초 넘김 (경계값)
    public void boundary(HttpServletResponse response) {
        Cookie c = new Cookie("uid", "1001");
        // ruleid: mois-2-12-persistent-cookie
        c.setMaxAge(86401);
        response.addCookie(c);
    }

    // 무기한
    public void forever(HttpServletResponse response) {
        Cookie c = new Cookie("uid", "1001");
        // ruleid: mois-2-12-persistent-cookie
        c.setMaxAge(Integer.MAX_VALUE);
        response.addCookie(c);
        Cookie d = new Cookie("sid", "1001");
        // ruleid: mois-2-12-persistent-cookie
        d.setMaxAge(java.lang.Integer.MAX_VALUE);
        response.addCookie(d);
    }
}
