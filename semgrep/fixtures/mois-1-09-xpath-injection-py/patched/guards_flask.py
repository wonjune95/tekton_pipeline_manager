"""guard 형태별 안전한 예제 (Flask)."""
import re

from flask import Flask, abort, request
from lxml import etree

app = Flask(__name__)
USERS_XML = "/srv/data/users.xml"
PARSER = etree.XMLParser(resolve_entities=False, no_network=True)
NAME_RE = re.compile(r"[A-Za-z0-9_]{1,40}")


@app.route("/guard/abort")
def guard_abort():
    name = request.args.get("name", "")
    if not re.fullmatch(r"[A-Za-z0-9_]{1,40}", name):
        abort(400)
    tree = etree.parse(USERS_XML, PARSER)
    # ok: mois-1-09-xpath-injection-py 실패하면 abort
    tree.xpath("//user[@name='" + name + "']")
    return "ok"


@app.route("/guard/abort_empty")
def guard_abort_empty():
    name = request.args.get("name", "")
    if not name or not name.isalnum():
        abort(400)
    tree = etree.parse(USERS_XML, PARSER)
    # ok: mois-1-09-xpath-injection-py 값이 없거나 실패하면 abort
    tree.xpath("//user[@name='" + name + "']")
    return "ok"
