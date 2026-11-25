"""guard 형태별 안전한 예제 (Django)."""
import os

from django.http import HttpResponse, HttpResponseBadRequest

MEDIA_DIR = "/srv/media"


def guard_1(request):
    name = request.GET.get("name", "")
    target = os.path.realpath(os.path.join(MEDIA_DIR, name))
    if not target.startswith(MEDIA_DIR + os.sep):
        return HttpResponseBadRequest("invalid")
    # ok: mois-1-03-path-traversal-py 실패하면 return
    os.remove(target)
    return HttpResponse("ok")


def guard_2(request):
    name = request.GET.get("name", "")
    target = os.path.realpath(os.path.join(MEDIA_DIR, name))
    if not target.startswith(MEDIA_DIR + os.path.sep):
        raise ValueError("invalid")
    # ok: mois-1-03-path-traversal-py 실패하면 raise
    os.remove(target)
    return HttpResponse("ok")


def guard_3(request):
    name = request.GET.get("name", "")
    target = os.path.realpath(os.path.join(MEDIA_DIR, name))
    if not target.startswith(MEDIA_DIR + "/"):
        return HttpResponseBadRequest("invalid")
    # ok: mois-1-03-path-traversal-py 실패하면 return
    os.remove(target)
    return HttpResponse("ok")


def guard_4(request):
    name = request.GET.get("name", "")
    target = os.path.realpath(os.path.join(MEDIA_DIR, name))
    if not target.startswith(os.path.join(MEDIA_DIR, "")):
        raise ValueError("invalid")
    # ok: mois-1-03-path-traversal-py 실패하면 raise
    os.remove(target)
    return HttpResponse("ok")


def guard_5(request):
    name = request.GET.get("name", "")
    target = os.path.realpath(os.path.join(MEDIA_DIR, name))
    if not target.startswith("/srv/media/"):
        return HttpResponseBadRequest("invalid")
    # ok: mois-1-03-path-traversal-py 실패하면 return
    os.remove(target)
    return HttpResponse("ok")


def guard_6(request):
    name = request.GET.get("name", "")
    target = os.path.realpath(os.path.join(MEDIA_DIR, name))
    if os.path.commonpath([MEDIA_DIR, target]) != MEDIA_DIR:
        raise ValueError("invalid")
    # ok: mois-1-03-path-traversal-py 실패하면 raise
    os.remove(target)
    return HttpResponse("ok")


def guard_7(request):
    name = request.GET.get("name", "")
    target = os.path.realpath(os.path.join(MEDIA_DIR, name))
    if os.path.commonpath([target, MEDIA_DIR]) != MEDIA_DIR:
        return HttpResponseBadRequest("invalid")
    # ok: mois-1-03-path-traversal-py 실패하면 return
    os.remove(target)
    return HttpResponse("ok")


def guard_8(request):
    name = request.GET.get("name", "")
    target = os.path.realpath(os.path.join(MEDIA_DIR, name))
    if name.startswith(".") or not target.startswith(MEDIA_DIR + os.sep):
        raise ValueError("invalid")
    # ok: mois-1-03-path-traversal-py 값이 없거나 실패하면 raise
    os.remove(target)
    return HttpResponse("ok")


def guard_9(request):
    name = request.GET.get("name", "")
    target = os.path.realpath(os.path.join(MEDIA_DIR, name))
    if name.startswith(".") or not target.startswith(MEDIA_DIR + os.path.sep):
        return HttpResponseBadRequest("invalid")
    # ok: mois-1-03-path-traversal-py 값이 없거나 실패하면 return
    os.remove(target)
    return HttpResponse("ok")


def guard_10(request):
    name = request.GET.get("name", "")
    target = os.path.realpath(os.path.join(MEDIA_DIR, name))
    if name.startswith(".") or not target.startswith(MEDIA_DIR + "/"):
        raise ValueError("invalid")
    # ok: mois-1-03-path-traversal-py 값이 없거나 실패하면 raise
    os.remove(target)
    return HttpResponse("ok")


def guard_11(request):
    name = request.GET.get("name", "")
    target = os.path.realpath(os.path.join(MEDIA_DIR, name))
    if name.startswith(".") or not target.startswith(os.path.join(MEDIA_DIR, "")):
        return HttpResponseBadRequest("invalid")
    # ok: mois-1-03-path-traversal-py 값이 없거나 실패하면 return
    os.remove(target)
    return HttpResponse("ok")


