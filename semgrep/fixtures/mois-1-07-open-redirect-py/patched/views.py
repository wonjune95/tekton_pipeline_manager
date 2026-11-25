import django.urls
from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.http import url_has_allowed_host_and_scheme

PARTNER_SITES = {
    "portal": "https://portal.example.go.kr/",
    "help": "https://help.example.go.kr/",
}


def after_login(request):
    next_url = request.GET.get("next", "/")
    # 같은 호스트의 주소만 허용
    if not url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}, require_https=True):
        next_url = "/"
    # ok: mois-1-07-open-redirect-py 다른 호스트면 "/" 로 바꿈
    return redirect(next_url)


def outbound(request):
    # 허용 목록에 있는 사이트로만 이동
    url = PARTNER_SITES.get(request.GET.get("site", ""))
    if url is None:
        return HttpResponseBadRequest("unknown site")
    # ok: mois-1-07-open-redirect-py 같은 파일의 dict 에서 꺼낸 주소
    return HttpResponseRedirect(url)


# ---- reverse() 뒤에 덧붙인 값 ----
def back_to_path_info(request):
    # ok: mois-1-07-open-redirect-py path_info 는 공통 source 가 외부 입력으로 보지 않는다
    return redirect(request.path_info)


def search_with_query(request):
    q = request.GET.get("q", "")
    # ok: mois-1-07-open-redirect-py reverse() 로 만든 경로 뒤에 "?q=" 리터럴을 두고 질의 값을 붙인다
    return redirect(reverse("search") + "?q=" + q)


def search_with_tag(request):
    # ok: mois-1-07-open-redirect-py django.urls.reverse(...) 로 쓴 경우도 같다
    return redirect(django.urls.reverse("search") + "?tag=" + request.GET.get("tag", ""))
