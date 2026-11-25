import re

import ldap
from django.conf import settings
from django.http import JsonResponse
from ldap.dn import escape_dn_chars
from ldap.filter import filter_format
from ldap3.utils.dn import escape_rdn

def escaped_dn(request):
    dept = request.GET.get("dept", "")
    team = request.GET.get("team", "")
    conn = ldap.initialize(settings.LDAP_URI)
    # ok: mois-1-10-ldap-injection-py DN 값 이스케이프
    rows = conn.search_s("ou=" + escape_dn_chars(dept) + ",dc=example,dc=go,dc=kr", ldap.SCOPE_ONELEVEL)
    # ok: mois-1-10-ldap-injection-py
    rows += conn.search_s("ou=" + escape_rdn(team) + ",dc=example,dc=go,dc=kr", ldap.SCOPE_ONELEVEL)
    return JsonResponse({"count": len(rows)})


def formatted_filter(request):
    conn = ldap.initialize(settings.LDAP_URI)
    # ok: mois-1-10-ldap-injection-py filter_format 은 인자를 이스케이프해 끼워 넣는다
    flt = filter_format("(&(uid=%s)(employeeNumber=%s))", [request.GET.get("uid", ""), request.GET.get("no", "")])
    rows = conn.search_s(settings.LDAP_BASE_DN, ldap.SCOPE_SUBTREE, flt)
    # ok: mois-1-10-ldap-injection-py 정수로 바꾼 값
    rows += conn.search_s(settings.LDAP_BASE_DN, ldap.SCOPE_SUBTREE, "(uidNumber=%d)" % int(request.GET.get("id", "0")))
    return JsonResponse({"count": len(rows)})


def not_ldap(request):
    keyword = request.GET.get("q", "")
    # ok: mois-1-10-ldap-injection-py re.search·검색 엔진 클라이언트의 search 는 LDAP 이 아니다
    found = re.search("error", keyword, re.IGNORECASE)
    hits = settings.SEARCH_INDEX.search("docs", "title", keyword)
    return JsonResponse({"found": bool(found), "hits": len(hits)})
