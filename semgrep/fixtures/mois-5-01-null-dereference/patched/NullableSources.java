package demo;

import com.google.common.base.Strings;
import java.util.List;
import java.util.Objects;
import javax.servlet.http.HttpServletRequest;
import org.apache.commons.lang3.StringUtils;

// 탐지되면 안 되는 경우: null 이 아님이 확인된 자리에서만 사용
public class NullableSources {

    // ── (1) null 이 아닐 때만 실행되는 분기 ──

    public String thenBranch(HttpServletRequest request, boolean flag) {
        String url = request.getParameter("url");
        // ok: mois-5-01-null-dereference — != null 인 분기 안
        if (url != null) {
            return url.trim();
        }
        String type = request.getHeader("X-Type");
        // ok: mois-5-01-null-dereference — && 로 묶인 검사는 둘 다 참이어야 들어온다
        if (null != type && flag) {
            return type.trim();
        }
        return "";
    }

    // ── (2) == null 의 else ──

    public String elseBranch(HttpServletRequest request, boolean flag) {
        String url = request.getParameter("url");
        String out = "";
        if (url == null) {
            out = "none";
        } else {
            // ok: mois-5-01-null-dereference — == null 의 else
            out = url.trim();
        }
        String type = System.getenv("APP_TYPE");
        if (null == type || flag) {
            out = "none";
        } else {
            // ok: mois-5-01-null-dereference — `null == x || ...` 의 else 는 x 가 null 이 아니다
            out = type.trim();
        }
        return out;
    }

    // ── (3) 단락 평가·조건식 ──

    public boolean shortCircuit(HttpServletRequest request) {
        String a = request.getParameter("a");
        String b = request.getParameter("b");
        String c = request.getParameter("c");
        String d = request.getParameter("d");
        // ok: mois-5-01-null-dereference — 왼쪽 null 검사가 먼저 평가된다
        return (a != null && a.isEmpty()) || (null != b && b.isEmpty())
                || (c == null || c.isEmpty()) || (null == d || d.isEmpty());
    }

    public String ternary(HttpServletRequest request) {
        String a = request.getParameter("a");
        String b = request.getParameter("b");
        String c = request.getParameter("c");
        String d = request.getParameter("d");
        // ok: mois-5-01-null-dereference — null 이 아닌 쪽 갈래에서만 사용
        String r1 = a != null ? a.trim() : "";
        String r2 = null != b ? b.trim() : "";
        String r3 = c == null ? "" : c.trim();
        String r4 = null == d ? "" : d.trim();
        return r1 + r2 + r3 + r4;
    }

    // ── (4) null 이면 중단하거나 기본값을 대입한 if 문 뒤 ──

    public String exitReturn(HttpServletRequest request) {
        String url = request.getParameter("url");
        if (url == null) {
            return "";
        }
        // ok: mois-5-01-null-dereference — null 이면 return
        return url.trim();
    }

    public String exitThrow(HttpServletRequest request) {
        String url = request.getParameter("url");
        if (null == url) {
            throw new IllegalArgumentException("url");
        }
        // ok: mois-5-01-null-dereference — null 이면 throw
        return url.trim();
    }

    public int exitLoop(HttpServletRequest request, List<String> names) {
        int total = 0;
        for (String n : names) {
            String v = request.getParameter(n);
            if (v == null) {
                continue;
            }
            // ok: mois-5-01-null-dereference — null 이면 continue
            total += v.length();
        }
        for (String n : names) {
            String h = request.getHeader(n);
            if (h == null) {
                break;
            }
            // ok: mois-5-01-null-dereference — null 이면 break
            total += h.length();
        }
        return total;
    }

    public String defaultValue(HttpServletRequest request) {
        String url = request.getParameter("url");
        if (url == null) {
            url = "";
        }
        String type = request.getHeader("X-Type");
        if (null == type) type = "none";
        // ok: mois-5-01-null-dereference — null 이면 기본값을 대입
        return url.trim() + type.trim();
    }

    public String exitNoBrace(HttpServletRequest request, List<String> names) {
        int total = 0;
        for (String n : names) {
            String v = request.getParameter(n);
            if (v == null) continue;
            String h = request.getHeader(n);
            if (h == null) break;
            // ok: mois-5-01-null-dereference — 중괄호 없는 continue·break
            total += v.length() + h.length();
        }
        String a = request.getParameter("a");
        if (a == null) return "";
        String b = request.getParameter("b");
        if (b == null) throw new IllegalArgumentException("b");
        // ok: mois-5-01-null-dereference — 중괄호 없는 return·throw
        return a.trim() + b.trim() + total;
    }

    // ok: mois-5-01-null-dereference — 중단하기 전에 다른 문장이 있어도 마지막 문장이 중단이면 같다
    public String exitAfterOtherStatements(HttpServletRequest request, List<String> names) {
        int missing = 0;
        int total = 0;
        for (String n : names) {
            String v = request.getParameter(n);
            if (v == null) {
                missing++;
                continue;
            }
            String h = request.getHeader(n);
            if (h == null) {
                missing++;
                break;
            }
            total += v.length() + h.length();
        }
        String a = request.getParameter("a");
        if (a == null) {
            missing++;
            return "";
        }
        String b = request.getParameter("b");
        if (b == null) {
            missing++;
            throw new IllegalArgumentException("b");
        }
        String c = request.getParameter("c");
        if (c == null) {
            missing++;
            c = "";
        }
        return a.trim() + b.trim() + c.trim() + total + missing;
    }

