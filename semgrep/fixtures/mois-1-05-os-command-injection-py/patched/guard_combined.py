"""허용 목록 검사를 다른 조건과 묶어도 안전한 경우 — 빠져나가는 쪽은 or, 들어가는 쪽은 and."""
import os

from django.http import HttpResponse, HttpResponseBadRequest

ALLOWED_HOSTS = ("intra.example.go.kr", "mail.example.go.kr")


def empty_or_unknown(request):
    host = request.GET.get("host")
    if host is None or host not in ALLOWED_HOSTS:
        return HttpResponseBadRequest("unknown host")
    # ok: mois-1-05-os-command-injection-py 비었거나 목록에 없으면 빠져나감
    os.system("ping -c 1 " + host)
    return HttpResponse("ok")


def maintenance_or_unknown(request):
    host = request.GET.get("host", "")
    if request.user.is_anonymous or host not in ALLOWED_HOSTS:
        return HttpResponseBadRequest("not allowed")
    # ok: mois-1-05-os-command-injection-py
    os.system("ping -c 1 " + host)
    return HttpResponse("ok")


def unknown_or_closed(request):
    host = request.GET.get("host", "")
    if host not in ALLOWED_HOSTS or is_closed():
        return HttpResponseBadRequest("not allowed")
    # ok: mois-1-05-os-command-injection-py
    os.system("ping -c 1 " + host)
    return HttpResponse("ok")


def staff_and_known(request):
    host = request.GET.get("host", "")
    if request.user.is_staff and host in ALLOWED_HOSTS:
        # ok: mois-1-05-os-command-injection-py 목록에 있을 때만 들어감
        os.system("ping -c 1 " + host)
    return HttpResponse("ok")


def known_and_open(request):
    fmt = request.GET.get("format", "")
    if fmt in ("png", "jpg") and not is_closed():
        # ok: mois-1-05-os-command-injection-py
        os.system("convert in.dat out." + fmt)
    return HttpResponse("ok")


def is_closed():
    return False
