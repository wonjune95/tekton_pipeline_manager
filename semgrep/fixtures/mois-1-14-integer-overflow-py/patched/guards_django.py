"""guard 형태별 안전한 예제 (Django)."""
from django.http import HttpResponse, HttpResponseBadRequest

MAX_SIZE = 1024 * 1024


def guard_1(request):
    size = int(request.GET.get("size", "0"))
    if size >= MAX_SIZE:
        return HttpResponseBadRequest("invalid")
    # ok: mois-1-14-integer-overflow-py 실패하면 return
    buf = bytearray(size)
    return HttpResponse(bytes(buf))


def guard_2(request):
    size = int(request.GET.get("size", "0"))
    if size > MAX_SIZE:
        raise ValueError("invalid")
    # ok: mois-1-14-integer-overflow-py 실패하면 raise
    buf = bytearray(size)
    return HttpResponse(bytes(buf))


def guard_3(request):
    size = int(request.GET.get("size", "0"))
    if MAX_SIZE <= size:
        return HttpResponseBadRequest("invalid")
    # ok: mois-1-14-integer-overflow-py 실패하면 return
    buf = bytearray(size)
    return HttpResponse(bytes(buf))


def guard_4(request):
    size = int(request.GET.get("size", "0"))
    if MAX_SIZE < size:
        raise ValueError("invalid")
    # ok: mois-1-14-integer-overflow-py 실패하면 raise
    buf = bytearray(size)
    return HttpResponse(bytes(buf))


def guard_5(request):
    size = int(request.GET.get("size", "0"))
    if not 0 < size < MAX_SIZE:
        return HttpResponseBadRequest("invalid")
    # ok: mois-1-14-integer-overflow-py 실패하면 return
    buf = bytearray(size)
    return HttpResponse(bytes(buf))


def guard_6(request):
    size = int(request.GET.get("size", "0"))
    if not 0 < size <= MAX_SIZE:
        raise ValueError("invalid")
    # ok: mois-1-14-integer-overflow-py 실패하면 raise
    buf = bytearray(size)
    return HttpResponse(bytes(buf))


def guard_7(request):
    size = int(request.GET.get("size", "0"))
    if not 0 <= size < MAX_SIZE:
        return HttpResponseBadRequest("invalid")
    # ok: mois-1-14-integer-overflow-py 실패하면 return
    buf = bytearray(size)
    return HttpResponse(bytes(buf))


def guard_8(request):
    size = int(request.GET.get("size", "0"))
    if not 0 <= size <= MAX_SIZE:
        raise ValueError("invalid")
    # ok: mois-1-14-integer-overflow-py 실패하면 raise
    buf = bytearray(size)
    return HttpResponse(bytes(buf))


def guard_9(request):
    size = int(request.GET.get("size", "0"))
    if size is None or size >= MAX_SIZE:
        raise ValueError("invalid")
    # ok: mois-1-14-integer-overflow-py 값이 없거나 실패하면 raise
    buf = bytearray(size)
    return HttpResponse(bytes(buf))


def guard_10(request):
    size = int(request.GET.get("size", "0"))
    if size is None or size > MAX_SIZE:
        return HttpResponseBadRequest("invalid")
    # ok: mois-1-14-integer-overflow-py 값이 없거나 실패하면 return
    buf = bytearray(size)
    return HttpResponse(bytes(buf))


def guard_11(request):
    size = int(request.GET.get("size", "0"))
    if size is None or MAX_SIZE <= size:
        raise ValueError("invalid")
    # ok: mois-1-14-integer-overflow-py 값이 없거나 실패하면 raise
    buf = bytearray(size)
    return HttpResponse(bytes(buf))


def guard_12(request):
    size = int(request.GET.get("size", "0"))
    if size is None or MAX_SIZE < size:
        return HttpResponseBadRequest("invalid")
    # ok: mois-1-14-integer-overflow-py 값이 없거나 실패하면 return
    buf = bytearray(size)
    return HttpResponse(bytes(buf))


