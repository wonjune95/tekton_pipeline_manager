package egovframework.demo.cmm;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

// EgovWebUtil 을 같은 패키지로 옮겨 쓰는 프로젝트 (import 없이 짧은 이름으로 부른다)
public class EgovHeaderControllerLocal {
    public void download(HttpServletRequest request, HttpServletResponse response) {
        // ok: mois-1-13-http-response-splitting
        response.setHeader("Content-Disposition", "attachment;filename=" + EgovWebUtil.removeCRLF(request.getParameter("file")));
    }
}
