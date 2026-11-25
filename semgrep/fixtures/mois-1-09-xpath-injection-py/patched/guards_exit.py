"""guard 형태별 안전한 예제 — import 로 확인되는 종료 호출(flask.abort·sys.exit).

내장 exit()·quit() 와 이름만 abort 인 함수는 vulnerable/ 쪽에 있다 (종료로 보지 않는다).
"""
import sys

import flask
from flask import Flask, request
from lxml import etree

app = Flask(__name__)
USERS_XML = "/srv/data/users.xml"
PARSER = etree.XMLParser(resolve_entities=False, no_network=True)


@app.route("/guard/flask_abort")
def guard_flask_abort():
    name = request.args.get("name", "")
    if not name.isalnum():
        flask.abort(400)
    tree = etree.parse(USERS_XML, PARSER)
    # ok: mois-1-09-xpath-injection-py 실패하면 flask.abort
    found = tree.xpath("//user[@name='" + name + "']")
    return str(len(found))


def guard_sys_exit():
    # 라우트가 아닌 일괄 작업용 보조 함수 (요청 문맥 안에서 호출된다)
    name = request.args.get("name", "")
    if not name.isalnum():
        sys.exit(2)
    tree = etree.parse(USERS_XML, PARSER)
    # ok: mois-1-09-xpath-injection-py 실패하면 sys.exit
    found = tree.xpath("//user[@name='" + name + "']")
    return str(len(found))