def guard_13(request):
    size = int(request.GET.get("size", "0"))
    if size is None or not 0 < size < MAX_SIZE:
        raise ValueError("invalid")
    # ok: mois-1-14-integer-overflow-py 값이 없거나 실패하면 raise
    buf = bytearray(size)
    return HttpResponse(bytes(buf))


def guard_14(request):
    size = int(request.GET.get("size", "0"))
    if size is None or not 0 < size <= MAX_SIZE:
        return HttpResponseBadRequest("invalid")
    # ok: mois-1-14-integer-overflow-py 값이 없거나 실패하면 return
    buf = bytearray(size)
    return HttpResponse(bytes(buf))


def guard_15(request):
    size = int(request.GET.get("size", "0"))
    if size is None or not 0 <= size < MAX_SIZE:
        raise ValueError("invalid")
    # ok: mois-1-14-integer-overflow-py 값이 없거나 실패하면 raise
    buf = bytearray(size)
    return HttpResponse(bytes(buf))


def guard_16(request):
    size = int(request.GET.get("size", "0"))
    if size is None or not 0 <= size <= MAX_SIZE:
        return HttpResponseBadRequest("invalid")
    # ok: mois-1-14-integer-overflow-py 값이 없거나 실패하면 return
    buf = bytearray(size)
    return HttpResponse(bytes(buf))


def guard_17(request):
    for raw in request.GET.getlist("size"):
        size = int(raw)
        if size >= MAX_SIZE:
            continue
        # ok: mois-1-14-integer-overflow-py 실패한 값은 건너뜀
        buf = bytearray(size)
    return HttpResponse(bytes(buf))


def guard_18(request):
    for raw in request.GET.getlist("size"):
        size = int(raw)
        if size is None or not 0 <= size <= MAX_SIZE:
            continue
        # ok: mois-1-14-integer-overflow-py 비었거나 실패한 값은 건너뜀
        buf = bytearray(size)
    return HttpResponse(bytes(buf))


def guard_19(request):
    size = int(request.GET.get("size", "0"))
    if size < MAX_SIZE:
        # ok: mois-1-14-integer-overflow-py 검사를 통과한 조건 안에서만 사용
        buf = bytearray(size)
    return HttpResponse(bytes(buf))


def guard_20(request):
    size = int(request.GET.get("size", "0"))
    if size <= MAX_SIZE:
        # ok: mois-1-14-integer-overflow-py 검사를 통과한 조건 안에서만 사용
        buf = bytearray(size)
    return HttpResponse(bytes(buf))


def guard_21(request):
    size = int(request.GET.get("size", "0"))
    if MAX_SIZE > size:
        # ok: mois-1-14-integer-overflow-py 검사를 통과한 조건 안에서만 사용
        buf = bytearray(size)
    return HttpResponse(bytes(buf))


def guard_22(request):
    size = int(request.GET.get("size", "0"))
    if MAX_SIZE >= size:
        # ok: mois-1-14-integer-overflow-py 검사를 통과한 조건 안에서만 사용
        buf = bytearray(size)
    return HttpResponse(bytes(buf))


def guard_23(request):
    size = int(request.GET.get("size", "0"))
    if 0 < size < MAX_SIZE:
        # ok: mois-1-14-integer-overflow-py 검사를 통과한 조건 안에서만 사용
        buf = bytearray(size)
    return HttpResponse(bytes(buf))


def guard_24(request):
    size = int(request.GET.get("size", "0"))
    if 0 < size <= MAX_SIZE:
        # ok: mois-1-14-integer-overflow-py 검사를 통과한 조건 안에서만 사용
        buf = bytearray(size)
    return HttpResponse(bytes(buf))


def guard_25(request):
    size = int(request.GET.get("size", "0"))
    if 0 <= size < MAX_SIZE:
        # ok: mois-1-14-integer-overflow-py 검사를 통과한 조건 안에서만 사용
        buf = bytearray(size)
    return HttpResponse(bytes(buf))


def guard_26(request):
    size = int(request.GET.get("size", "0"))
    if 0 <= size <= MAX_SIZE:
        # ok: mois-1-14-integer-overflow-py 검사를 통과한 조건 안에서만 사용
        buf = bytearray(size)
    return HttpResponse(bytes(buf))
