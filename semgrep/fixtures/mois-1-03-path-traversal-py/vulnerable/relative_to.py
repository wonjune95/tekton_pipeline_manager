"""relative_to · safe_join 을 속이는 형태 — 모두 탐지되어야 한다."""
import contextlib
import logging
import os
from pathlib import Path

from django.http import HttpResponse, HttpResponseBadRequest
from werkzeug.utils import safe_join

BASE = Path("/srv/media")
logger = logging.getLogger(__name__)


# ---- 호출은 있지만 예외로 멈추지 않는 경우 ----
def relative_to_swallowed(request):
    target = (BASE / request.GET.get("name", "")).resolve()
    try:
        target.relative_to(BASE)
    except ValueError:
        pass
    # 예외를 삼켰다 — 기준 밖의 경로가 그대로 내려온다
    # ruleid: mois-1-03-path-traversal-py
    return HttpResponse(target.read_bytes())


def relative_to_only_logged(request):
    target = (BASE / request.GET.get("name", "")).resolve()
    try:
        target.relative_to(BASE)
    except ValueError as exc:
        logger.warning("outside base: %s", exc)
    # ruleid: mois-1-03-path-traversal-py
    return HttpResponse(target.read_bytes())


def relative_to_one_handler_swallows(request):
    target = (BASE / request.GET.get("name", "")).resolve()
    try:
        target.relative_to(BASE)
    except ValueError:
        pass
    except OSError:
        raise
    # 빠져나가는 except 는 OSError 쪽뿐이다
    # ruleid: mois-1-03-path-traversal-py
    return HttpResponse(target.read_bytes())


def relative_to_used_in_handler(request):
    target = (BASE / request.GET.get("name", "")).resolve()
    try:
        target.relative_to(BASE)
    except ValueError:
        # 기준 밖일 때 실행되는 자리에서 읽는다
        # ruleid: mois-1-03-path-traversal-py
        return HttpResponse(target.read_bytes())
    return HttpResponse("ok")


def relative_to_conditional_raise(request):
    target = (BASE / request.GET.get("name", "")).resolve()
    try:
        target.relative_to(BASE)
    except ValueError:
        if request.GET.get("strict"):
            raise
    # ruleid: mois-1-03-path-traversal-py
    return HttpResponse(target.read_bytes())


def relative_to_suppressed(request):
    target = (BASE / request.GET.get("name", "")).resolve()
    with contextlib.suppress(ValueError):
        target.relative_to(BASE)
    # ruleid: mois-1-03-path-traversal-py
    return HttpResponse(target.read_bytes())


def relative_to_only_in_strict_mode(request):
    target = (BASE / request.GET.get("name", "")).resolve()
    if request.GET.get("strict"):
        target.relative_to(BASE)
    # ruleid: mois-1-03-path-traversal-py
    return HttpResponse(target.read_bytes())


def relative_to_conditional_inside_try(request):
    target = (BASE / request.GET.get("name", "")).resolve()
    try:
        if request.GET.get("strict"):
            target.relative_to(BASE)
    except ValueError:
        return HttpResponseBadRequest("invalid path")
    # ruleid: mois-1-03-path-traversal-py
    return HttpResponse(target.read_bytes())


def relative_to_unresolved(request):
    # resolve() 하지 않은 경로: relative_to 는 ".." 을 풀지 않으므로 예외가 나지 않는다
    target = BASE / request.GET.get("name", "")
    target.relative_to(BASE)
    # ruleid: mois-1-03-path-traversal-py
    return HttpResponse(target.read_bytes())


def relative_to_unresolved_in_try(request):
    target = BASE / request.GET.get("name", "")
    try:
        target.relative_to(BASE)
    except ValueError:
        return HttpResponseBadRequest("invalid path")
    # ruleid: mois-1-03-path-traversal-py
    return HttpResponse(target.read_bytes())


def relative_to_rejoined_before_check(request):
    target = (BASE / request.GET.get("name", "")).resolve()
    target = target / request.GET.get("sub", "")
    target.relative_to(BASE)
    # ruleid: mois-1-03-path-traversal-py
    return HttpResponse(target.read_bytes())


def relative_to_appended_after_check(request):
    target = (BASE / request.GET.get("name", "")).resolve()
    target.relative_to(BASE)
    target /= request.GET.get("sub", "")
    # ruleid: mois-1-03-path-traversal-py
    return HttpResponse(target.read_bytes())


