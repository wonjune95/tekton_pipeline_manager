package demo;

import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.nio.file.Path;
import java.nio.file.Paths;
import javax.servlet.http.HttpServletRequest;

// 탐지돼야 하는 경우: 경로 검사가 다른 식에 묶여 있어 "검사 실패 = 중단" 이 성립하지 않는다
// (만드는 줄과 쓰는 줄이 모두 탐지된다: 인정되지 않는 guard 는 sink 제외에도 쓰이지 않는다)
public class GuardOperatorBypass {
    private static final String BASE = "/data/upload";
    private final Path baseDir = Paths.get(BASE);

    // & 는 && 와 같은 뜻이다: strict 가 false 면 기준 디렉터리 밖이어도 계속 진행한다
    public FileInputStream fileBitwiseAnd(HttpServletRequest request, boolean strict) throws IOException {
        // ruleid: mois-1-03-path-traversal
        File f = new File(BASE, request.getParameter("file"));
        if (!f.getCanonicalPath().startsWith(BASE + File.separator) & strict) {
            throw new SecurityException("허용되지 않은 경로");
        }
        // ruleid: mois-1-03-path-traversal
        return new FileInputStream(f);
    }

    public FileInputStream canonicalBitwiseAnd(HttpServletRequest request, boolean strict) throws IOException {
        // ruleid: mois-1-03-path-traversal
        File f = new File(BASE, request.getParameter("file"));
        String canonical = f.getCanonicalPath();
        if (!canonical.startsWith(BASE + File.separator) & strict) {
            throw new SecurityException("허용되지 않은 경로");
        }
        // ruleid: mois-1-03-path-traversal
        return new FileInputStream(f);
    }

    public FileInputStream pathBitwiseAnd(HttpServletRequest request, boolean strict) throws IOException {
        // ruleid: mois-1-03-path-traversal
        Path p = baseDir.resolve(request.getParameter("file")).normalize();
        if (!p.startsWith(baseDir) & strict) {
            throw new SecurityException("허용되지 않은 경로");
        }
        // ruleid: mois-1-03-path-traversal
        return new FileInputStream(p.toFile());
    }

    // 조건 연산자: strict 가 false 면 검사하지 않는다
    public FileInputStream fileTernary(HttpServletRequest request, boolean strict) throws IOException {
        // ruleid: mois-1-03-path-traversal
        File f = new File(BASE, request.getParameter("file"));
        if (strict ? !f.getCanonicalPath().startsWith(BASE + File.separator) : false) {
            throw new SecurityException("허용되지 않은 경로");
        }
        // ruleid: mois-1-03-path-traversal
        return new FileInputStream(f);
    }

    // ^ : legacy 가 true 면 기준 디렉터리 "안"일 때 중단하고 밖이면 계속 진행한다
    public FileInputStream canonicalXor(HttpServletRequest request, boolean legacy) throws IOException {
        // ruleid: mois-1-03-path-traversal
        File f = new File(BASE, request.getParameter("file"));
        String canonical = f.getCanonicalPath();
        if (!canonical.startsWith(BASE + File.separator) ^ legacy) {
            throw new SecurityException("허용되지 않은 경로");
        }
        // ruleid: mois-1-03-path-traversal
        return new FileInputStream(f);
    }

    // 전체를 다시 부정: 기준 디렉터리 안이면 중단하고, 밖이면 계속 진행한다
    public FileInputStream pathNegatedWhole(HttpServletRequest request) throws IOException {
        // ruleid: mois-1-03-path-traversal
        Path p = baseDir.resolve(request.getParameter("file")).normalize();
        if (!(p == null || !p.startsWith(baseDir))) {
            throw new SecurityException("허용되지 않은 경로");
        }
        // ruleid: mois-1-03-path-traversal
        return new FileInputStream(p.toFile());
    }

    public FileInputStream fileComparedWithFalse(HttpServletRequest request) throws IOException {
        // ruleid: mois-1-03-path-traversal
        File f = new File(BASE, request.getParameter("file"));
        if (!f.getCanonicalPath().startsWith(BASE + File.separator) == false) {
            throw new SecurityException("허용되지 않은 경로");
        }
        // ruleid: mois-1-03-path-traversal
        return new FileInputStream(f);
    }

    // 검사 결과를 다른 호출의 인자로 넘긴다: 조건의 참·거짓은 그 호출이 정한다
    public FileInputStream pathPassedToCall(HttpServletRequest request) throws IOException {
        // ruleid: mois-1-03-path-traversal
        Path p = baseDir.resolve(request.getParameter("file")).normalize();
        if (Boolean.FALSE.equals(!p.startsWith(baseDir))) {
            throw new SecurityException("허용되지 않은 경로");
        }
        // ruleid: mois-1-03-path-traversal
        return new FileInputStream(p.toFile());
    }
}
