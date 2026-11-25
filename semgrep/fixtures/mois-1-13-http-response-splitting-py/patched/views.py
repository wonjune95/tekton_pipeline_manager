import re

from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect

from .reports import build_csv

SUPPORTED_LANGUAGES = ("ko", "en")


def export_report(request):
    filename = request.GET.get("filename", "report.csv")
    # 개행 문자를 제거한 뒤 헤더에 넣음
    safe_name = re.sub(r"[\r\n]", "", filename)
    response = HttpResponse(build_csv(), content_type="text/csv")
    # ok: mois-1-13-http-response-splitting-py
    response["Content-Disposition"] = "attachment; filename=" + safe_name
    return response


def set_language(request):
    lang = request.GET.get("lang", "ko")
    if lang not in SUPPORTED_LANGUAGES:
        return HttpResponseBadRequest("unsupported language")
    response = HttpResponseRedirect("/")
    # ok: mois-1-13-http-response-splitting-py 허용 목록에 없으면 위에서 빠져나감
    response.set_cookie("lang", lang, secure=True, httponly=True, samesite="Lax")
    return response