def relative_to_try_then_reassigned(request):
    target = (BASE / request.GET.get("name", "")).resolve()
    try:
        target.relative_to(BASE)
    except ValueError:
        return HttpResponseBadRequest("invalid path")
    target = BASE / request.GET.get("alias", "")
    # ruleid: mois-1-03-path-traversal-py
    return HttpResponse(target.read_bytes())


def relative_to_appended_before_try(request):
    target = (BASE / request.GET.get("name", "")).resolve()
    target /= request.GET.get("sub", "")
    try:
        target.relative_to(BASE)
    except ValueError:
        return HttpResponseBadRequest("invalid path")
    # ruleid: mois-1-03-path-traversal-py
    return HttpResponse(target.read_bytes())


def relative_to_other_path_checked(request):
    source = (BASE / request.GET.get("src", "")).resolve()
    target = (BASE / request.GET.get("dst", "")).resolve()
    source.relative_to(BASE)
    # 검사한 것은 source 뿐이다
    # ruleid: mois-1-03-path-traversal-py
    return HttpResponse(target.read_bytes())


def relative_to_result_kept_on_failure(request):
    relative = request.GET.get("name", "")
    target = (BASE / relative).resolve()
    try:
        relative = target.relative_to(BASE)
    except ValueError:
        pass
    # 예외가 나면 relative 에는 입력이 그대로 남아 있다
    # ruleid: mois-1-03-path-traversal-py
    return HttpResponse((BASE / relative).read_bytes())


# ---- 정규화는 바깥 블록에서, 검사와 재대입은 안쪽 블록에서 ----
def relative_to_appended_before_check(request):
    target = (BASE / request.GET.get("name", "")).resolve()
    target /= request.GET.get("sub", "")
    target.relative_to(BASE)
    # ruleid: mois-1-03-path-traversal-py
    return HttpResponse(target.read_bytes())


def relative_to_reassigned_after_check_in_block(request):
    target = (BASE / request.GET.get("name", "")).resolve()
    if request.method == "POST":
        target.relative_to(BASE)
        target = BASE / request.POST.get("alias", "")
        # ruleid: mois-1-03-path-traversal-py
        return HttpResponse(target.read_bytes())
    return HttpResponse("ok")


def relative_to_appended_after_check_in_block(request):
    target = (BASE / request.GET.get("name", "")).resolve()
    if request.method == "POST":
        target.relative_to(BASE)
        target /= request.POST.get("sub", "")
        # ruleid: mois-1-03-path-traversal-py
        return HttpResponse(target.read_bytes())
    return HttpResponse("ok")


def relative_to_rejoined_before_try(request):
    target = (BASE / request.GET.get("name", "")).resolve()
    target = target / request.GET.get("sub", "")
    try:
        target.relative_to(BASE)
    except ValueError:
        return HttpResponseBadRequest("invalid path")
    # ruleid: mois-1-03-path-traversal-py
    return HttpResponse(target.read_bytes())


def relative_to_try_then_reassigned_in_block(request):
    target = (BASE / request.GET.get("name", "")).resolve()
    if request.method == "POST":
        try:
            target.relative_to(BASE)
        except ValueError:
            return HttpResponseBadRequest("invalid path")
        target = BASE / request.POST.get("alias", "")
        # ruleid: mois-1-03-path-traversal-py
        return HttpResponse(target.read_bytes())
    return HttpResponse("ok")


def relative_to_try_then_appended_in_block(request):
    target = (BASE / request.GET.get("name", "")).resolve()
    if request.method == "POST":
        try:
            target.relative_to(BASE)
        except ValueError:
            return HttpResponseBadRequest("invalid path")
        target /= request.POST.get("sub", "")
        # ruleid: mois-1-03-path-traversal-py
        return HttpResponse(target.read_bytes())
    return HttpResponse("ok")


# ---- safe_join 의 기준 디렉터리가 외부 입력 ----
def safe_join_with_tainted_base(request):
    # 뒤쪽 인자는 기준 안으로 묶이지만, 기준 자체를 요청이 정한다
    # ruleid: mois-1-03-path-traversal-py
    os.remove(safe_join(request.GET.get("dir", ""), request.GET.get("name", "")))
    return HttpResponse("deleted")
