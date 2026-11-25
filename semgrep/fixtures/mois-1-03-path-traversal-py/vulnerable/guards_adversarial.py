"""기준 디렉터리 검사를 속이는 형태 (2) — & · | 연산자, 검사 뒤에 바뀌는 값. 모두 탐지되어야 한다."""
import os
from pathlib import Path

from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest

BASE = Path("/srv/media")


# ---- & · | 로 묶인 검사 ----
def check_joined_with_bitand(request, strict):
    base = os.path.realpath(settings.MEDIA_ROOT)
    target = os.path.realpath(os.path.join(base, request.GET.get("name", "")))
    # & 는 and 와 같다: strict 가 거짓이면 검사에 실패해도 내려온다
    if (not target.startswith(base + os.sep)) & strict:
        return HttpResponse("ok")
    # ruleid: mois-1-03-path-traversal-py
    os.remove(target)
    return HttpResponse("ok")


def check_joined_with_bitor(request):
    base = os.path.realpath(settings.MEDIA_ROOT)
    target = os.path.realpath(os.path.join(base, request.GET.get("name", "")))
    # | 는 or 와 같다
    if request.user.is_staff | target.startswith(base + os.sep):
        # ruleid: mois-1-03-path-traversal-py
        os.remove(target)
    return HttpResponse("ok")


# ---- 검사한 뒤에 값이 바뀌는 경우 ----
def guard_with_else_reassign(request):
    base = os.path.realpath(settings.MEDIA_ROOT)
    target = os.path.realpath(os.path.join(base, request.GET.get("name", "")))
    if not target.startswith(base + os.sep):
        return HttpResponse("ok")
    else:
        # 검사를 통과한 쪽에서 다른 입력으로 바꾼다
        target = os.path.join(base, request.GET.get("alias", ""))
    # ruleid: mois-1-03-path-traversal-py
    os.remove(target)
    return HttpResponse("ok")


def path_appended_after_check(request):
    target = (BASE / request.GET.get("name", "")).resolve()
    if not target.is_relative_to(BASE):
        return HttpResponse("ok")
    # 검사한 뒤에 검사하지 않은 입력을 이어 붙인다 (pathlib 의 /=)
    target /= request.GET.get("sub", "")
    # ruleid: mois-1-03-path-traversal-py
    return HttpResponse(target.read_bytes())


def positive_reassigned_inside(request):
    base = os.path.realpath(settings.MEDIA_ROOT)
    target = os.path.realpath(os.path.join(base, request.GET.get("name", "")))
    if target.startswith(base + os.sep):
        # 검사를 통과한 조건 안에서 다른 입력으로 바꾼다
        target = os.path.join(base, request.GET.get("alias", ""))
        # ruleid: mois-1-03-path-traversal-py
        os.remove(target)
    return HttpResponse("ok")


def positive_appended_inside(request):
    base = os.path.realpath(settings.MEDIA_ROOT)
    target = os.path.realpath(os.path.join(base, request.GET.get("name", "")))
    if target.startswith(base + os.sep):
        target += os.sep + request.GET.get("sub", "")
        # ruleid: mois-1-03-path-traversal-py
        os.remove(target)
    return HttpResponse("ok")


def positive_path_appended_inside(request):
    target = (BASE / request.GET.get("name", "")).resolve()
    if target.is_relative_to(BASE):
        target /= request.GET.get("sub", "")
        # ruleid: mois-1-03-path-traversal-py
        return HttpResponse(target.read_bytes())
    return HttpResponse("ok")


def positive_reassigned_in_nested_block(request):
    target = (BASE / request.GET.get("name", "")).resolve()
    if target.is_relative_to(BASE):
        if request.GET.get("alias"):
            target = BASE / request.GET.get("alias", "")
        # 안쪽 블록에서 바뀐 값이 내려온다
        # ruleid: mois-1-03-path-traversal-py
        return HttpResponse(target.read_bytes())
    return HttpResponse("ok")
