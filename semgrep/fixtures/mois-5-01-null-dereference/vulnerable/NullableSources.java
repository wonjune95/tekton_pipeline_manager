package demo;

import java.util.List;
import java.util.Objects;
import javax.servlet.http.HttpServletRequest;
import org.apache.commons.lang3.StringUtils;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

// 탐지돼야 하는 경우: null 을 돌려줄 수 있는 값(요청 파라미터·헤더, 시스템 속성·환경변수)을 검사 없이,
// 또는 "검사처럼 보이지만 null 을 막지 못하는" 코드 뒤에서 사용
public class NullableSources {
    private static final Logger LOG = LoggerFactory.getLogger(NullableSources.class);

    // ── null 을 돌려줄 수 있는 값 4종 ──

    public String header(HttpServletRequest request) {
        String agent = request.getHeader("User-Agent");
        // ruleid: mois-5-01-null-dereference
        return agent.toLowerCase();
    }

    public String env() {
        String home = System.getenv("APP_HOME");
        // ruleid: mois-5-01-null-dereference
        return home.trim();
    }

    // 형식 검사(matches)도 null 이면 NullPointerException 이다 — null 검사가 먼저 있어야 한다
    public boolean validName(HttpServletRequest request) {
        String name = request.getParameter("name");
        // ruleid: mois-5-01-null-dereference
        if (!name.matches("[a-zA-Z0-9]{1,20}")) {
            return false;
        }
        return true;
    }

    // ── 검사처럼 보이지만 null 을 막지 못하는 경우 ──

    // null 이어도 기록만 하고 계속 진행한다
    public String logOnly(HttpServletRequest request) {
        String url = request.getParameter("url");
        if (url == null) {
            LOG.warn("url 없음");
        }
        // ruleid: mois-5-01-null-dereference
        return url.trim();
    }

    // 다른 변수를 검사했다
    public String otherVariable(HttpServletRequest request) {
        String url = request.getParameter("url");
        String type = request.getParameter("type");
        if (type == null) {
            return "";
        }
        // ruleid: mois-5-01-null-dereference
        return url.trim();
    }

    // 다른 변수를 검사했다: 예외로 중단 / 분기 안에서 사용 / 유틸리티 검사 / ?: · && 
    public String otherVariableForms(HttpServletRequest request, List<String> out) {
        String url = request.getParameter("url");
        String type = request.getParameter("type");
        if (type == null) {
            throw new IllegalArgumentException("type");
        }
        // ruleid: mois-5-01-null-dereference
        out.add(url.trim());
        if (type != null) {
            // ruleid: mois-5-01-null-dereference
            out.add(url.strip());
        }
        if (StringUtils.isNotBlank(type)) {
            // ruleid: mois-5-01-null-dereference
            out.add(url.toLowerCase());
        }
        // ruleid: mois-5-01-null-dereference
        out.add(type != null ? url.toUpperCase() : "");
        // ruleid: mois-5-01-null-dereference
        if (type != null && url.isEmpty()) {
            return "";
        }
        if (StringUtils.isBlank(type)) {
            throw new IllegalArgumentException("type");
        }
        // ruleid: mois-5-01-null-dereference
        return url.intern();
    }

    // || 로 묶여 있어 url 이 null 이어도 분기에 들어온다
    public String orCondition(HttpServletRequest request, boolean force) {
        String url = request.getParameter("url");
        if (url != null || force) {
            // ruleid: mois-5-01-null-dereference
            return url.trim();
        }
        return "";
    }

    // && 로 묶여 있어 url 이 null 이어도 중단하지 않을 수 있다
    public String andExit(HttpServletRequest request, boolean strict) {
        String url = request.getParameter("url");
        if (url == null && strict) {
            return "";
        }
        // ruleid: mois-5-01-null-dereference
        return url.trim();
    }

    // `x == null && ...` 의 else 는 null 일 수 있다
    public String andElse(HttpServletRequest request, boolean strict) {
        String url = request.getParameter("url");
        if (url == null && strict) {
            return "";
        } else {
            // ruleid: mois-5-01-null-dereference
            return url.trim();
        }
    }

    // ?: 의 반대쪽 갈래
    public String ternaryWrongSide(HttpServletRequest request) {
        String url = request.getParameter("url");
        // ruleid: mois-5-01-null-dereference
        String a = url != null ? "" : url.trim();
        // ruleid: mois-5-01-null-dereference
        String b = url == null ? url.trim() : "";
        return a + b;
    }

