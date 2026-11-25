"""검증처럼 보이지만 다른 사이트로 보낼 수 있는 경우 — 모두 탐지되어야 한다."""
import logging

from django.http import HttpResponseBadRequest
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.http import url_has_allowed_host_and_scheme

logger = logging.getLogger(__name__)


def check_result_ignored(request):
    next_url = request.GET.get("next", "/")
    # 검사 결과를 쓰지 않음
    url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()})
    # ruleid: mois-1-07-open-redirect-py
    return redirect(next_url)


def failure_does_not_exit(request):
    next_url = request.GET.get("next", "/")
    if not url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
        print("external redirect", next_url)
    # ruleid: mois-1-07-open-redirect-py
    return redirect(next_url)


def opposite_branch(request):
    next_url = request.GET.get("next", "/")
    if url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
        return redirect("/")
    else:
        # ruleid: mois-1-07-open-redirect-py
        return redirect(next_url)


def used_when_check_fails(request):
    next_url = request.GET.get("next", "/")
    if not url_has_allowed_host_and_scheme(url=next_url, allowed_hosts={request.get_host()}):
        # ruleid: mois-1-07-open-redirect-py
        return redirect(next_url)
    return redirect("/")


def exits_when_check_passes(request):
    next_url = request.GET.get("next", "/")
    # 조건이 반대: 같은 호스트면 빠져나간다
    if url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
        return HttpResponseBadRequest("internal")
    # ruleid: mois-1-07-open-redirect-py
    return redirect(next_url)


def other_variable_checked(request):
    next_url = request.GET.get("next", "/")
    fallback = request.GET.get("fallback", "/")
    if not url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
        # 검사하지 않은 값으로 바꾼다
        next_url = fallback
    # ruleid: mois-1-07-open-redirect-py
    return redirect(next_url)


def other_variable_checked_or(request):
    next_url = request.GET.get("next", "/")
    fallback = request.GET.get("fallback", "/")
    if not next_url or not url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
        next_url = fallback
    # ruleid: mois-1-07-open-redirect-py
    return redirect(next_url)


def slash_then_input(request):
    target = request.GET.get("to", "")
    # "/" 바로 뒤에 입력: to=/evil.example 이면 //evil.example (다른 호스트)
    # ruleid: mois-1-07-open-redirect-py
    first = redirect("/" + target)
    # ruleid: mois-1-07-open-redirect-py
    second = redirect("/%s" % target)
    # ruleid: mois-1-07-open-redirect-py
    third = redirect(f"/{target}")
    return first or second or third


def host_not_fixed(request):
    host = request.GET.get("host", "")
    path = request.GET.get("path", "")
    # ruleid: mois-1-07-open-redirect-py
    first = redirect("https://" + host + "/welcome")
    # ruleid: mois-1-07-open-redirect-py
    second = redirect("https://%s/welcome" % host)
    # 호스트 뒤에 구분자가 없다: path=.evil.example 이면 portal.example.go.kr.evil.example
    # ruleid: mois-1-07-open-redirect-py
    third = redirect("https://portal.example.go.kr" + path)
    # ruleid: mois-1-07-open-redirect-py
    fourth = redirect(f"https://{host}.example.go.kr/welcome")
    return first or second or third or fourth


def literal_first_but_not_prefix(request, first_login, default_path):
    target = request.GET.get("to", "")
    site = request.GET.get("site", "")
    # 리터럴로 시작하지만 값은 입력에서 올 수 있는 식
    # ruleid: mois-1-07-open-redirect-py
    a = redirect("/welcome/" + site if first_login else target)
    # ruleid: mois-1-07-open-redirect-py
    b = redirect("/board/".join([site, target]))
    # ruleid: mois-1-07-open-redirect-py
    c = redirect("/home" + default_path and target)
    # ruleid: mois-1-07-open-redirect-py
    d = redirect("/home" + default_path < site or target)
    # 리터럴을 바꾸거나 없애는 연산: 접두가 남지 않는다
    # ruleid: mois-1-07-open-redirect-py
    e = redirect("/home" * first_login + target)
    # ruleid: mois-1-07-open-redirect-py
    f = redirect("/home".replace("/home", target))
    # ruleid: mois-1-07-open-redirect-py
    g = redirect("/home"[:0] + target)
    # ruleid: mois-1-07-open-redirect-py
    h = redirect("/welcome" if first_login else target)
    return a or b or c or d or e or f or g or h


def fallback_assigned_inside_other_branch(request):
    next_url = request.GET.get("next", "/")
    if not url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
        if request.user.is_staff:
            next_url = "/"
    # 일부 경우에만 바꾼다 — 나머지는 검사에 실패한 값 그대로
    # ruleid: mois-1-07-open-redirect-py
    return redirect(next_url)


