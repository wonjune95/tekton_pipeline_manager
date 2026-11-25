import os

from django.conf import settings
from django.http import FileResponse, HttpResponse, HttpResponseNotFound


def download(request, name):
    path = os.path.join(settings.REPORT_DIR, os.path.basename(name))
    if os.path.isfile(path):
        # 검사와 열기 사이에 파일이 바뀌거나 지워질 수 있음
        # ruleid: mois-3-01-toctou-py
        return FileResponse(open(path, "rb"))
    return HttpResponseNotFound()


def delete_report(request, name):
    path = os.path.join(settings.REPORT_DIR, os.path.basename(name))
    if os.access(path, os.W_OK):
        # ruleid: mois-3-01-toctou-py
        os.remove(path)  # 검사 후 잠금 없이 삭제
    return HttpResponse(status=204)


def ensure_dir(request):
    if not os.path.exists(settings.UPLOAD_DIR):
        # ruleid: mois-3-01-toctou-py
        os.makedirs(settings.UPLOAD_DIR)  # 동시에 두 요청이 들어오면 한쪽이 실패
    return HttpResponse("ok")


def read_note(request, name):
    path = os.path.join(settings.NOTE_DIR, os.path.basename(name))
    if os.path.exists(path):
        # ruleid: mois-3-01-toctou-py
        with open(path, encoding="utf-8") as f:  # 검사 후 잠금 없이 열기
            return HttpResponse(f.read())
    return HttpResponseNotFound()
