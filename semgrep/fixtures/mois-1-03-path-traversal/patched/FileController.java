package demo;

import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import javax.servlet.http.HttpServletRequest;
import org.apache.commons.io.FilenameUtils;

// 탐지되면 안 되는 경우
public class FileController {
    private static final String BASE = "/data/uploads/";

    // 경로를 떼고 파일 이름만 쓴다
    public byte[] download(HttpServletRequest request) throws IOException {
        // ok: mois-1-03-path-traversal — FilenameUtils.getName 은 디렉터리 부분을 버린다
        String name = FilenameUtils.getName(request.getParameter("file"));
        return Files.readAllBytes(Paths.get(BASE + name));
    }

    public FileInputStream byFileName(HttpServletRequest request) throws IOException {
        // ok: mois-1-03-path-traversal — new File(입력).getName() 은 이름만 꺼낸다
        String name = new File(request.getParameter("file")).getName();
        return new FileInputStream(new File(BASE, name));
    }

    public byte[] byPathFileName(HttpServletRequest request) throws IOException {
        // ok: mois-1-03-path-traversal — Paths.get(입력).getFileName() 은 마지막 요소만 남긴다
        String name = Paths.get(request.getParameter("file")).getFileName().toString();
        return Files.readAllBytes(Paths.get(BASE).resolve(name));
    }

    public byte[] byPathOfFileName(HttpServletRequest request) throws IOException {
        // ok: mois-1-03-path-traversal — Path.of(입력).getFileName()
        String name = Path.of(request.getParameter("file")).getFileName().toString();
        return Files.readAllBytes(Path.of(BASE).resolve(name));
    }

    // 입력값은 선택에만 쓰고 경로는 정해진 값만 쓴다
    public FileInputStream open(HttpServletRequest request) throws IOException {
        String path = "default.pdf";
        if ("report".equals(request.getParameter("path"))) {
            path = "report.pdf";
        }
        // ok: mois-1-03-path-traversal — 경로에 들어가는 값은 모두 상수
        return new FileInputStream(new File(BASE, path));
    }
}
