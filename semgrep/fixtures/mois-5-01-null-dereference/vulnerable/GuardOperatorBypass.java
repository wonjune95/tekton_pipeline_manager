package demo;

import javax.servlet.http.HttpServletRequest;
import org.apache.commons.lang3.StringUtils;

// 탐지돼야 하는 경우: null 검사가 다른 식에 묶여 있어 "null 이면 중단", "본문 진입 = null 아님" 이 성립하지 않는다
public class GuardOperatorBypass {

    // ── 실패 시 중단 형태 ──

    // & 는 && 와 같은 뜻이다: strict 가 false 면 null 이어도 계속 진행한다
    public String bitwiseAnd(HttpServletRequest request, boolean strict) {
        String url = request.getParameter("url");
        if (url == null & strict) {
            return "";
        }
        // ruleid: mois-5-01-null-dereference
        return url.trim();
    }

    public String bitwiseAndUtil(HttpServletRequest request, boolean strict) {
        String url = request.getParameter("url");
        if (StringUtils.isEmpty(url) & strict) return "";
        // ruleid: mois-5-01-null-dereference
        return url.trim();
    }

    public String bitwiseAndNotHasText(HttpServletRequest request, boolean strict) {
        String url = request.getParameter("url");
        if (!StringUtils.hasText(url) & strict) return "";
        // ruleid: mois-5-01-null-dereference
        return url.trim();
    }

    // 조건 연산자: strict 가 false 면 검사하지 않는다
    public String ternary(HttpServletRequest request, boolean strict) {
        String url = request.getParameter("url");
        if (strict ? url == null : false) {
            return "";
        }
        // ruleid: mois-5-01-null-dereference
        return url.trim();
    }

    // null 이 "아닐" 때 중단한다
    public String comparedWithFalse(HttpServletRequest request) {
        String url = request.getParameter("url");
        if ((url == null) == false) {
            return "";
        }
        // ruleid: mois-5-01-null-dereference
        return url.trim();
    }

    public String negatedUtil(HttpServletRequest request) {
        String url = request.getParameter("url");
        if (!StringUtils.isBlank(url)) {
            return "";
        }
        // ruleid: mois-5-01-null-dereference
        return url.trim();
    }

    // 검사 결과를 다른 호출의 인자로 넘긴다
    public String passedToCall(HttpServletRequest request) {
        String url = request.getParameter("url");
        if (Boolean.FALSE.equals(StringUtils.isEmpty(url))) {
            return "";
        }
        // ruleid: mois-5-01-null-dereference
        return url.trim();
    }

    // ── else 분기 형태: if (x == null ...) { } else { 여기 } ──

    public String elseBitwiseAnd(HttpServletRequest request, boolean strict) {
        String url = request.getParameter("url");
        if (url == null & strict) {
            return "";
        } else {
            // ruleid: mois-5-01-null-dereference
            return url.trim();
        }
    }

    public String elseTernary(HttpServletRequest request, boolean strict) {
        String url = request.getParameter("url");
        if (strict ? url == null : true) {
            return "";
        } else {
            // ruleid: mois-5-01-null-dereference
            return url.trim();
        }
    }

    // ── 조건 안에서만 사용하는 형태 ──

    // | 는 || 와 같은 뜻이다: force 면 null 이어도 본문에 들어온다
    public String positiveBitwiseOr(HttpServletRequest request, boolean force) {
        String url = request.getParameter("url");
        if (url != null | force) {
            // ruleid: mois-5-01-null-dereference
            return url.trim();
        }
        return "";
    }

    public String positiveTernary(HttpServletRequest request, boolean force) {
        String url = request.getParameter("url");
        if (force ? true : url != null) {
            // ruleid: mois-5-01-null-dereference
            return url.trim();
        }
        return "";
    }

    // 본문이 null 인 쪽이다
    public String positiveNegated(HttpServletRequest request) {
        String url = request.getParameter("url");
        if (!(url != null)) {
            // ruleid: mois-5-01-null-dereference
            return url.trim();
        }
        return "";
    }

    public String positiveUtilBitwiseOr(HttpServletRequest request, boolean force) {
        String url = request.getParameter("url");
        if (StringUtils.hasText(url) | force) {
            // ruleid: mois-5-01-null-dereference
            return url.trim();
        }
        return "";
    }

    public String positiveNotEmptyBitwiseOr(HttpServletRequest request, boolean force) {
        String url = request.getParameter("url");
        if (!StringUtils.isEmpty(url) | force) {
            // ruleid: mois-5-01-null-dereference
            return url.trim();
        }
        return "";
    }

    public String positiveUtilNegated(HttpServletRequest request) {
        String url = request.getParameter("url");
        if (!StringUtils.isNotBlank(url)) {
            // ruleid: mois-5-01-null-dereference
            return url.trim();
        }
        return "";
    }

    public String positiveUtilPassedToCall(HttpServletRequest request) {
        String url = request.getParameter("url");
        if (Boolean.FALSE.equals(StringUtils.hasText(url))) {
            // ruleid: mois-5-01-null-dereference
            return url.trim();
        }
        return "";
    }
}
