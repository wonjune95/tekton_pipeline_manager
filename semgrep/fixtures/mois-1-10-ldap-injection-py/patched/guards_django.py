"""guard 형태별 안전한 예제 (Django)."""
import re

import ldap
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest

UID_RE = re.compile(r"[a-z0-9]{1,32}")


def guard_1(request):
    uid = request.GET.get("uid", "")
    if not re.fullmatch(r"[a-z0-9]{1,32}", uid):
        return HttpResponseBadRequest("invalid")
    conn = ldap.initialize(settings.LDAP_URI)
    # ok: mois-1-10-ldap-injection-py 실패하면 return
    conn.search_s(settings.LDAP_BASE_DN, ldap.SCOPE_SUBTREE, "(uid=" + uid + ")")
    return HttpResponse("ok")


def guard_2(request):
    uid = request.GET.get("uid", "")
    if not UID_RE.fullmatch(uid):
        raise ValueError("invalid")
    conn = ldap.initialize(settings.LDAP_URI)
    # ok: mois-1-10-ldap-injection-py 실패하면 raise
    conn.search_s(settings.LDAP_BASE_DN, ldap.SCOPE_SUBTREE, "(uid=" + uid + ")")
    return HttpResponse("ok")


def guard_3(request):
    uid = request.GET.get("uid", "")
    if not uid.isalnum():
        return HttpResponseBadRequest("invalid")
    conn = ldap.initialize(settings.LDAP_URI)
    # ok: mois-1-10-ldap-injection-py 실패하면 return
    conn.search_s(settings.LDAP_BASE_DN, ldap.SCOPE_SUBTREE, "(uid=" + uid + ")")
    return HttpResponse("ok")


def guard_4(request):
    uid = request.GET.get("uid", "")
    if not uid or not re.fullmatch(r"[a-z0-9]{1,32}", uid):
        raise ValueError("invalid")
    conn = ldap.initialize(settings.LDAP_URI)
    # ok: mois-1-10-ldap-injection-py 값이 없거나 실패하면 raise
    conn.search_s(settings.LDAP_BASE_DN, ldap.SCOPE_SUBTREE, "(uid=" + uid + ")")
    return HttpResponse("ok")


def guard_5(request):
    uid = request.GET.get("uid", "")
    if not uid or not UID_RE.fullmatch(uid):
        return HttpResponseBadRequest("invalid")
    conn = ldap.initialize(settings.LDAP_URI)
    # ok: mois-1-10-ldap-injection-py 값이 없거나 실패하면 return
    conn.search_s(settings.LDAP_BASE_DN, ldap.SCOPE_SUBTREE, "(uid=" + uid + ")")
    return HttpResponse("ok")


def guard_6(request):
    uid = request.GET.get("uid", "")
    if not uid or not uid.isalnum():
        raise ValueError("invalid")
    conn = ldap.initialize(settings.LDAP_URI)
    # ok: mois-1-10-ldap-injection-py 값이 없거나 실패하면 raise
    conn.search_s(settings.LDAP_BASE_DN, ldap.SCOPE_SUBTREE, "(uid=" + uid + ")")
    return HttpResponse("ok")


def guard_7(request):
    for uid in request.GET.getlist("uid"):
        if not re.fullmatch(r"[a-z0-9]{1,32}", uid):
            continue
        conn = ldap.initialize(settings.LDAP_URI)
        # ok: mois-1-10-ldap-injection-py 실패한 값은 건너뜀
        conn.search_s(settings.LDAP_BASE_DN, ldap.SCOPE_SUBTREE, "(uid=" + uid + ")")
    return HttpResponse("ok")


def guard_8(request):
    for uid in request.GET.getlist("uid"):
        if not uid or not uid.isalnum():
            continue
        conn = ldap.initialize(settings.LDAP_URI)
        # ok: mois-1-10-ldap-injection-py 비었거나 실패한 값은 건너뜀
        conn.search_s(settings.LDAP_BASE_DN, ldap.SCOPE_SUBTREE, "(uid=" + uid + ")")
    return HttpResponse("ok")


def guard_9(request):
    uid = request.GET.get("uid", "")
    if re.fullmatch(r"[a-z0-9]{1,32}", uid):
        conn = ldap.initialize(settings.LDAP_URI)
        # ok: mois-1-10-ldap-injection-py 검사를 통과한 조건 안에서만 사용
        conn.search_s(settings.LDAP_BASE_DN, ldap.SCOPE_SUBTREE, "(uid=" + uid + ")")
    return HttpResponse("ok")


def guard_10(request):
    uid = request.GET.get("uid", "")
    if UID_RE.fullmatch(uid):
        conn = ldap.initialize(settings.LDAP_URI)
        # ok: mois-1-10-ldap-injection-py 검사를 통과한 조건 안에서만 사용
        conn.search_s(settings.LDAP_BASE_DN, ldap.SCOPE_SUBTREE, "(uid=" + uid + ")")
    return HttpResponse("ok")


def guard_11(request):
    uid = request.GET.get("uid", "")
    if uid.isalnum():
        conn = ldap.initialize(settings.LDAP_URI)
        # ok: mois-1-10-ldap-injection-py 검사를 통과한 조건 안에서만 사용
        conn.search_s(settings.LDAP_BASE_DN, ldap.SCOPE_SUBTREE, "(uid=" + uid + ")")
    return HttpResponse("ok")
