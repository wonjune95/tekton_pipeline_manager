package demo;

import javax.script.ScriptEngine;
import javax.script.ScriptException;
import javax.servlet.http.HttpServletRequest;

// 검사식이 다른 식에 묶여 있어 "검사 실패 = 중단", "본문 진입 = 검사 통과" 가 성립하지 않는 경우: 모두 탐지되어야 한다
public class GuardOperatorBypass {
    private ScriptEngine engine;

    // & 는 && 와 같은 뜻이다: strict 가 false 면 검사에 실패해도 계속 진행한다
    public Object bitwiseAnd(HttpServletRequest request, boolean strict) throws ScriptException {
        String src = request.getParameter("src");
        if (!src.matches("[\\w]*") & strict) {
            return null;
        }
        // ruleid: mois-1-02-code-injection
        return engine.eval(src);
    }

    public Object bitwiseAndEqFalse(HttpServletRequest request, boolean strict) throws ScriptException {
        String src = request.getParameter("src");
        if (src.matches("[\\w]*") == false & strict) return null;
        // ruleid: mois-1-02-code-injection
        return engine.eval(src);
    }

    // 조건 연산자: strict 가 false 면 검사하지 않는다
    public Object ternary(HttpServletRequest request, boolean strict) throws ScriptException {
        String src = request.getParameter("src");
        if (strict ? !src.matches("[\\w]*") : false) {
            return null;
        }
        // ruleid: mois-1-02-code-injection
        return engine.eval(src);
    }

    // ^ : legacy 가 true 면 검사에 "통과한" 값에서 중단하고 실패한 값은 계속 진행한다
    public Object xor(HttpServletRequest request, boolean legacy) throws ScriptException {
        String src = request.getParameter("src");
        if (!src.matches("[\\w]*") ^ legacy) {
            return null;
        }
        // ruleid: mois-1-02-code-injection
        return engine.eval(src);
    }

    // 전체를 다시 부정: 검사에 통과하면 중단하고, 실패하면 계속 진행한다
    public Object negatedWhole(HttpServletRequest request) throws ScriptException {
        String src = request.getParameter("src");
        if (!(src == null || !src.matches("[\\w]*"))) {
            return null;
        }
        // ruleid: mois-1-02-code-injection
        return engine.eval(src);
    }

    public Object comparedWithFalse(HttpServletRequest request) throws ScriptException {
        String src = request.getParameter("src");
        if (!src.matches("[\\w]*") == false) {
            return null;
        }
        // ruleid: mois-1-02-code-injection
        return engine.eval(src);
    }

    // 검사 결과를 다른 호출의 인자로 넘긴다: 조건의 참·거짓은 그 호출이 정한다
    public Object passedToCall(HttpServletRequest request) throws ScriptException {
        String src = request.getParameter("src");
        if (Boolean.FALSE.equals(!src.matches("[\\w]*"))) {
            return null;
        }
        // ruleid: mois-1-02-code-injection
        return engine.eval(src);
    }

    // 조건 안에서만 사용하는 형태: || · | 는 검사가 거짓이어도 본문에 들어온다
    public Object positiveOr(HttpServletRequest request, boolean admin) throws ScriptException {
        String src = request.getParameter("src");
        if (src.matches("[\\w]*") || admin) {
            // ruleid: mois-1-02-code-injection
            return engine.eval(src);
        }
        return null;
    }

    public Object positiveBitwiseOr(HttpServletRequest request, boolean admin) throws ScriptException {
        String src = request.getParameter("src");
        if (src.matches("[\\w]*") | admin) {
            // ruleid: mois-1-02-code-injection
            return engine.eval(src);
        }
        return null;
    }

    public Object positiveTernary(HttpServletRequest request, boolean admin) throws ScriptException {
        String src = request.getParameter("src");
        if (admin ? true : src.matches("[\\w]*")) {
            // ruleid: mois-1-02-code-injection
            return engine.eval(src);
        }
        return null;
    }

    // 본문이 검사에 "실패한" 쪽이다
    public Object positiveNotTrue(HttpServletRequest request) throws ScriptException {
        String src = request.getParameter("src");
        if (src.matches("[\\w]*") != true) {
            // ruleid: mois-1-02-code-injection
            return engine.eval(src);
        }
        return null;
    }

    public Object positiveNegatedWhole(HttpServletRequest request) throws ScriptException {
        String src = request.getParameter("src");
        if (!(src != null && src.matches("[\\w]*"))) {
            // ruleid: mois-1-02-code-injection
            return engine.eval(src);
        }
        return null;
    }

    public Object positivePassedToCall(HttpServletRequest request) throws ScriptException {
        String src = request.getParameter("src");
        if (Boolean.FALSE.equals(src.matches("[\\w]*"))) {
            // ruleid: mois-1-02-code-injection
            return engine.eval(src);
        }
        return null;
    }

    // 조건식 안에서 먼저 실행하고 그 뒤에 검사한다
    public boolean usedInConditionBeforeCheck(HttpServletRequest request) throws ScriptException {
        String src = request.getParameter("src");
        // ruleid: mois-1-02-code-injection
        if (engine.eval(src) != null && src.matches("[\\w]*")) {
            return true;
        }
        return false;
    }

    // 검사에 통과한 뒤 본문에서 다른 입력으로 바꾸거나 덧붙인다
    public Object reassignedInBody(HttpServletRequest request) throws ScriptException {
        String src = request.getParameter("src");
        if (src.matches("[\\w]*")) {
            src = request.getParameter("alias");
            // ruleid: mois-1-02-code-injection
            return engine.eval(src);
        }
        return null;
    }

    public Object appendedInBody(HttpServletRequest request) throws ScriptException {
        String src = request.getParameter("src");
        if (src.matches("[\\w]*")) {
            src += request.getParameter("suffix");
            // ruleid: mois-1-02-code-injection
            return engine.eval(src);
        }
        return null;
    }

    public Object reassignedInNestedBlock(HttpServletRequest request, boolean useAlias) throws ScriptException {
        String src = request.getParameter("src");
        if (src.matches("[\\w]*")) {
            if (useAlias) {
                src = request.getParameter("alias");
            }
            // ruleid: mois-1-02-code-injection
            return engine.eval(src);
        }
        return null;
    }
}
