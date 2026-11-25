from django.http import HttpResponse, HttpResponseRedirect

from .reports import build_csv


def export_report(request):
    filename = request.GET.get("filename", "report.csv")
    response = HttpResponse(build_csv(), content_type="text/csv")
    # 외부 입력을 개행 문자 제거 없이 응답 헤더에 넣음
    # ruleid: mois-1-13-http-response-splitting-py
    response["Content-Disposition"] = "attachment; filename=" + filename
    return response


def set_language(request):
    response = HttpResponseRedirect("/")
    # 외부 입력을 그대로 쿠키 값으로 사용
    # ruleid: mois-1-13-http-response-splitting-py
    response.set_cookie("lang", request.GET["lang"], secure=True, httponly=True, samesite="Lax")
    return response
