"""guard 를 속이는 경우 — 모두 탐지되어야 한다.

종료처럼 보이는 호출(exit·quit·이름만 abort), 검사식을 다른 식으로 감싼 조건(&·|·not not·비교·호출 인자),
검사 뒤·조건 안의 재대입, 아무것이나 통과시키는 정규식.
"""
import re

from django.http import HttpResponse, HttpResponseBadRequest
from .patterns import TOKEN_PATTERN

GOOD_RE = re.compile(r"[A-Za-z0-9_.-]{1,64}")
SWAPPED_RE = re.compile(r"[A-Za-z0-9_.-]{1,64}")
ANY_RE = re.compile(r".*")
REDEFINED_RE = re.compile(r"[A-Za-z0-9_.-]{1,64}")
REDEFINED_RE = re.compile(r".*")
PLUS_TO_Z_RE = re.compile(r"[+-z]+")
UPPER_TO_LOWER_RE = re.compile(r"[A-z]+")


def abort(code):
    print("rejected", code)


def audit(result):
    print("check", result)
    return False


def builtin_exit(request):
    token = request.GET.get("token", "")
    response = HttpResponse("ok")
    if not token.isalnum():
        exit(2)
    # 내장 exit() 는 site 모듈이 넣어 주는 대화형 도우미다 (python -S·임베디드 환경에는 없다) — import 로 확인되는 sys.exit 만 종료로 본다
    # ruleid: mois-1-13-http-response-splitting-py
    response.set_cookie("token", token)
    return response


def builtin_quit(request):
    token = request.GET.get("token", "")
    response = HttpResponse("ok")
    if not token.isalnum():
        quit()
    # 내장 quit() 도 같다
    # ruleid: mois-1-13-http-response-splitting-py
    response.set_cookie("token", token)
    return response


def local_abort(request):
    token = request.GET.get("token", "")
    response = HttpResponse("ok")
    if not token.isalnum():
        abort(400)
    # 이 파일의 abort 는 기록만 하고 돌아온다 — 이름이 abort 일 뿐 중단하지 않는다
    # ruleid: mois-1-13-http-response-splitting-py
    response.set_cookie("token", token)
    return response


def check_joined_with_bitand(request, strict):
    token = request.GET.get("token", "")
    response = HttpResponse("ok")
    if (not token.isalnum()) & strict:
        return HttpResponseBadRequest("invalid")
    # & 로 묶이면 strict 가 거짓일 때 검사에 실패한 값이 그대로 내려온다
    # ruleid: mois-1-13-http-response-splitting-py
    response.set_cookie("token", token)
    return response


def double_negation(request):
    token = request.GET.get("token", "")
    response = HttpResponse("ok")
    if not (not re.fullmatch(r"[A-Za-z0-9_.-]{1,64}", token)):
        return HttpResponseBadRequest("invalid")
    # not (not …) 은 뜻이 뒤집힌다: 형식이 맞으면 빠져나가고 틀린 값이 내려온다
    # ruleid: mois-1-13-http-response-splitting-py
    response.set_cookie("token", token)
    return response


def check_compared_with_flag(request, strict):
    token = request.GET.get("token", "")
    response = HttpResponse("ok")
    if (not GOOD_RE.fullmatch(token)) == strict:
        return HttpResponseBadRequest("invalid")
    # 검사 결과를 다른 값과 비교하면 strict 가 거짓일 때 틀린 값이 내려온다
    # ruleid: mois-1-13-http-response-splitting-py
    response.set_cookie("token", token)
    return response


def check_passed_to_call(request):
    token = request.GET.get("token", "")
    response = HttpResponse("ok")
    if audit(not token.isalnum()):
        return HttpResponseBadRequest("invalid")
    # 검사 결과를 다른 함수에 넘기면 그 함수가 무엇을 돌려주는지 알 수 없다
    # ruleid: mois-1-13-http-response-splitting-py
    response.set_cookie("token", token)
    return response


def tuple_reassigned_after_check(request):
    token = request.GET.get("token", "")
    response = HttpResponse("ok")
    if not token.isalnum():
        return HttpResponseBadRequest("invalid")
    token, mode = request.GET.get("alias", "").split(":")
    # 검사한 뒤에 튜플 풀기 대입으로 다른 입력을 넣는다
    # ruleid: mois-1-13-http-response-splitting-py
    response.set_cookie("token", token)
    return response


def check_joined_with_bitor(request, strict):
    token = request.GET.get("token", "")
    response = HttpResponse("ok")
    if strict | token.isalnum():
        # | 로 묶이면 strict 가 참일 때 검사를 통과하지 않은 값도 들어온다
        # ruleid: mois-1-13-http-response-splitting-py
        response.set_cookie("token", token)
    return response


