package egovframework.demo;

import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStream;

import javax.servlet.http.HttpServletRequest;

import egovframework.com.cmm.EgovWebUtil;

// 전자정부 표준프레임워크의 경로 필터를 거친 값
public class EgovFileDown {
    private static final String STORE = "/data/upload/";

    public InputStream open(HttpServletRequest request) throws IOException {
        // ok: mois-1-03-path-traversal — ".." 를 지운 이름을 기준 디렉터리 뒤에 붙인다
        File f = new File(STORE, EgovWebUtil.filePathBlackList(request.getParameter("name")));
        return new FileInputStream(f);
    }

    public File withBasePath(HttpServletRequest request) {
        // ok: mois-1-03-path-traversal — 기준 경로를 함께 넘기는 두 인자형 (기준 경로 뒤에 붙여 ".." 를 지운다)
        return new File(EgovWebUtil.filePathBlackList(request.getParameter("name"), STORE));
    }

    public File fullNameWithBasePath(HttpServletRequest request) {
        // ok: mois-1-03-path-traversal
        return new File(egovframework.com.cmm.EgovWebUtil.filePathBlackList(request.getParameter("name"), STORE));
    }

    public File replaced(HttpServletRequest request) {
        // ok: mois-1-03-path-traversal
        return new File(STORE + EgovWebUtil.filePathReplaceAll(request.getParameter("name")));
    }

    public File injected(HttpServletRequest request) {
        // ok: mois-1-03-path-traversal
        return new File(STORE + EgovWebUtil.fileInjectPathReplaceAll(request.getParameter("name")));
    }

    public File prefixedInside(HttpServletRequest request) {
        // ok: mois-1-03-path-traversal — 기준 경로를 붙인 값을 통째로 넘김 (전자정부 공통컴포넌트의 흔한 형태)
        return new File(EgovWebUtil.filePathBlackList(STORE + request.getParameter("name") + ".xml"));
    }

    public File fullNamePrefixedInside(HttpServletRequest request) {
        // ok: mois-1-03-path-traversal
        return new File(egovframework.com.cmm.EgovWebUtil.filePathBlackList(STORE + request.getParameter("name")));
    }

    public File prefixedVariable(HttpServletRequest request) {
        String xmlFile = STORE + request.getParameter("id") + ".xml";
        // ok: mois-1-03-path-traversal — 기준 경로를 붙인 값을 변수에 담아 넘김 (공통컴포넌트 메일 첨부·업로드 유틸의 형태)
        return new File(EgovWebUtil.filePathBlackList(xmlFile));
    }

    public File prefixedAssigned(HttpServletRequest request) {
        String fullPath;
        fullPath = STORE + request.getParameter("name") + "_upfile";
        // ok: mois-1-03-path-traversal
        return new File(egovframework.com.cmm.EgovWebUtil.filePathBlackList(fullPath));
    }

    public File fullName(HttpServletRequest request) {
        // ok: mois-1-03-path-traversal — 패키지 전체 이름으로 부른 경우
        return new File(STORE + egovframework.com.cmm.EgovWebUtil.filePathBlackList(request.getParameter("name")));
    }

    public File fullNameReplaced(HttpServletRequest request) {
        // ok: mois-1-03-path-traversal — 패키지 전체 이름으로 부른 filePathReplaceAll
        return new File(STORE + egovframework.com.cmm.EgovWebUtil.filePathReplaceAll(request.getParameter("name")));
    }

    public File fullNameInjected(HttpServletRequest request) {
        // ok: mois-1-03-path-traversal — 패키지 전체 이름으로 부른 fileInjectPathReplaceAll
        return new File(STORE + egovframework.com.cmm.EgovWebUtil.fileInjectPathReplaceAll(request.getParameter("name")));
    }
}
