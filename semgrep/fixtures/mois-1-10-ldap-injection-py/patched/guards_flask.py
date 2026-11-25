"""guard 형태별 안전한 예제 (Flask)."""
import re

import ldap
from flask import Flask, abort, current_app, request

app = Flask(__name__)
UID_RE = re.compile(r"[a-z0-9]{1,32}")


@app.route("/guard/abort")
def guard_abort():
    uid = request.args.get("uid", "")
    if not re.fullmatch(r"[a-z0-9]{1,32}", uid):
        abort(400)
    conn = ldap.initialize(current_app.config["LDAP_URI"])
    # ok: mois-1-10-ldap-injection-py 실패하면 abort
    conn.search_s(current_app.config["LDAP_BASE_DN"], ldap.SCOPE_SUBTREE, "(uid=" + uid + ")")
    return "ok"


@app.route("/guard/abort_empty")
def guard_abort_empty():
    uid = request.args.get("uid", "")
    if not uid or not uid.isalnum():
        abort(400)
    conn = ldap.initialize(current_app.config["LDAP_URI"])
    # ok: mois-1-10-ldap-injection-py 값이 없거나 실패하면 abort
    conn.search_s(current_app.config["LDAP_BASE_DN"], ldap.SCOPE_SUBTREE, "(uid=" + uid + ")")
    return "ok"