def positive_check_is_none(request):
    token = request.GET.get("token", "")
    response = HttpResponse("ok")
    if GOOD_RE.fullmatch(token) is None:
        # is None 과 비교하면 뜻이 뒤집힌다: 형식이 틀렸을 때만 들어온다
        # ruleid: mois-1-13-http-response-splitting-py
        response.set_cookie("token", token)
    return response


def positive_inline_check_is_none(request):
    token = request.GET.get("token", "")
    response = HttpResponse("ok")
    if re.fullmatch(r"[A-Za-z0-9_.-]{1,64}", token) is None:
        # 조건에 적은 정규식도 마찬가지다: is None 이면 형식이 틀렸을 때만 들어온다
        # ruleid: mois-1-13-http-response-splitting-py
        response.set_cookie("token", token)
    return response


def positive_check_passed_to_call(request):
    token = request.GET.get("token", "")
    response = HttpResponse("ok")
    if audit(token.isalnum()):
        # 검사 결과를 다른 함수에 넘긴 조건은 검사가 아니다
        # ruleid: mois-1-13-http-response-splitting-py
        response.set_cookie("token", token)
    return response


def used_in_condition_before_check(request):
    token = request.GET.get("token", "")
    response = HttpResponse("ok")
    # 조건식 안에서 검사보다 먼저 쓴다 (and 는 왼쪽부터 실행한다)
    # ruleid: mois-1-13-http-response-splitting-py
    if response.headers.setdefault("X-Token", token) and token.isalnum():
        pass
    return response


def reassigned_inside_if(request):
    token = request.GET.get("token", "")
    response = HttpResponse("ok")
    if token.isalnum():
        token = request.GET.get("alias", "")
        # 검사를 통과한 조건 안에서 다른 입력으로 바꿔 넣는다
        # ruleid: mois-1-13-http-response-splitting-py
        response.set_cookie("token", token)
    return response


def appended_inside_if(request):
    token = request.GET.get("token", "")
    response = HttpResponse("ok")
    if GOOD_RE.fullmatch(token):
        token += request.GET.get("suffix", "")
        # 검사를 통과한 조건 안에서 검사하지 않은 입력을 덧붙인다
        # ruleid: mois-1-13-http-response-splitting-py
        response.set_cookie("token", token)
    return response


def tuple_reassigned_inside_if(request):
    token = request.GET.get("token", "")
    response = HttpResponse("ok")
    if token.isalnum():
        token, mode = request.GET.get("alias", "").split(":")
        # 검사를 통과한 조건 안에서 튜플 풀기 대입으로 다른 입력을 넣는다
        # ruleid: mois-1-13-http-response-splitting-py
        response.set_cookie("token", token)
    return response


def wildcard_pattern(request):
    token = request.GET.get("token", "")
    response = HttpResponse("ok")
    if not re.fullmatch(r".+", token):
        return HttpResponseBadRequest("invalid")
    # . 은 (개행을 뺀) 모든 글자에 맞는다 — fullmatch 여도 아무 값이나 통과한다
    # ruleid: mois-1-13-http-response-splitting-py
    response.set_cookie("token", token)
    return response


def negated_class_pattern(request):
    token = request.GET.get("token", "")
    response = HttpResponse("ok")
    if re.fullmatch(r"[^<>]+", token):
        # [^<>] 는 < > 만 빼고 따옴표·괄호·개행까지 모두 통과시킨다
        # ruleid: mois-1-13-http-response-splitting-py
        response.set_cookie("token", token)
    return response


def wide_range_pattern(request):
    token = request.GET.get("token", "")
    response = HttpResponse("ok")
    if not re.fullmatch(r"[!-~]+", token):
        return HttpResponseBadRequest("invalid")
    # [!-~] 는 따옴표·괄호·역슬래시를 포함한 모든 ASCII 기호에 맞는다 (범위는 a-z·A-Z·0-9 안에서만 인정한다)
    # ruleid: mois-1-13-http-response-splitting-py
    response.set_cookie("token", token)
    return response


def class_with_whitespace_escape(request):
    token = request.GET.get("token", "")
    response = HttpResponse("ok")
    if not re.fullmatch(r"[\w\s]+", token):
        return HttpResponseBadRequest("invalid")
    # [\w\s] 의 \s 는 공백과 개행(CR·LF)에 맞는다 — 집합 안의 이스케이프도 \w·\d·\.·\- 만 인정한다
    # ruleid: mois-1-13-http-response-splitting-py
    response.set_cookie("token", token)
    return response


def range_from_symbol(request):
    token = request.GET.get("token", "")
    response = HttpResponse("ok")
    if not PLUS_TO_Z_RE.fullmatch(token):
        return HttpResponseBadRequest("invalid")
    # [+-z] 는 + 부터 z 까지의 범위다: , / : ; < = > ? @ [ \ ] ^ ` 가 모두 통과한다
    # ruleid: mois-1-13-http-response-splitting-py
    response.set_cookie("token", token)
    return response


