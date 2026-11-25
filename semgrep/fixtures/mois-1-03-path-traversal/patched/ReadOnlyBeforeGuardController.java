package demo;

import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.logging.Logger;
import javax.servlet.http.HttpServletRequest;

// 탐지되면 안 되는 경우: guard 앞에서 경로를 "읽기만" 하는 호출(이름·부모·존재 여부 조회, 정규화)은 사용으로 보지 않는다.
// 구분자를 "/"·'/' 리터럴로 붙인 접두 비교도 File.separator 와 같이 인정한다.
public class ReadOnlyBeforeGuardController {
    private static final Logger LOG = Logger.getLogger("file");
    private static final String BASE = "/data/uploads";
    private final Path baseDir = Paths.get(BASE).toAbsolutePath().normalize();

    public FileInputStream named(HttpServletRequest request) throws IOException {
        // ok: mois-1-03-path-traversal — 검사 전에 이름·경로를 기록만 한다 (구분자는 '/')
        File f = new File(BASE, request.getParameter("file"));
        String shown = f.toString();
        LOG.fine("요청 파일 " + f.getName() + ": " + f.getPath() + " = " + f.getAbsolutePath());
        if (!f.getCanonicalPath().startsWith(BASE + '/')) {
            throw new SecurityException("허용되지 않은 경로: " + shown.length());
        }
        return new FileInputStream(f);
    }

    public FileInputStream parents(HttpServletRequest request) throws IOException {
        // ok: mois-1-03-path-traversal — 부모·절대 경로 객체를 얻기만 한다 (구분자는 "/")
        File f = new File(BASE, request.getParameter("file"));
        File parent = f.getParentFile();
        String parentName = f.getParent();
        File absolute = f.getAbsoluteFile();
        File resolved = f.getCanonicalFile();
        Path asPath = f.toPath();
        boolean rooted = f.isAbsolute();
        String canonical = f.getCanonicalPath();
        if (!canonical.startsWith(BASE + "/")) {
            throw new SecurityException("허용되지 않은 경로");
        }
        return new FileInputStream(f);
    }

    public FileInputStream existing(HttpServletRequest request) throws IOException {
        // ok: mois-1-03-path-traversal — 존재 여부·종류를 조회만 한다 (구분자는 '/')
        File f = new File(BASE, request.getParameter("file"));
        boolean regular = f.exists() && f.isFile() && !f.isDirectory();
        String canonical = f.getCanonicalPath();
        if (!regular || !canonical.startsWith(BASE + '/')) {
            return null;
        }
        return new FileInputStream(f);
    }

    public Path normalized(HttpServletRequest request) throws IOException {
        // ok: mois-1-03-path-traversal — Path 의 이름·절대 경로·정규화 결과를 얻기만 한다
        Path p = baseDir.resolve(request.getParameter("file")).normalize();
        Path leaf = p.getFileName();
        Path absolute = p.toAbsolutePath();
        Path again = p.normalize();
        Path real = p.toRealPath();
        File asFile = p.toFile();
        boolean inside = p.startsWith(baseDir);
        if (!p.startsWith(baseDir)) {
            throw new SecurityException("허용되지 않은 경로");
        }
        return p;
    }
}
