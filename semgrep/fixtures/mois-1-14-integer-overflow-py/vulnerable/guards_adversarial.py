"""guard 를 속이는 경우 — 모두 탐지되어야 한다.

종료처럼 보이는 호출(exit·quit·이름만 abort), 검사식을 다른 식으로 감싼 조건(&·|·비교·호출 인자·조건식),
검사 뒤·조건 안의 재대입, 요청에서 받은 값을 상한으로 쓴 검사.
"""
import numpy as np
from django.http import HttpResponse, HttpResponseBadRequest

MAX_SIZE = 1024 * 1024


def abort(code):
    print("rejected", code)


def audit(result):
    print("check", result)
    return False


def builtin_exit(request):
    size = int(request.GET.get("size", "0"))
    if size > MAX_SIZE:
        exit(2)
    # 내장 exit() 는 site 모듈이 넣어 주는 대화형 도우미다 (python -S·임베디드 환경에는 없다) — import 로 확인되는 sys.exit 만 종료로 본다
    # ruleid: mois-1-14-integer-overflow-py
    return HttpResponse(bytes(bytearray(size)))


def builtin_quit(request):
    size = int(request.GET.get("size", "0"))
    if size > MAX_SIZE:
        quit()
    # 내장 quit() 도 같다
    # ruleid: mois-1-14-integer-overflow-py
    return HttpResponse(bytes(bytearray(size)))


def local_abort(request):
    size = int(request.GET.get("size", "0"))
    if size > MAX_SIZE:
        abort(400)
    # 이 파일의 abort 는 기록만 하고 돌아온다 — 이름이 abort 일 뿐 중단하지 않는다
    # ruleid: mois-1-14-integer-overflow-py
    return HttpResponse(bytes(bytearray(size)))


def check_joined_with_bitand(request, strict):
    size = int(request.GET.get("size", "0"))
    if (size > MAX_SIZE) & strict:
        return HttpResponseBadRequest("too large")
    # & 로 묶이면 strict 가 거짓일 때 상한을 넘은 값이 그대로 내려온다
    # ruleid: mois-1-14-integer-overflow-py
    return HttpResponse(bytes(bytearray(size)))


def check_compared_with_flag(request, strict):
    size = int(request.GET.get("size", "0"))
    if (size > MAX_SIZE) == strict:
        return HttpResponseBadRequest("too large")
    # 검사 결과를 다른 값과 비교하면 strict 가 거짓일 때 상한을 넘은 값이 내려온다
    # ruleid: mois-1-14-integer-overflow-py
    return HttpResponse(bytes(bytearray(size)))


def check_passed_to_call(request):
    size = int(request.GET.get("size", "0"))
    if audit(size > MAX_SIZE):
        return HttpResponseBadRequest("too large")
    # 검사 결과를 다른 함수에 넘기면 그 함수가 무엇을 돌려주는지 알 수 없다
    # ruleid: mois-1-14-integer-overflow-py
    return HttpResponse(bytes(bytearray(size)))


def check_in_conditional_expression(request, strict):
    size = int(request.GET.get("size", "0"))
    if (size > MAX_SIZE if strict else False):
        return HttpResponseBadRequest("too large")
    # 조건식 안의 검사는 strict 가 거짓이면 실행되지 않는다
    # ruleid: mois-1-14-integer-overflow-py
    return HttpResponse(bytes(bytearray(size)))


def tuple_reassigned_after_check(request):
    size = int(request.GET.get("size", "0"))
    if size > MAX_SIZE:
        return HttpResponseBadRequest("too large")
    # 검사한 뒤에 튜플 풀기 대입으로 다른 입력을 넣는다
    size, unit = parse_size(request.GET.get("padding", "0"))
    # ruleid: mois-1-14-integer-overflow-py
    return HttpResponse(bytes(bytearray(size)))


def check_joined_with_bitor(request, strict):
    size = int(request.GET.get("size", "0"))
    if strict | (size <= MAX_SIZE):
        # | 로 묶이면 strict 가 참일 때 상한을 넘은 값도 들어온다
        # ruleid: mois-1-14-integer-overflow-py
        return HttpResponse(bytes(bytearray(size)))
    return HttpResponseBadRequest("too large")


