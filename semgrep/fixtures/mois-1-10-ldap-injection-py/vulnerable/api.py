import os

from fastapi import FastAPI
from ldap3 import SUBTREE, Connection, Server

app = FastAPI()
BASE_DN = "ou=people,dc=example,dc=go,dc=kr"


@app.get("/staff")
def staff(dept: str):
    server = Server(os.environ["LDAP_HOST"], use_ssl=True)
    with Connection(server, user=os.environ["LDAP_USER"], password=os.environ["LDAP_PASSWORD"], auto_bind=True) as conn:
        # 외부 입력으로 검색 필터를 만듦
        # ruleid: mois-1-10-ldap-injection-py
        conn.search(BASE_DN, f"(&(objectClass=person)(departmentNumber={dept}))", search_scope=SUBTREE, attributes=["cn"])
        return {"names": [str(entry.cn) for entry in conn.entries]}
