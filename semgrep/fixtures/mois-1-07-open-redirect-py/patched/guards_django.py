"""guard 형태별 안전한 예제 (Django)."""
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import redirect
from django.utils.http import is_safe_url, url_has_allowed_host_and_scheme  # is_safe_url: Django 3.x 까지의 이름

from .conf import ALLOWED_HOSTS




def guard_1(request):
    next_url = request.GET.get("next", "")
    if not url_has_allowed_host_and_scheme(next_url, allowed_hosts=ALLOWED_HOSTS):
        return HttpResponseBadRequest("invalid")
    # ok: mois-1-07-open-redirect-py 실패하면 return
    response = redirect(next_url)
    return response


def guard_2(request):
    next_url = request.GET.get("next", "")
    if not url_has_allowed_host_and_scheme(url=next_url, allowed_hosts=ALLOWED_HOSTS, require_https=True):
        raise ValueError("invalid")
    # ok: mois-1-07-open-redirect-py 실패하면 raise
    response = redirect(next_url)
    return response


def guard_3(request):
    next_url = request.GET.get("next", "")
    if not is_safe_url(next_url, allowed_hosts=ALLOWED_HOSTS):
        return HttpResponseBadRequest("invalid")
    # ok: mois-1-07-open-redirect-py 실패하면 return
    response = redirect(next_url)
    return response


def guard_4(request):
    next_url = request.GET.get("next", "")
    if not next_url or not url_has_allowed_host_and_scheme(next_url, allowed_hosts=ALLOWED_HOSTS):
        raise ValueError("invalid")
    # ok: mois-1-07-open-redirect-py 값이 없거나 실패하면 raise
    response = redirect(next_url)
    return response


def guard_5(request):
    next_url = request.GET.get("next", "")
    if not next_url or not url_has_allowed_host_and_scheme(url=next_url, allowed_hosts=ALLOWED_HOSTS, require_https=True):
        return HttpResponseBadRequest("invalid")
    # ok: mois-1-07-open-redirect-py 값이 없거나 실패하면 return
    response = redirect(next_url)
    return response


def guard_6(request):
    next_url = request.GET.get("next", "")
    if not next_url or not is_safe_url(next_url, allowed_hosts=ALLOWED_HOSTS):
        raise ValueError("invalid")
    # ok: mois-1-07-open-redirect-py 값이 없거나 실패하면 raise
    response = redirect(next_url)
    return response


def guard_7(request):
    for next_url in request.GET.getlist("next"):
        if not url_has_allowed_host_and_scheme(next_url, allowed_hosts=ALLOWED_HOSTS):
            continue
        # ok: mois-1-07-open-redirect-py 실패한 값은 건너뜀
        response = redirect(next_url)
    return response


def guard_8(request):
    for next_url in request.GET.getlist("next"):
        if not next_url or not is_safe_url(next_url, allowed_hosts=ALLOWED_HOSTS):
            continue
        # ok: mois-1-07-open-redirect-py 비었거나 실패한 값은 건너뜀
        response = redirect(next_url)
    return response


def guard_9(request):
    next_url = request.GET.get("next", "")
    if url_has_allowed_host_and_scheme(next_url, allowed_hosts=ALLOWED_HOSTS):
        # ok: mois-1-07-open-redirect-py 검사를 통과한 조건 안에서만 사용
        response = redirect(next_url)
    return response


def guard_10(request):
    next_url = request.GET.get("next", "")
    if url_has_allowed_host_and_scheme(url=next_url, allowed_hosts=ALLOWED_HOSTS, require_https=True):
        # ok: mois-1-07-open-redirect-py 검사를 통과한 조건 안에서만 사용
        response = redirect(next_url)
    return response


def guard_11(request):
    next_url = request.GET.get("next", "")
    if is_safe_url(next_url, allowed_hosts=ALLOWED_HOSTS):
        # ok: mois-1-07-open-redirect-py 검사를 통과한 조건 안에서만 사용
        response = redirect(next_url)
    return response
