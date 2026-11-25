import html
import json
from urllib.parse import quote, quote_plus

import bleach
import nh3
from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.html import conditional_escape, format_html
from django.utils.safestring import mark_safe
from flask import Flask, Response, jsonify, make_response, render_template, render_template_string, request

from reports.pdf import build_pdf

app = Flask(__name__)


def escaped(request):
    q = request.GET.get("q", "")
    # ok: mois-1-04-xss-py 이스케이프한 값
    a = HttpResponse("<p>" + html.escape(q) + "</p>")
    # ok: mois-1-04-xss-py
    b = HttpResponse("<p>" + conditional_escape(q) + "</p>")
    # ok: mois-1-04-xss-py format_html 은 인자를 이스케이프한다
    c = HttpResponse(format_html("<p>{}</p>", q))
    # ok: mois-1-04-xss-py 허용한 태그만 남기는 정화 라이브러리
    d = mark_safe(bleach.clean(q))
    # ok: mois-1-04-xss-py
    e = mark_safe(nh3.clean(q))
    return a or b or c or d or e


def url_encoded(request):
    q = request.GET.get("q", "")
    # ok: mois-1-04-xss-py URL 인코딩한 값은 < > " 를 포함하지 않는다
    a = HttpResponse("<a href='/search?q=" + quote(q) + "'>다시 검색</a>")
    # ok: mois-1-04-xss-py
    b = HttpResponse("<a href='/search?q=" + quote_plus(q) + "'>다시 검색</a>")
    return a or b


def numbers(request):
    # ok: mois-1-04-xss-py 숫자로 바꾼 값
    a = HttpResponse("<p>page %d</p>" % int(request.GET.get("page", "1")))
    # ok: mois-1-04-xss-py
    b = HttpResponse("<p>ratio %.2f</p>" % float(request.GET.get("ratio", "0")))
    return a or b


def templates(request):
    q = request.GET.get("q", "")
    # ok: mois-1-04-xss-py 자동 이스케이프되는 템플릿으로 만든 본문
    a = HttpResponse(render_to_string("search.html", {"q": q}))
    # ok: mois-1-04-xss-py
    b = HttpResponse(render(request, "search.html", {"q": q}).content)
    return a or b


def not_html(request):
    q = request.GET.get("q", "")
    # ok: mois-1-04-xss-py HTML 이 아닌 content_type 을 지정한 응답
    a = HttpResponse(json.dumps({"q": q}), content_type="application/json")
    # ok: mois-1-04-xss-py
    b = HttpResponse("q=" + q, content_type="text/plain; charset=utf-8")
    # ok: mois-1-04-xss-py 내려받는 형식
    c = HttpResponse(request.body, content_type="application/octet-stream")
    # ok: mois-1-04-xss-py
    d = HttpResponse(build_pdf(q), content_type="application/pdf")
    return a or b or c or d


@app.route("/flask/export")
def flask_not_html():
    name = request.args.get("name", "")
    # ok: mois-1-04-xss-py HTML 이 아닌 mimetype 을 지정한 flask 응답
    return Response("name=" + name, mimetype="text/plain")


@app.route("/flask/export.csv")
def flask_csv():
    name = request.args.get("name", "")
    # ok: mois-1-04-xss-py HTML 이 아닌 content_type 을 지정한 flask 응답
    return Response(name + "\n", content_type="text/csv; charset=utf-8")


@app.route("/flask/templates")
def flask_templates():
    name = request.args.get("name", "")
    # ok: mois-1-04-xss-py 자동 이스케이프되는 템플릿·JSON 으로 만든 본문
    a = make_response(render_template("hello.html", name=name))
    # ok: mois-1-04-xss-py
    b = make_response(render_template_string("<h1>{{ name }}</h1>", name=name))
    # ok: mois-1-04-xss-py
    c = make_response(jsonify({"name": name}))
    # ok: mois-1-04-xss-py Flask 가 자동 이스케이프하는 나머지 확장자
    d = make_response(render_template("hello.htm", name=name))
    # ok: mois-1-04-xss-py
    e = make_response(render_template("feed.xml", name=name))
    # ok: mois-1-04-xss-py
    f = make_response(render_template("page.xhtml", name=name))
    # ok: mois-1-04-xss-py
    g = make_response(render_template("badge.svg", name=name))
    return a or b or c or d or e or f or g


@app.route("/flask/json")
def flask_json():
    # ok: mois-1-04-xss-py dict 를 반환하면 JSON 으로 응답된다
    return {"name": request.args.get("name", "")}, 200


def escaped_variable_in_body(request):
    safe = html.escape(request.GET.get("q", ""))
    # ok: mois-1-04-xss-py 이스케이프한 값을 본문 위치에 넣음 (변수 경유)
    return HttpResponse("<p>" + safe + "</p>")


def escaped_variable_in_quoted_attribute(request):
    safe = html.escape(request.GET.get("title", ""))
    # ok: mois-1-04-xss-py 따옴표로 감싼 일반 속성 값 (html.escape 가 따옴표를 바꾼다)
    return HttpResponse('<p title="' + safe + '">hello</p>')
