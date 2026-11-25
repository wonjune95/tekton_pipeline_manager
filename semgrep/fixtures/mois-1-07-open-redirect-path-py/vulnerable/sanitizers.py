"""검증처럼 보이지만 요청 경로가 주소의 맨 앞에 그대로 올 수 있는 경우 — 모두 탐지되어야 한다."""
import logging

from django.http import HttpResponseBadRequest
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.http import url_has_allowed_host_and_scheme

logger = logging.getLogger(__name__)


# ---- 고정 접두가 아닌 식 ----
def slash_then_path(request):
    # "/" 바로 뒤에 경로: "/" + "/admin" = "//admin" (호스트가 admin 인 주소)
    # ruleid: mois-1-07-open-redirect-path-py
    first = redirect("/" + request.path)
    # ruleid: mois-1-07-open-redirect-path-py
    second = redirect("/%s" % request.path)
    # ruleid: mois-1-07-open-redirect-path-py
    third = redirect(f"/{request.path}")
    return first or second or third


def literal_first_but_not_prefix(request, first_login, site):
    # 리터럴로 시작하지만 값은 요청 경로에서 올 수 있는 식
    # ruleid: mois-1-07-open-redirect-path-py
    a = redirect("/welcome/" + site if first_login else request.path)
    # ruleid: mois-1-07-open-redirect-path-py
    b = redirect("/home" + site and request.path)
    # ruleid: mois-1-07-open-redirect-path-py
    c = redirect("/home" + site < site or request.path)
    # ruleid: mois-1-07-open-redirect-path-py
    d = redirect("/home".replace("/home", request.path))
    return a or b or c or d


def path_right_after_framework_path(request):
    # 경로가 "/" 인 라우트면 "/" + "/evil.example" = "//evil.example"
    # ruleid: mois-1-07-open-redirect-path-py
    return redirect(reverse("home") + request.path)


def framework_path_not_kept(request, first_login, site):
    # reverse(...) + 리터럴로 시작하지만 값은 요청 경로에서 올 수 있는 식
    # ruleid: mois-1-07-open-redirect-path-py
    a = redirect(reverse("search") + "?from=" + site if first_login else request.path)
    # ruleid: mois-1-07-open-redirect-path-py
    b = redirect(reverse("search") + "?from=" + site and request.path)
    # ruleid: mois-1-07-open-redirect-path-py
    c = redirect(reverse("search") + "?from=" + site < site or request.path)
    return a or b or c


# ---- 호스트·스킴 검사를 속이는 형태 ----
def check_result_ignored(request):
    path = request.get_full_path()
    # 검사 결과를 쓰지 않음
    url_has_allowed_host_and_scheme(path, allowed_hosts=None)
    # ruleid: mois-1-07-open-redirect-path-py
    return redirect(path)


def failure_does_not_exit(request):
    path = request.get_full_path()
    if not url_has_allowed_host_and_scheme(path, allowed_hosts=None):
        logger.warning("suspicious path")
    # ruleid: mois-1-07-open-redirect-path-py
    return redirect(path)


def used_when_check_fails(request):
    path = request.get_full_path()
    if not url_has_allowed_host_and_scheme(path, allowed_hosts=None):
        # ruleid: mois-1-07-open-redirect-path-py
        return redirect(path)
    return redirect("/")


def opposite_branch(request):
    path = request.get_full_path()
    if url_has_allowed_host_and_scheme(path, allowed_hosts=None):
        return redirect("/")
    else:
        # ruleid: mois-1-07-open-redirect-path-py
        return redirect(path)


def check_joined_with_and(request):
    path = request.get_full_path()
    # 엄격 모드일 때만 검사한다
    if request.GET.get("strict") and not url_has_allowed_host_and_scheme(path, allowed_hosts=None):
        return HttpResponseBadRequest("invalid path")
    # ruleid: mois-1-07-open-redirect-path-py
    return redirect(path)


def check_joined_with_bitand(request, strict):
    path = request.get_full_path()
    if (not url_has_allowed_host_and_scheme(path, allowed_hosts=None)) & strict:
        return HttpResponseBadRequest("invalid path")
    # ruleid: mois-1-07-open-redirect-path-py
    return redirect(path)


def check_joined_with_or(request):
    path = request.get_full_path()
    if request.user.is_staff or url_has_allowed_host_and_scheme(path, allowed_hosts=None):
        # ruleid: mois-1-07-open-redirect-path-py
        return redirect(path)
    return redirect("/")


def check_joined_with_bitor(request):
    path = request.get_full_path()
    if request.user.is_staff | url_has_allowed_host_and_scheme(path, allowed_hosts=None):
        # ruleid: mois-1-07-open-redirect-path-py
        return redirect(path)
    return redirect("/")


def guard_with_else_reassign(request):
    path = request.get_full_path()
    if not url_has_allowed_host_and_scheme(path, allowed_hosts=None):
        return HttpResponseBadRequest("invalid path")
    else:
        # 검사를 통과한 쪽에서 검사하지 않은 값으로 바꾼다
        path = request.path
    # ruleid: mois-1-07-open-redirect-path-py
    return redirect(path)


def reassigned_after_check(request):
    path = request.get_full_path()
    if not url_has_allowed_host_and_scheme(path, allowed_hosts=None):
        return HttpResponseBadRequest("invalid path")
    # 검사한 뒤에 검사하지 않은 값으로 바꿔 넣는다
    path = request.path
    # ruleid: mois-1-07-open-redirect-path-py
    return redirect(path)


def appended_after_check(request):
    path = request.GET.get("prefix", "")
    current = request.path
    if not url_has_allowed_host_and_scheme(current, allowed_hosts=None):
        return HttpResponseBadRequest("invalid path")
    # 검사한 변수 앞에 다른 값을 놓는 대신, 검사하지 않은 경로를 이어 붙인다
    current += request.get_full_path()
    # ruleid: mois-1-07-open-redirect-path-py
    return redirect(current)


def positive_reassigned_inside(request):
    path = request.get_full_path()
    if url_has_allowed_host_and_scheme(path, allowed_hosts=None):
        path = request.path
        # ruleid: mois-1-07-open-redirect-path-py
        return redirect(path)
    return redirect("/")


def positive_appended_inside(request):
    path = request.get_full_path()
    if url_has_allowed_host_and_scheme(path, allowed_hosts=None):
        path += request.path
        # ruleid: mois-1-07-open-redirect-path-py
        return redirect(path)
    return redirect("/")
