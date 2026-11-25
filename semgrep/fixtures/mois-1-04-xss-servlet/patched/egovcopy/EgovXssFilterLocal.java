package egovframework.demo.cmm;

import java.io.IOException;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

// EgovWebUtil 을 같은 패키지로 옮겨 쓰는 프로젝트 (import 없이 짧은 이름으로 부른다)
public class EgovXssFilterLocal {
    public void a(HttpServletRequest request, HttpServletResponse response) throws IOException {
        // ok: mois-1-04-xss-servlet
        response.getWriter().print(EgovWebUtil.clearXSSMinimum(request.getParameter("q")));
    }

    public void b(HttpServletRequest request, HttpServletResponse response) throws IOException {
        // ok: mois-1-04-xss-servlet
        response.getWriter().print(EgovWebUtil.clearXSSMaximum(request.getParameter("q")));
    }

    public void c(HttpServletRequest request, HttpServletResponse response) throws IOException {
        // ok: mois-1-04-xss-servlet
        response.getWriter().print(EgovWebUtil.clearXSS(request.getParameter("q")));
    }

    public void d(HttpServletRequest request, HttpServletResponse response) throws IOException {
        // ok: mois-1-04-xss-servlet
        response.getWriter().print(EgovWebUtil.escapeXml(request.getParameter("q")));
    }
}
