"""상한의 종류별 안전한 예제 — 숫자 리터럴 · len(이름) · and 로 묶은 범위 검사."""
import numpy as np
from django.http import HttpResponse, HttpResponseBadRequest

PAYLOAD = b"0123456789abcdef" * 4096
MAX_SIZE = 1024 * 1024


def literal_bound(request):
    size = int(request.GET.get("size", "0"))
    if size > 4 * 1024 * 1024:
        return HttpResponseBadRequest("too large")
    # ok: mois-1-14-integer-overflow-py 숫자 리터럴 상한을 넘으면 return
    return HttpResponse(bytes(bytearray(size)))


def literal_bound_inside_if(request):
    size = int(request.GET.get("size", "0"))
    if size <= 4096:
        # ok: mois-1-14-integer-overflow-py 숫자 리터럴 상한 아래일 때만 사용
        return HttpResponse(bytes(bytearray(size)))
    return HttpResponseBadRequest("too large")


def length_bound(request):
    count = int(request.GET.get("count", "0"))
    if count < 0 or count >= len(PAYLOAD):
        return HttpResponseBadRequest("out of range")
    # ok: mois-1-14-integer-overflow-py 실제 자료 길이(len)를 넘으면 return
    return HttpResponse(bytes(bytearray(count)))


def length_bound_inside_if(request):
    count = int(request.GET.get("count", "0"))
    if count < len(PAYLOAD):
        # ok: mois-1-14-integer-overflow-py 실제 자료 길이(len) 아래일 때만 사용
        return HttpResponse(bytes(bytearray(count)))
    return HttpResponseBadRequest("out of range")


def both_bounds_with_and(request):
    size = int(request.GET.get("size", "0"))
    if size >= 0 and size <= MAX_SIZE:
        # ok: mois-1-14-integer-overflow-py 하한·상한을 and 로 묶은 조건 안
        return HttpResponse(bytes(bytearray(size)))
    return HttpResponseBadRequest("out of range")


def clamped(request):
    width = int(request.GET.get("width", "0"))
    index = int(request.GET.get("index", "0"))
    # ok: mois-1-14-integer-overflow-py min(상한, 값) — 상한이 앞에 와도 같다
    first = bytearray(min(4096, width))
    # ok: mois-1-14-integer-overflow-py 실제 자료 길이로 자른 값
    second = bytearray(int(np.clip(index, 0, len(PAYLOAD))))
    return HttpResponse(bytes(first + second))
