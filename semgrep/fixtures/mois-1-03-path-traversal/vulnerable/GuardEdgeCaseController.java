package demo;

import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.logging.Logger;
import javax.servlet.http.HttpServletRequest;

// 탐지돼야 하는 경우: 올바른 경로 검사식을 썼지만 guard 로 동작하지 않는 형태 (docs/rule-conventions.md §1 v2)
public class GuardEdgeCaseController {
    private static final Logger LOG = Logger.getLogger("file");
    private static final String BASE = "/data/uploads";
    private final Path baseDir = Paths.get(BASE).toAbsolutePath().normalize();

    // ── File 을 검사식 안에서 정규화 ──

    // 실패 분기 안에서 사용: 검사에 걸린 경로를 그대로 연다
    public FileInputStream fileUsedInFailingBranch(HttpServletRequest request) throws IOException {
        File f = new File(BASE, request.getParameter("file"));
        if (!f.getCanonicalPath().startsWith(BASE + File.separator)) {
            LOG.warning("기준 디렉터리 밖의 경로");
            // ruleid: mois-1-03-path-traversal
            return new FileInputStream(f);
        }
        return null;
    }

    // 안쪽 조건부 throw: strict 가 아니면 검사에 걸려도 계속 진행한다
    public FileInputStream fileNestedConditionalExit(HttpServletRequest request, boolean strict) throws IOException {
        // ruleid: mois-1-03-path-traversal
        File f = new File(BASE, request.getParameter("file"));
        if (!f.getCanonicalPath().startsWith(BASE + File.separator)) {
            if (strict) {
                throw new SecurityException("허용되지 않은 경로");
            }
        }
        // ruleid: mois-1-03-path-traversal
        return new FileInputStream(f);
    }

    // && 로 다른 조건에 묶임: strict 가 아니면 검사하지 않는다
    public FileInputStream fileJoinedWithAnd(HttpServletRequest request, boolean strict) throws IOException {
        // ruleid: mois-1-03-path-traversal
        File f = new File(BASE, request.getParameter("file"));
        if (strict && !f.getCanonicalPath().startsWith(BASE + File.separator)) {
            throw new SecurityException("허용되지 않은 경로");
        }
        // ruleid: mois-1-03-path-traversal
        return new FileInputStream(f);
    }

    // 검사 뒤에 다시 대입: 검사한 값이 아니다
    public FileInputStream fileReassignedAfterCheck(HttpServletRequest request) throws IOException {
        File f = new File(BASE, request.getParameter("file"));
        if (!f.getCanonicalPath().startsWith(BASE + File.separator)) {
            throw new SecurityException("허용되지 않은 경로");
        }
        // ruleid: mois-1-03-path-traversal
        f = new File(BASE, request.getParameter("other"));
        // ruleid: mois-1-03-path-traversal
        return new FileInputStream(f);
    }

    // ── 정규화한 문자열을 변수에 받아 비교 ──

    // 실패 분기 안에서 사용: 검사에 걸린 경로를 그대로 연다
    public FileInputStream canonicalUsedInFailingBranch(HttpServletRequest request) throws IOException {
        File f = new File(BASE, request.getParameter("file"));
        String canonical = f.getCanonicalPath();
        if (!canonical.startsWith(BASE + File.separator)) {
            LOG.warning("기준 디렉터리 밖의 경로");
            // ruleid: mois-1-03-path-traversal
            return new FileInputStream(f);
        }
        return null;
    }

    // 안쪽 조건부 throw: strict 가 아니면 검사에 걸려도 계속 진행한다
    public FileInputStream canonicalNestedConditionalExit(HttpServletRequest request, boolean strict) throws IOException {
        // ruleid: mois-1-03-path-traversal
        File f = new File(BASE, request.getParameter("file"));
        String canonical = f.getCanonicalPath();
        if (!canonical.startsWith(BASE + File.separator)) {
            if (strict) {
                throw new SecurityException("허용되지 않은 경로");
            }
        }
        // ruleid: mois-1-03-path-traversal
        return new FileInputStream(f);
    }

    // && 로 다른 조건에 묶임: strict 가 아니면 검사하지 않는다
    public FileInputStream canonicalJoinedWithAnd(HttpServletRequest request, boolean strict) throws IOException {
        // ruleid: mois-1-03-path-traversal
        File f = new File(BASE, request.getParameter("file"));
        String canonical = f.getCanonicalPath();
        if (strict && !canonical.startsWith(BASE + File.separator)) {
            throw new SecurityException("허용되지 않은 경로");
        }
        // ruleid: mois-1-03-path-traversal
        return new FileInputStream(f);
    }

    // 검사 뒤에 다시 대입: 검사한 값이 아니다
    public FileInputStream canonicalReassignedAfterCheck(HttpServletRequest request) throws IOException {
        File f = new File(BASE, request.getParameter("file"));
        String canonical = f.getCanonicalPath();
        if (!canonical.startsWith(BASE + File.separator)) {
            throw new SecurityException("허용되지 않은 경로");
        }
        // ruleid: mois-1-03-path-traversal
        f = new File(BASE, request.getParameter("other"));
        // ruleid: mois-1-03-path-traversal
        return new FileInputStream(f);
    }

    // ── 정규화해 둔 Path 를 Path.startsWith 로 비교 ──

    // 실패 분기 안에서 사용: 검사에 걸린 경로를 그대로 연다
    public FileInputStream pathUsedInFailingBranch(HttpServletRequest request) throws IOException {
        Path p = baseDir.resolve(request.getParameter("file")).normalize();
        if (!p.startsWith(baseDir)) {
            LOG.warning("기준 디렉터리 밖의 경로");
            // ruleid: mois-1-03-path-traversal
            return new FileInputStream(p.toFile());
        }
        return null;
    }

    // 안쪽 조건부 throw: strict 가 아니면 검사에 걸려도 계속 진행한다
    public FileInputStream pathNestedConditionalExit(HttpServletRequest request, boolean strict) throws IOException {
        // ruleid: mois-1-03-path-traversal
        Path p = baseDir.resolve(request.getParameter("file")).normalize();
        if (!p.startsWith(baseDir)) {
            if (strict) {
                throw new SecurityException("허용되지 않은 경로");
            }
        }
        // ruleid: mois-1-03-path-traversal
        return new FileInputStream(p.toFile());
    }

    // && 로 다른 조건에 묶임: strict 가 아니면 검사하지 않는다
    public FileInputStream pathJoinedWithAnd(HttpServletRequest request, boolean strict) throws IOException {
        // ruleid: mois-1-03-path-traversal
        Path p = baseDir.resolve(request.getParameter("file")).normalize();
        if (strict && !p.startsWith(baseDir)) {
            throw new SecurityException("허용되지 않은 경로");
        }
        // ruleid: mois-1-03-path-traversal
        return new FileInputStream(p.toFile());
    }

    // 검사 뒤에 다시 대입: 검사한 값이 아니다
    public FileInputStream pathReassignedAfterCheck(HttpServletRequest request) throws IOException {
        Path p = baseDir.resolve(request.getParameter("file")).normalize();
        if (!p.startsWith(baseDir)) {
            throw new SecurityException("허용되지 않은 경로");
        }
        // ruleid: mois-1-03-path-traversal
        p = baseDir.resolve(request.getParameter("other"));
        // ruleid: mois-1-03-path-traversal
        return new FileInputStream(p.toFile());
    }
}
