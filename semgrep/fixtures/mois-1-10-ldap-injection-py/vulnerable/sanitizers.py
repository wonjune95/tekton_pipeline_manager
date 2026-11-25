"""검증처럼 보이지만 검증이 아닌 경우 — 모두 탐지되어야 한다."""
import re

import ldap
from django.conf import settings
from django.http import HttpResponseBadRequest, JsonResponse
from ldap.filter import escape_filter_chars

UID_RE = re.compile(r"[a-z0-9]{1,32}")



def prefix_match_only(request):
    uid = request.GET.get("uid", "")
    # re.match 는 앞부분만 맞아도 통과한다: "abc)(uid=*" 도 통과
    if not re.match(r"[a-z0-9]+", uid):
        return HttpResponseBadRequest("invalid uid")
    conn = ldap.initialize(settings.LDAP_URI)
    # ruleid: mois-1-10-ldap-injection-py
    rows = conn.search_s(settings.LDAP_BASE_DN, ldap.SCOPE_SUBTREE, "(uid=" + uid + ")")
    return JsonResponse({"count": len(rows)})


def compiled_prefix_match(request):
    uid = request.GET.get("uid", "")
    if not UID_RE.match(uid) or not re.search(r"[a-z]", uid):
        return HttpResponseBadRequest("invalid uid")
    conn = ldap.initialize(settings.LDAP_URI)
    # ruleid: mois-1-10-ldap-injection-py
    rows = conn.search_s(settings.LDAP_BASE_DN, ldap.SCOPE_SUBTREE, "(uid=" + uid + ")")
    return JsonResponse({"count": len(rows)})


def result_ignored(request):
    uid = request.GET.get("uid", "")
    # 검사 결과를 쓰지 않음
    UID_RE.fullmatch(uid)
    uid.isalnum()
    conn = ldap.initialize(settings.LDAP_URI)
    # ruleid: mois-1-10-ldap-injection-py
    rows = conn.search_s(settings.LDAP_BASE_DN, ldap.SCOPE_SUBTREE, "(uid=" + uid + ")")
    return JsonResponse({"count": len(rows)})


def failure_does_not_exit(request):
    uid = request.GET.get("uid", "")
    if not UID_RE.fullmatch(uid):
        print("suspicious uid", uid)
    conn = ldap.initialize(settings.LDAP_URI)
    # ruleid: mois-1-10-ldap-injection-py
    rows = conn.search_s(settings.LDAP_BASE_DN, ldap.SCOPE_SUBTREE, "(uid=" + uid + ")")
    return JsonResponse({"count": len(rows)})


def opposite_branch(request):
    uid = request.GET.get("uid", "")
    conn = ldap.initialize(settings.LDAP_URI)
    if uid.isalnum():
        rows = []
    else:
        # ruleid: mois-1-10-ldap-injection-py
        rows = conn.search_s(settings.LDAP_BASE_DN, ldap.SCOPE_SUBTREE, "(uid=" + uid + ")")
    return JsonResponse({"count": len(rows)})


def used_when_check_fails(request):
    uid = request.GET.get("uid", "")
    conn = ldap.initialize(settings.LDAP_URI)
    rows = []
    if not re.fullmatch(r"[a-z0-9]+", uid):
        # ruleid: mois-1-10-ldap-injection-py
        rows = conn.search_s(settings.LDAP_BASE_DN, ldap.SCOPE_SUBTREE, "(uid=" + uid + ")")
    return JsonResponse({"count": len(rows)})


def exits_when_check_passes(request):
    uid = request.GET.get("uid", "")
    # 조건이 반대: 형식이 맞으면 빠져나가고, 맞지 않는 값으로 검색한다
    if UID_RE.fullmatch(uid):
        return HttpResponseBadRequest("reserved")
    conn = ldap.initialize(settings.LDAP_URI)
    # ruleid: mois-1-10-ldap-injection-py
    rows = conn.search_s(settings.LDAP_BASE_DN, ldap.SCOPE_SUBTREE, "(uid=" + uid + ")")
    return JsonResponse({"count": len(rows)})


def other_variable_checked(request):
    uid = request.GET.get("uid", "")
    dept = request.GET.get("dept", "")
    if not uid or not UID_RE.fullmatch(uid):
        return HttpResponseBadRequest("invalid uid")
    conn = ldap.initialize(settings.LDAP_URI)
    # 검사한 변수는 uid 뿐이다
    # ruleid: mois-1-10-ldap-injection-py
    rows = conn.search_s(settings.LDAP_BASE_DN, ldap.SCOPE_SUBTREE, "(&(uid=" + uid + ")(ou=" + dept + "))")
    return JsonResponse({"count": len(rows)})


