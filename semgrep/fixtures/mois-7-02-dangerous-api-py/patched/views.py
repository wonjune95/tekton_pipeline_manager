import tempfile

import requests
from django.http import HttpResponse, HttpResponseForbidden

from .reports import render_report

NOTIFY_URL = "https://notify.internal.example.go.kr/report-ready"


def export_report(request):
    if not request.user.is_staff:
        return HttpResponseForbidden()
    # 파일을 만들면서 이름을 정한다
    with tempfile.NamedTemporaryFile("w", suffix=".csv", encoding="utf-8", delete=False) as f:
        f.write(render_report())
    return HttpResponse(f.name)


def reload_config(request):
    if request.POST.get("mode") == "restart":
        # 프로세스를 끝내지 않고 오류 응답을 돌려준다
        return HttpResponse("E503", status=503)
    return HttpResponse("ok")


def notify(request):
    resp = requests.post(NOTIFY_URL, timeout=5)
    resp.raise_for_status()
    return HttpResponse("sent")
