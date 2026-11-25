import fnmatch
import re
import socket

from flask import Flask, abort, request

app = Flask(__name__)
TRUSTED = {"batch01.internal.example.go.kr", "batch02.internal.example.go.kr"}
ADMIN_HOST = "admin.internal.example.go.kr"


@app.before_request
def direct_comparisons():
    peer = request.remote_addr
    # ruleid: mois-7-01-dns-security-decision-py
    if ADMIN_HOST == socket.getfqdn(peer):
        return None
    # ruleid: mois-7-01-dns-security-decision-py
    if socket.gethostbyname(ADMIN_HOST) == peer:
        return None
    # ruleid: mois-7-01-dns-security-decision-py
    if peer != socket.gethostbyname_ex(ADMIN_HOST)[0]:
        abort(403)
    # ruleid: mois-7-01-dns-security-decision-py
    if socket.gethostbyaddr(peer)[0] in TRUSTED:
        return None
    # ruleid: mois-7-01-dns-security-decision-py
    if socket.getnameinfo((peer, 0), 0)[0] not in TRUSTED:
        abort(403)
    return None


def by_variable(peer):
    fqdn = socket.getfqdn(peer)
    # 정규식으로 이름을 확인
    # ruleid: mois-7-01-dns-security-decision-py
    if re.match(r".*\.internal\.example\.go\.kr$", fqdn):
        return True
    # ruleid: mois-7-01-dns-security-decision-py
    if fnmatch.fnmatch(fqdn, "*.internal.example.go.kr"):
        return True
    # ruleid: mois-7-01-dns-security-decision-py
    return fqdn.lower().startswith("batch")


def by_nameinfo(sockaddr):
    name, _port = socket.getnameinfo(sockaddr, socket.NI_NAMEREQD)
    # ruleid: mois-7-01-dns-security-decision-py
    return name in TRUSTED
