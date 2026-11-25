import os
import pathlib
from pathlib import Path, PurePath, PurePosixPath

from django.conf import settings
from django.http import Http404, HttpResponse, HttpResponseBadRequest
from django.utils._os import safe_join as django_safe_join
from django.utils.text import get_valid_filename
from werkzeug.security import safe_join as legacy_safe_join
from werkzeug.utils import safe_join, secure_filename

BASE = Path("/srv/media")


def file_name_only(request):
    name = request.GET.get("name", "")
    # ok: mois-1-03-path-traversal-py 파일명만 남기는 함수들
    os.remove(os.path.join(settings.MEDIA_ROOT, secure_filename(name)))
    # ok: mois-1-03-path-traversal-py
    os.remove(os.path.join(settings.MEDIA_ROOT, get_valid_filename(name)))
    # ok: mois-1-03-path-traversal-py
    os.remove(BASE / PurePath(name).name)
    # ok: mois-1-03-path-traversal-py
    os.remove(BASE / PurePosixPath(name).name)
    # ok: mois-1-03-path-traversal-py
    os.remove(BASE / pathlib.Path(name).name)
    return HttpResponse("deleted")


def safe_joined(request):
    name = request.GET.get("name", "")
    # ok: mois-1-03-path-traversal-py 기준 디렉터리를 벗어나면 None·예외가 되는 결합 함수
    os.remove(safe_join(settings.MEDIA_ROOT, name))
    # ok: mois-1-03-path-traversal-py
    os.remove(legacy_safe_join(settings.MEDIA_ROOT, name))
    # ok: mois-1-03-path-traversal-py
    os.remove(django_safe_join(settings.MEDIA_ROOT, name))
    return HttpResponse("deleted")


def numbered_file(request):
    # ok: mois-1-03-path-traversal-py 정수로 바꾼 값
    path = os.path.join(settings.MEDIA_ROOT, "report-%d.pdf" % int(request.GET.get("no", "0")))
    os.remove(path)
    return HttpResponse("deleted")


def relative_to_raises(request):
    target = (BASE / request.GET.get("name", "")).resolve()
    # 기준 밖이면 여기서 ValueError
    target.relative_to(BASE)
    # ok: mois-1-03-path-traversal-py
    return HttpResponse(target.read_bytes(), content_type="application/octet-stream")


def pathlib_guard_with_empty_check(request):
    name = request.GET.get("name", "")
    target = (BASE / name).resolve()
    if name.startswith(".") or not target.is_relative_to(BASE):
        return HttpResponseBadRequest("invalid path")
    # ok: mois-1-03-path-traversal-py 숨김 파일이거나 기준 밖이면 위에서 빠져나감
    return HttpResponse(target.read_bytes(), content_type="application/octet-stream")


def pathlib_positive_branch(request):
    target = (BASE / request.GET.get("name", "")).resolve()
    if target.is_relative_to(BASE):
        # ok: mois-1-03-path-traversal-py 기준 안일 때만 읽음
        return HttpResponse(target.read_bytes(), content_type="application/octet-stream")
    return HttpResponseBadRequest("invalid path")


def prefix_with_slash(request):
    base = os.path.realpath(settings.MEDIA_ROOT)
    target = os.path.realpath(os.path.join(base, request.GET.get("name", "")))
    if not target.startswith(base + "/"):
        return HttpResponseBadRequest("invalid path")
    # ok: mois-1-03-path-traversal-py 구분자를 붙인 접두 비교
    os.remove(target)
    return HttpResponse("deleted")


def prefix_with_slash_and_hidden_check(request):
    name = request.GET.get("name", "")
    base = os.path.realpath(settings.MEDIA_ROOT)
    target = os.path.realpath(os.path.join(base, name))
    if name.startswith(".") or not target.startswith(base + "/"):
        raise PermissionError(name)
    # ok: mois-1-03-path-traversal-py
    os.remove(target)
    return HttpResponse("deleted")


def prefix_with_slash_positive(request):
    base = os.path.realpath(settings.MEDIA_ROOT)
    target = os.path.realpath(os.path.join(base, request.GET.get("name", "")))
    if target.startswith(base + "/"):
        # ok: mois-1-03-path-traversal-py
        os.remove(target)
    return HttpResponse("deleted")