    // 검사 결과를 쓰지 않는다
    public String resultIgnored(HttpServletRequest request) {
        String url = request.getParameter("url");
        StringUtils.isEmpty(url);
        Objects.isNull(url);
        // ruleid: mois-5-01-null-dereference
        return url.trim();
    }

    // 비었을 때(null 포함) 실행되는 분기에서 사용 — 유틸리티 검사의 방향이 반대다
    public void emptyBranch(HttpServletRequest request, List<String> out) {
        String url = request.getParameter("url");
        if (StringUtils.isEmpty(url)) {
            // ruleid: mois-5-01-null-dereference
            out.add(url.trim());
        }
        String type = request.getParameter("type");
        if (!StringUtils.isNotBlank(type)) {
            // ruleid: mois-5-01-null-dereference
            out.add(type.strip());
        }
    }

    // 유틸리티 검사가 || 로 묶여 있다
    public String utilOr(HttpServletRequest request, boolean force) {
        String url = request.getParameter("url");
        if (StringUtils.isNotEmpty(url) || force) {
            // ruleid: mois-5-01-null-dereference
            return url.trim();
        }
        return "";
    }

    // 유틸리티 검사가 && 로 묶여 있어 중단하지 않을 수 있다 / 비었어도 기록만 한다
    public String utilAndExit(HttpServletRequest request, boolean strict, List<String> out) {
        String url = request.getParameter("url");
        if (StringUtils.isBlank(url) && strict) {
            return "";
        }
        // ruleid: mois-5-01-null-dereference
        out.add(url.trim());
        String type = request.getParameter("type");
        if (StringUtils.isBlank(type)) {
            LOG.warn("type 없음");
        }
        // ruleid: mois-5-01-null-dereference
        return type.trim();
    }

    // 실패 분기 "안"에서 사용: 중단하더라도 그 안에서는 null 일 수 있다
    public String insideFailingBranch(HttpServletRequest request) {
        String url = request.getParameter("url");
        if (StringUtils.isEmpty(url)) {
            // ruleid: mois-5-01-null-dereference
            return url.trim();
        }
        String type = request.getParameter("type");
        if (type == null) {
            // ruleid: mois-5-01-null-dereference
            throw new IllegalArgumentException(type.trim());
        }
        return "";
    }

    // 분기 안쪽의 조건부 return 은 중단이 아니다 (strict 가 아니면 계속 진행)
    public String nestedConditionalReturn(HttpServletRequest request, boolean strict) {
        String url = request.getParameter("url");
        if (url == null) {
            if (strict) {
                return "";
            }
        }
        // ruleid: mois-5-01-null-dereference
        return url.trim();
    }

    // 검사한 뒤에 null 일 수 있는 값을 다시 대입했다
    public String reassignedAfterCheck(HttpServletRequest request) {
        String url = request.getParameter("url");
        if (url == null) {
            return "";
        }
        url = request.getParameter("fallback");
        // ruleid: mois-5-01-null-dereference
        return url.trim();
    }

    // 기본값 대입이 조건부다 (strict 이면 null 그대로)
    public String conditionalDefault(boolean strict) {
        String home = System.getenv("APP_HOME");
        if (home == null) {
            if (!strict) {
                home = "/";
            }
        }
        // ruleid: mois-5-01-null-dereference
        return home.trim();
    }

    // 검사를 부정했다: 값이 있을 때 중단하므로 그 뒤는 null(또는 빈 값)이다
    public String negatedExit(HttpServletRequest request, List<String> out) {
        String url = request.getParameter("url");
        if (!StringUtils.isEmpty(url)) {
            return "ok";
        }
        // ruleid: mois-5-01-null-dereference
        out.add(url.trim());
        String type = request.getParameter("type");
        if (!(type == null)) {
            return "ok";
        }
        // ruleid: mois-5-01-null-dereference
        return type.trim();
    }

    // requireNonNull 을 다른 변수에 했다
    public String requireOther(HttpServletRequest request) {
        String url = request.getParameter("url");
        String type = request.getParameter("type");
        Objects.requireNonNull(type, "type");
        // ruleid: mois-5-01-null-dereference
        return url.trim();
    }
}
