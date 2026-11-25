import os

from django.conf import settings
from django.http import FileResponse, HttpResponse, HttpResponseNotFound


def download(request, name):
    path = os.path.join(settings.REPORT_DIR, os.path.basename(name))
    try:
        # 검사 없이 바로 열고, 없으면 예외로 처리
        return FileResponse(open(path, "rb"))
    except FileNotFoundError:
        return HttpResponseNotFound()


def delete_report(request, name):
    path = os.path.join(settings.REPORT_DIR, os.path.basename(name))
    try:
        os.remove(path)
    except FileNotFoundError:
        return HttpResponseNotFound()
    return HttpResponse(status=204)


def ensure_dir(request):
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    return HttpResponse("ok")
