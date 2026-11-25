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

// 탐지돼야 하는 경우: 외부 엔티티 제한 설정 없이 XML 을 파싱. 파서 종류마다 한 줄씩
public class XmlParser {
    public Document unmarshal(File receivedXml) throws ParserConfigurationException, SAXException, IOException {
        DocumentBuilderFactory dbf = DocumentBuilderFactory.newInstance();
        dbf.setNamespaceAware(true);
        // ruleid: mois-1-08-xxe
        DocumentBuilder db = dbf.newDocumentBuilder();
        return db.parse(receivedXml);
    }

    public void sax(File xmlFile) throws ParserConfigurationException, SAXException, IOException {
        SAXParserFactory factory = SAXParserFactory.newInstance();
        // ruleid: mois-1-08-xxe
        SAXParser saxParser = factory.newSAXParser();
        try (FileInputStream in = new FileInputStream(xmlFile)) {
            saxParser.parse(in, new DefaultHandler());
        }
    }

    public XMLStreamReader stax(InputStream in) throws XMLStreamException {
        XMLInputFactory factory = XMLInputFactory.newFactory();
        // ruleid: mois-1-08-xxe
        return factory.createXMLStreamReader(in);
    }

    public XMLEventReader staxEvents(InputStream in) throws XMLStreamException {
        XMLInputFactory factory = XMLInputFactory.newInstance();
        // ruleid: mois-1-08-xxe
        return factory.createXMLEventReader(in);
    }

    public Transformer transformer(Source xslt) throws TransformerConfigurationException {
        TransformerFactory factory = TransformerFactory.newInstance();
        // ruleid: mois-1-08-xxe
        return factory.newTransformer(xslt);
    }

    public Templates templates(Source xslt) throws TransformerConfigurationException {
        TransformerFactory factory = TransformerFactory.newInstance();
        // ruleid: mois-1-08-xxe
        return factory.newTemplates(xslt);
    }

    public Schema schema(File xsd) throws SAXException {
        SchemaFactory factory = SchemaFactory.newInstance(XMLConstants.W3C_XML_SCHEMA_NS_URI);
        // ruleid: mois-1-08-xxe
        return factory.newSchema(xsd);
    }

    public org.dom4j.Document dom4j(File xmlFile) throws DocumentException {
        SAXReader reader = new SAXReader();
        // ruleid: mois-1-08-xxe
        return reader.read(xmlFile);
    }

    public void xmlReader(InputSource source) throws SAXException, IOException {
        XMLReader reader = XMLReaderFactory.createXMLReader();
        reader.setContentHandler(new DefaultHandler());
        // ruleid: mois-1-08-xxe
        reader.parse(source);
    }

    // 팩토리를 변수에 담지 않고 바로 파서를 얻는 경우: 설정할 방법이 없다
    public void chained(File xmlFile, InputStream in, Source xslt, InputSource source) throws Exception {
        // ruleid: mois-1-08-xxe
        Document a = DocumentBuilderFactory.newInstance().newDocumentBuilder().parse(xmlFile);
        // ruleid: mois-1-08-xxe
        SAXParser b = SAXParserFactory.newInstance().newSAXParser();
        // ruleid: mois-1-08-xxe
        XMLStreamReader c = XMLInputFactory.newInstance().createXMLStreamReader(in);
        // ruleid: mois-1-08-xxe
        XMLEventReader d = XMLInputFactory.newFactory().createXMLEventReader(in);
        // ruleid: mois-1-08-xxe
        Transformer e = TransformerFactory.newInstance().newTransformer(xslt);
        // ruleid: mois-1-08-xxe
        Templates f = TransformerFactory.newInstance().newTemplates(xslt);
        // ruleid: mois-1-08-xxe
        Schema g = SchemaFactory.newInstance(XMLConstants.W3C_XML_SCHEMA_NS_URI).newSchema(xmlFile);
        // ruleid: mois-1-08-xxe
        org.dom4j.Document h = new SAXReader().read(xmlFile);
        // ruleid: mois-1-08-xxe
        XMLReaderFactory.createXMLReader().parse(source);
    }
}
