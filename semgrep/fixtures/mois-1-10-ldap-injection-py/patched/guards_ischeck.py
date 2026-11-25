"""guard 형태별 안전한 예제 — 문자 종류 검사별(isdigit·isdecimal·isalpha·isidentifier)."""
import ldap
from flask import Flask, current_app, request

app = Flask(__name__)


@app.route("/guard/isdigit")
def guard_isdigit():
    uid = request.args.get("uid", "")
    if not uid.isdigit():
        return "invalid", 400
    conn = ldap.initialize(current_app.config["LDAP_URI"])
    # ok: mois-1-10-ldap-injection-py 숫자만 통과 (실패하면 return)
    found = conn.search_s(current_app.config["LDAP_BASE_DN"], ldap.SCOPE_SUBTREE, "(uid=" + uid + ")")
    return str(len(found))


@app.route("/inside/isdigit")
def inside_isdigit():
    uid = request.args.get("uid", "")
    if uid.isdigit():
        conn = ldap.initialize(current_app.config["LDAP_URI"])
        # ok: mois-1-10-ldap-injection-py 숫자만 통과한 조건 안에서만 사용
        found = conn.search_s(current_app.config["LDAP_BASE_DN"], ldap.SCOPE_SUBTREE, "(uid=" + uid + ")")
    return "ok"


@app.route("/guard/isdecimal")
def guard_isdecimal():
    uid = request.args.get("uid", "")
    if not uid.isdecimal():
        return "invalid", 400
    conn = ldap.initialize(current_app.config["LDAP_URI"])
    # ok: mois-1-10-ldap-injection-py 10진 숫자만 통과 (실패하면 return)
    found = conn.search_s(current_app.config["LDAP_BASE_DN"], ldap.SCOPE_SUBTREE, "(uid=" + uid + ")")
    return str(len(found))


@app.route("/inside/isdecimal")
def inside_isdecimal():
    uid = request.args.get("uid", "")
    if uid.isdecimal():
        conn = ldap.initialize(current_app.config["LDAP_URI"])
        # ok: mois-1-10-ldap-injection-py 10진 숫자만 통과한 조건 안에서만 사용
        found = conn.search_s(current_app.config["LDAP_BASE_DN"], ldap.SCOPE_SUBTREE, "(uid=" + uid + ")")
    return "ok"


@app.route("/guard/isalpha")
def guard_isalpha():
    uid = request.args.get("uid", "")
    if not uid.isalpha():
        return "invalid", 400
    conn = ldap.initialize(current_app.config["LDAP_URI"])
    # ok: mois-1-10-ldap-injection-py 글자만 통과 (실패하면 return)
    found = conn.search_s(current_app.config["LDAP_BASE_DN"], ldap.SCOPE_SUBTREE, "(uid=" + uid + ")")
    return str(len(found))


@app.route("/inside/isalpha")
def inside_isalpha():
    uid = request.args.get("uid", "")
    if uid.isalpha():
        conn = ldap.initialize(current_app.config["LDAP_URI"])
        # ok: mois-1-10-ldap-injection-py 글자만 통과한 조건 안에서만 사용
        found = conn.search_s(current_app.config["LDAP_BASE_DN"], ldap.SCOPE_SUBTREE, "(uid=" + uid + ")")
    return "ok"


@app.route("/guard/isidentifier")
def guard_isidentifier():
    uid = request.args.get("uid", "")
    if not uid.isidentifier():
        return "invalid", 400
    conn = ldap.initialize(current_app.config["LDAP_URI"])
    # ok: mois-1-10-ldap-injection-py 식별자 문자만 통과 (실패하면 return)
    found = conn.search_s(current_app.config["LDAP_BASE_DN"], ldap.SCOPE_SUBTREE, "(uid=" + uid + ")")
    return str(len(found))


@app.route("/inside/isidentifier")
def inside_isidentifier():
    uid = request.args.get("uid", "")
    if uid.isidentifier():
        conn = ldap.initialize(current_app.config["LDAP_URI"])
        # ok: mois-1-10-ldap-injection-py 식별자 문자만 통과한 조건 안에서만 사용
        found = conn.search_s(current_app.config["LDAP_BASE_DN"], ldap.SCOPE_SUBTREE, "(uid=" + uid + ")")
    return "ok"
