import importlib
from re import compile

from flask import Flask, request
from jinja2 import Environment

from .models import Color, Version

app = Flask(__name__)
renderer = Environment(autoescape=True)
CARD = renderer.from_string("<div class='card'>{{ title }}</div>")
EXPORTERS = ("csv", "xlsx", "pdf")


@app.route("/card")
def card():
    # ok: mois-1-02-code-injection-py 템플릿은 고정하고 입력은 변수로 전달
    return CARD.render(title=request.args.get("title", ""))


@app.route("/parse")
def parse_values():
    # ok: mois-1-02-code-injection-py 템플릿 환경이 아닌 클래스의 from_string 은 코드 실행이 아니다
    color = Color.from_string(request.args.get("color", "#000000"))
    version = Version.from_string(request.args.get("version", "1.0"))
    return {"color": color.hex, "version": str(version)}


@app.route("/match")
def match():
    # ok: mois-1-02-code-injection-py re.compile 은 코드를 실행하지 않는다 (정규식 삽입은 이 규칙의 대상이 아님)
    pattern = compile(request.args.get("pattern", ""))
    return {"groups": pattern.groups}


@app.route("/export")
def export():
    fmt = request.args.get("format", "csv")
    if fmt not in EXPORTERS:
        return {"error": "unknown format"}, 400
    # ok: mois-1-02-code-injection-py 허용 목록에 있는 이름만 import
    module = importlib.import_module("exporters." + fmt)
    return {"name": module.__name__}
