package demo;

import javax.servlet.http.HttpServletRequest;
import javax.xml.xpath.XPath;
import javax.xml.xpath.XPathExpressionException;
import org.w3c.dom.Node;

// 문자를 지우기는 하지만 XPath 문자열을 벗어나는 문자를 막지 못하는 경우: 모두 탐지되어야 한다
public class XPathReplaceBypass {
    private XPath xpath;
    private Node doc;

    // 작은따옴표를 지우지 않는다
    public String quoteNotRemoved(HttpServletRequest request) throws XPathExpressionException {
        String name = request.getParameter("name").replaceAll("[()\\[\\]]", "");
        // ruleid: mois-1-09-xpath-injection
        return xpath.evaluate("//food[name='" + name + "']/price", doc);
    }

    // 공백만 지운다
    public String whitespaceOnly(HttpServletRequest request) throws XPathExpressionException {
        String name = request.getParameter("name").replaceAll("\\s", "");
        // ruleid: mois-1-09-xpath-injection
        return xpath.evaluate("//food[name='" + name + "']/price", doc);
    }

    // 남기는 문자에 따옴표가 들어 있다
    public String allowListKeepsQuote(HttpServletRequest request) throws XPathExpressionException {
        String name = request.getParameter("name").replaceAll("[^\\w']", "");
        // ruleid: mois-1-09-xpath-injection
        return xpath.evaluate("//food[name='" + name + "']/price", doc);
    }

    // 남기는 범위가 넓어 따옴표가 포함된다 (공백 ~ 물결표)
    public String allowListRangeTooWide(HttpServletRequest request) throws XPathExpressionException {
        String name = request.getParameter("name").replaceAll("[^ -~]", "");
        // ruleid: mois-1-09-xpath-injection
        return xpath.evaluate("//food[name='" + name + "']/price", doc);
    }

    // 지우지 않고 다른 문자열로 바꾼다 (XPath 1.0 에는 따옴표 이스케이프가 없다)
    public String replacedNotRemoved(HttpServletRequest request) throws XPathExpressionException {
        String name = request.getParameter("name").replaceAll("[']", "&apos;");
        // ruleid: mois-1-09-xpath-injection
        return xpath.evaluate("//food[name='" + name + "']/price", doc);
    }

    // 정규식이 리터럴이 아니어서 무엇을 지우는지 알 수 없다
    public String patternNotLiteral(HttpServletRequest request, String pattern) throws XPathExpressionException {
        String name = request.getParameter("name").replaceAll(pattern, "");
        // ruleid: mois-1-09-xpath-injection
        return xpath.evaluate("//food[name='" + name + "']/price", doc);
    }

    // 지운 결과를 버리고 원래 값을 쓴다
    public String resultIgnored(HttpServletRequest request) throws XPathExpressionException {
        String name = request.getParameter("name");
        name.replaceAll("[()\\-'\\[\\]:,*/]", "");
        // ruleid: mois-1-09-xpath-injection
        return xpath.evaluate("//food[name='" + name + "']/price", doc);
    }

    // --- 지우는 문자는 맞지만 넣는 자리가 다르다 (v0.6.1) ---

    // 작은따옴표만 지웠는데 큰따옴표 문자열 안에 넣는다: " or "1"="1 로 벗어난다
    public String wrongQuote(HttpServletRequest request) throws XPathExpressionException {
        String name = request.getParameter("name");
        // ruleid: mois-1-09-xpath-injection
        return xpath.evaluate("//user[@name=\"" + name.replaceAll("[']", "") + "\"]/secret", doc);
    }

    // 따옴표 없는 숫자 자리: 따옴표를 지워도 1 or 1=1 은 그대로 들어간다
    public String unquotedPosition(HttpServletRequest request) throws XPathExpressionException {
        String id = request.getParameter("id");
        // ruleid: mois-1-09-xpath-injection
        return xpath.evaluate("//user[@id=" + id.replaceAll("[()\\-'\\[\\]:,*/]", "") + "]/secret", doc);
    }

    // 변수에 담아 두어도 같다: 따옴표 없는 자리, 큰따옴표 자리
    public String unquotedVariable(HttpServletRequest request) throws XPathExpressionException {
        String id = request.getParameter("id").replaceAll("[()\\-'\\[\\]:,*/]", "");
        // ruleid: mois-1-09-xpath-injection
        String byId = xpath.evaluate("//user[@id=" + id + "]/secret", doc);
        // ruleid: mois-1-09-xpath-injection
        return byId + xpath.evaluate("//user[@name=\"" + id + "\"]/secret", doc);
    }

