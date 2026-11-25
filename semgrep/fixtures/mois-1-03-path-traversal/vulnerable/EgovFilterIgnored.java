package egovframework.demo;

import java.io.File;
import java.nio.file.Path;

import javax.servlet.http.HttpServletRequest;

import org.springframework.web.multipart.MultipartFile;

import egovframework.com.cmm.EgovWebUtil;

public class EgovFilterIgnored {
    private static final String STORE = "/data/upload/";

    // 필터를 부르기만 하고 결과를 쓰지 않으면 원래 값이 그대로 간다
    public File ignored(HttpServletRequest request) {
        String name = request.getParameter("name");
        EgovWebUtil.filePathBlackList(name);
        // ruleid: mois-1-03-path-traversal
        return new File(STORE + name);
    }

    // filePathBlackList(값) 은 ".." 만 지운다: 기준 경로 없이 쓰면 /etc/passwd 같은 절대 경로가 그대로 통과한다
    public File wholePathFiltered(HttpServletRequest request) {
        // ruleid: mois-1-03-path-traversal
        return new File(EgovWebUtil.filePathBlackList(request.getParameter("path")));
    }

    public java.io.FileInputStream wholePathOpened(HttpServletRequest request) throws java.io.IOException {
        // ruleid: mois-1-03-path-traversal
        return new java.io.FileInputStream(egovframework.com.cmm.EgovWebUtil.filePathBlackList(request.getParameter("path")));
    }

    public File filteredThenStored(HttpServletRequest request) {
        String path = EgovWebUtil.filePathBlackList(request.getParameter("path"));
        // ruleid: mois-1-03-path-traversal
        return new File(path);
    }

    // 기준 자리에 입력이 오면 뒤에 붙인 값을 걸러도 소용없다
    public File baseFromInput(HttpServletRequest request) {
        // ruleid: mois-1-03-path-traversal
        return new File(request.getParameter("dir") + EgovWebUtil.filePathBlackList(request.getParameter("name")));
    }

    // File 에서 얻은 Path 에 업로드 파일의 원본 이름을 그대로 붙인다
    public Path viaToPath(File dir, MultipartFile upload) {
        // ruleid: mois-1-03-path-traversal
        return dir.toPath().resolve(upload.getOriginalFilename());
    }

    public Path sibling(File current, MultipartFile upload) {
        // ruleid: mois-1-03-path-traversal
        return current.toPath().resolveSibling(upload.getOriginalFilename());
    }

    // 기준 경로를 붙인 변수를 필터 전에 다시 입력으로 바꾸면 인정하지 않는다
    public File prefixedThenReplaced(HttpServletRequest request) {
        String xmlFile = STORE + request.getParameter("id") + ".xml";
        xmlFile = request.getParameter("path");
        // ruleid: mois-1-03-path-traversal
        return new File(EgovWebUtil.filePathBlackList(xmlFile));
    }
}