def safe_joined_nested(request):
    # ok: mois-1-03-path-traversal-py 기준은 설정 값이고, 입력은 뒤쪽 인자로만 들어간다
    os.remove(safe_join(settings.MEDIA_ROOT, "docs", request.GET.get("name", "")))
    return HttpResponse("deleted")


# ---- relative_to: 예외로 실제로 멈추는 자리 ----
def relative_to_inside_try(request):
    target = (BASE / request.GET.get("name", "")).resolve()
    try:
        target.relative_to(BASE)
        # ok: mois-1-03-path-traversal-py 기준 밖이면 위에서 예외가 나 여기로 오지 않는다
        os.remove(target)
    except ValueError:
        return HttpResponseBadRequest("invalid path")
    return HttpResponse("deleted")


def relative_to_except_raises(request):
    target = (BASE / request.GET.get("name", "")).resolve()
    try:
        target.relative_to(BASE)
    except ValueError as exc:
        raise Http404("not found") from exc
    # ok: mois-1-03-path-traversal-py 기준 밖이면 except 에서 예외를 다시 던진다
    os.remove(target)
    return HttpResponse("deleted")


def relative_to_except_raises_other(request):
    target = (BASE / request.GET.get("name", "")).resolve()
    try:
        target.relative_to(BASE)
    except ValueError:
        raise Http404("not found")
    # ok: mois-1-03-path-traversal-py
    os.remove(target)
    return HttpResponse("deleted")


def relative_to_except_reraises(request):
    target = (BASE / request.GET.get("name", "")).resolve()
    try:
        target.relative_to(BASE)
    except ValueError:
        raise
    # ok: mois-1-03-path-traversal-py
    os.remove(target)
    return HttpResponse("deleted")


def relative_to_except_returns(request):
    target = (BASE / request.GET.get("name", "")).resolve()
    try:
        target.relative_to(BASE)
    except (ValueError, OSError):
        return HttpResponseBadRequest("invalid path")
    # ok: mois-1-03-path-traversal-py 기준 밖이면 except 에서 return
    os.remove(target)
    return HttpResponse("deleted")


# ---- 정규화 함수별 (abspath · normpath) ----
def abspath_guard(request):
    target = os.path.abspath(os.path.join(settings.MEDIA_ROOT, request.GET.get("name", "")))
    if not target.startswith(settings.MEDIA_ROOT + os.sep):
        return HttpResponseBadRequest("invalid path")
    # ok: mois-1-03-path-traversal-py abspath 로 ".." 을 푼 뒤 비교
    os.remove(target)
    return HttpResponse("deleted")


def normpath_guard(request):
    target = os.path.normpath(os.path.join(settings.MEDIA_ROOT, request.GET.get("name", "")))
    if not target.startswith(settings.MEDIA_ROOT + os.sep):
        return HttpResponseBadRequest("invalid path")
    # ok: mois-1-03-path-traversal-py normpath 로 ".." 을 푼 뒤 비교
    os.remove(target)
    return HttpResponse("deleted")


def abspath_positive(request):
    target = os.path.abspath(os.path.join(settings.MEDIA_ROOT, request.GET.get("name", "")))
    if target.startswith(settings.MEDIA_ROOT + os.sep):
        # ok: mois-1-03-path-traversal-py
        os.remove(target)
    return HttpResponse("deleted")


def normpath_positive(request):
    target = os.path.normpath(os.path.join(settings.MEDIA_ROOT, request.GET.get("name", "")))
    if target.startswith(settings.MEDIA_ROOT + os.sep):
        # ok: mois-1-03-path-traversal-py
        os.remove(target)
    return HttpResponse("deleted")


def model_save(request, profile, form):
    # ok: mois-1-03-path-traversal-py 모델·폼의 save 는 파일 경로를 받지 않는다
    profile.save(update_fields=request.POST.getlist("fields"))
    form.save(request.POST.get("commit") == "1")
    return HttpResponse("saved")
