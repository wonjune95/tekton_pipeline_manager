import ldap
from django.conf import settings
from django.http import JsonResponse


def lookup_user(request):
    uid = request.GET.get("uid", "")
    conn = ldap.initialize(settings.LDAP_URI)
    conn.simple_bind_s(settings.LDAP_BIND_DN, settings.LDAP_BIND_PASSWORD)
    # 외부 입력을 검색 필터에 이어 붙임
    # ruleid: mois-1-10-ldap-injection-py
    result = conn.search_s(settings.LDAP_BASE_DN, ldap.SCOPE_SUBTREE, "(uid=" + uid + ")", ["cn", "mail"])
    return JsonResponse({"count": len(result)})
