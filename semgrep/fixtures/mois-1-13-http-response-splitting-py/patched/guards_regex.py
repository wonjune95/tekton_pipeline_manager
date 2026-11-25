"""형식 검사 guard 의 안전한 예제 — 허용 문자만 적은 정규식 리터럴과 and 로 묶은 조건."""
import re

from django.http import HttpResponse, HttpResponseBadRequest

GOOD_RE = re.compile(r"[A-Za-z0-9_.-]{1,64}")
DIGITS_RE = re.compile(r"\d{1,9}")


def digits_inline(request):
    token = request.GET.get("token", "")
    response = HttpResponse("ok")
    if not re.fullmatch(r"\d{1,9}", token):
        return HttpResponseBadRequest("invalid")
    # ok: mois-1-13-http-response-splitting-py \d 만 적은 정규식 (실패하면 return)
    response.set_cookie("token", token)
    return response


def digits_compiled(request):
    token = request.GET.get("token", "")
    response = HttpResponse("ok")
    if not DIGITS_RE.fullmatch(token):
        return HttpResponseBadRequest("invalid")
    # ok: mois-1-13-http-response-splitting-py 모듈 수준에서 컴파일한 \d 정규식 (실패하면 return)
    response.set_cookie("token", token)
    return response


def digits_inline_inside_if(request):
    token = request.GET.get("token", "")
    response = HttpResponse("ok")
    if re.fullmatch(r"\d{1,9}", token):
        # ok: mois-1-13-http-response-splitting-py \d 만 적은 정규식을 통과한 조건 안
        response.set_cookie("token", token)
    return response


def digits_compiled_inside_if(request):
    token = request.GET.get("token", "")
    response = HttpResponse("ok")
    if DIGITS_RE.fullmatch(token):
        # ok: mois-1-13-http-response-splitting-py 컴파일한 \d 정규식을 통과한 조건 안
        response.set_cookie("token", token)
    return response


def nonempty_and_ischeck(request):
    token = request.GET.get("token", "")
    response = HttpResponse("ok")
    if token and token.isalnum():
        # ok: mois-1-13-http-response-splitting-py 값이 있고(and) 검사를 통과한 조건 안
        response.set_cookie("token", token)
    return response


def nonempty_and_compiled(request):
    token = request.GET.get("token", "")
    response = HttpResponse("ok")
    if token and GOOD_RE.fullmatch(token):
        # ok: mois-1-13-http-response-splitting-py 값이 있고(and) 컴파일한 정규식을 통과한 조건 안
        response.set_cookie("token", token)
    return response


def nonempty_and_inline(request):
    token = request.GET.get("token", "")
    response = HttpResponse("ok")
    if token and re.fullmatch(r"[A-Za-z0-9_.-]{1,64}", token):
        # ok: mois-1-13-http-response-splitting-py 값이 있고(and) 조건에 적은 정규식을 통과한 조건 안
        response.set_cookie("token", token)
    return response


def literal_tokens(request):
    token = request.GET.get("token", "")
    response = HttpResponse("ok")
    if not re.fullmatch(r"(?:[a-z0-9]+-)*[a-z0-9]+@[\w-]+\.example\.com", token, re.IGNORECASE):
        return HttpResponseBadRequest("invalid")
    # ok: mois-1-13-http-response-splitting-py 글자·묶음·\w·\. 만 쓴 정규식
    response.set_cookie("token", token)
    return response
