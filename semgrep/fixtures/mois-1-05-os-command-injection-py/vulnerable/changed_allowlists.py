"""허용 목록·dict 가 쓰는 함수 안에서 바뀌는 경우 — 모두 탐지되어야 한다.

이름 붙은 허용 목록은 "그 함수 안에서 다시 대입하거나 바꾸지 않을 때"만 인정한다.
함수 안에서 만든 목록·dict 도 같은 이유로 인정하지 않는다 (만든 뒤 안쪽 블록에서 바뀌는지 보지 못한다).
"""
import os

from django.http import HttpResponse, HttpResponseBadRequest

TOOL_PATHS = {"convert": "/opt/tools/convert", "resize": "/opt/tools/resize"}
ALLOWED_HOSTS = ["intra.example.go.kr", "mail.example.go.kr"]
ALLOWED_UNITS = {"nginx", "gunicorn"}


# ---- (공통 1) dict 조회 ----
def dict_built_in_function(request):
    table = {"safe": "/opt/tools/convert"}
    table["safe"] = request.GET["tool"]
    # ruleid: mois-1-05-os-command-injection-py
    os.system(table[request.GET["key"]] + " in.png out.png")
    return HttpResponse("ok")


def dict_item_assigned(request):
    TOOL_PATHS["custom"] = request.GET["tool"]
    # ruleid: mois-1-05-os-command-injection-py
    os.system(TOOL_PATHS[request.GET["key"]] + " in.png out.png")
    return HttpResponse("ok")


def dict_updated(request):
    TOOL_PATHS.update(request.GET.dict())
    # ruleid: mois-1-05-os-command-injection-py
    os.system(TOOL_PATHS.get(request.GET["key"]) + " in.png out.png")
    return HttpResponse("ok")


def dict_setdefault(request):
    TOOL_PATHS.setdefault(request.GET["key"], request.GET["tool"])
    # ruleid: mois-1-05-os-command-injection-py
    os.system(TOOL_PATHS[request.GET["key"]] + " in.png out.png")
    return HttpResponse("ok")


def dict_merged(request):
    global TOOL_PATHS
    TOOL_PATHS |= request.GET.dict()
    # ruleid: mois-1-05-os-command-injection-py
    os.system(TOOL_PATHS[request.GET["key"]] + " in.png out.png")
    return HttpResponse("ok")


# ---- (공통 2-가) 실패 시 중단 ----
def guard_list_built_in_function(request):
    allowed = ["intra.example.go.kr"]
    allowed.append(request.GET.get("extra", ""))
    host = request.GET.get("host", "")
    if host not in allowed:
        return HttpResponseBadRequest("unknown host")
    # ruleid: mois-1-05-os-command-injection-py
    os.system("ping -c 1 " + host)
    return HttpResponse("ok")


def guard_list_shadowed(request):
    ALLOWED_HOSTS = request.GET.getlist("allowed")
    host = request.GET.get("host", "")
    if host not in ALLOWED_HOSTS:
        return HttpResponseBadRequest("unknown host")
    # ruleid: mois-1-05-os-command-injection-py
    os.system("ping -c 1 " + host)
    return HttpResponse("ok")


def guard_list_item_assigned(request):
    host = request.GET.get("host", "")
    ALLOWED_HOSTS[0] = request.GET.get("extra", "")
    if host not in ALLOWED_HOSTS:
        return HttpResponseBadRequest("unknown host")
    # ruleid: mois-1-05-os-command-injection-py
    os.system("ping -c 1 " + host)
    return HttpResponse("ok")


def guard_list_plus_equals(request):
    global ALLOWED_HOSTS
    host = request.GET.get("host", "")
    ALLOWED_HOSTS += request.GET.getlist("extra")
    if host not in ALLOWED_HOSTS:
        return HttpResponseBadRequest("unknown host")
    # ruleid: mois-1-05-os-command-injection-py
    os.system("ping -c 1 " + host)
    return HttpResponse("ok")


def guard_set_or_equals(request):
    global ALLOWED_UNITS
    unit = request.GET.get("unit", "")
    ALLOWED_UNITS |= set(request.GET.getlist("extra"))
    if unit not in ALLOWED_UNITS:
        return HttpResponseBadRequest("unknown unit")
    # ruleid: mois-1-05-os-command-injection-py
    os.system("systemctl restart " + unit)
    return HttpResponse("ok")


