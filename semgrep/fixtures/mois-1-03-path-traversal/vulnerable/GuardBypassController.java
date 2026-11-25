package demo;

import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.logging.Logger;
import javax.servlet.http.HttpServletRequest;

// 탐지돼야 하는 경우: 경로 검사가 있어 보이지만 실제로는 막지 못하는 형태
public class GuardBypassController {
    private static final Logger LOG = Logger.getLogger("file");
    private static final String BASE = "/data/uploads";
    private final Path baseDir = Paths.get(BASE).toAbsolutePath().normalize();

    // 구분자 없이 비교: /data/uploads-secret/a 가 /data/uploads 로 시작하므로 통과한다
    public FileInputStream noSeparator(HttpServletRequest request) throws IOException {
        // ruleid: mois-1-03-path-traversal
        File f = new File(BASE, request.getParameter("file"));
        if (!f.getCanonicalPath().startsWith(BASE)) {
            throw new SecurityException("허용되지 않은 경로");
        }
        // ruleid: mois-1-03-path-traversal
        return new FileInputStream(f);
    }

    // 검사에 실패해도 기록만 하고 계속 진행
    public FileInputStream logOnly(HttpServletRequest request) throws IOException {
        // ruleid: mois-1-03-path-traversal
        File f = new File(BASE, request.getParameter("file"));
        if (!f.getCanonicalPath().startsWith(BASE + File.separator)) {
            LOG.warning("허용되지 않은 경로");
        }
        // ruleid: mois-1-03-path-traversal
        return new FileInputStream(f);
    }

    // 검사 결과를 쓰지 않음
    public FileInputStream resultIgnored(HttpServletRequest request) throws IOException {
        // ruleid: mois-1-03-path-traversal
        File f = new File(BASE, request.getParameter("file"));
        f.getCanonicalPath().startsWith(BASE + File.separator);
        // ruleid: mois-1-03-path-traversal
        return new FileInputStream(f);
    }

    // 반대 분기: 기준 디렉터리 아래일 때 중단하고, 벗어났을 때 연다
    public FileInputStream oppositeBranch(HttpServletRequest request) throws IOException {
        // ruleid: mois-1-03-path-traversal
        File f = new File(BASE, request.getParameter("file"));
        if (f.getCanonicalPath().startsWith(BASE + File.separator)) {
            throw new SecurityException("허용되지 않은 경로");
        }
        // ruleid: mois-1-03-path-traversal
        return new FileInputStream(f);
    }

    // 검사한 변수와 쓰는 변수가 다름
    public FileInputStream otherVariable(HttpServletRequest request) throws IOException {
        File checked = new File(BASE, "notice.txt");
        // ruleid: mois-1-03-path-traversal
        File f = new File(BASE, request.getParameter("file"));
        if (!checked.getCanonicalPath().startsWith(BASE + File.separator)) {
            throw new SecurityException("허용되지 않은 경로");
        }
        // ruleid: mois-1-03-path-traversal
        return new FileInputStream(f);
    }

    // 정규화하지 않은 절대 경로 비교: /data/uploads/../../etc/passwd 가 통과한다
    public FileInputStream absoluteNotCanonical(HttpServletRequest request) throws IOException {
        // ruleid: mois-1-03-path-traversal
        File f = new File(BASE, request.getParameter("file"));
        if (!f.getAbsolutePath().startsWith(BASE + File.separator)) {
            throw new SecurityException("허용되지 않은 경로");
        }
        // ruleid: mois-1-03-path-traversal
        return new FileInputStream(f);
    }

    // 정규화한 문자열을 변수에 받았지만 구분자 없이 비교
    public FileInputStream canonicalVariableNoSeparator(HttpServletRequest request) throws IOException {
        // ruleid: mois-1-03-path-traversal
        File f = new File(BASE, request.getParameter("file"));
        String canonical = f.getCanonicalPath();
        if (!canonical.startsWith(BASE)) {
            throw new SecurityException("허용되지 않은 경로");
        }
        // ruleid: mois-1-03-path-traversal
        return new FileInputStream(f);
    }

    // 검사하기 전에 이미 사용
    public void usedBeforeCheck(HttpServletRequest request) throws IOException {
        // ruleid: mois-1-03-path-traversal
        File f = new File(BASE, request.getParameter("file"));
        f.delete();
        if (!f.getCanonicalPath().startsWith(BASE + File.separator)) {
            throw new SecurityException("허용되지 않은 경로");
        }
    }

    // 검사한 File 과 별개로 입력에서 File 을 하나 더 만든다
    public FileInputStream secondFile(HttpServletRequest request) throws IOException {
        File f = new File(BASE, request.getParameter("file"));
        // ruleid: mois-1-03-path-traversal
        File backup = new File(BASE, request.getParameter("backup"));
        if (!f.getCanonicalPath().startsWith(BASE + File.separator)) {
            throw new SecurityException("허용되지 않은 경로");
        }
        // ruleid: mois-1-03-path-traversal
        return new FileInputStream(backup);
    }

    // Path: 검사하기 전에 이미 삭제
    public void pathUsedBeforeCheck(HttpServletRequest request) throws IOException {
        // ruleid: mois-1-03-path-traversal
        Path p = baseDir.resolve(request.getParameter("file")).normalize();
        Files.delete(p);
        if (!p.startsWith(baseDir)) {
            throw new SecurityException("허용되지 않은 경로");
        }
    }

    // Path: 정규화하지 않고 startsWith — /data/uploads/../x 는 요소 단위로 /data/uploads 로 시작한다
    public byte[] pathNotNormalized(HttpServletRequest request) throws IOException {
        // ruleid: mois-1-03-path-traversal
        Path p = baseDir.resolve(request.getParameter("file"));
        if (!p.startsWith(baseDir)) {
            throw new SecurityException("허용되지 않은 경로");
        }
        return Files.readAllBytes(p);
    }

    // Path: 정규화했지만 실패해도 계속 진행
    public byte[] pathLogOnly(HttpServletRequest request) throws IOException {
        // ruleid: mois-1-03-path-traversal
        Path p = baseDir.resolve(request.getParameter("file")).normalize();
        if (!p.startsWith(baseDir)) {
            LOG.warning("허용되지 않은 경로");
        }
        return Files.readAllBytes(p);
    }

    // 문자열을 이어 붙여 구분자까지 비교했지만 정규화하지 않음: /data/uploads/../../etc/passwd
    public FileInputStream stringPrefixOnly(HttpServletRequest request) throws IOException {
        String path = BASE + File.separator + request.getParameter("file");
        if (!path.startsWith(BASE + File.separator)) {
            throw new SecurityException("허용되지 않은 경로");
        }
        // ruleid: mois-1-03-path-traversal
        return new FileInputStream(path);
    }
}
