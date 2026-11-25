package demo;

import javax.script.ScriptEngine;
import javax.script.ScriptException;
import javax.servlet.http.HttpServletRequest;

// 정규식 검사가 "있기만" 하고 막지는 못하는 경우: 모두 탐지되어야 한다
public class RegexGuardBypass {
    private ScriptEngine engine;

    // 검사 결과를 쓰지 않는다
    public Object resultIgnored(HttpServletRequest request) throws ScriptException {
        String src = request.getParameter("src");
        src.matches("[\\w]*");
        // ruleid: mois-1-02-code-injection
        return engine.eval(src);
    }

    // 검사 결과를 변수에 담기만 한다
    public Object resultStoredOnly(HttpServletRequest request) throws ScriptException {
        String src = request.getParameter("src");
        boolean valid = src.matches("[\\w]*");
        // ruleid: mois-1-02-code-injection
        return engine.eval(src);
    }

    // 실패해도 기록만 하고 계속 진행한다
    public Object failureDoesNotExit(HttpServletRequest request) throws ScriptException {
        String src = request.getParameter("src");
        if (!src.matches("[\\w]*")) {
            System.err.println("invalid script");
        }
        // ruleid: mois-1-02-code-injection
        return engine.eval(src);
    }

    // null 검사와 묶었지만 실패해도 계속 진행한다
    public Object nullCheckedButNoExit(HttpServletRequest request) throws ScriptException {
        String src = request.getParameter("src");
        if (src == null || !src.matches("[\\w]*")) {
            System.err.println("invalid script");
        }
        // ruleid: mois-1-02-code-injection
        return engine.eval(src);
    }

    // 검사를 통과하지 못한 쪽(else)에서 실행한다
    public Object oppositeBranch(HttpServletRequest request) throws ScriptException {
        String src = request.getParameter("src");
        if (src.matches("[\\w]*")) {
            return null;
        } else {
            // ruleid: mois-1-02-code-injection
            return engine.eval(src);
        }
    }

    // 통과한 분기 밖에서 실행한다
    public Object usedAfterPositiveIf(HttpServletRequest request) throws ScriptException {
        String src = request.getParameter("src");
        if (src.matches("[\\w]*")) {
            System.out.println("valid");
        }
        // ruleid: mois-1-02-code-injection
        return engine.eval(src);
    }

    // null 검사와 묶은 실패 분기 안에서 실행한다
    public Object usedInFailureBranch(HttpServletRequest request) throws ScriptException {
        String src = request.getParameter("src");
        if (src == null || !src.matches("[\\w]*")) {
            // ruleid: mois-1-02-code-injection
            return engine.eval(src);
        }
        return null;
    }

    // `== false` 로 쓴 실패 분기 안에서 실행한다
    public Object usedInFalseBranch(HttpServletRequest request) throws ScriptException {
        String src = request.getParameter("src");
        if (src.matches("[\\w]*") == false) {
            // ruleid: mois-1-02-code-injection
            return engine.eval(src);
        }
        return null;
    }

    // 검사한 뒤 다른 입력으로 바꿔 실행한다
    public Object reassignedAfterCheck(HttpServletRequest request) throws ScriptException {
        String src = request.getParameter("src");
        if (src == null || !src.matches("[\\w]*")) {
            throw new IllegalArgumentException();
        }
        src = request.getParameter("raw");
        // ruleid: mois-1-02-code-injection
        return engine.eval(src);
    }

    // 검사한 뒤 검사하지 않은 입력을 덧붙여 실행한다
    public Object appendedAfterCheck(HttpServletRequest request) throws ScriptException {
        String src = request.getParameter("src");
        if (src == null || !src.matches("[\\w]*")) {
            throw new IllegalArgumentException();
        }
        src += request.getParameter("tail");
        // ruleid: mois-1-02-code-injection
        return engine.eval(src);
    }

    // 다른 값만 검사한다
    public Object otherValueChecked(HttpServletRequest request) throws ScriptException {
        String src = request.getParameter("src");
        String name = request.getParameter("name");
        if (name == null || !name.matches("[\\w]*")) {
            throw new IllegalArgumentException();
        }
        // ruleid: mois-1-02-code-injection
        return engine.eval(src);
    }

    // 다른 조건이 거짓이면 검사 자체를 건너뛴다
    public Object checkSkippedByAnd(HttpServletRequest request, boolean strict) throws ScriptException {
        String src = request.getParameter("src");
        if (strict && !src.matches("[\\w]*")) {
            throw new IllegalArgumentException();
        }
        // ruleid: mois-1-02-code-injection
        return engine.eval(src);
    }

    // 실패 분기 안의 또 다른 조건에서만 중단한다
    public Object exitsOnlySometimes(HttpServletRequest request, boolean strict) throws ScriptException {
        String src = request.getParameter("src");
        if (!src.matches("[\\w]*")) {
            if (strict) {
                throw new IllegalArgumentException();
            }
        }
        // ruleid: mois-1-02-code-injection
        return engine.eval(src);
    }
}
