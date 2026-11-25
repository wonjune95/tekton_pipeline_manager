package egovframework.demo;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import egovframework.com.cmm.EgovWebUtil;

public class EgovFilterIgnored {
    // 필터를 부르기만 하고 결과를 쓰지 않으면 CR·LF 가 그대로 헤더에 들어간다
    public void ignored(HttpServletRequest request, HttpServletResponse response) {
        String trace = request.getParameter("trace");
        EgovWebUtil.removeCRLF(trace);
        // ruleid: mois-1-13-http-response-splitting
        response.setHeader("X-Trace", trace);
    }
}
