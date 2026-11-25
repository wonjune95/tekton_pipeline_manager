"""기준 디렉터리 검사를 속이는 형태 (3) — 정규화하지 않은 경로, 정규화와 검사 사이·뒤에 바뀌는 경로. 모두 탐지되어야 한다."""
import os
from pathlib import Path

from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest

BASE = Path("/srv/media")


# ---- 정규화하지 않은 경로를 검사하는 경우 ("/srv/media/../../etc/passwd" 는 "/srv/media/" 로 시작한다) ----
def unnormalized_prefix_check(request):
    target = os.path.join(settings.MEDIA_ROOT, request.GET.get("name", ""))
    if not target.startswith(settings.MEDIA_ROOT + os.sep):
        return HttpResponseBadRequest("invalid path")
    # ruleid: mois-1-03-path-traversal-py
    os.remove(target)
    return HttpResponse("deleted")


def normalized_base_only(request):
    # 정규화한 것은 기준 디렉터리뿐이다
    target = os.path.join(os.path.realpath(settings.MEDIA_ROOT), request.GET.get("name", ""))
    if not target.startswith(settings.MEDIA_ROOT + os.sep):
        return HttpResponseBadRequest("invalid path")
    # ruleid: mois-1-03-path-traversal-py
    os.remove(target)
    return HttpResponse("deleted")


def unnormalized_positive_check(request):
    # pathlib 의 is_relative_to 도 ".." 을 풀지 않는다
    target = BASE / request.GET.get("name", "")
    if target.is_relative_to(BASE):
        # ruleid: mois-1-03-path-traversal-py
        return HttpResponse(target.read_bytes())
    return HttpResponse("ok")


def rejoined_before_check(request):
    base = os.path.realpath(settings.MEDIA_ROOT)
    target = os.path.realpath(os.path.join(base, request.GET.get("name", "")))
    # 정규화한 뒤에 입력을 다시 붙이고 나서 검사한다
    target = os.path.join(target, request.GET.get("sub", ""))
    if not target.startswith(base + os.sep):
        return HttpResponseBadRequest("invalid path")
    # ruleid: mois-1-03-path-traversal-py
    os.remove(target)
    return HttpResponse("deleted")


def appended_before_check(request):
    base = os.path.realpath(settings.MEDIA_ROOT)
    target = os.path.realpath(os.path.join(base, request.GET.get("name", "")))
    target += os.sep + request.GET.get("sub", "")
    if not target.startswith(base + os.sep):
        return HttpResponseBadRequest("invalid path")
    # ruleid: mois-1-03-path-traversal-py
    os.remove(target)
    return HttpResponse("deleted")


def path_appended_before_check(request):
    target = (BASE / request.GET.get("name", "")).resolve()
    target /= request.GET.get("sub", "")
    if not target.is_relative_to(BASE):
        return HttpResponseBadRequest("invalid path")
    # ruleid: mois-1-03-path-traversal-py
    return HttpResponse(target.read_bytes())


def positive_rejoined_before_check(request):
    base = os.path.realpath(settings.MEDIA_ROOT)
    target = os.path.realpath(os.path.join(base, request.GET.get("name", "")))
    target = os.path.join(target, request.GET.get("sub", ""))
    if target.startswith(base + os.sep):
        # ruleid: mois-1-03-path-traversal-py
        os.remove(target)
    return HttpResponse("deleted")


def positive_appended_before_check(request):
    base = os.path.realpath(settings.MEDIA_ROOT)
    target = os.path.realpath(os.path.join(base, request.GET.get("name", "")))
    target += os.sep + request.GET.get("sub", "")
    if target.startswith(base + os.sep):
        # ruleid: mois-1-03-path-traversal-py
        os.remove(target)
    return HttpResponse("deleted")


def positive_path_appended_before_check(request):
    target = (BASE / request.GET.get("name", "")).resolve()
    target /= request.GET.get("sub", "")
    if target.is_relative_to(BASE):
        # ruleid: mois-1-03-path-traversal-py
        return HttpResponse(target.read_bytes())
    return HttpResponse("ok")


# ---- 정규화는 바깥 블록에서, 검사와 재대입은 안쪽 블록에서 ----
# ---- 정규화는 바깥 블록에서, 검사와 재대입은 안쪽 블록에서 ----
def reassigned_after_check_in_block(request):
    base = os.path.realpath(settings.MEDIA_ROOT)
    target = os.path.realpath(os.path.join(base, request.GET.get("name", "")))
    if request.method == "POST":
        if not target.startswith(base + os.sep):
            return HttpResponse("ok")
        target = os.path.join(base, request.POST.get("alias", ""))
        # ruleid: mois-1-03-path-traversal-py
        os.remove(target)
    return HttpResponse("ok")


def appended_after_check_in_block(request):
    base = os.path.realpath(settings.MEDIA_ROOT)
    target = os.path.realpath(os.path.join(base, request.GET.get("name", "")))
    if request.method == "POST":
        if not target.startswith(base + os.sep):
            return HttpResponse("ok")
        target += os.sep + request.POST.get("sub", "")
        # ruleid: mois-1-03-path-traversal-py
        os.remove(target)
    return HttpResponse("ok")


def path_appended_after_check_in_block(request):
    target = (BASE / request.GET.get("name", "")).resolve()
    if request.method == "POST":
        if not target.is_relative_to(BASE):
            return HttpResponse("ok")
        target /= request.POST.get("sub", "")
        # ruleid: mois-1-03-path-traversal-py
        return HttpResponse(target.read_bytes())
    return HttpResponse("ok")