def escape_result_discarded(request):
    uid = request.GET.get("uid", "")
    escape_filter_chars(uid)
    conn = ldap.initialize(settings.LDAP_URI)
    # ruleid: mois-1-10-ldap-injection-py
    rows = conn.search_s(settings.LDAP_BASE_DN, ldap.SCOPE_SUBTREE, "(uid=" + uid + ")")
    return JsonResponse({"count": len(rows)})


def sink_inside_failing_branch(request):
    uid = request.GET.get("uid", "")
    conn = ldap.initialize(settings.LDAP_URI)
    if not UID_RE.fullmatch(uid):
        # 형식이 틀린 값으로 검색하고 빠져나간다
        # ruleid: mois-1-10-ldap-injection-py
        return JsonResponse({"count": len(conn.search_s(settings.LDAP_BASE_DN, ldap.SCOPE_SUBTREE, "(uid=" + uid + ")"))})
    return JsonResponse({"count": 0})


def nested_conditional_exit(request):
    uid = request.GET.get("uid", "")
    conn = ldap.initialize(settings.LDAP_URI)
    if not UID_RE.fullmatch(uid):
        if request.GET.get("strict"):
            return JsonResponse({"ok": True})
    # 엄격 모드가 아니면 검사에 실패한 값이 그대로 내려온다
    # ruleid: mois-1-10-ldap-injection-py
    conn.search_s(settings.LDAP_BASE_DN, ldap.SCOPE_SUBTREE, "(uid=" + uid + ")")
    return JsonResponse({"ok": True})


def reassigned_after_check(request):
    uid = request.GET.get("uid", "")
    conn = ldap.initialize(settings.LDAP_URI)
    if not UID_RE.fullmatch(uid):
        return JsonResponse({"ok": True})
    # 검사한 뒤에 다른 입력으로 바꿔 넣는다
    uid = request.GET.get("alias", "")
    # ruleid: mois-1-10-ldap-injection-py
    conn.search_s(settings.LDAP_BASE_DN, ldap.SCOPE_SUBTREE, "(uid=" + uid + ")")
    return JsonResponse({"ok": True})


def appended_after_check(request):
    uid = request.GET.get("uid", "")
    conn = ldap.initialize(settings.LDAP_URI)
    if not UID_RE.fullmatch(uid):
        return JsonResponse({"ok": True})
    # 검사한 뒤에 검사하지 않은 입력을 덧붙인다
    uid += request.GET.get("suffix", "")
    # ruleid: mois-1-10-ldap-injection-py
    conn.search_s(settings.LDAP_BASE_DN, ldap.SCOPE_SUBTREE, "(uid=" + uid + ")")
    return JsonResponse({"ok": True})


def check_joined_with_and(request):
    uid = request.GET.get("uid", "")
    conn = ldap.initialize(settings.LDAP_URI)
    # 엄격 모드일 때만 검사한다
    if request.GET.get("strict") and not UID_RE.fullmatch(uid):
        return JsonResponse({"ok": True})
    # ruleid: mois-1-10-ldap-injection-py
    conn.search_s(settings.LDAP_BASE_DN, ldap.SCOPE_SUBTREE, "(uid=" + uid + ")")
    return JsonResponse({"ok": True})


def check_joined_with_or(request):
    uid = request.GET.get("uid", "")
    conn = ldap.initialize(settings.LDAP_URI)
    # or 로 묶이면 검사를 통과하지 않은 값도 들어온다
    if request.user.is_staff or UID_RE.fullmatch(uid):
        # ruleid: mois-1-10-ldap-injection-py
        conn.search_s(settings.LDAP_BASE_DN, ldap.SCOPE_SUBTREE, "(uid=" + uid + ")")
    return JsonResponse({"ok": True})


def filter_format_template_from_request(request):
    uid = request.GET.get("uid", "")
    conn = ldap.initialize(settings.LDAP_URI)
    # filter_format 은 인자만 이스케이프한다 — 틀을 요청에서 받으면 그대로 필터가 된다
    flt = ldap.filter.filter_format(request.GET.get("filter", "(uid=%s)"), [uid])
    # ruleid: mois-1-10-ldap-injection-py
    conn.search_s(settings.LDAP_BASE_DN, ldap.SCOPE_SUBTREE, flt)
    return JsonResponse({"ok": True})


def filter_format_template_concatenated(request):
    uid = request.GET.get("uid", "")
    conn = ldap.initialize(settings.LDAP_URI)
    # 입력을 틀에 이어 붙이면 이스케이프되지 않는다 (인자 목록이 비어 있다)
    flt = ldap.filter.filter_format("(&(objectClass=person)(uid=" + uid + "))", [])
    # ruleid: mois-1-10-ldap-injection-py
    conn.search_s(settings.LDAP_BASE_DN, ldap.SCOPE_SUBTREE, flt)
    return JsonResponse({"ok": True})
