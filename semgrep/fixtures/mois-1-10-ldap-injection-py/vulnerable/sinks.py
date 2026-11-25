import ldap
import ldap3
from flask import Flask, request

app = Flask(__name__)
BASE_DN = "ou=people,dc=example,dc=go,dc=kr"


@app.route("/python-ldap/filter")
def python_ldap_filter():
    name = request.args["name"]
    directory = ldap.initialize("ldaps://ldap.example.go.kr")
    # 키워드 인자 filterstr
    # ruleid: mois-1-10-ldap-injection-py
    rows = directory.search_ext_s(BASE_DN, ldap.SCOPE_SUBTREE, filterstr="(cn=" + name + ")")
    # 시간 제한이 있는 검색
    # ruleid: mois-1-10-ldap-injection-py
    rows += directory.search_st(BASE_DN, ldap.SCOPE_SUBTREE, f"(sn={name})", timeout=3)
    # 비동기 search(base, scope, filter) — 같은 함수에서 ldap.initialize 로 만든 객체
    # ruleid: mois-1-10-ldap-injection-py
    msgid = directory.search(BASE_DN, ldap.SCOPE_SUBTREE, "(mail=%s)" % name)
    # ruleid: mois-1-10-ldap-injection-py
    other = directory.search(BASE_DN, ldap.SCOPE_SUBTREE, filterstr="(uid=%s)" % name)
    # 확장 검색 search_ext(base, scope, filter)
    # ruleid: mois-1-10-ldap-injection-py
    ext_id = directory.search_ext(BASE_DN, ldap.SCOPE_SUBTREE, "(displayName=" + name + ")", sizelimit=10)
    return {"count": len(rows), "msgid": msgid, "other": other, "ext": ext_id}


@app.route("/python-ldap/base")
def python_ldap_base():
    dept = request.args["dept"]
    directory = ldap.initialize("ldaps://ldap.example.go.kr")
    # 검색 기준 DN 에 외부 입력
    # ruleid: mois-1-10-ldap-injection-py
    rows = directory.search_s("ou=" + dept + ",dc=example,dc=go,dc=kr", ldap.SCOPE_ONELEVEL)
    # ruleid: mois-1-10-ldap-injection-py
    rows += directory.search_ext_s(base=f"ou={dept},dc=example,dc=go,dc=kr", scope=ldap.SCOPE_ONELEVEL)
    # ruleid: mois-1-10-ldap-injection-py
    msgid = directory.search("ou=" + dept + ",dc=example,dc=go,dc=kr", ldap.SCOPE_ONELEVEL)
    # ruleid: mois-1-10-ldap-injection-py
    rows += directory.search_st("ou=" + dept + ",dc=example,dc=go,dc=kr", ldap.SCOPE_ONELEVEL, timeout=3)
    # ruleid: mois-1-10-ldap-injection-py
    ext_id = directory.search_ext("ou=" + dept + ",dc=example,dc=go,dc=kr", ldap.SCOPE_ONELEVEL, sizelimit=10)
    return {"count": len(rows), "msgid": msgid, "ext": ext_id}


@app.route("/ldap3/keyword")
def ldap3_keyword():
    mail = request.args["mail"]
    unit = request.args["unit"]
    link = ldap3.Connection(ldap3.Server("ldap.example.go.kr"), auto_bind=True)
    # ruleid: mois-1-10-ldap-injection-py
    link.search(search_base=BASE_DN, search_filter=f"(mail={mail})")
    # ruleid: mois-1-10-ldap-injection-py
    link.extend.standard.paged_search(search_base="ou=" + unit + ",dc=example,dc=go,dc=kr", search_filter="(objectClass=person)")
    return {"count": len(link.entries)}


@app.route("/ldap3/positional")
def ldap3_positional():
    mail = request.args["mail"]
    unit = request.args["unit"]
    link = ldap3.Connection(ldap3.Server("ldap.example.go.kr"), auto_bind=True)
    # 같은 함수에서 ldap3.Connection 으로 만든 객체: search(base, filter)
    # ruleid: mois-1-10-ldap-injection-py
    link.search(BASE_DN, "(mail=" + mail + ")")
    # ruleid: mois-1-10-ldap-injection-py
    link.search(f"ou={unit},dc=example,dc=go,dc=kr", "(objectClass=person)")
    return {"count": len(link.entries)}


@app.route("/ldap3/with")
def ldap3_with_block():
    mail = request.args["mail"]
    with ldap3.Connection(ldap3.Server("ldap.example.go.kr"), auto_bind=True) as link:
        # with 문으로 만든 연결
        # ruleid: mois-1-10-ldap-injection-py
        link.search(BASE_DN, "(mail=" + mail + ")")
        return {"count": len(link.entries)}


class DirectoryService:
    def __init__(self, ldap_conn):
        self.ldap_conn = ldap_conn

    def find(self, request):
        # 만든 곳은 보이지 않지만 이름이 LDAP 연결(conn·ldap)인 객체
        # ruleid: mois-1-10-ldap-injection-py
        self.ldap_conn.search(BASE_DN, "(uid=" + request.GET["uid"] + ")")
        return self.ldap_conn.entries

    def find_in_unit(self, request):
        unit = request.GET["unit"]
        # 검색 기준 DN (첫 번째 인자)
        # ruleid: mois-1-10-ldap-injection-py
        self.ldap_conn.search("ou=" + unit + ",dc=example,dc=go,dc=kr", "(objectClass=person)")
        # python-ldap 방식 search(base, scope, filter)
        # ruleid: mois-1-10-ldap-injection-py
        return self.ldap_conn.search(BASE_DN, 2, "(ou=" + unit + ")")


class StaffDirectory:
    def __init__(self, conn, ldap_client):
        self.conn = conn
        self.ldap_client = ldap_client

    def find_by_uid(self, request):
        # 이름이 conn 인 객체
        # ruleid: mois-1-10-ldap-injection-py
        self.conn.search(BASE_DN, "(uid=" + request.GET["uid"] + ")")
        return self.conn.entries

    def find_by_mail(self, request):
        # 이름에 ldap 이 든 객체
        # ruleid: mois-1-10-ldap-injection-py
        self.ldap_client.search(BASE_DN, "(mail=" + request.GET["mail"] + ")")
        return self.ldap_client.entries
