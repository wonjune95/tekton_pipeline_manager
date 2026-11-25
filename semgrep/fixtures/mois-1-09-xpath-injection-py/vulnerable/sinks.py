import xml.etree.ElementTree as ET

import elementpath
from flask import Flask, request
from lxml import etree
from parsel import Selector

app = Flask(__name__)
USERS_XML = "/srv/data/users.xml"
PARSER = etree.XMLParser(resolve_entities=False, no_network=True)


@app.route("/lxml/compiled")
def lxml_compiled():
    name = request.args["name"]
    tree = etree.parse(USERS_XML, PARSER)
    # 질의문을 미리 컴파일하는 클래스
    # ruleid: mois-1-09-xpath-injection-py
    find = etree.XPath("//user[@name='" + name + "']")
    # ruleid: mois-1-09-xpath-injection-py
    find_ns = etree.ETXPath("//{urn:example}user[@name='%s']" % name)
    # ruleid: mois-1-09-xpath-injection-py
    hits = etree.XPathEvaluator(tree)(f"count(//user[@name='{name}'])")
    return {"a": len(find(tree)), "b": len(find_ns(tree)), "c": hits}


@app.route("/elementpath")
def elementpath_select():
    role = request.args["role"]
    root = ET.parse(USERS_XML).getroot()
    # ruleid: mois-1-09-xpath-injection-py
    nodes = elementpath.select(root, "//user[role='" + role + "']/name")
    return {"names": [n.text for n in nodes]}


@app.route("/parsel", methods=["POST"])
def parsel_selector():
    tag = request.form["tag"]
    sel = Selector(text=request.form["html"])
    # parsel·scrapy 의 xpath()
    # ruleid: mois-1-09-xpath-injection-py
    return {"values": sel.xpath("//" + tag + "/text()").getall()}


@app.route("/etree/find")
def etree_find():
    uid = request.args["uid"]
    root = ET.parse(USERS_XML).getroot()
    # 속성 조건 [@…]
    # ruleid: mois-1-09-xpath-injection-py
    node = root.find("user[@id='" + uid + "']")
    # 자식 값 조건 [태그=…]
    # ruleid: mois-1-09-xpath-injection-py
    mail = root.findtext(f"user[uid='{uid}']/mail")
    # 자기 값 조건 [.=…]
    # ruleid: mois-1-09-xpath-injection-py
    same = list(root.iterfind("user/uid[.='%s']" % uid))
    # 모든 깊이 검색 (.//) 에 태그 이름을 붙임
    # ruleid: mois-1-09-xpath-injection-py
    nested = root.findall(".//" + uid)
    return {"found": node is not None, "mail": mail, "same": len(same), "nested": len(nested)}


@app.route("/etree/variable")
def etree_variable():
    dept = request.args["dept"]
    root = ET.parse(USERS_XML).getroot()
    path = "dept[@code='{}']/user".format(dept)
    # 변수에 담은 경로식
    # ruleid: mois-1-09-xpath-injection-py
    return {"count": len(root.findall(path))}
