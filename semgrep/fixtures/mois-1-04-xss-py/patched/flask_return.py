"""Flask 뷰의 반환값 중 문자열이 아닌 것 — 탐지되면 안 된다."""
from flask import Blueprint, Flask, Response, request

from myproject.pages import build_page

app = Flask(__name__)
bp = Blueprint("pages", __name__)


@app.route("/page")
def helper_result():
    name = request.args["name"]
    # ok: mois-1-04-xss-py 함수 호출 결과는 응답 객체일 수 있다 (문자열이라고 증명할 수 없다)
    return build_page(name)


@app.route("/page-created")
def helper_result_with_status():
    name = request.args["name"]
    # ok: mois-1-04-xss-py
    return build_page(name), 201


@app.route("/names")
def list_literal():
    # ok: mois-1-04-xss-py list 를 반환하면 JSON 으로 응답된다
    return [request.args["name"]]


@app.route("/profile")
def dict_literal_in_parentheses():
    # ok: mois-1-04-xss-py 괄호로 감싼 (dict, 상태 코드)
    return ({"name": request.args["name"]}, 200)


@bp.get("/export")
def response_call():
    name = request.args["name"]
    # ok: mois-1-04-xss-py 응답 객체를 바로 반환 (본문은 text/plain 으로 지정했다)
    return Response("name=" + name, mimetype="text/plain")
