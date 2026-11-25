package demo;

import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStream;
import javax.xml.XMLConstants;
import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.parsers.ParserConfigurationException;
import javax.xml.parsers.SAXParser;
import javax.xml.parsers.SAXParserFactory;
import javax.xml.stream.XMLEventReader;
import javax.xml.stream.XMLInputFactory;
import javax.xml.stream.XMLStreamException;
import javax.xml.stream.XMLStreamReader;
import javax.xml.transform.Source;
import javax.xml.transform.Templates;
import javax.xml.transform.Transformer;
import javax.xml.transform.TransformerConfigurationException;
import javax.xml.transform.TransformerFactory;
import javax.xml.validation.Schema;
import javax.xml.validation.SchemaFactory;
import org.dom4j.DocumentException;
import org.dom4j.io.SAXReader;
import org.w3c.dom.Document;
import org.xml.sax.InputSource;
import org.xml.sax.SAXException;
import org.xml.sax.XMLReader;
import org.xml.sax.helpers.DefaultHandler;
import org.xml.sax.helpers.XMLReaderFactory;

// 탐지되면 안 되는 경우: 파서를 얻기 전에, 그 팩토리에 DTD·외부 엔티티 제한을 건다
public class XmlParser {
    private static final String DISALLOW_DOCTYPE = "http://apache.org/xml/features/disallow-doctype-decl";

    public Document unmarshal(File receivedXml) throws ParserConfigurationException, SAXException, IOException {
        DocumentBuilderFactory dbf = DocumentBuilderFactory.newInstance();
        dbf.setFeature("http://apache.org/xml/features/disallow-doctype-decl", true);
        dbf.setXIncludeAware(false);
        dbf.setExpandEntityReferences(false);
        // ok: mois-1-08-xxe — 같은 팩토리에 DOCTYPE 금지를 먼저 설정
        DocumentBuilder db = dbf.newDocumentBuilder();
        return db.parse(receivedXml);
    }

    public Document byConstant(File receivedXml) throws ParserConfigurationException, SAXException, IOException {
        DocumentBuilderFactory dbf = DocumentBuilderFactory.newInstance();
        dbf.setFeature(DISALLOW_DOCTYPE, true);
        // ok: mois-1-08-xxe — 기능 이름을 상수로 둔 경우도 같은 설정으로 본다
        return dbf.newDocumentBuilder().parse(receivedXml);
    }

    public Document entitiesOff(File receivedXml) throws ParserConfigurationException, SAXException, IOException {
        DocumentBuilderFactory dbf = DocumentBuilderFactory.newInstance();
        dbf.setFeature("http://xml.org/sax/features/external-general-entities", false);
        dbf.setFeature("http://xml.org/sax/features/external-parameter-entities", false);
        dbf.setFeature("http://apache.org/xml/features/nonvalidating/load-external-dtd", false);
        // ok: mois-1-08-xxe — 일반·파라미터 엔티티를 둘 다 끔
        return dbf.newDocumentBuilder().parse(receivedXml);
    }

    public Document accessRestricted(File receivedXml) throws ParserConfigurationException, SAXException, IOException {
        DocumentBuilderFactory dbf = DocumentBuilderFactory.newInstance();
        dbf.setAttribute(XMLConstants.ACCESS_EXTERNAL_DTD, "");
        dbf.setAttribute(XMLConstants.ACCESS_EXTERNAL_SCHEMA, "");
        // ok: mois-1-08-xxe — 외부 DTD 접근 프로토콜을 비움
        return dbf.newDocumentBuilder().parse(receivedXml);
    }

    public void sax(File xmlFile) throws ParserConfigurationException, SAXException, IOException {
        SAXParserFactory factory = SAXParserFactory.newInstance();
        // ok: mois-1-08-xxe — 이 팩토리에서 얻은 파서에 바로 접근 제한을 건다
        SAXParser parser = factory.newSAXParser();
        parser.setProperty(XMLConstants.ACCESS_EXTERNAL_DTD, "");
        parser.setProperty(XMLConstants.ACCESS_EXTERNAL_SCHEMA, "");
        try (FileInputStream in = new FileInputStream(xmlFile)) {
            parser.parse(in, new DefaultHandler());
        }
    }

    public void saxByName(File xmlFile) throws ParserConfigurationException, SAXException, IOException {
        SAXParserFactory factory = SAXParserFactory.newInstance();
        // ok: mois-1-08-xxe — 속성 이름을 문자열로 적은 경우
        SAXParser parser = factory.newSAXParser();
        parser.setProperty("http://javax.xml.XMLConstants/property/accessExternalDTD", "");
        parser.parse(xmlFile, new DefaultHandler());
    }