def guard_list_append(request):
    host = request.GET.get("host", "")
    ALLOWED_HOSTS.append(request.GET.get("extra", ""))
    if host not in ALLOWED_HOSTS:
        return HttpResponseBadRequest("unknown host")
    # ruleid: mois-1-05-os-command-injection-py
    os.system("ping -c 1 " + host)
    return HttpResponse("ok")


def guard_list_extend(request):
    host = request.GET.get("host", "")
    ALLOWED_HOSTS.extend(request.GET.getlist("extra"))
    if host not in ALLOWED_HOSTS:
        return HttpResponseBadRequest("unknown host")
    # ruleid: mois-1-05-os-command-injection-py
    os.system("ping -c 1 " + host)
    return HttpResponse("ok")


def guard_list_insert(request):
    host = request.GET.get("host", "")
    ALLOWED_HOSTS.insert(0, request.GET.get("extra", ""))
    if host not in ALLOWED_HOSTS:
        return HttpResponseBadRequest("unknown host")
    # ruleid: mois-1-05-os-command-injection-py
    os.system("ping -c 1 " + host)
    return HttpResponse("ok")


def guard_set_add(request):
    unit = request.GET.get("unit", "")
    ALLOWED_UNITS.add(request.GET.get("extra", ""))
    if unit not in ALLOWED_UNITS:
        return HttpResponseBadRequest("unknown unit")
    # ruleid: mois-1-05-os-command-injection-py
    os.system("systemctl restart " + unit)
    return HttpResponse("ok")


def guard_set_update(request):
    unit = request.GET.get("unit", "")
    ALLOWED_UNITS.update(request.GET.getlist("extra"))
    if unit not in ALLOWED_UNITS:
        return HttpResponseBadRequest("unknown unit")
    # ruleid: mois-1-05-os-command-injection-py
    os.system("systemctl restart " + unit)
    return HttpResponse("ok")


def guard_bitwise_and(request, strict):
    host = request.GET.get("host", "")
    # & 는 둘 다 참일 때만 참이다 — strict 가 거짓이면 목록에 없어도 지나간다
    if (host not in ALLOWED_HOSTS) & strict:
        return HttpResponseBadRequest("unknown host")
    # ruleid: mois-1-05-os-command-injection-py
    os.system("ping -c 1 " + host)
    return HttpResponse("ok")


def inline_bitwise_and(request, strict):
    fmt = request.GET.get("format", "")
    if (fmt not in ("png", "jpg")) & strict:
        return HttpResponseBadRequest("unsupported format")
    # ruleid: mois-1-05-os-command-injection-py
    os.system("convert in.dat out." + fmt)
    return HttpResponse("ok")


def inline_bitwise_and_reversed(request, strict):
    fmt = request.GET.get("format", "")
    if strict & (fmt not in ("png", "jpg")):
        return HttpResponseBadRequest("unsupported format")
    # ruleid: mois-1-05-os-command-injection-py
    os.system("convert in.dat out." + fmt)
    return HttpResponse("ok")


def guard_list_made_in_function(request):
    # 바꾸는 줄이 없어도 함수 안에서 만든 목록은 인정하지 않는다 (보수적 탐지 — 목록을 모듈 수준 상수로 올리면 사라진다)
    allowed = ("intra.example.go.kr", "mail.example.go.kr")
    host = request.GET.get("host", "")
    if host not in allowed:
        return HttpResponseBadRequest("unknown host")
    # ruleid: mois-1-05-os-command-injection-py
    os.system("ping -c 1 " + host)
    return HttpResponse("ok")


# ---- (공통 3) 조건 안에서만 사용 ----
def positive_list_made_in_function(request):
    allowed = ("intra.example.go.kr", "mail.example.go.kr")
    host = request.GET.get("host", "")
    if host in allowed:
        # ruleid: mois-1-05-os-command-injection-py
        os.system("ping -c 1 " + host)
    return HttpResponse("ok")


def positive_list_built_in_function(request):
    allowed = ["intra.example.go.kr"]
    allowed.append(request.GET.get("extra", ""))
    host = request.GET.get("host", "")
    if host in allowed:
        # ruleid: mois-1-05-os-command-injection-py
        os.system("ping -c 1 " + host)
    return HttpResponse("ok")


def positive_list_shadowed(request):
    ALLOWED_HOSTS = request.GET.getlist("allowed")
    host = request.GET.get("host", "")
    if host in ALLOWED_HOSTS:
        # ruleid: mois-1-05-os-command-injection-py
        os.system("ping -c 1 " + host)
    return HttpResponse("ok")


