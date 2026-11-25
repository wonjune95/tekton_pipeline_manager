"""검사식을 감싸거나 뒤집어 뜻이 바뀐 경우, 튜플로 다시 대입한 경우 — 모두 탐지되어야 한다."""
import os

from django.http import HttpResponse, HttpResponseBadRequest

ALLOWED_HOSTS = ("intra.example.go.kr", "mail.example.go.kr")


def negated_check(request):
    host = request.GET.get("host", "")
    # 목록에 "있으면" 빠져나간다 — 뒤의 host 는 목록 밖의 값이다
    if not (host not in ALLOWED_HOSTS):
        return HttpResponseBadRequest("already known")
    # ruleid: mois-1-05-os-command-injection-py
    os.system("ping -c 1 " + host)
    return HttpResponse("ok")


def compared_check(request):
    host = request.GET.get("host", "")
    if (host not in ALLOWED_HOSTS) == False:
        return HttpResponseBadRequest("already known")
    # ruleid: mois-1-05-os-command-injection-py
    os.system("ping -c 1 " + host)
    return HttpResponse("ok")


def inline_negated_check(request):
    fmt = request.GET.get("format", "")
    if not (fmt not in ("png", "jpg")):
        return HttpResponseBadRequest("already known")
    # ruleid: mois-1-05-os-command-injection-py
    os.system("convert in.dat out." + fmt)
    return HttpResponse("ok")


def tuple_reassigned(request):
    host = request.GET.get("host", "")
    if host not in ALLOWED_HOSTS:
        return HttpResponseBadRequest("unknown host")
    host, port = request.GET.get("alias", host), 22
    # ruleid: mois-1-05-os-command-injection-py
    os.system("ssh -p %d " % port + host)
    return HttpResponse("ok")


def inline_tuple_reassigned(request):
    fmt = request.GET.get("format", "")
    if fmt not in ("png", "jpg"):
        return HttpResponseBadRequest("unsupported format")
    fmt, quality = request.GET.get("raw", fmt), 90
    # ruleid: mois-1-05-os-command-injection-py
    os.system("convert -quality %d in.dat out." % quality + fmt)
    return HttpResponse("ok")


def positive_compared(request):
    host = request.GET.get("host", "")
    if (host in ALLOWED_HOSTS) == False:
        # ruleid: mois-1-05-os-command-injection-py
        os.system("logger unknown host " + host)
    return HttpResponse("ok")


def positive_negated(request):
    host = request.GET.get("host", "")
    if not host in ALLOWED_HOSTS:
        # ruleid: mois-1-05-os-command-injection-py
        os.system("logger unknown host " + host)
    return HttpResponse("ok")


def inline_positive_compared(request):
    fmt = request.GET.get("format", "")
    if (fmt in ("png", "jpg")) != True:
        # ruleid: mois-1-05-os-command-injection-py
        os.system("logger unsupported " + fmt)
    return HttpResponse("ok")


def inline_positive_negated(request):
    fmt = request.GET.get("format", "")
    if not fmt in ("png", "jpg"):
        # ruleid: mois-1-05-os-command-injection-py
        os.system("logger unsupported " + fmt)
    return HttpResponse("ok")