def positive_check_is_false(request):
    size = int(request.GET.get("size", "0"))
    if (size <= MAX_SIZE) is False:
        # is False 와 비교하면 뜻이 뒤집힌다: 상한을 넘었을 때만 들어온다
        # ruleid: mois-1-14-integer-overflow-py
        return HttpResponse(bytes(bytearray(size)))
    return HttpResponseBadRequest("ok")


def positive_check_passed_to_call(request):
    size = int(request.GET.get("size", "0"))
    if audit(size <= MAX_SIZE):
        # 검사 결과를 다른 함수에 넘긴 조건은 검사가 아니다
        # ruleid: mois-1-14-integer-overflow-py
        return HttpResponse(bytes(bytearray(size)))
    return HttpResponseBadRequest("too large")


def used_in_condition_before_check(request):
    size = int(request.GET.get("size", "0"))
    # 조건식 안에서 검사보다 먼저 쓴다 (and 는 왼쪽부터 실행한다)
    # ruleid: mois-1-14-integer-overflow-py
    if bytearray(size) and size <= MAX_SIZE:
        return HttpResponse(b"ok")
    return HttpResponseBadRequest("too large")


def reassigned_inside_if(request):
    size = int(request.GET.get("size", "0"))
    if size <= MAX_SIZE:
        # 검사를 통과한 조건 안에서 다른 입력으로 바꿔 넣는다
        size = int(request.GET.get("padding", "0"))
        # ruleid: mois-1-14-integer-overflow-py
        return HttpResponse(bytes(bytearray(size)))
    return HttpResponseBadRequest("too large")


def added_inside_if(request):
    size = int(request.GET.get("size", "0"))
    if size <= MAX_SIZE:
        # 검사를 통과한 조건 안에서 검사하지 않은 입력을 더한다
        size += int(request.GET.get("padding", "0"))
        # ruleid: mois-1-14-integer-overflow-py
        return HttpResponse(bytes(bytearray(size)))
    return HttpResponseBadRequest("too large")


def tuple_reassigned_inside_if(request):
    size = int(request.GET.get("size", "0"))
    if size <= MAX_SIZE:
        # 검사를 통과한 조건 안에서 튜플 풀기 대입으로 다른 입력을 넣는다
        size, unit = parse_size(request.GET.get("padding", "0"))
        # ruleid: mois-1-14-integer-overflow-py
        return HttpResponse(bytes(bytearray(size)))
    return HttpResponseBadRequest("too large")


def request_supplied_bound(request):
    size = int(request.GET.get("size", "0"))
    limit = int(request.GET.get("limit", "0"))
    if size > limit:
        return HttpResponseBadRequest("too large")
    # 상한(limit)도 요청에서 받았다 — 둘 다 크게 보내면 통과한다
    # ruleid: mois-1-14-integer-overflow-py
    return HttpResponse(bytes(bytearray(size)))


def request_supplied_bound_in_range(request):
    size = int(request.GET.get("size", "0"))
    limit = int(request.GET.get("limit", "0"))
    if not 0 <= size <= limit:
        return HttpResponseBadRequest("out of range")
    # 범위의 상한이 요청 값이다
    # ruleid: mois-1-14-integer-overflow-py
    return HttpResponse(bytes(bytearray(size)))


def request_supplied_bound_inside_if(request):
    size = int(request.GET.get("size", "0"))
    limit = int(request.GET.get("limit", "0"))
    if size <= limit:
        # 조건 안에서 써도 상한이 요청 값이면 마찬가지다
        # ruleid: mois-1-14-integer-overflow-py
        return HttpResponse(bytes(bytearray(size)))
    return HttpResponseBadRequest("too large")


def min_of_two_inputs(request):
    size = int(request.GET.get("size", "0"))
    limit = int(request.GET.get("limit", "0"))
    # 두 값이 모두 입력이면 min 은 상한을 정하지 못한다
    # ruleid: mois-1-14-integer-overflow-py
    first = bytearray(min(size, limit))
    # ruleid: mois-1-14-integer-overflow-py
    second = bytearray(min(limit, size))
    return HttpResponse(bytes(first + second))


def clip_without_upper_bound(request):
    level = int(request.GET.get("level", "0"))
    # 상한이 None 이면 아래쪽만 자른다
    clipped = np.clip(level, 0, None)
    # ruleid: mois-1-14-integer-overflow-py
    return HttpResponse(bytes(bytearray(clipped)))
