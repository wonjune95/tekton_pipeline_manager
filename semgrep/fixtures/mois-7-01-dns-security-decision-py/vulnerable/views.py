import socket

from django.http import HttpResponse, HttpResponseForbidden

TRUSTED_HOST = "batch.internal.example.go.kr"


def batch_sync(request):
    # 접속 IP 를 역방향 DNS 로 조회한 이름으로 신뢰 여부를 판단: DNS 위조로 우회 가능
    host = socket.gethostbyaddr(request.META["REMOTE_ADDR"])[0]
    # ruleid: mois-7-01-dns-security-decision-py
    if host == TRUSTED_HOST:
        return HttpResponse("synced")
    return HttpResponseForbidden()


def internal_only(request):
    name, _aliases, _addrs = socket.gethostbyaddr(request.META["REMOTE_ADDR"])
    # ruleid: mois-7-01-dns-security-decision-py
    if not name.endswith(".internal.example.go.kr"):  # DNS 이름으로 판단
        return HttpResponseForbidden()
    return HttpResponse("ok")


def peer_check(request):
    # 호스트 이름을 조회한 주소와 접속 주소를 비교
    # ruleid: mois-7-01-dns-security-decision-py
    if socket.gethostbyname(TRUSTED_HOST) != request.META["REMOTE_ADDR"]:
        return HttpResponseForbidden()
    return HttpResponse("ok")
