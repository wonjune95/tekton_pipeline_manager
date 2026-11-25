import ipaddress
import logging
import socket

from django.http import HttpResponse, HttpResponseForbidden

logger = logging.getLogger(__name__)
TRUSTED_NETWORK = ipaddress.ip_network("10.20.0.0/24")


def batch_sync(request):
    # DNS 조회 없이 접속 IP 주소로 판단
    try:
        addr = ipaddress.ip_address(request.META.get("REMOTE_ADDR", ""))
    except ValueError:
        return HttpResponseForbidden()
    if addr not in TRUSTED_NETWORK:
        return HttpResponseForbidden()
    return HttpResponse("synced")


def whoami(request):
    # 조회한 이름을 기록에만 쓰는 것은 보안결정이 아니다
    host = socket.getfqdn()
    logger.info("served by %s", host)
    return HttpResponse("ok")
