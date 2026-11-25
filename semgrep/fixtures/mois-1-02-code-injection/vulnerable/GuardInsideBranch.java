package demo;

import javax.script.ScriptEngine;
import javax.script.ScriptException;
import javax.servlet.http.HttpServletRequest;

// 검사에 실패한 분기 "안"에서 쓰는 값은 검증된 값이 아니다
public class GuardInsideBranch {
    private final ScriptEngine engine;

    public GuardInsideBranch(ScriptEngine engine) {
        this.engine = engine;
    }

    public Object run(HttpServletRequest request) throws ScriptException {
        String expr = request.getParameter("expr");
        if (expr == null || !expr.matches("[0-9+*/ -]+")) {
            // ruleid: mois-1-02-code-injection
            return engine.eval("log('rejected: " + expr + "')");
        }
        // ok: mois-1-02-code-injection — 위에서 실패하면 빠져나갔다
        return engine.eval(expr);
    }
}
