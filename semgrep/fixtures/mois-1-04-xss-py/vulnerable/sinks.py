import starlette.responses
from django.http import HttpResponse
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from flask import Flask, Response, make_response, request
from markupsafe import Markup

app = Flask(__name__)
api = FastAPI()


def django_keyword(request):
    # content= 키워드, text/html 을 명시한 경우도 같다
    # ruleid: mois-1-04-xss-py
    return HttpResponse(content="<p>" + request.GET.get("q", "") + "</p>", content_type="text/html; charset=utf-8")


@app.route("/flask/response")
def flask_make_response():
    name = request.args.get("name", "")
    # ruleid: mois-1-04-xss-py
    return make_response("<h1>" + name + "</h1>")


@app.route("/flask/response-class")
def flask_response_class():
    name = request.args.get("name", "")
    # ruleid: mois-1-04-xss-py
    return Response(f"<h1>{name}</h1>")


@app.route("/flask/response-keyword")
def flask_response_keyword():
    name = request.args.get("name", "")
    # ruleid: mois-1-04-xss-py
    return Response(response="<h1>%s</h1>" % name, status=200)


@app.route("/flask/tuple")
def flask_tuple():
    # (본문, 상태 코드) 로 반환
    # ruleid: mois-1-04-xss-py
    return "<p>not found: " + request.args.get("page", "") + "</p>", 404


@app.route("/flask/tuple-suffix")
def flask_tuple_suffix():
    name = request.args.get("name", "")
    # 입력으로 시작하고 리터럴로 끝나는 본문
    # ruleid: mois-1-04-xss-py
    return name + " 님, 권한이 없습니다", 403


@app.route("/flask/markup")
def flask_markup():
    # 이스케이프를 끄는 표시
    # ruleid: mois-1-04-xss-py
    return {"badge": Markup("<b>" + request.args.get("name", "") + "</b>")}


@api.get("/fastapi/positional")
def fastapi_positional(name: str):
    # ruleid: mois-1-04-xss-py
    return HTMLResponse("<h1>" + name + "</h1>")


@api.get("/starlette")
def starlette_response(name: str, title: str):
    # ruleid: mois-1-04-xss-py
    first = starlette.responses.HTMLResponse("<h1>" + name + "</h1>")
    # ruleid: mois-1-04-xss-py
    second = starlette.responses.HTMLResponse(content=f"<title>{title}</title>")
    return first or second


@api.get("/fastapi/tuple")
def fastapi_string_tuple(name: str):
    # 태그가 들어간 문자열을 (본문, 상태) 로 반환 (Flask 2 의 @app.get 도 같은 모양)
    # ruleid: mois-1-04-xss-py
    return f"<li>{name}</li>", 200


@app.route("/flask/prefix")
def flask_prefix():
    # 문자열 리터럴로 시작하고 입력으로 끝나는 식
    # ruleid: mois-1-04-xss-py
    return "검색어: " + request.args.get("q", "")


@api.api_route("/fastapi/notice", methods=["GET", "POST"], response_class=HTMLResponse)
def fastapi_api_route(title: str):
    # ruleid: mois-1-04-xss-py
    return f"<h2>{title}</h2>"
