package egovframework.demo;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import egovframework.com.cmm.EgovWebUtil;

// 전자정부 표준프레임워크의 CR·LF 제거 필터를 거친 값만 헤더에 넣는다
public class EgovHeaderController {
    public void download(HttpServletRequest request, HttpServletResponse response) {
        // ok: mois-1-13-http-response-splitting
        response.setHeader("Content-Disposition", "attachment;filename=" + EgovWebUtil.removeCRLF(request.getParameter("file")));
    }

    public void fullName(HttpServletRequest request, HttpServletResponse response) {
        // ok: mois-1-13-http-response-splitting — 패키지 전체 이름으로 부른 경우
        response.setHeader("X-Trace", egovframework.com.cmm.EgovWebUtil.removeCRLF(request.getParameter("trace")));
    }
}
