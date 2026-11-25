import os

from django.conf import settings
from django.http import Http404, HttpResponse, HttpResponseBadRequest


def download(request):
    # ok: mois-1-03-path-traversal-py 디렉터리 부분을 버리고 파일명만 사용
    name = os.path.basename(request.GET.get("name", ""))
    path = os.path.join(settings.MEDIA_ROOT, "docs", name)
    try:
        with open(path, "rb") as fp:
            data = fp.read()
    except FileNotFoundError as exc:
        raise Http404("not found") from exc
    return HttpResponse(data, content_type="application/octet-stream")


def delete_attachment(request):
    base = os.path.realpath(settings.MEDIA_ROOT)
    target = os.path.realpath(os.path.join(base, request.POST.get("file", "")))
    # 정규화한 경로가 기준 디렉터리 안인지 확인
    if not target.startswith(base + os.sep):
        return HttpResponseBadRequest("invalid path")
    # ok: mois-1-03-path-traversal-py 구분자를 붙인 접두 비교에 실패하면 위에서 빠져나감
    os.remove(target)
    return HttpResponse("deleted")
