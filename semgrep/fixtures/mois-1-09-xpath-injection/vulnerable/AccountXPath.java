package demo;

import javax.servlet.http.HttpServletRequest;
import javax.xml.xpath.XPath;
import javax.xml.xpath.XPathConstants;
import javax.xml.xpath.XPathExpression;
import javax.xml.xpath.XPathExpressionException;
import javax.xml.xpath.XPathFactory;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import org.w3c.dom.Node;

// 탐지돼야 하는 경우: 외부 입력을 XPath 질의문에 이어 붙임
@RestController
public class AccountXPath {
    private final Node accounts;

    public AccountXPath(Node accounts) {
        this.accounts = accounts;
    }

    // 진단가이드 정탐 예: StringBuffer 로 조립한 질의문을 compile
    public Object email(HttpServletRequest request) throws XPathExpressionException {
        String acctID = request.getParameter("acctID");
        StringBuffer sb = new StringBuffer("/accounts/account[acctID='");
        sb.append(acctID);
        sb.append("']/email/text()");
        XPath xpath = XPathFactory.newInstance().newXPath();
        // ruleid: mois-1-09-xpath-injection
        XPathExpression expr = xpath.compile(sb.toString());
        return expr.evaluate(accounts, XPathConstants.NODESET);
    }

    @GetMapping("/price")
    public String price(@RequestParam String name) throws XPathExpressionException {
        XPath xpath = XPathFactory.newInstance().newXPath();
        // ruleid: mois-1-09-xpath-injection
        return xpath.evaluate("//food[name='" + name + "']/price", accounts);
    }
}
