import os

from django.conf import settings
from django.http import FileResponse, HttpResponse


def download(request):
    name = request.GET.get("name", "")
    # 외부 입력을 그대로 경로에 합침 (../ 로 상위 디렉터리 접근 가능)
    path = os.path.join(settings.MEDIA_ROOT, "docs", name)
    # ruleid: mois-1-03-path-traversal-py
    return FileResponse(open(path, "rb"))


def delete_attachment(request):
    target = os.path.join(settings.MEDIA_ROOT, request.POST["file"])
    # 외부 입력 경로의 파일을 삭제
    # ruleid: mois-1-03-path-traversal-py
    os.remove(target)
    return HttpResponse("deleted")
