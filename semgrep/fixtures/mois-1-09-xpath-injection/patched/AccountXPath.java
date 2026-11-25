package demo;

import javax.servlet.http.HttpServletRequest;
import javax.xml.xpath.XPath;
import javax.xml.xpath.XPathExpressionException;
import javax.xml.xpath.XPathFactory;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import org.w3c.dom.Node;

// 탐지되면 안 되는 경우: 질의문은 고정하고 값은 XPath 변수로 넘긴다. 문자열로 조립해야 하면 허용 문자만 남기거나,
// 작은따옴표를 지운 값을 작은따옴표 문자열('…') 안에 넣는다
@RestController
public class AccountXPath {
    private final Node accounts;

    public AccountXPath(Node accounts) {
        this.accounts = accounts;
    }

    // 가장 안전한 형태: 질의문은 상수, 입력값은 변수($id)로 전달
    public String email(HttpServletRequest request) throws XPathExpressionException {
        String acctID = request.getParameter("acctID");
        XPath xpath = XPathFactory.newInstance().newXPath();
        xpath.setXPathVariableResolver(v -> acctID);
        // ok: mois-1-09-xpath-injection — 질의문이 상수
        return xpath.evaluate("/accounts/account[acctID=$id]/email/text()", accounts);
    }

    @GetMapping(value = "/stock", produces = "text/plain;charset=UTF-8")
    public String stock(@RequestParam String name) throws XPathExpressionException {
        XPath xpath = XPathFactory.newInstance().newXPath();
        xpath.setXPathVariableResolver(v -> name);
        // ok: mois-1-09-xpath-injection — 질의문이 상수
        return xpath.evaluate("//food[name=$name]/stock", accounts);
    }

    // 진단가이드 안전한 코드 예: 작은따옴표를 포함한 특수문자를 지운 뒤 작은따옴표 문자열 안에 넣는다
    @GetMapping(value = "/price", produces = "text/plain;charset=UTF-8")
    public String price(@RequestParam String name) throws XPathExpressionException {
        String safe = name.replaceAll("[()\\-'\\[\\]:,*/]", "");
        XPath xpath = XPathFactory.newInstance().newXPath();
        // ok: mois-1-09-xpath-injection — 지우는 문자 집합에 작은따옴표가 리터럴로 들어 있다
        return xpath.evaluate("//food[name='" + safe + "']/price", accounts);
    }

    // 영문자·숫자·밑줄만 남긴다
    @GetMapping(value = "/calories", produces = "text/plain;charset=UTF-8")
    public String calories(@RequestParam String name) throws XPathExpressionException {
        String safe = name.replaceAll("[^A-Za-z0-9_]", "");
        XPath xpath = XPathFactory.newInstance().newXPath();
        // ok: mois-1-09-xpath-injection — 허용 문자만 남기는 정규식이 리터럴로 보인다
        return xpath.evaluate("//food[name='" + safe + "']/calories", accounts);
    }

    // 문자 클래스 줄임꼴(\\w)로 영문자·숫자·밑줄만 남긴다
    @GetMapping(value = "/vendor", produces = "text/plain;charset=UTF-8")
    public String vendor(@RequestParam String name) throws XPathExpressionException {
        String safe = name.replaceAll("[^\\w]", "");
        XPath xpath = XPathFactory.newInstance().newXPath();
        // ok: mois-1-09-xpath-injection — \\w 밖의 문자(작은따옴표 포함)를 모두 지운다
        return xpath.evaluate("//food[name='" + safe + "']/vendor", accounts);
    }

    // 이어 붙이는 자리에서 바로 지워도 된다. 앞 리터럴이 작은따옴표를 여는 것(=')이 보인다
    @GetMapping(value = "/origin", produces = "text/plain;charset=UTF-8")
    public String origin(@RequestParam String name, @RequestParam String country) throws XPathExpressionException {
        XPath xpath = XPathFactory.newInstance().newXPath();
        // ok: mois-1-09-xpath-injection — 두 값 모두 작은따옴표 문자열 안에 들어가고, 지우는 집합에 작은따옴표가 있다
        return xpath.evaluate("//food[name='" + name.replaceAll("[']", "") + "' and country='" + country.replaceAll("[<>&'\"]", "") + "']/origin", accounts);
    }

    // 변수에 담은 값을 두 번째 조건에 넣는 경우, 함수 인자 자리(,')
    @GetMapping(value = "/search", produces = "text/plain;charset=UTF-8")
    public String search(@RequestParam String kind, @RequestParam String word) throws XPathExpressionException {
        String safeWord = word.replaceAll("[()\\-'\\[\\]:,*/]", "");
        XPath xpath = XPathFactory.newInstance().newXPath();
        // ok: mois-1-09-xpath-injection — 허용 문자만 남긴 값과, 작은따옴표를 지워 작은따옴표 문자열 안에 넣은 값
        return xpath.evaluate("//food[kind='" + kind.replaceAll("[^a-z]", "") + "' and contains(name, '" + safeWord + "')]/name", accounts);
    }

    // 따옴표 없는 숫자 자리에는 허용 문자만 남기는 형태만 인정된다
    @GetMapping(value = "/byId", produces = "text/plain;charset=UTF-8")
    public String byId(@RequestParam String id) throws XPathExpressionException {
        XPath xpath = XPathFactory.newInstance().newXPath();
        // ok: mois-1-09-xpath-injection — 숫자만 남는다
        return xpath.evaluate("//food[@id=" + id.replaceAll("[^0-9]", "") + "]/name", accounts);
    }
}