def nested_conditional_exit(request):
    next_url = request.GET.get("next", "/")
    if not url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
        if request.GET.get("strict"):
            return redirect("/")
    # 엄격 모드가 아니면 검사에 실패한 값이 그대로 내려온다
    # ruleid: mois-1-07-open-redirect-py
    response = redirect(next_url)
    return response


def reassigned_after_check(request):
    next_url = request.GET.get("next", "/")
    if not url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
        return redirect("/")
    # 검사한 뒤에 다른 입력으로 바꿔 넣는다
    next_url = request.GET.get("return_to", "/")
    # ruleid: mois-1-07-open-redirect-py
    response = redirect(next_url)
    return response


def appended_after_check(request):
    next_url = request.GET.get("next", "/")
    if not url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
        return redirect("/")
    # 검사한 뒤에 검사하지 않은 입력을 덧붙인다 ("/" + "/evil.example" 은 다른 호스트다)
    next_url += request.GET.get("tail", "")
    # ruleid: mois-1-07-open-redirect-py
    response = redirect(next_url)
    return response


def check_joined_with_and(request):
    next_url = request.GET.get("next", "/")
    # 엄격 모드일 때만 검사한다
    if request.GET.get("strict") and not url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
        return redirect("/")
    # ruleid: mois-1-07-open-redirect-py
    response = redirect(next_url)
    return response


def check_joined_with_or(request):
    next_url = request.GET.get("next", "/")
    # or 로 묶이면 검사를 통과하지 않은 값도 들어온다
    if request.user.is_staff or url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
        # ruleid: mois-1-07-open-redirect-py
        return redirect(next_url)
    return redirect("/")


def fallback_used_before_replacing(request):
    next_url = request.GET.get("next", "/")
    response = redirect("/")
    if not url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
        # 바꾸기 전에 실패한 값을 쓴다
        # ruleid: mois-1-07-open-redirect-py
        response = redirect(next_url)
        next_url = "/"
    return response


def fallback_then_reassigned(request):
    next_url = request.GET.get("next", "/")
    if not url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
        next_url = "/"
    # 바꾼 뒤에 다른 입력으로 다시 덮어쓴다
    next_url = request.GET.get("return_to", next_url)
    # ruleid: mois-1-07-open-redirect-py
    return redirect(next_url)


def fallback_then_appended(request):
    next_url = request.GET.get("next", "/")
    if not url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
        next_url = "/"
    # 바꾼 뒤에 검사하지 않은 입력을 덧붙인다
    next_url += request.GET.get("tail", "")
    # ruleid: mois-1-07-open-redirect-py
    return redirect(next_url)


def fallback_joined_with_and(request):
    next_url = request.GET.get("next", "/")
    if request.GET.get("strict") and not url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
        next_url = "/"
    # ruleid: mois-1-07-open-redirect-py
    return redirect(next_url)


# ---- 호스트가 비었는지만 보는 검사(netloc) — 어떤 형태로 써도 인정하지 않는다 (vulnerable/netloc.py 참고) ----
from urllib.parse import urlsplit as _urlsplit


def netloc_result_ignored(request):
    target = request.GET.get("next", "")
    _urlsplit(target).netloc != ""
    # ruleid: mois-1-07-open-redirect-py
    return redirect(target)


def netloc_failure_only_logged(request):
    target = request.GET.get("next", "")
    if _urlsplit(target).netloc != "":
        logger.warning("external redirect requested")
    # ruleid: mois-1-07-open-redirect-py
    return redirect(target)


def netloc_used_in_failing_branch(request):
    target = request.GET.get("next", "")
    if _urlsplit(target).netloc != "":
        # ruleid: mois-1-07-open-redirect-py
        return redirect(target)
    return redirect("/")


def netloc_replaced_with_input(request):
    target = request.GET.get("next", "")
    if _urlsplit(target).netloc != "":
        target = request.GET.get("fallback", "")
    # ruleid: mois-1-07-open-redirect-py
    return redirect(target)


def input_before_framework_path(request):
    host = request.GET.get("host", "")
    # ruleid: mois-1-07-open-redirect-py
    return redirect(host + reverse("search"))


def input_before_framework_path_then_literal(request):
    host = request.GET.get("host", "")
    # reverse(...) 가 식 안에 있지만 맨 앞이 아니다
    # ruleid: mois-1-07-open-redirect-py
    return redirect(host + reverse("search") + "?q=1")