    // 앞 리터럴이 작은따옴표로 끝나도 여는 따옴표(=' (' ,')가 아니면 문자열 안이라고 볼 수 없다
    public String afterClosingQuote(HttpServletRequest request) throws XPathExpressionException {
        String id = request.getParameter("id");
        // ruleid: mois-1-09-xpath-injection
        return xpath.evaluate("//user[@type='admin'" + id.replaceAll("[']", "") + "]/secret", doc);
    }

    // 지운 뒤에 다른 입력을 다시 대입
    public String reassigned(HttpServletRequest request) throws XPathExpressionException {
        String name = request.getParameter("name").replaceAll("[']", "");
        name = request.getParameter("other");
        // ruleid: mois-1-09-xpath-injection
        return xpath.evaluate("//food[name='" + name + "']/price", doc);
    }

    // 지운 뒤에 다른 입력을 덧붙임
    public String appended(HttpServletRequest request) throws XPathExpressionException {
        String name = request.getParameter("name").replaceAll("[']", "");
        name += request.getParameter("other");
        // ruleid: mois-1-09-xpath-injection
        return xpath.evaluate("//food[name='" + name + "']/price", doc);
    }

    // 조건이 맞을 때만 지움: 지우지 않은 값이 그대로 올 수 있다
    public String conditional(HttpServletRequest request, boolean strict) throws XPathExpressionException {
        String name = request.getParameter("name");
        if (strict) {
            name = name.replaceAll("[']", "");
        }
        // ruleid: mois-1-09-xpath-injection
        return xpath.evaluate("//food[name='" + name + "']/price", doc);
    }

    // 지우는 문장의 오른쪽에 든 name 은 아직 지우기 전 값이고, 결과는 따옴표 없는 자리에 들어간다
    public String selfReference(HttpServletRequest request) throws XPathExpressionException {
        String name = request.getParameter("name");
        name = ("x='" + name + "'").replaceAll("[']", "");
        // ruleid: mois-1-09-xpath-injection
        return xpath.evaluate("//food[" + name + "]/price", doc);
    }

    // 객체의 필드: 지운 뒤에 변수가 다른 객체를 가리키면 필드 값도 달라진다 (단순 변수만 인정한다)
    public String fieldOfAnotherObject(HttpServletRequest request) throws XPathExpressionException {
        Holder h = new Holder();
        h.name = request.getParameter("name").replaceAll("[']", "");
        h = new Holder(request.getParameter("other"));
        // ruleid: mois-1-09-xpath-injection
        return xpath.evaluate("//food[name='" + h.name + "']/price", doc);
    }

    // --- 문자 집합이 보이는 것과 다르다 ---

    // && 교집합: ' 와 a 의 교집합은 비어 있어 아무것도 지우지 않는다
    public String intersection(HttpServletRequest request) throws XPathExpressionException {
        String name = request.getParameter("name");
        // ruleid: mois-1-09-xpath-injection
        return xpath.evaluate("//food[name='" + name.replaceAll("['&&a]", "") + "']/price", doc);
    }

    // 부정 문자 집합: 작은따옴표만 남기고 나머지를 지운다
    public String negatedClass(HttpServletRequest request) throws XPathExpressionException {
        String name = request.getParameter("name");
        // ruleid: mois-1-09-xpath-injection
        return xpath.evaluate("//food[name='" + name.replaceAll("[^']", "") + "']/price", doc);
    }

    // \c' 는 따옴표가 아니라 제어 문자다
    public String controlEscape(HttpServletRequest request) throws XPathExpressionException {
        String name = request.getParameter("name");
        // ruleid: mois-1-09-xpath-injection
        return xpath.evaluate("//food[name='" + name.replaceAll("[\\c']", "") + "']/price", doc);
    }

    // 남기는 범위가 넓다: 0-z 에는 @ = [ ] 가 들어 있어 따옴표 없는 자리에서 [@id=@id] 가 된다
    public String allowListRangeKeepsOperators(HttpServletRequest request) throws XPathExpressionException {
        String id = request.getParameter("id");
        // ruleid: mois-1-09-xpath-injection
        return xpath.evaluate("//user[@id=" + id.replaceAll("[^0-z]", "") + "]/secret", doc);
    }

    // 역슬래시 4개: \w 가 아니라 역슬래시와 w 두 글자만 남긴다 (값은 못 쓰게 되지만 허용 목록으로 증명되는 형태가 아니다)
    public String allowListBackslashW(HttpServletRequest request) throws XPathExpressionException {
        String id = request.getParameter("id");
        // ruleid: mois-1-09-xpath-injection
        return xpath.evaluate("//user[@id=" + id.replaceAll("[^\\\\w]", "") + "]/secret", doc);
    }

    static class Holder {
        String name;

        Holder() {
        }

        Holder(String name) {
            this.name = name;
        }
    }
}