def range_to_symbol(request):
    token = request.GET.get("token", "")
    response = HttpResponse("ok")
    if re.fullmatch(r"[A-_]+", token):
        # [A-_] 는 A 부터 _ 까지의 범위다: [ \ ] ^ 가 통과한다
        # ruleid: mois-1-13-http-response-splitting-py
        response.set_cookie("token", token)
    return response


def range_upper_to_lower(request):
    token = request.GET.get("token", "")
    response = HttpResponse("ok")
    if UPPER_TO_LOWER_RE.fullmatch(token):
        # [A-z] 는 대문자와 소문자 사이의 [ \ ] ^ _ ` 까지 통과시킨다 (흔한 실수)
        # ruleid: mois-1-13-http-response-splitting-py
        response.set_cookie("token", token)
    return response


def range_digit_to_upper(request):
    token = request.GET.get("token", "")
    response = HttpResponse("ok")
    if not re.fullmatch(r"[0-Z]+", token):
        return HttpResponseBadRequest("invalid")
    # [0-Z] 는 숫자와 대문자 사이의 : ; < = > ? @ 까지 통과시킨다
    # ruleid: mois-1-13-http-response-splitting-py
    response.set_cookie("token", token)
    return response


def request_supplied_pattern(request):
    token = request.GET.get("token", "")
    response = HttpResponse("ok")
    if not re.fullmatch(request.GET.get("pattern", ""), token):
        return HttpResponseBadRequest("invalid")
    # 정규식을 요청에서 받으면 무엇이든 통과시킬 수 있다
    # ruleid: mois-1-13-http-response-splitting-py
    response.set_cookie("token", token)
    return response


def compiled_wildcard(request):
    token = request.GET.get("token", "")
    response = HttpResponse("ok")
    if not ANY_RE.fullmatch(token):
        return HttpResponseBadRequest("invalid")
    # ANY_RE 는 .* 이다 — 이름이 정규식일 뿐 아무것도 거르지 않는다
    # ruleid: mois-1-13-http-response-splitting-py
    response.set_cookie("token", token)
    return response


def compiled_wildcard_inside_if(request):
    token = request.GET.get("token", "")
    response = HttpResponse("ok")
    if ANY_RE.fullmatch(token):
        # 조건 안에서 써도 마찬가지다
        # ruleid: mois-1-13-http-response-splitting-py
        response.set_cookie("token", token)
    return response


def imported_pattern(request):
    token = request.GET.get("token", "")
    response = HttpResponse("ok")
    if not TOKEN_PATTERN.fullmatch(token):
        return HttpResponseBadRequest("invalid")
    # 다른 모듈에서 가져온 정규식은 무엇을 허용하는지 볼 수 없다
    # ruleid: mois-1-13-http-response-splitting-py
    response.set_cookie("token", token)
    return response


def compiled_shadowed(request):
    token = request.GET.get("token", "")
    response = HttpResponse("ok")
    GOOD_RE = re.compile(request.GET.get("pattern", ".*"))
    if not GOOD_RE.fullmatch(token):
        return HttpResponseBadRequest("invalid")
    # 함수 안에서 같은 이름의 지역 변수에 다른 정규식을 대입했다 — 모듈 수준의 정의는 쓰이지 않는다
    # ruleid: mois-1-13-http-response-splitting-py
    response.set_cookie("token", token)
    return response


def compiled_replaced_globally(request):
    global SWAPPED_RE
    token = request.GET.get("token", "")
    response = HttpResponse("ok")
    SWAPPED_RE = re.compile(request.GET.get("pattern", ".*"))
    if not SWAPPED_RE.fullmatch(token):
        return HttpResponseBadRequest("invalid")
    # global 로 모듈 수준의 정규식을 요청 값으로 바꿔 넣었다
    # ruleid: mois-1-13-http-response-splitting-py
    response.set_cookie("token", token)
    return response


def compiled_replaced_globally_inside_if(request):
    global SWAPPED_RE
    token = request.GET.get("token", "")
    response = HttpResponse("ok")
    SWAPPED_RE = re.compile(request.GET.get("pattern", ".*"))
    if SWAPPED_RE.fullmatch(token):
        # 조건 안에서 써도 마찬가지다
        # ruleid: mois-1-13-http-response-splitting-py
        response.set_cookie("token", token)
    return response


def compiled_redefined(request):
    token = request.GET.get("token", "")
    response = HttpResponse("ok")
    if not REDEFINED_RE.fullmatch(token):
        return HttpResponseBadRequest("invalid")
    # REDEFINED_RE 는 모듈 수준에서 .* 로 다시 정의되었다
    # ruleid: mois-1-13-http-response-splitting-py
    response.set_cookie("token", token)
    return response


def compiled_redefined_inside_if(request):
    token = request.GET.get("token", "")
    response = HttpResponse("ok")
    if REDEFINED_RE.fullmatch(token):
        # 조건 안에서 써도 마찬가지다
        # ruleid: mois-1-13-http-response-splitting-py
        response.set_cookie("token", token)
    return response
