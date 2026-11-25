import os

from fastapi import FastAPI
from ldap3 import SUBTREE, Connection, Server
from ldap3.utils.conv import escape_filter_chars

app = FastAPI()
BASE_DN = "ou=people,dc=example,dc=go,dc=kr"


@app.get("/staff")
def staff(dept: str):
    server = Server(os.environ["LDAP_HOST"], use_ssl=True)
    with Connection(server, user=os.environ["LDAP_USER"], password=os.environ["LDAP_PASSWORD"], auto_bind=True) as conn:
        # ok: mois-1-10-ldap-injection-py 필터 특수문자를 이스케이프
        safe_dept = escape_filter_chars(dept)
        conn.search(BASE_DN, f"(&(objectClass=person)(departmentNumber={safe_dept}))", search_scope=SUBTREE, attributes=["cn"])
        return {"names": [str(entry.cn) for entry in conn.entries]}
