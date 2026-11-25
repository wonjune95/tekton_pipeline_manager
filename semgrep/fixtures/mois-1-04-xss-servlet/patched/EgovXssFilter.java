package egovframework.demo;

import java.io.IOException;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import egovframework.com.cmm.EgovWebUtil;

// 전자정부 표준프레임워크의 XSS 필터를 거친 값
public class EgovXssFilter {
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

    public void e(HttpServletRequest request, HttpServletResponse response) throws IOException {
        // ok: mois-1-04-xss-servlet — 패키지 전체 이름
        response.getWriter().print(egovframework.com.cmm.EgovWebUtil.clearXSSMinimum(request.getParameter("q")));
        response.getWriter().print(egovframework.com.cmm.EgovWebUtil.clearXSSMaximum(request.getParameter("q")));
        response.getWriter().print(egovframework.com.cmm.EgovWebUtil.clearXSS(request.getParameter("q")));
        response.getWriter().print(egovframework.com.cmm.EgovWebUtil.escapeXml(request.getParameter("q")));
    }
}
