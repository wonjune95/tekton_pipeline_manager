package demo;

import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import javax.servlet.http.HttpServletRequest;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

// 탐지되면 안 되는 경우: 정규화한 경로가 기준 디렉터리 아래인지 검사하고, 아니면 중단한다
@RestController
public class CanonicalPathController {
    private static final String BASE = "/data/uploads";
    private final File baseFile = new File(BASE);
    private final Path baseDir = Paths.get(BASE).toAbsolutePath().normalize();

    public FileInputStream canonical(HttpServletRequest request) throws IOException {
        // ok: mois-1-03-path-traversal — 아래에서 같은 변수 f 를 검사하고 실패 시 throw
        File f = new File(baseFile, request.getParameter("file"));
        if (!f.getCanonicalPath().startsWith(baseFile.getCanonicalPath() + File.separator)) {
            throw new SecurityException("허용되지 않은 경로");
        }
        // ok: mois-1-03-path-traversal — 검사를 통과한 f
        return new FileInputStream(f);
    }

    public FileInputStream canonicalReturn(HttpServletRequest request) throws IOException {
        File f;
        // ok: mois-1-03-path-traversal — 대입 형태, "/" 를 붙여 비교하고 실패 시 return
        f = new File(BASE, request.getParameter("file"));
        if (f.isDirectory() || !f.getCanonicalPath().startsWith(BASE + "/")) {
            return null;
        }
        // ok: mois-1-03-path-traversal — `조건 || !검사` 형태여도 if 문 뒤의 f 는 검사를 통과한 값
        return new FileInputStream(f);
    }

    public FileInputStream canonicalVariable(HttpServletRequest request) throws IOException {
        // ok: mois-1-03-path-traversal — 정규화한 문자열을 변수에 받아 구분자까지 비교
        File f = new File(BASE, request.getParameter("file"));
        String canonical = f.getCanonicalPath();
        if (!canonical.startsWith(BASE + File.separatorChar)) {
            throw new SecurityException("허용되지 않은 경로");
        }
        return new FileInputStream(f);
    }

    @GetMapping(value = "/files/{name}", produces = "application/octet-stream")
    public byte[] normalized(@PathVariable String name) throws IOException {
        // ok: mois-1-03-path-traversal — normalize() 한 Path 를 Path.startsWith 로 비교
        Path p = baseDir.resolve(name).normalize();
        if (!p.startsWith(baseDir)) {
            throw new SecurityException("허용되지 않은 경로");
        }
        // ok: mois-1-03-path-traversal — 검사를 통과한 p
        return Files.readAllBytes(p.resolveSibling(p.getFileName()));
    }

    public FileInputStream realPath(HttpServletRequest request) throws IOException {
        // ok: mois-1-03-path-traversal — toRealPath() 는 심볼릭 링크까지 풀어 준다
        Path p = Paths.get(BASE, request.getParameter("file")).toRealPath();
        if (!p.startsWith(baseDir)) {
            return null;
        }
        // ok: mois-1-03-path-traversal — 검사를 통과한 p
        return new FileInputStream(p.toFile());
    }

    public byte[] normalizedInCheck(HttpServletRequest request) throws IOException {
        // ok: mois-1-03-path-traversal — 검사식 안에서 정규화
        Path p = baseDir.resolve(request.getParameter("file"));
        if (!p.normalize().startsWith(baseDir)) {
            return new byte[0];
        }
        return Files.readAllBytes(Paths.get(p.toString()));
    }

    public byte[] absoluteNormalizedInCheck(HttpServletRequest request) throws IOException {
        // ok: mois-1-03-path-traversal — toAbsolutePath().normalize() 후 비교
        Path p = Path.of(BASE, request.getParameter("file"));
        if (!p.toAbsolutePath().normalize().startsWith(baseDir)) {
            throw new SecurityException("허용되지 않은 경로");
        }
        try (FileInputStream in = new FileInputStream(p.toFile())) {
            return in.readAllBytes();
        }
    }

    public byte[] realPathInCheck(HttpServletRequest request) throws IOException {
        // ok: mois-1-03-path-traversal — 검사식 안에서 toRealPath()
        Path p = baseDir.resolveSibling(request.getParameter("file"));
        if (!p.toRealPath().startsWith(baseDir)) {
            throw new SecurityException("허용되지 않은 경로");
        }
        return Files.readAllBytes(Paths.get(p.toString()));
    }
}
