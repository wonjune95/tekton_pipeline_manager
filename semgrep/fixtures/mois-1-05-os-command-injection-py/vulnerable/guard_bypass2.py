"""허용 목록 검사를 거친 것처럼 보이지만 값이 다시 바뀌거나 끝나지 않는 경우 — 모두 탐지되어야 한다."""
import os

import flask
from django.http import HttpResponse, HttpResponseBadRequest

ALLOWED_HOSTS = ("intra.example.go.kr", "mail.example.go.kr")


def else_reassigned(request):
    host = request.GET.get("host", "")
    if host not in ALLOWED_HOSTS:
        return HttpResponseBadRequest("unknown host")
    else:
        host = request.GET.get("override", host)
    # ruleid: mois-1-05-os-command-injection-py
    os.system("ping -c 1 " + host)
    return HttpResponse("ok")


def else_without_change(request):
    host = request.GET.get("host", "")
    if host not in ALLOWED_HOSTS:
        return HttpResponseBadRequest("unknown host")
    else:
        pass
    # else 가 붙은 검사는 인정하지 않는다 (보수적 탐지 — else 를 지우면 사라진다)
    # ruleid: mois-1-05-os-command-injection-py
    os.system("ping -c 1 " + host)
    return HttpResponse("ok")


def nested_if_reassigned(request):
    host = request.GET.get("host", "")
    if host not in ALLOWED_HOSTS:
        return HttpResponseBadRequest("unknown host")
    if request.GET.get("alias"):
        host = request.GET.get("alias")
    # ruleid: mois-1-05-os-command-injection-py
    os.system("ping -c 1 " + host)
    return HttpResponse("ok")


def nested_if_appended(request):
    host = request.GET.get("host", "")
    if host not in ALLOWED_HOSTS:
        return HttpResponseBadRequest("unknown host")
    if request.GET.get("verbose"):
        host += request.GET.get("options", "")
    # ruleid: mois-1-05-os-command-injection-py
    os.system("ping -c 1 " + host)
    return HttpResponse("ok")


def nested_else_reassigned(request):
    host = request.GET.get("host", "")
    if host not in ALLOWED_HOSTS:
        return HttpResponseBadRequest("unknown host")
    if request.user.is_staff:
        pass
    else:
        host = request.GET.get("alias", host)
    # ruleid: mois-1-05-os-command-injection-py
    os.system("ping -c 1 " + host)
    return HttpResponse("ok")


def nested_else_appended(request):
    host = request.GET.get("host", "")
    if host not in ALLOWED_HOSTS:
        return HttpResponseBadRequest("unknown host")
    if request.user.is_staff:
        pass
    else:
        host += request.GET.get("options", "")
    # ruleid: mois-1-05-os-command-injection-py
    os.system("ping -c 1 " + host)
    return HttpResponse("ok")


def for_reassigned(request):
    host = request.GET.get("host", "")
    if host not in ALLOWED_HOSTS:
        return HttpResponseBadRequest("unknown host")
    for candidate in request.GET.getlist("fallback"):
        host = candidate
    # ruleid: mois-1-05-os-command-injection-py
    os.system("ping -c 1 " + host)
    return HttpResponse("ok")


def for_appended(request):
    host = request.GET.get("host", "")
    if host not in ALLOWED_HOSTS:
        return HttpResponseBadRequest("unknown host")
    for opt in request.GET.getlist("opt"):
        host += " " + opt
    # ruleid: mois-1-05-os-command-injection-py
    os.system("ping -c 1 " + host)
    return HttpResponse("ok")


def while_reassigned(request):
    host = request.GET.get("host", "")
    if host not in ALLOWED_HOSTS:
        return HttpResponseBadRequest("unknown host")
    while not host.endswith(".kr"):
        host = request.GET.get("next", "x.kr")
    # ruleid: mois-1-05-os-command-injection-py
    os.system("ping -c 1 " + host)
    return HttpResponse("ok")


def while_appended(request):
    host = request.GET.get("host", "")
    if host not in ALLOWED_HOSTS:
        return HttpResponseBadRequest("unknown host")
    while len(host) < 40:
        host += request.GET.get("pad", "x")
    # ruleid: mois-1-05-os-command-injection-py
    os.system("ping -c 1 " + host)
    return HttpResponse("ok")


