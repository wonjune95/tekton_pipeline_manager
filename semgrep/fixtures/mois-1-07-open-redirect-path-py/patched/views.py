"""요청 경로를 쓰지만 주소의 맨 앞이 고정되어 있거나, 프레임워크 검사를 통과한 경우 (Django)."""
from django.core.exceptions import SuspiciousOperation
from django.http import HttpResponseBadRequest, HttpResponsePermanentRedirect
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.http import url_has_allowed_host_and_scheme


# ---- 고정 접두 뒤에 붙인 경로 ----
def login_redirect(request):
    # ok: mois-1-07-open-redirect-path-py 고정된 상대 경로 뒤(질의 문자열)에 들어간다
    first = redirect("/accounts/login/?next=" + request.path)
    # ok: mois-1-07-open-redirect-path-py
    second = redirect("/accounts/login/?next=%s" % request.get_full_path())
    # ok: mois-1-07-open-redirect-path-py
    third = redirect("/accounts/login/?next={}".format(request.path))
    # ok: mois-1-07-open-redirect-path-py
    fourth = redirect(f"/accounts/login/?next={request.path}")
    return first or second or third or fourth


def canonical_host(request):
    # ok: mois-1-07-open-redirect-path-py 스킴과 호스트가 리터럴로 고정됨
    return HttpResponsePermanentRedirect("https://www.example.go.kr/app" + request.get_full_path())


# ---- 프레임워크가 만든 경로 ----
def login_redirect_named(request):
    # ok: mois-1-07-open-redirect-path-py reverse() 로 만든 경로 뒤에 "?next=" 리터럴을 두고 붙인다
    return redirect(reverse("login") + "?next=" + request.path)


def board_redirect(request, board_id):
    # ok: mois-1-07-open-redirect-path-py 인자에 괄호가 든 호출, 리터럴이 f-string 인 경우
    return redirect(reverse("board:detail", args=(board_id,)) + f"?from={request.path}")


def docs_redirect(request):
    # ok: mois-1-07-open-redirect-path-py 경로는 reverse() 의 인자로만 들어간다 (reverse 는 "//" 로 시작하는 주소를 만들지 않는다)
    return redirect(reverse("docs:page", kwargs={"path": request.path}))


# ---- Django 의 호스트·스킴 검사 ----
def checked_then_redirect(request):
    path = request.get_full_path()
    if not url_has_allowed_host_and_scheme(path, allowed_hosts=None):
        return HttpResponseBadRequest("invalid path")
    # ok: mois-1-07-open-redirect-path-py "//host" · "/\\host" 면 위에서 return
    return redirect(path)


def checked_or_raise(request):
    path = request.get_full_path()
    if not path or not url_has_allowed_host_and_scheme(path, allowed_hosts={request.get_host()}):
        raise SuspiciousOperation("invalid path")
    # ok: mois-1-07-open-redirect-path-py 실패하면 raise
    return redirect(path)


def redirect_only_when_checked(request):
    path = request.get_full_path()
    if url_has_allowed_host_and_scheme(path, allowed_hosts=None):
        # ok: mois-1-07-open-redirect-path-py 검사를 통과한 조건 안에서만 사용
        return redirect(path)
    return redirect("/")