    // ok: mois-5-01-null-dereference — null 검사와 형식 검사를 || 로 묶은 guard
    public boolean nullOrInvalid(HttpServletRequest request) {
        String name = request.getParameter("name");
        if (name == null || !name.matches("[a-z]{1,20}")) {
            return false;
        }
        return name.startsWith("a");
    }

    public String orExit(HttpServletRequest request, boolean disabled) {
        String url = request.getParameter("url");
        if (url == null || disabled) {
            return "";
        }
        // ok: mois-5-01-null-dereference — || 로 묶인 검사는 null 이면 반드시 중단한다
        return url.trim();
    }

    // ── (5) 문자열 유틸리티 검사 ──

    public String utilExit(HttpServletRequest request) {
        String a = request.getParameter("a");
        if (StringUtils.isEmpty(a)) {
            return "";
        }
        String b = request.getParameter("b");
        if (StringUtils.isBlank(b)) {
            throw new IllegalArgumentException("b");
        }
        String c = request.getParameter("c");
        if (Objects.isNull(c)) {
            return "";
        }
        String d = request.getParameter("d");
        if (Strings.isNullOrEmpty(d)) {
            return "";
        }
        // ok: mois-5-01-null-dereference — 비었으면(null 포함) 중단한 뒤
        return a.trim() + b.trim() + c.trim() + d.trim();
    }

    public int utilExitLoop(HttpServletRequest request, List<String> names) {
        int total = 0;
        for (String n : names) {
            String v = request.getParameter(n);
            if (StringUtils.isEmpty(v)) {
                continue;
            }
            // ok: mois-5-01-null-dereference — 비었으면 continue
            total += v.length();
        }
        for (String n : names) {
            String h = request.getHeader(n);
            if (StringUtils.isEmpty(h)) {
                break;
            }
            // ok: mois-5-01-null-dereference — 비었으면 break
            total += h.length();
        }
        return total;
    }

    public String utilNegatedExit(HttpServletRequest request) {
        String a = request.getParameter("a");
        if (!org.springframework.util.StringUtils.hasText(a)) {
            return "";
        }
        String b = request.getParameter("b");
        if (!org.springframework.util.StringUtils.hasLength(b)) {
            return "";
        }
        String c = request.getParameter("c");
        if (!StringUtils.isNotEmpty(c)) {
            return "";
        }
        String d = request.getParameter("d");
        if (!StringUtils.isNotBlank(d)) {
            return "";
        }
        String e = request.getParameter("e");
        if (!Objects.nonNull(e)) {
            return "";
        }
        // ok: mois-5-01-null-dereference — 값이 없으면 중단한 뒤
        return a.trim() + b.trim() + c.trim() + d.trim() + e.trim();
    }

    public String utilThenBranch(HttpServletRequest request) {
        StringBuilder sb = new StringBuilder();
        String a = request.getParameter("a");
        // ok: mois-5-01-null-dereference — 값이 있을 때만 실행되는 분기
        if (org.springframework.util.StringUtils.hasText(a)) {
            sb.append(a.trim());
        }
        String b = request.getParameter("b");
        if (org.springframework.util.StringUtils.hasLength(b)) {
            sb.append(b.trim());
        }
        String c = request.getParameter("c");
        if (StringUtils.isNotEmpty(c)) {
            sb.append(c.trim());
        }
        String d = request.getParameter("d");
        if (StringUtils.isNotBlank(d)) {
            sb.append(d.trim());
        }
        String e = request.getParameter("e");
        if (Objects.nonNull(e)) {
            sb.append(e.trim());
        }
        return sb.toString();
    }

    public String utilNegatedThenBranch(HttpServletRequest request) {
        StringBuilder sb = new StringBuilder();
        String a = request.getParameter("a");
        // ok: mois-5-01-null-dereference — 비어 있지 않을 때만 실행되는 분기
        if (!StringUtils.isEmpty(a)) {
            sb.append(a.trim());
        }
        String b = request.getParameter("b");
        if (!StringUtils.isBlank(b)) {
            sb.append(b.trim());
        }
        String c = request.getParameter("c");
        if (!Objects.isNull(c)) {
            sb.append(c.trim());
        }
        String d = request.getParameter("d");
        if (!Strings.isNullOrEmpty(d)) {
            sb.append(d.trim());
        }
        return sb.toString();
    }

    // ── (6) null 이면 예외를 던지는 검사 ──

    public String required(HttpServletRequest request) {
        String url = request.getParameter("url");
        Objects.requireNonNull(url, "url");
        // ok: mois-5-01-null-dereference — requireNonNull 뒤
        return url.trim();
    }

    // ── 값을 받은 뒤 다른 값으로 다시 대입 ──

    // 값이 있음을 확인하는 검사가 다른 조건과 && 로만 묶여 있다 (검사식을 감싸는 식이 && 뿐이다)
    public String insideHasTextAnd(HttpServletRequest request, boolean enabled) {
        String url = request.getParameter("url");
        if (enabled && StringUtils.isNotBlank(url)) {
            // ok: mois-5-01-null-dereference — 두 조건이 모두 참일 때만 들어온다
            return url.trim();
        }
        return "";
    }

    public String reassigned(HttpServletRequest request) {
        String url = request.getParameter("url");
        url = Objects.toString(url, "");
        String home = System.getenv("APP_HOME");
        home = home == null ? "/" : home;
        String tmp = System.getProperty("java.io.tmpdir");
        tmp = Objects.toString(tmp, "/tmp");
        // ok: mois-5-01-null-dereference — null 이 아닌 값으로 다시 대입한 뒤
        return url.trim() + home.trim() + tmp.trim();
    }
}