def with_reassigned(request):
    host = request.GET.get("host", "")
    if host not in ALLOWED_HOSTS:
        return HttpResponseBadRequest("unknown host")
    with open("/etc/hostname") as fh:
        host = request.GET.get("alias", fh.read())
    # ruleid: mois-1-05-os-command-injection-py
    os.system("ping -c 1 " + host)
    return HttpResponse("ok")


def with_appended(request):
    host = request.GET.get("host", "")
    if host not in ALLOWED_HOSTS:
        return HttpResponseBadRequest("unknown host")
    with open("/etc/hostname") as fh:
        host += request.GET.get("suffix", fh.read())
    # ruleid: mois-1-05-os-command-injection-py
    os.system("ping -c 1 " + host)
    return HttpResponse("ok")


def try_reassigned(request):
    host = request.GET.get("host", "")
    if host not in ALLOWED_HOSTS:
        return HttpResponseBadRequest("unknown host")
    try:
        host = request.GET["alias"]
    except KeyError:
        pass
    # ruleid: mois-1-05-os-command-injection-py
    os.system("ping -c 1 " + host)
    return HttpResponse("ok")


def try_appended(request):
    host = request.GET.get("host", "")
    if host not in ALLOWED_HOSTS:
        return HttpResponseBadRequest("unknown host")
    try:
        host += request.GET["suffix"]
    except KeyError:
        pass
    # ruleid: mois-1-05-os-command-injection-py
    os.system("ping -c 1 " + host)
    return HttpResponse("ok")


def except_reassigned(request):
    host = request.GET.get("host", "")
    if host not in ALLOWED_HOSTS:
        return HttpResponseBadRequest("unknown host")
    try:
        int(request.GET["n"])
    except ValueError:
        host = request.GET.get("alias", host)
    # ruleid: mois-1-05-os-command-injection-py
    os.system("ping -c 1 " + host)
    return HttpResponse("ok")


def except_appended(request):
    host = request.GET.get("host", "")
    if host not in ALLOWED_HOSTS:
        return HttpResponseBadRequest("unknown host")
    try:
        int(request.GET["n"])
    except ValueError:
        host += request.GET.get("suffix", "")
    # ruleid: mois-1-05-os-command-injection-py
    os.system("ping -c 1 " + host)
    return HttpResponse("ok")


def conditional_abort_and():
    host = flask.request.args.get("host", "")
    if host not in ALLOWED_HOSTS:
        flask.request.args.get("strict") and flask.abort(400)
    # ruleid: mois-1-05-os-command-injection-py
    os.system("ping -c 1 " + host)
    return "ok"


def conditional_abort_or():
    host = flask.request.args.get("host", "")
    if host not in ALLOWED_HOSTS:
        flask.request.args.get("lenient") or flask.abort(400)
    # ruleid: mois-1-05-os-command-injection-py
    os.system("ping -c 1 " + host)
    return "ok"


def conditional_abort_ternary():
    # 조건식 문장은 끝내는 문장으로 인정되지 않는다 (규칙 쪽 별도 제외 불필요 — 확인용)
    host = flask.request.args.get("host", "")
    if host not in ALLOWED_HOSTS:
        flask.abort(400) if flask.request.args.get("strict") else None
    # ruleid: mois-1-05-os-command-injection-py
    os.system("ping -c 1 " + host)
    return "ok"


def inline_nested_reassigned(request):
    fmt = request.GET.get("format", "")
    if fmt not in ("png", "jpg"):
        return HttpResponseBadRequest("unsupported format")
    if request.GET.get("raw"):
        fmt = request.GET.get("raw")
    # ruleid: mois-1-05-os-command-injection-py
    os.system("convert in.dat out." + fmt)
    return HttpResponse("ok")


def inline_else(request):
    fmt = request.GET.get("format", "")
    if fmt not in ("png", "jpg"):
        return HttpResponseBadRequest("unsupported format")
    else:
        fmt = request.GET.get("raw", fmt)
    # ruleid: mois-1-05-os-command-injection-py
    os.system("convert in.dat out." + fmt)
    return HttpResponse("ok")


def inline_conditional_abort():
    fmt = flask.request.args.get("format", "")
    if fmt not in ("png", "jpg"):
        flask.request.args.get("strict") and flask.abort(400)
    # ruleid: mois-1-05-os-command-injection-py
    os.system("convert in.dat out." + fmt)
    return "ok"
