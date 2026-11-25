"""guard 형태별 안전한 예제 — 문자 종류 검사별(isdigit·isdecimal·isalpha·isidentifier)."""
from flask import Flask, request
from lxml import etree

app = Flask(__name__)
USERS_XML = "/srv/data/users.xml"
PARSER = etree.XMLParser(resolve_entities=False, no_network=True)


@app.route("/guard/isdigit")
def guard_isdigit():
    name = request.args.get("name", "")
    if not name.isdigit():
        return "invalid", 400
    tree = etree.parse(USERS_XML, PARSER)
    # ok: mois-1-09-xpath-injection-py 숫자만 통과 (실패하면 return)
    found = tree.xpath("//user[@name='" + name + "']")
    return str(len(found))


@app.route("/inside/isdigit")
def inside_isdigit():
    name = request.args.get("name", "")
    if name.isdigit():
        tree = etree.parse(USERS_XML, PARSER)
        # ok: mois-1-09-xpath-injection-py 숫자만 통과한 조건 안에서만 사용
        found = tree.xpath("//user[@name='" + name + "']")
    return "ok"


@app.route("/guard/isdecimal")
def guard_isdecimal():
    name = request.args.get("name", "")
    if not name.isdecimal():
        return "invalid", 400
    tree = etree.parse(USERS_XML, PARSER)
    # ok: mois-1-09-xpath-injection-py 10진 숫자만 통과 (실패하면 return)
    found = tree.xpath("//user[@name='" + name + "']")
    return str(len(found))


@app.route("/inside/isdecimal")
def inside_isdecimal():
    name = request.args.get("name", "")
    if name.isdecimal():
        tree = etree.parse(USERS_XML, PARSER)
        # ok: mois-1-09-xpath-injection-py 10진 숫자만 통과한 조건 안에서만 사용
        found = tree.xpath("//user[@name='" + name + "']")
    return "ok"


@app.route("/guard/isalpha")
def guard_isalpha():
    name = request.args.get("name", "")
    if not name.isalpha():
        return "invalid", 400
    tree = etree.parse(USERS_XML, PARSER)
    # ok: mois-1-09-xpath-injection-py 글자만 통과 (실패하면 return)
    found = tree.xpath("//user[@name='" + name + "']")
    return str(len(found))


@app.route("/inside/isalpha")
def inside_isalpha():
    name = request.args.get("name", "")
    if name.isalpha():
        tree = etree.parse(USERS_XML, PARSER)
        # ok: mois-1-09-xpath-injection-py 글자만 통과한 조건 안에서만 사용
        found = tree.xpath("//user[@name='" + name + "']")
    return "ok"


@app.route("/guard/isidentifier")
def guard_isidentifier():
    name = request.args.get("name", "")
    if not name.isidentifier():
        return "invalid", 400
    tree = etree.parse(USERS_XML, PARSER)
    # ok: mois-1-09-xpath-injection-py 식별자 문자만 통과 (실패하면 return)
    found = tree.xpath("//user[@name='" + name + "']")
    return str(len(found))


@app.route("/inside/isidentifier")
def inside_isidentifier():
    name = request.args.get("name", "")
    if name.isidentifier():
        tree = etree.parse(USERS_XML, PARSER)
        # ok: mois-1-09-xpath-injection-py 식별자 문자만 통과한 조건 안에서만 사용
        found = tree.xpath("//user[@name='" + name + "']")
    return "ok"
