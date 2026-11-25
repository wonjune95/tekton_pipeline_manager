"""형식 검사 guard 의 안전한 예제 — 허용 문자만 적은 정규식 리터럴과 and 로 묶은 조건."""
import re

import ldap
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest

GOOD_RE = re.compile(r"[a-z0-9]{1,32}")
DIGITS_RE = re.compile(r"\d{1,9}")


def digits_inline(request):
    uid = request.GET.get("uid", "")
    conn = ldap.initialize(settings.LDAP_URI)
    if not re.fullmatch(r"\d{1,9}", uid):
        return HttpResponseBadRequest("invalid")
    # ok: mois-1-10-ldap-injection-py \d 만 적은 정규식 (실패하면 return)
    conn.search_s(settings.LDAP_BASE_DN, ldap.SCOPE_SUBTREE, "(uid=" + uid + ")")
    return HttpResponse("ok")


def digits_compiled(request):
    uid = request.GET.get("uid", "")
    conn = ldap.initialize(settings.LDAP_URI)
    if not DIGITS_RE.fullmatch(uid):
        return HttpResponseBadRequest("invalid")
    # ok: mois-1-10-ldap-injection-py 모듈 수준에서 컴파일한 \d 정규식 (실패하면 return)
    conn.search_s(settings.LDAP_BASE_DN, ldap.SCOPE_SUBTREE, "(uid=" + uid + ")")
    return HttpResponse("ok")


def digits_inline_inside_if(request):
    uid = request.GET.get("uid", "")
    conn = ldap.initialize(settings.LDAP_URI)
    if re.fullmatch(r"\d{1,9}", uid):
        # ok: mois-1-10-ldap-injection-py \d 만 적은 정규식을 통과한 조건 안
        conn.search_s(settings.LDAP_BASE_DN, ldap.SCOPE_SUBTREE, "(uid=" + uid + ")")
    return HttpResponse("ok")


def digits_compiled_inside_if(request):
    uid = request.GET.get("uid", "")
    conn = ldap.initialize(settings.LDAP_URI)
    if DIGITS_RE.fullmatch(uid):
        # ok: mois-1-10-ldap-injection-py 컴파일한 \d 정규식을 통과한 조건 안
        conn.search_s(settings.LDAP_BASE_DN, ldap.SCOPE_SUBTREE, "(uid=" + uid + ")")
    return HttpResponse("ok")


def nonempty_and_ischeck(request):
    uid = request.GET.get("uid", "")
    conn = ldap.initialize(settings.LDAP_URI)
    if uid and uid.isalnum():
        # ok: mois-1-10-ldap-injection-py 값이 있고(and) 검사를 통과한 조건 안
        conn.search_s(settings.LDAP_BASE_DN, ldap.SCOPE_SUBTREE, "(uid=" + uid + ")")
    return HttpResponse("ok")


def nonempty_and_compiled(request):
    uid = request.GET.get("uid", "")
    conn = ldap.initialize(settings.LDAP_URI)
    if uid and GOOD_RE.fullmatch(uid):
        # ok: mois-1-10-ldap-injection-py 값이 있고(and) 컴파일한 정규식을 통과한 조건 안
        conn.search_s(settings.LDAP_BASE_DN, ldap.SCOPE_SUBTREE, "(uid=" + uid + ")")
    return HttpResponse("ok")


def nonempty_and_inline(request):
    uid = request.GET.get("uid", "")
    conn = ldap.initialize(settings.LDAP_URI)
    if uid and re.fullmatch(r"[a-z0-9]{1,32}", uid):
        # ok: mois-1-10-ldap-injection-py 값이 있고(and) 조건에 적은 정규식을 통과한 조건 안
        conn.search_s(settings.LDAP_BASE_DN, ldap.SCOPE_SUBTREE, "(uid=" + uid + ")")
    return HttpResponse("ok")


def literal_tokens(request):
    uid = request.GET.get("uid", "")
    conn = ldap.initialize(settings.LDAP_URI)
    if not re.fullmatch(r"(?:[a-z0-9]+-)*[a-z0-9]+@[\w-]+\.example\.com", uid, re.IGNORECASE):
        return HttpResponseBadRequest("invalid")
    # ok: mois-1-10-ldap-injection-py 글자·묶음·\w·\. 만 쓴 정규식
    conn.search_s(settings.LDAP_BASE_DN, ldap.SCOPE_SUBTREE, "(uid=" + uid + ")")
    return HttpResponse("ok")
