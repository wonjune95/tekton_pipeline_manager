"""guard 형태별 안전한 예제 — import 로 확인되는 종료 호출(flask.abort·sys.exit).

내장 exit()·quit() 와 이름만 abort 인 함수는 vulnerable/ 쪽에 있다 (종료로 보지 않는다).
"""
import sys

import flask
import ldap
from flask import Flask, current_app, request

app = Flask(__name__)


@app.route("/guard/flask_abort")
def guard_flask_abort():
    uid = request.args.get("uid", "")
    if not uid.isalnum():
        flask.abort(400)
    conn = ldap.initialize(current_app.config["LDAP_URI"])
    # ok: mois-1-10-ldap-injection-py 실패하면 flask.abort
    found = conn.search_s(current_app.config["LDAP_BASE_DN"], ldap.SCOPE_SUBTREE, "(uid=" + uid + ")")
    return str(len(found))


def guard_sys_exit():
    # 라우트가 아닌 일괄 작업용 보조 함수 (요청 문맥 안에서 호출된다)
    uid = request.args.get("uid", "")
    if not uid.isalnum():
        sys.exit(2)
    conn = ldap.initialize(current_app.config["LDAP_URI"])
    # ok: mois-1-10-ldap-injection-py 실패하면 sys.exit
    found = conn.search_s(current_app.config["LDAP_BASE_DN"], ldap.SCOPE_SUBTREE, "(uid=" + uid + ")")
    return str(len(found))
