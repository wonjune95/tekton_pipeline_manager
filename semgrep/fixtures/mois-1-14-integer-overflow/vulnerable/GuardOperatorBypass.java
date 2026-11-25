package demo;

import javax.servlet.http.HttpServletRequest;

// 범위 검사가 다른 식에 묶여 있어 "상한 초과 = 중단", "본문 진입 = 상한 이하" 가 성립하지 않는 경우: 모두 탐지되어야 한다
public class GuardOperatorBypass {
    private static final int MAX = 100;

    // & 는 && 와 같은 뜻이다: strict 가 false 면 상한을 넘어도 계속 진행한다
    public int[] bitwiseAnd(HttpServletRequest request, boolean strict) {
        int n = Integer.parseInt(request.getParameter("n"));
        if (n > MAX & strict) {
            return new int[0];
        }
        // ruleid: mois-1-14-integer-overflow
        return new int[n];
    }

    // 조건 연산자: strict 가 false 면 검사하지 않는다
    public int[] ternary(HttpServletRequest request, boolean strict) {
        int n = Integer.parseInt(request.getParameter("n"));
        if (strict ? n > MAX : false) {
            return new int[0];
        }
        // ruleid: mois-1-14-integer-overflow
        return new int[n];
    }

    // ^ : legacy 가 true 면 상한 "이하" 일 때 중단하고 넘으면 계속 진행한다
    public int[] xor(HttpServletRequest request, boolean legacy) {
        int n = Integer.parseInt(request.getParameter("n"));
        if (n > MAX ^ legacy) {
            return new int[0];
        }
        // ruleid: mois-1-14-integer-overflow
        return new int[n];
    }

    // 전체를 부정: 범위 안이면 중단하고, 범위를 벗어나면 계속 진행한다
    public int[] negatedWhole(HttpServletRequest request) {
        int n = Integer.parseInt(request.getParameter("n"));
        if (!(n < 0 || n > MAX)) {
            return new int[0];
        }
        // ruleid: mois-1-14-integer-overflow
        return new int[n];
    }

    public int[] comparedWithFalse(HttpServletRequest request) {
        int n = Integer.parseInt(request.getParameter("n"));
        if ((n > MAX) == false) {
            return new int[0];
        }
        // ruleid: mois-1-14-integer-overflow
        return new int[n];
    }

    // 비교 결과를 다른 호출의 인자로 넘긴다: 조건의 참·거짓은 그 호출이 정한다
    public int[] passedToCall(HttpServletRequest request) {
        int n = Integer.parseInt(request.getParameter("n"));
        if (Boolean.FALSE.equals(n > MAX)) {
            return new int[0];
        }
        // ruleid: mois-1-14-integer-overflow
        return new int[n];
    }

    // 조건 안에서만 사용하는 형태: | 는 || 와 같은 뜻이라 상한을 넘어도 본문에 들어온다
    public int[] positiveBitwiseOr(HttpServletRequest request, boolean admin) {
        int n = Integer.parseInt(request.getParameter("n"));
        if (n < MAX | admin) {
            // ruleid: mois-1-14-integer-overflow
            return new int[n];
        }
        return new int[0];
    }

    public int[] positiveTernary(HttpServletRequest request, boolean admin) {
        int n = Integer.parseInt(request.getParameter("n"));
        if (admin ? true : n < MAX) {
            // ruleid: mois-1-14-integer-overflow
            return new int[n];
        }
        return new int[0];
    }

    // 본문이 상한을 "넘은" 쪽이다
    public int[] positiveNotTrue(HttpServletRequest request) {
        int n = Integer.parseInt(request.getParameter("n"));
        if ((n < MAX) != true) {
            // ruleid: mois-1-14-integer-overflow
            return new int[n];
        }
        return new int[0];
    }

    public int[] positivePassedToCall(HttpServletRequest request) {
        int n = Integer.parseInt(request.getParameter("n"));
        if (Boolean.FALSE.equals(n < MAX)) {
            // ruleid: mois-1-14-integer-overflow
            return new int[n];
        }
        return new int[0];
    }

    // 조건식 안에서 먼저 배열을 만들고 그 뒤에 비교한다
    public boolean usedInConditionBeforeCheck(HttpServletRequest request) {
        int n = Integer.parseInt(request.getParameter("n"));
        // ruleid: mois-1-14-integer-overflow
        if (new int[n].length >= 0 && n < MAX) {
            return true;
        }
        return false;
    }

    // 검사에 통과한 뒤 본문에서 다른 입력으로 바꾸거나 더한다
    public int[] reassignedInBody(HttpServletRequest request) {
        int n = Integer.parseInt(request.getParameter("n"));
        if (n < MAX) {
            n = Integer.parseInt(request.getParameter("rows"));
            // ruleid: mois-1-14-integer-overflow
            return new int[n];
        }
        return new int[0];
    }

    public int[] addedInBody(HttpServletRequest request) {
        int n = Integer.parseInt(request.getParameter("n"));
        if (n < MAX) {
            n += Integer.parseInt(request.getParameter("extra"));
            // ruleid: mois-1-14-integer-overflow
            return new int[n];
        }
        return new int[0];
    }

    public int[] reassignedInNestedBlock(HttpServletRequest request, boolean wide) {
        int n = Integer.parseInt(request.getParameter("n"));
        if (n < MAX) {
            if (wide) {
                n = Integer.parseInt(request.getParameter("rows"));
            }
            // ruleid: mois-1-14-integer-overflow
            return new int[n];
        }
        return new int[0];
    }
}
