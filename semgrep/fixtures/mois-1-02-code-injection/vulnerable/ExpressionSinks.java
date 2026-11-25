package demo;

import groovy.lang.GroovyClassLoader;
import groovy.lang.GroovyShell;
import javax.el.ELContext;
import javax.script.Compilable;
import javax.script.ScriptEngine;
import javax.script.ScriptEngineManager;
import javax.servlet.http.HttpServletRequest;
import ognl.Ognl;
import org.mvel2.MVEL;
import org.springframework.expression.ExpressionParser;
import org.springframework.expression.spel.standard.SpelExpressionParser;

// sink 가지마다 한 줄씩: 외부 입력이 각 스크립트·표현식 엔진에서 코드로 실행됨
public class ExpressionSinks {
    private ScriptEngine engine;
    private ScriptEngineManager manager;
    private Compilable compilable;
    private ExpressionParser parser;
    private SpelExpressionParser spel;
    private GroovyShell shell;
    private GroovyClassLoader loader;
    private javax.el.ExpressionFactory elFactory;
    private jakarta.el.ExpressionFactory jakartaElFactory;
    private ELContext elContext;
    private jakarta.el.ELContext jakartaElContext;

    public void scriptEngine(HttpServletRequest request) throws Exception {
        String code = request.getParameter("code");
        // ruleid: mois-1-02-code-injection
        engine.eval(code, engine.getContext());
        // ruleid: mois-1-02-code-injection
        compilable.compile(code);
        // 엔진을 변수에 담지 않고 바로 실행 (new … 생성식도 타입 패턴에 맞는다)
        // ruleid: mois-1-02-code-injection
        new ScriptEngineManager().getEngineByName("javascript").eval(code);
        // ruleid: mois-1-02-code-injection
        manager.getEngineByExtension("js").eval(code);
    }

    public void spel(HttpServletRequest request) {
        String expr = request.getParameter("expr");
        // ruleid: mois-1-02-code-injection
        parser.parseExpression(expr);
        // ruleid: mois-1-02-code-injection
        spel.parseExpression(expr);
        // ruleid: mois-1-02-code-injection
        new SpelExpressionParser().parseExpression("#{" + expr + "}");
    }

    public void groovy(HttpServletRequest request) {
        String script = request.getParameter("script");
        // ruleid: mois-1-02-code-injection
        shell.evaluate(script);
        // ruleid: mois-1-02-code-injection
        shell.parse(script);
        // ruleid: mois-1-02-code-injection
        new GroovyShell().evaluate(script);
        // ruleid: mois-1-02-code-injection
        new GroovyShell().parse(script);
        // ruleid: mois-1-02-code-injection
        loader.parseClass(script);
    }

    public void el(HttpServletRequest request) {
        String expr = request.getParameter("expr");
        // ruleid: mois-1-02-code-injection
        elFactory.createValueExpression(elContext, expr, Object.class);
        // ruleid: mois-1-02-code-injection
        elFactory.createMethodExpression(elContext, expr, Object.class, new Class<?>[0]);
        // ruleid: mois-1-02-code-injection
        jakartaElFactory.createValueExpression(jakartaElContext, expr, Object.class);
        // ruleid: mois-1-02-code-injection
        jakartaElFactory.createMethodExpression(jakartaElContext, expr, Object.class, new Class<?>[0]);
    }

    public void mvelAndOgnl(HttpServletRequest request) throws Exception {
        String expr = request.getParameter("expr");
        // ruleid: mois-1-02-code-injection
        MVEL.eval(expr);
        // ruleid: mois-1-02-code-injection
        MVEL.compileExpression(expr);
        // ruleid: mois-1-02-code-injection
        Ognl.getValue(expr, this);
        // ruleid: mois-1-02-code-injection
        Ognl.parseExpression(expr);
    }
}