def positive_list_item_assigned(request):
    host = request.GET.get("host", "")
    ALLOWED_HOSTS[0] = request.GET.get("extra", "")
    if host in ALLOWED_HOSTS:
        # ruleid: mois-1-05-os-command-injection-py
        os.system("ping -c 1 " + host)
    return HttpResponse("ok")


def positive_list_plus_equals(request):
    global ALLOWED_HOSTS
    host = request.GET.get("host", "")
    ALLOWED_HOSTS += request.GET.getlist("extra")
    if host in ALLOWED_HOSTS:
        # ruleid: mois-1-05-os-command-injection-py
        os.system("ping -c 1 " + host)
    return HttpResponse("ok")


def positive_set_or_equals(request):
    global ALLOWED_UNITS
    unit = request.GET.get("unit", "")
    ALLOWED_UNITS |= set(request.GET.getlist("extra"))
    if unit in ALLOWED_UNITS:
        # ruleid: mois-1-05-os-command-injection-py
        os.system("systemctl restart " + unit)
    return HttpResponse("ok")


def positive_list_append(request):
    host = request.GET.get("host", "")
    ALLOWED_HOSTS.append(request.GET.get("extra", ""))
    if host in ALLOWED_HOSTS:
        # ruleid: mois-1-05-os-command-injection-py
        os.system("ping -c 1 " + host)
    return HttpResponse("ok")


def positive_list_extend(request):
    host = request.GET.get("host", "")
    ALLOWED_HOSTS.extend(request.GET.getlist("extra"))
    if host in ALLOWED_HOSTS:
        # ruleid: mois-1-05-os-command-injection-py
        os.system("ping -c 1 " + host)
    return HttpResponse("ok")


def positive_list_insert(request):
    host = request.GET.get("host", "")
    ALLOWED_HOSTS.insert(0, request.GET.get("extra", ""))
    if host in ALLOWED_HOSTS:
        # ruleid: mois-1-05-os-command-injection-py
        os.system("ping -c 1 " + host)
    return HttpResponse("ok")


def positive_set_add(request):
    unit = request.GET.get("unit", "")
    ALLOWED_UNITS.add(request.GET.get("extra", ""))
    if unit in ALLOWED_UNITS:
        # ruleid: mois-1-05-os-command-injection-py
        os.system("systemctl restart " + unit)
    return HttpResponse("ok")


def positive_set_update(request):
    unit = request.GET.get("unit", "")
    ALLOWED_UNITS.update(request.GET.getlist("extra"))
    if unit in ALLOWED_UNITS:
        # ruleid: mois-1-05-os-command-injection-py
        os.system("systemctl restart " + unit)
    return HttpResponse("ok")


def positive_reassigned_inside(request):
    host = request.GET.get("host", "")
    if host in ALLOWED_HOSTS:
        host = request.GET.get("override", host)
        # ruleid: mois-1-05-os-command-injection-py
        os.system("ping -c 1 " + host)
    return HttpResponse("ok")


def positive_appended_inside(request):
    host = request.GET.get("host", "")
    if host in ALLOWED_HOSTS:
        host += request.GET.get("options", "")
        # ruleid: mois-1-05-os-command-injection-py
        os.system("ping -c 1 " + host)
    return HttpResponse("ok")


def positive_bitwise_or(request):
    host = request.GET.get("host", "")
    if (host in ALLOWED_HOSTS) | request.user.is_staff:
        # ruleid: mois-1-05-os-command-injection-py
        os.system("ping -c 1 " + host)
    return HttpResponse("ok")


def positive_inline_reassigned_inside(request):
    fmt = request.GET.get("format", "")
    if fmt in ("png", "jpg"):
        fmt = request.GET.get("override", fmt)
        # ruleid: mois-1-05-os-command-injection-py
        os.system("convert in.dat out." + fmt)
    return HttpResponse("ok")


def positive_inline_appended_inside(request):
    fmt = request.GET.get("format", "")
    if fmt in ("png", "jpg"):
        fmt += request.GET.get("suffix", "")
        # ruleid: mois-1-05-os-command-injection-py
        os.system("convert in.dat out." + fmt)
    return HttpResponse("ok")


def positive_inline_bitwise_or(request):
    fmt = request.GET.get("format", "")
    if (fmt in ("png", "jpg")) | request.user.is_staff:
        # ruleid: mois-1-05-os-command-injection-py
        os.system("convert in.dat out." + fmt)
    return HttpResponse("ok")
