import struct

from django.http import HttpResponse, HttpResponseBadRequest

MAX_PADDING = 1024 * 1024
INT32_MAX = 2**31 - 1


def make_padding(request):
    size = int(request.GET.get("size", "0"))
    # 음수·상한을 검사한 뒤 크기로 사용
    if size < 0 or size > MAX_PADDING:
        return HttpResponseBadRequest("size out of range")
    # ok: mois-1-14-integer-overflow-py
    buf = bytearray(size)
    return HttpResponse(bytes(buf), content_type="application/octet-stream")


def pack_quantity(request):
    qty = int(request.POST.get("qty", "0"))
    if not 0 <= qty <= INT32_MAX:
        return HttpResponseBadRequest("qty out of range")
    # ok: mois-1-14-integer-overflow-py
    record = struct.pack("<i", qty)
    return HttpResponse(record, content_type="application/octet-stream")
