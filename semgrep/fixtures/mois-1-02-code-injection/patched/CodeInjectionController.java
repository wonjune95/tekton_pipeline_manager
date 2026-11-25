package demo;

import javax.script.ScriptEngine;
import javax.script.ScriptEngineManager;
import javax.script.ScriptException;
import javax.servlet.http.HttpServletRequest;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.expression.ExpressionParser;
import org.springframework.expression.spel.standard.SpelExpressionParser;
import org.springframework.expression.spel.support.StandardEvaluationContext;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RequestParam;

// 탐지되면 안 되는 경우: 허용 문자만 통과시킨 뒤 실행(검사에 실패하면 중단), 표현식은 고정하고 입력은 변수로 넘김
@Controller
public class CodeInjectionController {
    private static final Logger log = LoggerFactory.getLogger(CodeInjectionController.class);
    private final ScriptEngine scriptEngine = new ScriptEngineManager().getEngineByName("javascript");

    // 진단가이드 안전한 코드 예: 정규식으로 검증하고, 맞지 않으면 예외로 중단한다
    @RequestMapping(value = "/execute", method = RequestMethod.GET)
    public String execute(@RequestParam("src") String src) throws ScriptException {
        if (src.matches("[\\w]*") == false) {
            throw new IllegalArgumentException();
        }
        // ok: mois-1-02-code-injection — 검사에 실패하면 위에서 예외로 끝난다
        return (String) scriptEngine.eval(src);
    }

    @RequestMapping(value = "/run", method = RequestMethod.GET)
    public Object run(@RequestParam("src") String src) throws ScriptException {
        if (!src.matches("[\\w]*")) {
            return null;
        }
        // ok: mois-1-02-code-injection — 검사에 실패하면 위에서 return 으로 끝난다
        return scriptEngine.eval(src);
    }

    // 중괄호 없는 if 도 같다
    @RequestMapping(value = "/run2", method = RequestMethod.GET)
    public Object runBraceless(@RequestParam("src") String src) throws ScriptException {
        if (!src.matches("[\\w]*")) throw new IllegalArgumentException();
        // ok: mois-1-02-code-injection
        return scriptEngine.eval(src);
    }

    @RequestMapping(value = "/run3", method = RequestMethod.GET)
    public Object runBracelessReturn(@RequestParam("src") String src) throws ScriptException {
        if (!src.matches("[\\w]*")) return null;
        // ok: mois-1-02-code-injection
        return scriptEngine.eval(src);
    }

    // 실패 분기에서 기록을 남긴 뒤 중단한다 (마지막 문장이 return / throw)
    @RequestMapping(value = "/calc", method = RequestMethod.GET)
    public Object calcLogged(@RequestParam("expr") String expr) throws ScriptException {
        if (!expr.matches("[0-9+*/ -]+")) {
            log.warn("rejected expression");
            return null;
        }
        // ok: mois-1-02-code-injection — 기록 후 return 으로 끝난다
        return scriptEngine.eval(expr);
    }

    @RequestMapping(value = "/calc2", method = RequestMethod.GET)
    public Object calcAudited(@RequestParam("expr") String expr) throws ScriptException {
        if (!expr.matches("[0-9+*/ -]+")) {
            log.warn("rejected expression");
            throw new IllegalArgumentException();
        }
        // ok: mois-1-02-code-injection — 기록 후 예외로 끝난다
        return scriptEngine.eval(expr);
    }

    // null 검사와 함께 쓴 형태
    public Object runNullChecked(HttpServletRequest request) throws ScriptException {
        String src = request.getParameter("src");
        if (src == null || !src.matches("[\\w]*")) {
            throw new IllegalArgumentException();
        }
        // ok: mois-1-02-code-injection — null 이거나 형식이 틀리면 위에서 끝난다
        return scriptEngine.eval(src);
    }

    // 검사를 통과한 분기 안에서만 실행한다
    public Object runInsideCheck(HttpServletRequest request) throws ScriptException {
        String src = request.getParameter("src");
        if (src != null && src.matches("[\\w]*")) {
            // ok: mois-1-02-code-injection — 통과한 분기 안에서만 사용
            return scriptEngine.eval(src);
        }
        return null;
    }

    // 표현식은 상수, 입력값은 평가 컨텍스트의 변수로만 넘긴다
    public Object greet(HttpServletRequest request) {
        StandardEvaluationContext context = new StandardEvaluationContext();
        context.setVariable("name", request.getParameter("name"));
        ExpressionParser parser = new SpelExpressionParser();
        // ok: mois-1-02-code-injection — 표현식 문자열이 상수
        return parser.parseExpression("'Hello ' + #name").getValue(context);
    }
}
