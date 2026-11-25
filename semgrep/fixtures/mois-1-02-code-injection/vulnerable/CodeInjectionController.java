package demo;

import javax.script.ScriptEngine;
import javax.script.ScriptEngineManager;
import javax.script.ScriptException;
import javax.servlet.http.HttpServletRequest;
import org.springframework.expression.ExpressionParser;
import org.springframework.expression.spel.standard.SpelExpressionParser;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RequestParam;

// 탐지돼야 하는 경우 3건: 외부 입력을 스크립트·표현식으로 실행
@Controller
public class CodeInjectionController {
    // 진단가이드 예: ScriptEngine.eval 로 입력값 실행
    @RequestMapping(value = "/execute", method = RequestMethod.GET)
    public String execute(@RequestParam("src") String src) throws ScriptException {
        ScriptEngineManager scriptEngineManager = new ScriptEngineManager();
        ScriptEngine scriptEngine = scriptEngineManager.getEngineByName("javascript");
        // ruleid: mois-1-02-code-injection
        return (String) scriptEngine.eval(src);
    }

    // 진단가이드 정탐 예: 입력값을 코드 문자열에 이어 붙임
    public Object print(HttpServletRequest request) throws ScriptException {
        ScriptEngine engine = new ScriptEngineManager().getEngineByName("javascript");
        // ruleid: mois-1-02-code-injection
        return engine.eval("print('" + request.getParameter("name") + "')");
    }

    // Spring SpEL 표현식 삽입
    public Object calc(HttpServletRequest request) {
        ExpressionParser parser = new SpelExpressionParser();
        // ruleid: mois-1-02-code-injection
        return parser.parseExpression(request.getParameter("expr")).getValue();
    }
}
