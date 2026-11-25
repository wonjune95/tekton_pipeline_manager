import ipaddress
import logging
import socket

from flask import Flask, abort, request

app = Flask(__name__)
logger = logging.getLogger(__name__)
TRUSTED_NETWORKS = [ipaddress.ip_network("10.20.0.0/24"), ipaddress.ip_network("10.30.0.0/24")]


@app.before_request
def check_peer():
    addr = ipaddress.ip_address(request.remote_addr)
    # ok: mois-7-01-dns-security-decision-py 접속 IP 주소로 판단한다
    if not any(addr in net for net in TRUSTED_NETWORKS):
        abort(403)
    return None


def connect_upstream(host, port):
    # ok: mois-7-01-dns-security-decision-py 조회한 주소로 접속할 뿐 신뢰 여부를 정하지 않는다
    address = socket.gethostbyname(host)
    return socket.create_connection((address, port), timeout=3)


def describe_peer(peer):
    name, _aliases, _addrs = socket.gethostbyaddr(peer)
    # ok: mois-7-01-dns-security-decision-py 기록에만 쓴다
    logger.info("request from %s (%s)", peer, name)
    return name