def guard_12(request):
    name = request.GET.get("name", "")
    target = os.path.realpath(os.path.join(MEDIA_DIR, name))
    if name.startswith(".") or not target.startswith("/srv/media/"):
        raise ValueError("invalid")
    # ok: mois-1-03-path-traversal-py 값이 없거나 실패하면 raise
    os.remove(target)
    return HttpResponse("ok")


def guard_13(request):
    name = request.GET.get("name", "")
    target = os.path.realpath(os.path.join(MEDIA_DIR, name))
    if name.startswith(".") or os.path.commonpath([MEDIA_DIR, target]) != MEDIA_DIR:
        return HttpResponseBadRequest("invalid")
    # ok: mois-1-03-path-traversal-py 값이 없거나 실패하면 return
    os.remove(target)
    return HttpResponse("ok")


def guard_14(request):
    name = request.GET.get("name", "")
    target = os.path.realpath(os.path.join(MEDIA_DIR, name))
    if name.startswith(".") or os.path.commonpath([target, MEDIA_DIR]) != MEDIA_DIR:
        raise ValueError("invalid")
    # ok: mois-1-03-path-traversal-py 값이 없거나 실패하면 raise
    os.remove(target)
    return HttpResponse("ok")


def guard_15(request):
    for name in request.GET.getlist("name"):
        target = os.path.realpath(os.path.join(MEDIA_DIR, name))
        if not target.startswith(MEDIA_DIR + os.sep):
            continue
        # ok: mois-1-03-path-traversal-py 실패한 값은 건너뜀
        os.remove(target)
    return HttpResponse("ok")


def guard_16(request):
    for name in request.GET.getlist("name"):
        target = os.path.realpath(os.path.join(MEDIA_DIR, name))
        if name.startswith(".") or os.path.commonpath([target, MEDIA_DIR]) != MEDIA_DIR:
            continue
        # ok: mois-1-03-path-traversal-py 비었거나 실패한 값은 건너뜀
        os.remove(target)
    return HttpResponse("ok")


def guard_17(request):
    name = request.GET.get("name", "")
    target = os.path.realpath(os.path.join(MEDIA_DIR, name))
    if target.startswith(MEDIA_DIR + os.sep):
        # ok: mois-1-03-path-traversal-py 검사를 통과한 조건 안에서만 사용
        os.remove(target)
    return HttpResponse("ok")


def guard_18(request):
    name = request.GET.get("name", "")
    target = os.path.realpath(os.path.join(MEDIA_DIR, name))
    if target.startswith(MEDIA_DIR + os.path.sep):
        # ok: mois-1-03-path-traversal-py 검사를 통과한 조건 안에서만 사용
        os.remove(target)
    return HttpResponse("ok")


def guard_19(request):
    name = request.GET.get("name", "")
    target = os.path.realpath(os.path.join(MEDIA_DIR, name))
    if target.startswith(MEDIA_DIR + "/"):
        # ok: mois-1-03-path-traversal-py 검사를 통과한 조건 안에서만 사용
        os.remove(target)
    return HttpResponse("ok")


def guard_20(request):
    name = request.GET.get("name", "")
    target = os.path.realpath(os.path.join(MEDIA_DIR, name))
    if target.startswith(os.path.join(MEDIA_DIR, "")):
        # ok: mois-1-03-path-traversal-py 검사를 통과한 조건 안에서만 사용
        os.remove(target)
    return HttpResponse("ok")


def guard_21(request):
    name = request.GET.get("name", "")
    target = os.path.realpath(os.path.join(MEDIA_DIR, name))
    if target.startswith("/srv/media/"):
        # ok: mois-1-03-path-traversal-py 검사를 통과한 조건 안에서만 사용
        os.remove(target)
    return HttpResponse("ok")


def guard_22(request):
    name = request.GET.get("name", "")
    target = os.path.realpath(os.path.join(MEDIA_DIR, name))
    if os.path.commonpath([MEDIA_DIR, target]) == MEDIA_DIR:
        # ok: mois-1-03-path-traversal-py 검사를 통과한 조건 안에서만 사용
        os.remove(target)
    return HttpResponse("ok")


def guard_23(request):
    name = request.GET.get("name", "")
    target = os.path.realpath(os.path.join(MEDIA_DIR, name))
    if os.path.commonpath([target, MEDIA_DIR]) == MEDIA_DIR:
        # ok: mois-1-03-path-traversal-py 검사를 통과한 조건 안에서만 사용
        os.remove(target)
    return HttpResponse("ok")
