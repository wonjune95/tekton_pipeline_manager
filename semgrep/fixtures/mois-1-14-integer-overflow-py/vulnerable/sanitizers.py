"""범위 검사처럼 보이지만 상한이 걸리지 않는 경우 — 모두 탐지되어야 한다."""
from django.http import HttpResponse, HttpResponseBadRequest

MAX_SIZE = 1024 * 1024


def comparison_result_ignored(request):
    size = int(request.GET.get("size", "0"))
    # 비교 결과를 쓰지 않음
    size <= MAX_SIZE
    # ruleid: mois-1-14-integer-overflow-py
    return HttpResponse(bytes(bytearray(size)))


def lower_bound_only(request):
    size = int(request.GET.get("size", "0"))
    # 음수만 걸러낸다 — 상한이 없다
    if size < 0:
        return HttpResponseBadRequest("negative")
    # ruleid: mois-1-14-integer-overflow-py
    return HttpResponse(bytes(bytearray(size)))


def lower_bound_only_positive(request):
    size = int(request.GET.get("size", "0"))
    if size > 0:
        # ruleid: mois-1-14-integer-overflow-py
        return HttpResponse(bytes(bytearray(size)))
    return HttpResponseBadRequest("empty")


def failure_does_not_exit(request):
    size = int(request.GET.get("size", "0"))
    if size > MAX_SIZE:
        print("large request", size)
    # ruleid: mois-1-14-integer-overflow-py
    return HttpResponse(bytes(bytearray(size)))


def opposite_branch(request):
    size = int(request.GET.get("size", "0"))
    if size <= MAX_SIZE:
        return HttpResponse(b"")
    else:
        # ruleid: mois-1-14-integer-overflow-py
        return HttpResponse(bytes(bytearray(size)))


def sink_inside_failing_branch(request):
    size = int(request.GET.get("size", "0"))
    if size > MAX_SIZE:
        # 상한을 넘은 값으로 버퍼를 잡고 빠져나간다
        # ruleid: mois-1-14-integer-overflow-py
        return HttpResponse(bytes(bytearray(size)))
    return HttpResponse(b"")


def inverted_condition(request):
    size = int(request.GET.get("size", "0"))
    # not 때문에 뜻이 뒤집힌다: 상한 이하이면 빠져나가고, 넘는 값이 내려온다
    if not size > MAX_SIZE:
        return HttpResponse(b"")
    # ruleid: mois-1-14-integer-overflow-py
    return HttpResponse(bytes(bytearray(size)))


def inverted_range(request):
    size = int(request.GET.get("size", "0"))
    # 범위 밖일 때만 들어오는 분기
    if not 0 <= size <= MAX_SIZE:
        # ruleid: mois-1-14-integer-overflow-py
        return HttpResponse(bytes(bytearray(size)))
    return HttpResponse(b"")


def nested_conditional_exit(request):
    size = int(request.GET.get("size", "0"))
    if size > MAX_SIZE:
        if request.GET.get("strict"):
            return HttpResponseBadRequest("too large")
    # 엄격 모드가 아니면 상한을 넘은 값이 그대로 내려온다
    # ruleid: mois-1-14-integer-overflow-py
    return HttpResponse(bytes(bytearray(size)))


def reassigned_after_check(request):
    size = int(request.GET.get("size", "0"))
    if size > MAX_SIZE:
        return HttpResponseBadRequest("too large")
    # 검사한 뒤에 다른 입력으로 바꿔 넣는다
    size = int(request.GET.get("padding", "0"))
    # ruleid: mois-1-14-integer-overflow-py
    return HttpResponse(bytes(bytearray(size)))


def added_after_check(request):
    size = int(request.GET.get("size", "0"))
    if size > MAX_SIZE:
        return HttpResponseBadRequest("too large")
    # 검사한 뒤에 검사하지 않은 입력을 더한다
    size += int(request.GET.get("padding", "0"))
    # ruleid: mois-1-14-integer-overflow-py
    return HttpResponse(bytes(bytearray(size)))


def check_joined_with_and(request):
    size = int(request.GET.get("size", "0"))
    # 엄격 모드일 때만 검사한다
    if request.GET.get("strict") and size > MAX_SIZE:
        return HttpResponseBadRequest("too large")
    # ruleid: mois-1-14-integer-overflow-py
    return HttpResponse(bytes(bytearray(size)))


def check_joined_with_or(request):
    size = int(request.GET.get("size", "0"))
    # or 로 묶이면 상한을 넘은 값도 들어온다
    if request.user.is_staff or size <= MAX_SIZE:
        # ruleid: mois-1-14-integer-overflow-py
        return HttpResponse(bytes(bytearray(size)))
    return HttpResponseBadRequest("too large")


def other_variable_checked(request):
    rows = int(request.GET.get("rows", "0"))
    cols = int(request.GET.get("cols", "0"))
    if rows > 1000:
        return HttpResponseBadRequest("too large")
    # 검사한 것은 rows 뿐이다
    # ruleid: mois-1-14-integer-overflow-py
    return HttpResponse(bytes(bytearray(rows * cols)))


def min_result_discarded(request):
    size = int(request.GET.get("size", "0"))
    min(size, MAX_SIZE)
    # ruleid: mois-1-14-integer-overflow-py
    return HttpResponse(bytes(bytearray(size)))
