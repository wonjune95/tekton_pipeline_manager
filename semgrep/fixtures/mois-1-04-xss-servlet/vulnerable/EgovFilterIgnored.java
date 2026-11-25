package egovframework.demo;

import java.io.IOException;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import egovframework.com.cmm.EgovWebUtil;

public class EgovFilterIgnored {
    // 필터를 부르기만 하고 결과를 쓰지 않으면 원래 값이 그대로 출력된다
    public void ignored(HttpServletRequest request, HttpServletResponse response) throws IOException {
        String q = request.getParameter("q");
        EgovWebUtil.clearXSSMinimum(q);
        // ruleid: mois-1-04-xss-servlet
        response.getWriter().print(q);
    }
}
