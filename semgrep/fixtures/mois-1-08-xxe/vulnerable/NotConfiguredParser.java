package demo;

import java.io.File;
import java.io.IOException;
import java.io.InputStream;
import java.util.logging.Logger;
import javax.xml.XMLConstants;
import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.parsers.ParserConfigurationException;
import javax.xml.parsers.SAXParser;
import javax.xml.parsers.SAXParserFactory;
import javax.xml.stream.XMLInputFactory;
import javax.xml.stream.XMLStreamException;
import javax.xml.stream.XMLStreamReader;
import org.w3c.dom.Document;
import org.xml.sax.SAXException;

// 탐지돼야 하는 경우: 제한 설정이 있어 보이지만 이 파서에는 적용되지 않는 형태
public class NotConfiguredParser {
    private static final Logger LOG = Logger.getLogger("xml");

    // 같은 메서드의 다른 팩토리에만 설정
    public Document otherFactory(File trusted, File received) throws ParserConfigurationException, SAXException, IOException {
        DocumentBuilderFactory safe = DocumentBuilderFactory.newInstance();
        safe.setFeature("http://apache.org/xml/features/disallow-doctype-decl", true);
        safe.newDocumentBuilder().parse(trusted);

        DocumentBuilderFactory plain = DocumentBuilderFactory.newInstance();
        // ruleid: mois-1-08-xxe
        return plain.newDocumentBuilder().parse(received);
    }

    // 파서를 얻은 뒤에 설정: 이미 만들어진 파서에는 적용되지 않는다
    public Document configuredTooLate(File received) throws ParserConfigurationException, SAXException, IOException {
        DocumentBuilderFactory dbf = DocumentBuilderFactory.newInstance();
        // ruleid: mois-1-08-xxe
        DocumentBuilder db = dbf.newDocumentBuilder();
        dbf.setFeature("http://apache.org/xml/features/disallow-doctype-decl", true);
        return db.parse(received);
    }

    // 조건이 맞을 때만 설정
    public Document conditional(File received, boolean strict) throws ParserConfigurationException, SAXException, IOException {
        DocumentBuilderFactory dbf = DocumentBuilderFactory.newInstance();
        if (strict) {
            dbf.setFeature("http://apache.org/xml/features/disallow-doctype-decl", true);
        }
        // ruleid: mois-1-08-xxe
        return dbf.newDocumentBuilder().parse(received);
    }

    // 설정에 실패해도 기록만 하고 계속 진행
    public Document failureIgnored(File received) throws ParserConfigurationException, SAXException, IOException {
        DocumentBuilderFactory dbf = DocumentBuilderFactory.newInstance();
        try {
            dbf.setFeature("http://apache.org/xml/features/disallow-doctype-decl", true);
        } catch (ParserConfigurationException e) {
            LOG.warning("disallow-doctype-decl 을 지원하지 않는 파서");
        }
        // ruleid: mois-1-08-xxe
        return dbf.newDocumentBuilder().parse(received);
    }

    // 값이 반대: DOCTYPE 을 허용
    public Document wrongValue(File received) throws ParserConfigurationException, SAXException, IOException {
        DocumentBuilderFactory dbf = DocumentBuilderFactory.newInstance();
        dbf.setFeature("http://apache.org/xml/features/disallow-doctype-decl", false);
        // ruleid: mois-1-08-xxe
        return dbf.newDocumentBuilder().parse(received);
    }

    // 일반 엔티티만 끔: 파라미터 엔티티로 외부 DTD 를 읽을 수 있다
    public Document generalEntitiesOnly(File received) throws ParserConfigurationException, SAXException, IOException {
        DocumentBuilderFactory dbf = DocumentBuilderFactory.newInstance();
        dbf.setFeature("http://xml.org/sax/features/external-general-entities", false);
        // ruleid: mois-1-08-xxe
        return dbf.newDocumentBuilder().parse(received);
    }

    // FEATURE_SECURE_PROCESSING 만 켬: 구현체에 따라 외부 엔티티를 막지 못한다
    public Document secureProcessingOnly(File received) throws ParserConfigurationException, SAXException, IOException {
        DocumentBuilderFactory dbf = DocumentBuilderFactory.newInstance();
        dbf.setFeature(XMLConstants.FEATURE_SECURE_PROCESSING, true);
        // ruleid: mois-1-08-xxe
        return dbf.newDocumentBuilder().parse(received);
    }

    // 접근 허용 프로토콜을 비우지 않음
    public Document accessAll(File received) throws ParserConfigurationException, SAXException, IOException {
        DocumentBuilderFactory dbf = DocumentBuilderFactory.newInstance();
        dbf.setAttribute(XMLConstants.ACCESS_EXTERNAL_DTD, "all");
        // ruleid: mois-1-08-xxe
        return dbf.newDocumentBuilder().parse(received);
    }

    // StAX: DTD 지원을 켬
    public XMLStreamReader dtdSupported(InputStream in) throws XMLStreamException {
        XMLInputFactory factory = XMLInputFactory.newFactory();
        factory.setProperty(XMLInputFactory.SUPPORT_DTD, true);
        // ruleid: mois-1-08-xxe
        return factory.createXMLStreamReader(in);
    }

    // SAX: 다른 파서에만 접근 제한을 건다
    public SAXParser otherParser() throws ParserConfigurationException, SAXException {
        SAXParserFactory factory = SAXParserFactory.newInstance();
        SAXParser first = factory.newSAXParser();
        first.setProperty(XMLConstants.ACCESS_EXTERNAL_DTD, "");
        // ruleid: mois-1-08-xxe
        SAXParser second = factory.newSAXParser();
        return second;
    }
}
