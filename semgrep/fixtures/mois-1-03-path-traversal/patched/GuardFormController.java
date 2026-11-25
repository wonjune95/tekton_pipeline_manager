package demo;

import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.logging.Logger;
import javax.servlet.http.HttpServletRequest;

// 탐지되면 안 되는 경우: 경로 검사 guard 의 형태별(검사식 3가지 × 중단 방식 4가지) 예제.
// 만드는 줄(new File·resolve)은 뒤따르는 guard 때문에 제외되고, guard 뒤의 사용은 검증된 값으로 본다.
public class GuardFormController {
    private static final Logger LOG = Logger.getLogger("file");
    private static final String BASE = "/data/uploads";
    private final Path baseDir = Paths.get(BASE).toAbsolutePath().normalize();

    // ── File 을 검사식 안에서 정규화 ──

    public FileInputStream fileReturnBlock(HttpServletRequest request) throws IOException {
        // ok: mois-1-03-path-traversal — 블록 안 return
        File f = new File(BASE, request.getParameter("file"));
        if (!f.getCanonicalPath().startsWith(BASE + File.separator)) {
            LOG.warning("기준 디렉터리 밖의 경로 요청");
            return null;
        }
        return new FileInputStream(f);
    }

    public FileInputStream fileThrowBlock(HttpServletRequest request) throws IOException {
        // ok: mois-1-03-path-traversal — 블록 안 throw
        File f = new File(BASE, request.getParameter("file"));
        if (!f.getCanonicalPath().startsWith(BASE + File.separator)) {
            LOG.warning("기준 디렉터리 밖의 경로 요청");
            throw new SecurityException("허용되지 않은 경로");
        }
        return new FileInputStream(f);
    }

    public FileInputStream fileBareReturn(HttpServletRequest request) throws IOException {
        // ok: mois-1-03-path-traversal — 중괄호 없는 return
        File f = new File(BASE, request.getParameter("file"));
        if (!f.getCanonicalPath().startsWith(BASE + File.separator)) return null;
        return new FileInputStream(f);
    }

    public FileInputStream fileBareThrow(HttpServletRequest request) throws IOException {
        // ok: mois-1-03-path-traversal — 중괄호 없는 throw
        File f = new File(BASE, request.getParameter("file"));
        if (!f.getCanonicalPath().startsWith(BASE + File.separator)) throw new SecurityException("허용되지 않은 경로");
        return new FileInputStream(f);
    }

    public FileInputStream fileWithOtherCheck(HttpServletRequest request) throws IOException {
        // ok: mois-1-03-path-traversal — 다른 검사와 || 로 묶여도 실패하면 모두 중단한다
        File f = new File(BASE, request.getParameter("file"));
        if (f.isHidden() || !f.getCanonicalPath().startsWith(BASE + File.separator)) {
            throw new SecurityException("허용되지 않은 경로");
        }
        return new FileInputStream(f);
    }

    // ── 정규화한 문자열을 변수에 받아 비교 ──

    public FileInputStream canonicalReturnBlock(HttpServletRequest request) throws IOException {
        // ok: mois-1-03-path-traversal — 블록 안 return
        File f = new File(BASE, request.getParameter("file"));
        String canonical = f.getCanonicalPath();
        if (!canonical.startsWith(BASE + File.separator)) {
            LOG.warning("기준 디렉터리 밖의 경로 요청");
            return null;
        }
        return new FileInputStream(f);
    }

    public FileInputStream canonicalThrowBlock(HttpServletRequest request) throws IOException {
        // ok: mois-1-03-path-traversal — 블록 안 throw
        File f = new File(BASE, request.getParameter("file"));
        String canonical = f.getCanonicalPath();
        if (!canonical.startsWith(BASE + File.separator)) {
            LOG.warning("기준 디렉터리 밖의 경로 요청");
            throw new SecurityException("허용되지 않은 경로");
        }
        return new FileInputStream(f);
    }

    public FileInputStream canonicalBareReturn(HttpServletRequest request) throws IOException {
        // ok: mois-1-03-path-traversal — 중괄호 없는 return
        File f = new File(BASE, request.getParameter("file"));
        String canonical = f.getCanonicalPath();
        if (!canonical.startsWith(BASE + File.separator)) return null;
        return new FileInputStream(f);
    }

    public FileInputStream canonicalBareThrow(HttpServletRequest request) throws IOException {
        // ok: mois-1-03-path-traversal — 중괄호 없는 throw
        File f = new File(BASE, request.getParameter("file"));
        String canonical = f.getCanonicalPath();
        if (!canonical.startsWith(BASE + File.separator)) throw new SecurityException("허용되지 않은 경로");
        return new FileInputStream(f);
    }

    public FileInputStream canonicalWithOtherCheck(HttpServletRequest request) throws IOException {
        // ok: mois-1-03-path-traversal — 다른 검사와 || 로 묶여도 실패하면 모두 중단한다
        File f = new File(BASE, request.getParameter("file"));
        String canonical = f.getCanonicalPath();
        if (canonical.isEmpty() || !canonical.startsWith(BASE + File.separator)) {
            throw new SecurityException("허용되지 않은 경로");
        }
        return new FileInputStream(f);
    }

    // ── 정규화해 둔 Path 를 Path.startsWith 로 비교 ──

    public FileInputStream pathReturnBlock(HttpServletRequest request) throws IOException {
        // ok: mois-1-03-path-traversal — 블록 안 return
        Path p = baseDir.resolve(request.getParameter("file")).normalize();
        if (!p.startsWith(baseDir)) {
            LOG.warning("기준 디렉터리 밖의 경로 요청");
            return null;
        }
        return new FileInputStream(p.toFile());
    }

    public FileInputStream pathThrowBlock(HttpServletRequest request) throws IOException {
        // ok: mois-1-03-path-traversal — 블록 안 throw
        Path p = baseDir.resolve(request.getParameter("file")).normalize();
        if (!p.startsWith(baseDir)) {
            LOG.warning("기준 디렉터리 밖의 경로 요청");
            throw new SecurityException("허용되지 않은 경로");
        }
        return new FileInputStream(p.toFile());
    }

    public FileInputStream pathBareReturn(HttpServletRequest request) throws IOException {
        // ok: mois-1-03-path-traversal — 중괄호 없는 return
        Path p = baseDir.resolve(request.getParameter("file")).normalize();
        if (!p.startsWith(baseDir)) return null;
        return new FileInputStream(p.toFile());
    }

    public FileInputStream pathBareThrow(HttpServletRequest request) throws IOException {
        // ok: mois-1-03-path-traversal — 중괄호 없는 throw
        Path p = baseDir.resolve(request.getParameter("file")).normalize();
        if (!p.startsWith(baseDir)) throw new SecurityException("허용되지 않은 경로");
        return new FileInputStream(p.toFile());
    }

    public FileInputStream pathWithOtherCheck(HttpServletRequest request) throws IOException {
        // ok: mois-1-03-path-traversal — 다른 검사와 || 로 묶여도 실패하면 모두 중단한다
        Path p = baseDir.resolve(request.getParameter("file")).normalize();
        if (p.getFileName() == null || !p.startsWith(baseDir)) {
            throw new SecurityException("허용되지 않은 경로");
        }
        return new FileInputStream(p.toFile());
    }
}
