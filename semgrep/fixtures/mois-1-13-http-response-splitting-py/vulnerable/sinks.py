from django.http import HttpResponse
from flask import Flask, make_response, request

app = Flask(__name__)


@app.route("/export")
def export():
    name = request.args.get("name", "export.csv")
    trace = request.args.get("trace", "")
    resp = make_response("id,name\n")
    # werkzeug Headers 의 add·set·append·setdefault
    # ruleid: mois-1-13-http-response-splitting-py
    resp.headers.add("Content-Disposition", "attachment; filename=" + name)
    # ruleid: mois-1-13-http-response-splitting-py
    resp.headers.set("X-Trace-Id", trace)
    # ruleid: mois-1-13-http-response-splitting-py
    resp.headers.append("X-Trace-Parent", trace)
    # ruleid: mois-1-13-http-response-splitting-py
    resp.headers.setdefault("X-Request-Source", trace)
    return resp


@app.route("/theme")
def theme():
    resp = make_response("ok")
    # 쿠키 값(키워드 인자)
    # ruleid: mois-1-13-http-response-splitting-py
    resp.set_cookie("theme", value=request.args["theme"], secure=True, httponly=True)
    return resp


def remember_region(request):
    response = HttpResponse("ok")
    # 서명 쿠키도 값은 그대로 헤더에 실린다
    # ruleid: mois-1-13-http-response-splitting-py
    response.set_signed_cookie("region", request.GET["region"], secure=True, httponly=True)
    return response


def download(request):
    name = request.GET.get("name", "report.pdf")
    # 응답 생성자의 headers 인자
    # ruleid: mois-1-13-http-response-splitting-py
    return HttpResponse(b"", headers={"Content-Disposition": "attachment; filename=" + name})
