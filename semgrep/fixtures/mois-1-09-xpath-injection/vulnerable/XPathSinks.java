package demo;

import javax.servlet.http.HttpServletRequest;
import javax.xml.xpath.XPath;
import javax.xml.xpath.XPathConstants;
import javax.xml.xpath.XPathFactory;
import javax.xml.xquery.XQConnection;
import javax.xml.xquery.XQExpression;
import org.w3c.dom.Node;

// sink 가지마다 한 줄씩: XPath 실행 메서드별, XPath 객체를 얻는 방식별, XQuery(XQJ)
public class XPathSinks {
    private XPath xpath;
    private XPathFactory factory;
    private XQConnection xqConnection;
    private XQExpression xqExpression;
    private Node doc;

    public void xpath(HttpServletRequest request) throws Exception {
        String query = "//user[@name='" + request.getParameter("name") + "']";
        // ruleid: mois-1-09-xpath-injection
        xpath.evaluate(query, doc, XPathConstants.NODESET);
        // ruleid: mois-1-09-xpath-injection
        xpath.evaluateExpression(query, doc);
        // XPath 객체를 변수에 담지 않고 바로 쓰는 형태
        // ruleid: mois-1-09-xpath-injection
        XPathFactory.newInstance().newXPath().compile(query);
        // ruleid: mois-1-09-xpath-injection
        XPathFactory.newInstance().newXPath().evaluate(query, doc);
        // ruleid: mois-1-09-xpath-injection
        factory.newXPath().compile(query);
        // ruleid: mois-1-09-xpath-injection
        factory.newXPath().evaluate(query, doc);
    }

    public void xquery(HttpServletRequest request) throws Exception {
        String query = "doc('users.xml')//user[@name='" + request.getParameter("name") + "']";
        // ruleid: mois-1-09-xpath-injection
        xqConnection.prepareExpression(query);
        // ruleid: mois-1-09-xpath-injection
        xqExpression.executeQuery(query);
        // ruleid: mois-1-09-xpath-injection
        xqExpression.executeCommand(query);
    }
}
