import ldap
from django.conf import settings
from django.http import JsonResponse
from ldap.filter import escape_filter_chars


def lookup_user(request):
    uid = request.GET.get("uid", "")
    conn = ldap.initialize(settings.LDAP_URI)
    conn.simple_bind_s(settings.LDAP_BIND_DN, settings.LDAP_BIND_PASSWORD)
    # ok: mois-1-10-ldap-injection-py 필터 특수문자를 이스케이프
    result = conn.search_s(settings.LDAP_BASE_DN, ldap.SCOPE_SUBTREE, "(uid=" + escape_filter_chars(uid) + ")", ["cn", "mail"])
    return JsonResponse({"count": len(result)})
