"""guard 형태별 안전한 예제 (Django)."""
import re

from django.http import HttpResponse, HttpResponseBadRequest

TOKEN_RE = re.compile(r"[A-Za-z0-9_.-]{1,64}")


def guard_1(request):
    token = request.GET.get("token", "")
    if not re.fullmatch(r"[A-Za-z0-9_.-]{1,64}", token):
        return HttpResponseBadRequest("invalid")
    response = HttpResponse("ok")
    # ok: mois-1-13-http-response-splitting-py 실패하면 return
    response["X-Token"] = token
    return HttpResponse("ok")


def guard_2(request):
    token = request.GET.get("token", "")
    if not TOKEN_RE.fullmatch(token):
        raise ValueError("invalid")
    response = HttpResponse("ok")
    # ok: mois-1-13-http-response-splitting-py 실패하면 raise
    response["X-Token"] = token
    return HttpResponse("ok")


def guard_3(request):
    token = request.GET.get("token", "")
    if not token.isalnum():
        return HttpResponseBadRequest("invalid")
    response = HttpResponse("ok")
    # ok: mois-1-13-http-response-splitting-py 실패하면 return
    response["X-Token"] = token
    return HttpResponse("ok")


def guard_4(request):
    token = request.GET.get("token", "")
    if not token or not re.fullmatch(r"[A-Za-z0-9_.-]{1,64}", token):
        raise ValueError("invalid")
    response = HttpResponse("ok")
    # ok: mois-1-13-http-response-splitting-py 값이 없거나 실패하면 raise
    response["X-Token"] = token
    return HttpResponse("ok")


def guard_5(request):
    token = request.GET.get("token", "")
    if not token or not TOKEN_RE.fullmatch(token):
        return HttpResponseBadRequest("invalid")
    response = HttpResponse("ok")
    # ok: mois-1-13-http-response-splitting-py 값이 없거나 실패하면 return
    response["X-Token"] = token
    return HttpResponse("ok")


def guard_6(request):
    token = request.GET.get("token", "")
    if not token or not token.isalnum():
        raise ValueError("invalid")
    response = HttpResponse("ok")
    # ok: mois-1-13-http-response-splitting-py 값이 없거나 실패하면 raise
    response["X-Token"] = token
    return HttpResponse("ok")


def guard_7(request):
    for token in request.GET.getlist("token"):
        if not re.fullmatch(r"[A-Za-z0-9_.-]{1,64}", token):
            continue
        response = HttpResponse("ok")
        # ok: mois-1-13-http-response-splitting-py 실패한 값은 건너뜀
        response["X-Token"] = token
    return HttpResponse("ok")


def guard_8(request):
    for token in request.GET.getlist("token"):
        if not token or not token.isalnum():
            continue
        response = HttpResponse("ok")
        # ok: mois-1-13-http-response-splitting-py 비었거나 실패한 값은 건너뜀
        response["X-Token"] = token
    return HttpResponse("ok")


def guard_9(request):
    token = request.GET.get("token", "")
    if re.fullmatch(r"[A-Za-z0-9_.-]{1,64}", token):
        response = HttpResponse("ok")
        # ok: mois-1-13-http-response-splitting-py 검사를 통과한 조건 안에서만 사용
        response["X-Token"] = token
    return HttpResponse("ok")


def guard_10(request):
    token = request.GET.get("token", "")
    if TOKEN_RE.fullmatch(token):
        response = HttpResponse("ok")
        # ok: mois-1-13-http-response-splitting-py 검사를 통과한 조건 안에서만 사용
        response["X-Token"] = token
    return HttpResponse("ok")


def guard_11(request):
    token = request.GET.get("token", "")
    if token.isalnum():
        response = HttpResponse("ok")
        # ok: mois-1-13-http-response-splitting-py 검사를 통과한 조건 안에서만 사용
        response["X-Token"] = token
    return HttpResponse("ok")
