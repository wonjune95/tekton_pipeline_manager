import socket
import sys
import tempfile

from django.http import HttpResponse

from .reports import render_report


def export_report(request):
    # ruleid: mois-7-02-dangerous-api-py
    assert request.user.is_staff, "staff only"  # -O 옵션으로 실행하면 검사가 사라짐
    # ruleid: mois-7-02-dangerous-api-py
    path = tempfile.mktemp(suffix=".csv")  # 이름만 만들어 다른 프로세스가 선점할 수 있음
    with open(path, "w", encoding="utf-8") as f:
        f.write(render_report())
    return HttpResponse(path)


def reload_config(request):
    if request.POST.get("mode") == "restart":
        # ruleid: mois-7-02-dangerous-api-py
        sys.exit(1)  # 요청 처리 중 프로세스 종료: 서비스 전체가 멈춤
    return HttpResponse("ok")


def notify(request):
    # 요청 처리 코드에서 소켓을 직접 사용
    # ruleid: mois-7-02-dangerous-api-py
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect(("notify.internal", 9000))
        s.sendall(b"report-ready")
    finally:
        s.close()
    return HttpResponse("sent")
