"""조건에 바로 적은 허용 목록 — 검사를 거친 것처럼 보이지만 값이 다시 바뀌거나 끝나지 않는 경우. 모두 탐지되어야 한다."""
import os

import flask
from django.http import HttpResponse, HttpResponseBadRequest


def inline_else_reassigned(request):
    host = request.GET.get("host", "")
    if host not in ("intra.example.go.kr", "mail.example.go.kr"):
        return HttpResponseBadRequest("unknown host")
    else:
        host = request.GET.get("override", host)
    # ruleid: mois-1-05-os-command-injection-py
    os.system("ping -c 1 " + host)
    return HttpResponse("ok")


def inline_nested_if_reassigned(request):
    host = request.GET.get("host", "")
    if host not in ("intra.example.go.kr", "mail.example.go.kr"):
        return HttpResponseBadRequest("unknown host")
    if request.GET.get("alias"):
        host = request.GET.get("alias")
    # ruleid: mois-1-05-os-command-injection-py
    os.system("ping -c 1 " + host)
    return HttpResponse("ok")


def inline_nested_if_appended(request):
    host = request.GET.get("host", "")
    if host not in ("intra.example.go.kr", "mail.example.go.kr"):
        return HttpResponseBadRequest("unknown host")
    if request.GET.get("verbose"):
        host += request.GET.get("options", "")
    # ruleid: mois-1-05-os-command-injection-py
    os.system("ping -c 1 " + host)
    return HttpResponse("ok")


def inline_nested_else_reassigned(request):
    host = request.GET.get("host", "")
    if host not in ("intra.example.go.kr", "mail.example.go.kr"):
        return HttpResponseBadRequest("unknown host")
    if request.user.is_staff:
        pass
    else:
        host = request.GET.get("alias", host)
    # ruleid: mois-1-05-os-command-injection-py
    os.system("ping -c 1 " + host)
    return HttpResponse("ok")


def inline_nested_else_appended(request):
    host = request.GET.get("host", "")
    if host not in ("intra.example.go.kr", "mail.example.go.kr"):
        return HttpResponseBadRequest("unknown host")
    if request.user.is_staff:
        pass
    else:
        host += request.GET.get("options", "")
    # ruleid: mois-1-05-os-command-injection-py
    os.system("ping -c 1 " + host)
    return HttpResponse("ok")


def inline_for_reassigned(request):
    host = request.GET.get("host", "")
    if host not in ("intra.example.go.kr", "mail.example.go.kr"):
        return HttpResponseBadRequest("unknown host")
    for candidate in request.GET.getlist("fallback"):
        host = candidate
    # ruleid: mois-1-05-os-command-injection-py
    os.system("ping -c 1 " + host)
    return HttpResponse("ok")


def inline_for_appended(request):
    host = request.GET.get("host", "")
    if host not in ("intra.example.go.kr", "mail.example.go.kr"):
        return HttpResponseBadRequest("unknown host")
    for opt in request.GET.getlist("opt"):
        host += " " + opt
    # ruleid: mois-1-05-os-command-injection-py
    os.system("ping -c 1 " + host)
    return HttpResponse("ok")


def inline_while_reassigned(request):
    host = request.GET.get("host", "")
    if host not in ("intra.example.go.kr", "mail.example.go.kr"):
        return HttpResponseBadRequest("unknown host")
    while not host.endswith(".kr"):
        host = request.GET.get("next", "x.kr")
    # ruleid: mois-1-05-os-command-injection-py
    os.system("ping -c 1 " + host)
    return HttpResponse("ok")


def inline_while_appended(request):
    host = request.GET.get("host", "")
    if host not in ("intra.example.go.kr", "mail.example.go.kr"):
        return HttpResponseBadRequest("unknown host")
    while len(host) < 40:
        host += request.GET.get("pad", "x")
    # ruleid: mois-1-05-os-command-injection-py
    os.system("ping -c 1 " + host)
    return HttpResponse("ok")


def inline_with_reassigned(request):
    host = request.GET.get("host", "")
    if host not in ("intra.example.go.kr", "mail.example.go.kr"):
        return HttpResponseBadRequest("unknown host")
    with open("/etc/hostname") as fh:
        host = request.GET.get("alias", fh.read())
    # ruleid: mois-1-05-os-command-injection-py
    os.system("ping -c 1 " + host)
    return HttpResponse("ok")


def inline_with_appended(request):
    host = request.GET.get("host", "")
    if host not in ("intra.example.go.kr", "mail.example.go.kr"):
        return HttpResponseBadRequest("unknown host")
    with open("/etc/hostname") as fh:
        host += request.GET.get("suffix", fh.read())
    # ruleid: mois-1-05-os-command-injection-py
    os.system("ping -c 1 " + host)
    return HttpResponse("ok")


def inline_try_reassigned(request):
    host = request.GET.get("host", "")
    if host not in ("intra.example.go.kr", "mail.example.go.kr"):
        return HttpResponseBadRequest("unknown host")
    try:
        host = request.GET["alias"]
    except KeyError:
        pass
    # ruleid: mois-1-05-os-command-injection-py
    os.system("ping -c 1 " + host)
    return HttpResponse("ok")


def inline_try_appended(request):
    host = request.GET.get("host", "")
    if host not in ("intra.example.go.kr", "mail.example.go.kr"):
        return HttpResponseBadRequest("unknown host")
    try:
        host += request.GET["suffix"]
    except KeyError:
        pass
    # ruleid: mois-1-05-os-command-injection-py
    os.system("ping -c 1 " + host)
    return HttpResponse("ok")


def inline_except_reassigned(request):
    host = request.GET.get("host", "")
    if host not in ("intra.example.go.kr", "mail.example.go.kr"):
        return HttpResponseBadRequest("unknown host")
    try:
        int(request.GET["n"])
    except ValueError:
        host = request.GET.get("alias", host)
    # ruleid: mois-1-05-os-command-injection-py
    os.system("ping -c 1 " + host)
    return HttpResponse("ok")


def inline_except_appended(request):
    host = request.GET.get("host", "")
    if host not in ("intra.example.go.kr", "mail.example.go.kr"):
        return HttpResponseBadRequest("unknown host")
    try:
        int(request.GET["n"])
    except ValueError:
        host += request.GET.get("suffix", "")
    # ruleid: mois-1-05-os-command-injection-py
    os.system("ping -c 1 " + host)
    return HttpResponse("ok")


def inline_conditional_abort_and():
    host = flask.request.args.get("host", "")
    if host not in ("intra.example.go.kr", "mail.example.go.kr"):
        flask.request.args.get("strict") and flask.abort(400)
    # ruleid: mois-1-05-os-command-injection-py
    os.system("ping -c 1 " + host)
    return "ok"


def inline_conditional_abort_or():
    host = flask.request.args.get("host", "")
    if host not in ("intra.example.go.kr", "mail.example.go.kr"):
        flask.request.args.get("lenient") or flask.abort(400)
    # ruleid: mois-1-05-os-command-injection-py
    os.system("ping -c 1 " + host)
    return "ok"


def inline_conditional_abort_ternary():
    # 조건식 문장은 끝내는 문장으로 인정되지 않는다 (규칙 쪽 별도 제외 불필요 — 확인용)
    host = flask.request.args.get("host", "")
    if host not in ("intra.example.go.kr", "mail.example.go.kr"):
        flask.abort(400) if flask.request.args.get("strict") else None
    # ruleid: mois-1-05-os-command-injection-py
    os.system("ping -c 1 " + host)
    return "ok"
