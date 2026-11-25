"""응답 객체 변수 이름(resp·res·rsp·http_response)과 headers={...} 를 받는 응답 생성 함수별 예제."""
from django.http import HttpResponse
from flask_restful import Api
from sanic import Sanic
from sanic.response import redirect
from sanic_ext import render

sanic_app = Sanic("portal")
api = Api()


def export_csv(request):
    name = request.GET.get("name", "export.csv")
    resp = HttpResponse("id,name\n", content_type="text/csv")
    # ruleid: mois-1-13-http-response-splitting-py
    resp["Content-Disposition"] = "attachment; filename=" + name
    return resp


def export_pdf(request):
    res = HttpResponse(b"", content_type="application/pdf")
    # ruleid: mois-1-13-http-response-splitting-py
    res["Content-Disposition"] = "inline; filename=" + request.GET["name"]
    return res


def trace(request):
    rsp = HttpResponse("ok")
    # ruleid: mois-1-13-http-response-splitting-py
    rsp["X-Trace-Id"] = request.GET.get("trace", "")
    return rsp


def region(request):
    http_response = HttpResponse("ok")
    # ruleid: mois-1-13-http-response-splitting-py
    http_response["X-Region"] = request.POST["region"]
    return http_response


def restful_item(request):
    tag = request.args.get("tag", "")
    # Flask-RESTful Api.make_response(data, code, headers=...)
    # ruleid: mois-1-13-http-response-splitting-py
    return api.make_response({"ok": True}, 200, headers={"X-Request-Tag": tag})


@sanic_app.get("/lang")
async def switch_language(request):
    lang = request.args.get("lang", "ko")
    # Sanic redirect(to, headers=...)
    # ruleid: mois-1-13-http-response-splitting-py
    return redirect("/", headers={"Content-Language": lang})


@sanic_app.get("/home")
async def home(request):
    theme = request.args.get("theme", "light")
    # Sanic Extensions render(template, headers=...)
    # ruleid: mois-1-13-http-response-splitting-py
    return await render("home.html", headers={"X-Theme": theme})
