package demo;

import javax.servlet.http.HttpServletRequest;

// 범위 검사가 "있기만" 하고 막지는 못하는 경우: 모두 탐지되어야 한다
public class RangeCheckBypass {
    private static final int MAX = 100;

    // 비교 결과를 쓰지 않는다
    public int[] resultIgnored(HttpServletRequest request) {
        int n = Integer.parseInt(request.getParameter("n"));
        boolean small = n < MAX;
        // ruleid: mois-1-14-integer-overflow
        return new int[n];
    }

    // 반복 조건에 쓰인 비교는 검사가 아니다
    public int[] loopCondition(HttpServletRequest request) {
        int n = Integer.parseInt(request.getParameter("n"));
        for (int i = 0; i < n; i++) {
            System.out.println(i);
        }
        // ruleid: mois-1-14-integer-overflow
        return new int[n];
    }

    // 실패해도 기록만 하고 계속 진행한다
    public int[] failureDoesNotExit(HttpServletRequest request) {
        int n = Integer.parseInt(request.getParameter("n"));
        if (n < 0 || n > MAX) {
            System.err.println("out of range");
        }
        // ruleid: mois-1-14-integer-overflow
        return new int[n];
    }

    // 실패 분기 안의 또 다른 조건에서만 중단한다
    public int[] exitsOnlySometimes(HttpServletRequest request, boolean strict) {
        int n = Integer.parseInt(request.getParameter("n"));
        if (n > MAX) {
            if (strict) {
                return null;
            }
        }
        // ruleid: mois-1-14-integer-overflow
        return new int[n];
    }

    // 다른 조건이 거짓이면 검사를 건너뛴다
    public int[] checkSkippedByAnd(HttpServletRequest request, boolean strict) {
        int n = Integer.parseInt(request.getParameter("n"));
        if (strict && n > MAX) {
            throw new IllegalArgumentException();
        }
        // ruleid: mois-1-14-integer-overflow
        return new int[n];
    }

    // 하한만 검사한다 (상한이 없다)
    public int[] lowerBoundOnly(HttpServletRequest request) {
        int n = Integer.parseInt(request.getParameter("n"));
        if (n < 0) {
            throw new IllegalArgumentException();
        }
        // ruleid: mois-1-14-integer-overflow
        return new int[n];
    }

    // 하한만 확인한 분기 안에서 쓴다
    public int[] lowerBoundOnlyInside(HttpServletRequest request) {
        int n = Integer.parseInt(request.getParameter("n"));
        if (n > 0) {
            // ruleid: mois-1-14-integer-overflow
            return new int[n];
        }
        return new int[0];
    }

    // 범위를 벗어난 쪽 분기에서 쓴다
    public int[] usedInFailureBranch(HttpServletRequest request) {
        int n = Integer.parseInt(request.getParameter("n"));
        if (n < 0 || n > MAX) {
            // ruleid: mois-1-14-integer-overflow
            return new int[n];
        }
        return new int[0];
    }

    // 검사를 통과하지 못한 쪽(else)에서 쓴다
    public int[] oppositeBranch(HttpServletRequest request) {
        int n = Integer.parseInt(request.getParameter("n"));
        if (n <= MAX) {
            return new int[0];
        } else {
            // ruleid: mois-1-14-integer-overflow
            return new int[n];
        }
    }

    // 부정한 조건 안에서 쓴다
    public int[] negatedCondition(HttpServletRequest request) {
        int n = Integer.parseInt(request.getParameter("n"));
        if (!(n <= MAX)) {
            // ruleid: mois-1-14-integer-overflow
            return new int[n];
        }
        return new int[0];
    }

    // 조건을 뒤집어 "상한을 넘지 않으면" 중단한다 — 계속 진행하는 쪽이 상한을 넘은 값이다
    public int[] exitsWhenInRange(HttpServletRequest request) {
        int n = Integer.parseInt(request.getParameter("n"));
        if (!(n > MAX)) {
            return new int[0];
        }
        // ruleid: mois-1-14-integer-overflow
        return new int[n];
    }

    // 다른 조건만 참이어도 분기에 들어온다
    public int[] checkBypassedByOr(HttpServletRequest request, boolean force) {
        int n = Integer.parseInt(request.getParameter("n"));
        if (n <= MAX || force) {
            // ruleid: mois-1-14-integer-overflow
            return new int[n];
        }
        return new int[0];
    }

    // 통과한 분기 밖에서 쓴다
    public int[] usedAfterPositiveIf(HttpServletRequest request) {
        int n = Integer.parseInt(request.getParameter("n"));
        if (n >= 0 && n <= MAX) {
            System.out.println("in range");
        }
        // ruleid: mois-1-14-integer-overflow
        return new int[n];
    }

    // 다른 값만 검사한다
    public int[] otherValueChecked(HttpServletRequest request) {
        int n = Integer.parseInt(request.getParameter("n"));
        int m = Integer.parseInt(request.getParameter("m"));
        if (m < 0 || m > MAX) {
            throw new IllegalArgumentException();
        }
        // ruleid: mois-1-14-integer-overflow
        return new int[n];
    }

    // 검사한 뒤 다른 입력으로 바꾼다
    public int[] reassignedAfterCheck(HttpServletRequest request) {
        int n = Integer.parseInt(request.getParameter("n"));
        if (n < 0 || n > MAX) {
            throw new IllegalArgumentException();
        }
        n = Integer.parseInt(request.getParameter("m"));
        // ruleid: mois-1-14-integer-overflow
        return new int[n];
    }

    // 검사한 뒤 검사하지 않은 입력을 더한다
    public int[] addedAfterCheck(HttpServletRequest request) {
        int n = Integer.parseInt(request.getParameter("n"));
        if (n < 0 || n > MAX) {
            throw new IllegalArgumentException();
        }
        n += Integer.parseInt(request.getParameter("extra"));
        // ruleid: mois-1-14-integer-overflow
        return new int[n];
    }

    // Math.min 결과를 버린다
    public int[] minResultIgnored(HttpServletRequest request) {
        int n = Integer.parseInt(request.getParameter("n"));
        Math.min(n, MAX);
        // ruleid: mois-1-14-integer-overflow
        return new int[n];
    }

    // Math.max 는 하한만 정한다
    public int[] maxIsNotUpperBound(HttpServletRequest request) {
        int n = Math.max(Integer.parseInt(request.getParameter("n")), 0);
        // ruleid: mois-1-14-integer-overflow
        return new int[n];
    }
}
