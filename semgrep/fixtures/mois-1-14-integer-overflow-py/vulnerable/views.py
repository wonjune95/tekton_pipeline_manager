import struct

from django.http import HttpResponse


def make_padding(request):
    size = int(request.GET.get("size", "0"))
    # 외부 입력값을 범위 검사 없이 버퍼 크기로 사용
    # ruleid: mois-1-14-integer-overflow-py
    buf = bytearray(size)
    return HttpResponse(bytes(buf), content_type="application/octet-stream")


def pack_quantity(request):
    qty = int(request.POST.get("qty", "0"))
    # 범위 검사 없이 4바이트 부호 있는 정수로 변환
    # ruleid: mois-1-14-integer-overflow-py
    record = struct.pack("<i", qty)
    return HttpResponse(record, content_type="application/octet-stream")
