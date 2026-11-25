"""검증처럼 보이지만 경로가 기준 디렉터리를 벗어날 수 있는 경우 — 모두 탐지되어야 한다."""
import os
from pathlib import Path

from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest

BASE = Path("/srv/media")


def prefix_without_separator(request):
    base = os.path.realpath(settings.MEDIA_ROOT)
    target = os.path.realpath(os.path.join(base, request.GET.get("name", "")))
    # 구분자 없는 접두 비교: /srv/media-private/secret 도 /srv/media 로 시작한다
    if not target.startswith(base):
        return HttpResponseBadRequest("invalid path")
    # ruleid: mois-1-03-path-traversal-py
    os.remove(target)
    return HttpResponse("deleted")


def common_prefix(request):
    base = os.path.realpath(settings.MEDIA_ROOT)
    target = os.path.realpath(os.path.join(base, request.GET.get("name", "")))
    # commonprefix 는 글자 단위 비교라 같은 문제가 있다
    if os.path.commonprefix([base, target]) != base:
        return HttpResponseBadRequest("invalid path")
    # ruleid: mois-1-03-path-traversal-py
    os.remove(target)
    return HttpResponse("deleted")


def only_checks_leading_slash(request):
    target = request.GET.get("path", "")
    # 절대 경로인지만 본다
    if not target.startswith("/"):
        return HttpResponseBadRequest("invalid path")
    # ruleid: mois-1-03-path-traversal-py
    os.remove(target)
    return HttpResponse("deleted")


def result_ignored(request):
    target = (BASE / request.GET.get("name", "")).resolve()
    # 검사 결과를 쓰지 않음
    target.is_relative_to(BASE)
    # ruleid: mois-1-03-path-traversal-py
    return HttpResponse(target.read_bytes())


def failure_does_not_exit(request):
    base = os.path.realpath(settings.MEDIA_ROOT)
    target = os.path.realpath(os.path.join(base, request.GET.get("name", "")))
    if os.path.commonpath([base, target]) != base:
        print("path escapes base", target)
    # ruleid: mois-1-03-path-traversal-py
    os.remove(target)
    return HttpResponse("deleted")


def opposite_branch(request):
    target = (BASE / request.GET.get("name", "")).resolve()
    if target.is_relative_to(BASE):
        return HttpResponse("exists")
    else:
        # ruleid: mois-1-03-path-traversal-py
        return HttpResponse(target.read_bytes())


def used_when_check_fails(request):
    base = os.path.realpath(settings.MEDIA_ROOT)
    target = os.path.realpath(os.path.join(base, request.GET.get("name", "")))
    if not target.startswith(base + os.sep):
        # ruleid: mois-1-03-path-traversal-py
        os.remove(target)
    return HttpResponse("deleted")


def exits_when_check_passes(request):
    base = os.path.realpath(settings.MEDIA_ROOT)
    target = os.path.realpath(os.path.join(base, request.GET.get("name", "")))
    # 조건이 반대: 기준 안이면 빠져나간다
    if os.path.commonpath([base, target]) == base:
        return HttpResponseBadRequest("protected")
    # ruleid: mois-1-03-path-traversal-py
    os.remove(target)
    return HttpResponse("deleted")


def other_path_checked(request):
    base = os.path.realpath(settings.MEDIA_ROOT)
    source = os.path.realpath(os.path.join(base, request.GET.get("src", "")))
    target = os.path.realpath(os.path.join(base, request.GET.get("dst", "")))
    if not source.startswith(base + os.sep):
        return HttpResponseBadRequest("invalid path")
    # 검사한 것은 source 뿐이다
    # ruleid: mois-1-03-path-traversal-py
    os.replace(source, target)
    return HttpResponse("moved")


def basename_result_discarded(request):
    name = request.GET.get("name", "")
    os.path.basename(name)
    # ruleid: mois-1-03-path-traversal-py
    os.remove(os.path.join(settings.MEDIA_ROOT, name))
    return HttpResponse("deleted")


def sink_inside_failing_branch(request):
    target = (BASE / request.GET.get("name", "")).resolve()
    if not target.is_relative_to(BASE):
        # 기준 밖의 파일을 읽고 빠져나간다
        # ruleid: mois-1-03-path-traversal-py
        return HttpResponse(target.read_bytes())
    return HttpResponse("ok")


def nested_conditional_exit(request):
    base = os.path.realpath(settings.MEDIA_ROOT)
    target = os.path.realpath(os.path.join(base, request.GET.get("name", "")))
    if not target.startswith(base + os.sep):
        if request.GET.get("strict"):
            return HttpResponse("ok")
    # 엄격 모드가 아니면 검사에 실패한 값이 그대로 내려온다
    # ruleid: mois-1-03-path-traversal-py
    os.remove(target)
    return HttpResponse("ok")


def reassigned_after_check(request):
    base = os.path.realpath(settings.MEDIA_ROOT)
    target = os.path.realpath(os.path.join(base, request.GET.get("name", "")))
    if not target.startswith(base + os.sep):
        return HttpResponse("ok")
    # 검사한 뒤에 다른 입력으로 바꿔 넣는다
    target = os.path.join(base, request.GET.get("alias", ""))
    # ruleid: mois-1-03-path-traversal-py
    os.remove(target)
    return HttpResponse("ok")


def appended_after_check(request):
    base = os.path.realpath(settings.MEDIA_ROOT)
    target = os.path.realpath(os.path.join(base, request.GET.get("name", "")))
    if not target.startswith(base + os.sep):
        return HttpResponse("ok")
    # 검사한 뒤에 검사하지 않은 입력을 덧붙인다 (/../ 로 다시 빠져나갈 수 있다)
    target += os.sep + request.GET.get("sub", "")
    # ruleid: mois-1-03-path-traversal-py
    os.remove(target)
    return HttpResponse("ok")


def check_joined_with_and(request):
    base = os.path.realpath(settings.MEDIA_ROOT)
    target = os.path.realpath(os.path.join(base, request.GET.get("name", "")))
    # 엄격 모드일 때만 검사한다
    if request.GET.get("strict") and not target.startswith(base + os.sep):
        return HttpResponse("ok")
    # ruleid: mois-1-03-path-traversal-py
    os.remove(target)
    return HttpResponse("ok")


def check_joined_with_or(request):
    base = os.path.realpath(settings.MEDIA_ROOT)
    target = os.path.realpath(os.path.join(base, request.GET.get("name", "")))
    # or 로 묶이면 검사를 통과하지 않은 값도 들어온다
    if request.user.is_staff or target.startswith(base + os.sep):
        # ruleid: mois-1-03-path-traversal-py
        os.remove(target)
    return HttpResponse("ok")
