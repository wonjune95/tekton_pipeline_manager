"""content_type·mimetype 을 지정했지만 브라우저가 스크립트를 실행하는 형식 — 모두 탐지되어야 한다."""
from django.http import HttpResponse
from flask import Flask, Response, request

app = Flask(__name__)


def django_rendered_types(request):
    q = request.GET.get("q", "")
    # SVG·XML·XHTML 도 브라우저가 문서로 해석하고 <script> 를 실행한다
    # ruleid: mois-1-04-xss-py
    a = HttpResponse("<svg xmlns='http://www.w3.org/2000/svg'>" + q + "</svg>", content_type="image/svg+xml")
    # ruleid: mois-1-04-xss-py
    b = HttpResponse("<r>" + q + "</r>", content_type="text/xml")
    # ruleid: mois-1-04-xss-py
    c = HttpResponse("<p>" + q + "</p>", content_type="application/xhtml+xml")
    # 대소문자·앞 공백이 달라도 text/html 이다
    # ruleid: mois-1-04-xss-py
    d = HttpResponse("<p>" + q + "</p>", content_type="Text/HTML; charset=utf-8")
    # ruleid: mois-1-04-xss-py
    e = HttpResponse("<p>" + q + "</p>", content_type=" text/html")
    # 빈 값이면 브라우저가 내용을 보고 형식을 정한다
    # ruleid: mois-1-04-xss-py
    f = HttpResponse("<p>" + q + "</p>", content_type="")
    # 허용 목록의 형식으로 "시작"만 하는 다른 형식
    # ruleid: mois-1-04-xss-py
    g = HttpResponse("<p>" + q + "</p>", content_type="text/plainhtml")
    return a or b or c or d or e or f or g


@app.route("/flask/feed")
def flask_xml_mimetype():
    name = request.args.get("name", "")
    # ruleid: mois-1-04-xss-py
    return Response("<r>" + name + "</r>", mimetype="application/xml")


@app.route("/flask/feed2")
def flask_xml_content_type():
    name = request.args.get("name", "")
    # ruleid: mois-1-04-xss-py
    return Response("<r>" + name + "</r>", content_type="text/xml")


@app.route("/flask/both")
def flask_content_type_wins():
    name = request.args.get("name", "")
    # flask 는 content_type 이 mimetype 보다 우선한다 — 실제 응답은 text/html
    # ruleid: mois-1-04-xss-py
    return Response("<p>" + name + "</p>", mimetype="text/plain", content_type="text/html")
