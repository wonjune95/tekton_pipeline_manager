package egovframework.demo.cmm;

import java.io.File;

import javax.servlet.http.HttpServletRequest;

// EgovWebUtil 을 같은 패키지로 옮겨 쓰는 프로젝트 (import 없이 짧은 이름으로 부른다)
public class EgovFileDownLocal {
    private static final String STORE = "/data/upload/";

    public File a(HttpServletRequest request) {
        // ok: mois-1-03-path-traversal
        return new File(STORE + EgovWebUtil.filePathBlackList(request.getParameter("name")));
    }

    public File prefixedInside(HttpServletRequest request) {
        // ok: mois-1-03-path-traversal — 기준 경로를 붙인 값을 통째로 넘김
        return new File(EgovWebUtil.filePathBlackList(STORE + request.getParameter("name")));
    }

    public File prefixedVariable(HttpServletRequest request) {
        String xmlFile = STORE + request.getParameter("id") + ".xml";
        // ok: mois-1-03-path-traversal
        return new File(EgovWebUtil.filePathBlackList(xmlFile));
    }

    public File withBasePath(HttpServletRequest request) {
        // ok: mois-1-03-path-traversal — 기준 경로를 함께 넘기는 두 인자형
        return new File(EgovWebUtil.filePathBlackList(request.getParameter("name"), STORE));
    }

    public File b(HttpServletRequest request) {
        // ok: mois-1-03-path-traversal
        return new File(STORE + EgovWebUtil.filePathReplaceAll(request.getParameter("name")));
    }

    public File c(HttpServletRequest request) {
        // ok: mois-1-03-path-traversal
        return new File(STORE + EgovWebUtil.fileInjectPathReplaceAll(request.getParameter("name")));
    }
}