def input_right_after_framework_path(request):
    target = request.GET.get("to", "")
    # 경로가 "/" 인 라우트면 "/" + "/evil.example" = "//evil.example" (다른 호스트)
    # ruleid: mois-1-07-open-redirect-py
    first = redirect(reverse("home") + target)
    # ruleid: mois-1-07-open-redirect-py
    second = redirect(reverse("home") + "/" + target)
    # ruleid: mois-1-07-open-redirect-py
    third = redirect(reverse("home") + f"{target}")
    return first or second or third


def framework_path_not_kept(request, first_login):
    target = request.GET.get("to", "")
    site = request.GET.get("site", "")
    # reverse(...) + 리터럴로 시작하지만 값은 입력에서 올 수 있는 식
    # ruleid: mois-1-07-open-redirect-py
    a = redirect(reverse("search") + "?q=" + site if first_login else target)
    # ruleid: mois-1-07-open-redirect-py
    b = redirect(reverse("search") + "?q=" + site and target)
    # ruleid: mois-1-07-open-redirect-py
    c = redirect(reverse("search") + "?q=" + site < site or target)
    # ruleid: mois-1-07-open-redirect-py
    d = redirect(reverse("search") * first_login + "?q=" + target)
    # ruleid: mois-1-07-open-redirect-py
    e = redirect(reverse("search") + "?q=".replace("?q=", target))
    return a or b or c or d or e


def path_named_query_value(request):
    # request.path 가 아니라 이름이 "path" 인 질의 값 — 전체 주소를 넣을 수 있다
    path = request.GET.get("path", "/")
    # ruleid: mois-1-07-open-redirect-py
    return redirect(path)


def netloc_check_joined_with_and(request):
    target = request.GET.get("next", "")
    # 엄격 모드일 때만 호스트를 확인한다
    if request.GET.get("strict") and _urlsplit(target).netloc != "":
        return redirect("/")
    # ruleid: mois-1-07-open-redirect-py
    return redirect(target)


def netloc_exits_when_local(request):
    target = request.GET.get("next", "")
    # 조건이 반대: 호스트가 없는(안전한) 주소일 때 빠져나간다
    if _urlsplit(target).netloc == "":
        return redirect("/")
    # ruleid: mois-1-07-open-redirect-py
    return redirect(target)


# ---- & · | 로 묶인 검사 ----
def check_joined_with_bitand(request, strict):
    next_url = request.GET.get("next", "/")
    # & 는 and 와 같다: strict 가 거짓이면 검사에 실패해도 내려온다
    if (not url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()})) & strict:
        return redirect("/")
    # ruleid: mois-1-07-open-redirect-py
    return redirect(next_url)


def fallback_joined_with_bitand(request, strict):
    next_url = request.GET.get("next", "/")
    if (not url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()})) & strict:
        next_url = "/"
    # ruleid: mois-1-07-open-redirect-py
    return redirect(next_url)


def check_joined_with_bitor(request):
    next_url = request.GET.get("next", "/")
    # | 는 or 와 같다
    if request.user.is_staff | url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
        # ruleid: mois-1-07-open-redirect-py
        return redirect(next_url)
    return redirect("/")


# ---- 검사한 뒤에 값이 바뀌는 경우 ----
def positive_reassigned_inside(request):
    next_url = request.GET.get("next", "/")
    if url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
        # 검사를 통과한 조건 안에서 다른 입력으로 바꾼다
        next_url = request.GET.get("return_to", "/")
        # ruleid: mois-1-07-open-redirect-py
        return redirect(next_url)
    return redirect("/")


def positive_appended_inside(request):
    next_url = request.GET.get("next", "/")
    if url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
        next_url += request.GET.get("tail", "")
        # ruleid: mois-1-07-open-redirect-py
        return redirect(next_url)
    return redirect("/")


def guard_with_else_reassign(request):
    next_url = request.GET.get("next", "/")
    if not url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
        return redirect("/")
    else:
        # 검사를 통과한 쪽에서 다른 입력으로 바꾼다
        next_url = request.GET.get("return_to", "/")
    # ruleid: mois-1-07-open-redirect-py
    return redirect(next_url)


def fallback_with_else_reassign(request):
    next_url = request.GET.get("next", "/")
    if not url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
        next_url = "/"
    else:
        next_url = request.GET.get("return_to", "/")
    # ruleid: mois-1-07-open-redirect-py
    return redirect(next_url)


def fallback_to_resolved_input(request):
    from django.shortcuts import resolve_url

    next_url = request.GET.get("next", "/")
    if not url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
        # resolve_url 은 "/" 나 "." 이 든 값을 그대로 돌려준다 — 검사에 실패한 값이 그대로 남는다
        next_url = resolve_url(next_url)
    # ruleid: mois-1-07-open-redirect-py
    return redirect(next_url)