    public void saxChained(File xmlFile) throws ParserConfigurationException, SAXException, IOException {
        // ok: mois-1-08-xxe — 바로 얻은 파서에도 접근 제한을 걸 수 있다
        SAXParser parser = SAXParserFactory.newInstance().newSAXParser();
        parser.setProperty(XMLConstants.ACCESS_EXTERNAL_DTD, "");
        parser.parse(xmlFile, new DefaultHandler());
    }

    public void saxChainedByName(File xmlFile) throws ParserConfigurationException, SAXException, IOException {
        // ok: mois-1-08-xxe
        SAXParser parser = SAXParserFactory.newInstance().newSAXParser();
        parser.setProperty("http://javax.xml.XMLConstants/property/accessExternalDTD", "");
        parser.parse(xmlFile, new DefaultHandler());
    }

    public void saxEntitiesOff(File xmlFile) throws ParserConfigurationException, SAXException, IOException {
        SAXParserFactory factory = SAXParserFactory.newInstance();
        factory.setFeature("http://xml.org/sax/features/external-parameter-entities", false);
        factory.setFeature("http://xml.org/sax/features/external-general-entities", false);
        // ok: mois-1-08-xxe — 설정 순서는 상관없다
        factory.newSAXParser().parse(xmlFile, new DefaultHandler());
    }

    public XMLStreamReader stax(InputStream in) throws XMLStreamException {
        XMLInputFactory factory = XMLInputFactory.newFactory();
        factory.setProperty(XMLInputFactory.SUPPORT_DTD, false);
        // ok: mois-1-08-xxe — DTD 지원을 끔
        return factory.createXMLStreamReader(in);
    }

    public XMLStreamReader staxByName(InputStream in) throws XMLStreamException {
        XMLInputFactory factory = XMLInputFactory.newFactory();
        factory.setProperty("javax.xml.stream.supportDTD", Boolean.FALSE);
        // ok: mois-1-08-xxe
        return factory.createXMLStreamReader(in);
    }

    public XMLEventReader staxEntitiesOff(InputStream in) throws XMLStreamException {
        XMLInputFactory factory = XMLInputFactory.newInstance();
        factory.setProperty(XMLInputFactory.IS_SUPPORTING_EXTERNAL_ENTITIES, Boolean.FALSE);
        // ok: mois-1-08-xxe — 외부 엔티티를 끔
        return factory.createXMLEventReader(in);
    }

    public XMLEventReader staxEntitiesOffByName(InputStream in) throws XMLStreamException {
        XMLInputFactory factory = XMLInputFactory.newInstance();
        factory.setProperty("javax.xml.stream.isSupportingExternalEntities", false);
        // ok: mois-1-08-xxe
        return factory.createXMLEventReader(in);
    }

    public Transformer transformer(Source xslt) throws TransformerConfigurationException {
        TransformerFactory factory = TransformerFactory.newInstance();
        factory.setAttribute("http://javax.xml.XMLConstants/property/accessExternalDTD", "");
        factory.setAttribute("http://javax.xml.XMLConstants/property/accessExternalStylesheet", "");
        // ok: mois-1-08-xxe
        return factory.newTransformer(xslt);
    }

    public Templates templates(Source xslt) throws TransformerConfigurationException {
        TransformerFactory factory = TransformerFactory.newInstance();
        factory.setAttribute(XMLConstants.ACCESS_EXTERNAL_DTD, "");
        factory.setAttribute(XMLConstants.ACCESS_EXTERNAL_STYLESHEET, "");
        // ok: mois-1-08-xxe
        return factory.newTemplates(xslt);
    }

    public Schema schema(File xsd) throws SAXException {
        SchemaFactory factory = SchemaFactory.newInstance(XMLConstants.W3C_XML_SCHEMA_NS_URI);
        factory.setProperty(XMLConstants.ACCESS_EXTERNAL_DTD, "");
        factory.setProperty(XMLConstants.ACCESS_EXTERNAL_SCHEMA, "");
        // ok: mois-1-08-xxe
        return factory.newSchema(xsd);
    }

    public org.dom4j.Document dom4j(File xmlFile) throws DocumentException, SAXException {
        SAXReader reader = new SAXReader();
        reader.setFeature("http://apache.org/xml/features/disallow-doctype-decl", true);
        // ok: mois-1-08-xxe
        return reader.read(xmlFile);
    }

    public void xmlReader(InputSource source) throws SAXException, IOException {
        XMLReader reader = XMLReaderFactory.createXMLReader();
        reader.setFeature("http://apache.org/xml/features/disallow-doctype-decl", true);
        // ok: mois-1-08-xxe
        reader.parse(source);
    }
}
