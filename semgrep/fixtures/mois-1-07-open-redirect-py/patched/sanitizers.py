from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, resolve_url
from django.urls import reverse
from django.utils.http import url_has_allowed_host_and_scheme


def fixed_path_prefix(request):
    board = request.GET.get("board", "")
    # ok: mois-1-07-open-redirect-py 앞부분이 고정된 상대 경로
    first = redirect("/board/" + board)
    # ok: mois-1-07-open-redirect-py
    second = redirect("/board/%s/list" % board)
    # ok: mois-1-07-open-redirect-py
    third = redirect("/board/{}/list".format(board))
    # ok: mois-1-07-open-redirect-py
    fourth = redirect(f"/board/{board}/list")
    # ok: mois-1-07-open-redirect-py 값은 질의 문자열에만 들어간다
    fifth = redirect("/login?next=" + board)
    return first or second or third or fourth or fifth


def fixed_host(request):
    doc = request.GET.get("doc", "")
    # ok: mois-1-07-open-redirect-py 스킴과 호스트가 리터럴로 고정됨
    first = HttpResponseRedirect("https://docs.example.go.kr/view/" + doc)
    # ok: mois-1-07-open-redirect-py
    second = HttpResponseRedirect(f"https://docs.example.go.kr/view?id={doc}")
    return first or second


def named_route(request):
    # ok: mois-1-07-open-redirect-py 라우트 이름으로 만든 주소
    first = redirect(reverse("board:detail", args=[request.GET.get("id", "0")]))
    # ok: mois-1-07-open-redirect-py 정수로 바꾼 값 (상대 주소)
    second = redirect("../%d/" % int(request.GET.get("page", "1")))
    return first or second


def both_branches_fixed(request, first_login):
    # ok: mois-1-07-open-redirect-py 조건식이어도 양쪽이 모두 고정 값
    return redirect("/welcome" if first_login else "/home")


def fallback_when_missing_or_external(request):
    next_url = request.GET.get("next")
    if not next_url or not url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
        next_url = "/"
    # ok: mois-1-07-open-redirect-py 값이 없거나 다른 호스트면 "/" 로 바꿈
    return redirect(next_url)


def fallback_to_settings(request):
    next_url = request.POST.get("next", "")
    if not next_url or not url_has_allowed_host_and_scheme(url=next_url, allowed_hosts={request.get_host()}):
        next_url = settings.LOGIN_REDIRECT_URL
    # ok: mois-1-07-open-redirect-py
    return redirect(next_url)


def fallback_to_named_route(request):
    next_url = request.GET.get("next", "")
    if not url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
        next_url = reverse("home")
    # ok: mois-1-07-open-redirect-py
    return redirect(next_url)


def fallback_to_resolved_url(request):
    next_url = request.GET.get("next", "")
    if not url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
        next_url = resolve_url(settings.LOGIN_REDIRECT_URL)
    # ok: mois-1-07-open-redirect-py
    return redirect(next_url)


def fallback_legacy_check(request):
    from django.utils.http import is_safe_url  # Django 3.x 까지의 이름

    next_url = request.GET.get("next", "")
    if not is_safe_url(next_url, allowed_hosts={request.get_host()}):
        next_url = "/"
    # ok: mois-1-07-open-redirect-py
    return redirect(next_url)


def fallback_to_named_url(request):
    next_url = request.GET.get("next", "")
    if not url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
        next_url = resolve_url("home")
    # ok: mois-1-07-open-redirect-py 실패하면 라우트 이름(리터럴)으로 만든 주소로 바꿈
    return redirect(next_url)
