import importlib

import jinja2
from django import template as django_template
from django.http import HttpResponse
from django.template import engines
from flask import Flask, render_template_string, request
from jinja2 import Environment, Template
from mako.template import Template as MakoTemplate

app = Flask(__name__)
renderer = Environment(autoescape=True)


@app.route("/kw/run", methods=["POST"])
def run_by_keyword():
    """코드·모듈 이름·템플릿 원문을 키워드 인자로 넘겨도 같은 자리다 — "첫 번째 위치 인자"만 보면 통째로 놓친다."""
    body = request.form["body"]
    # ruleid: mois-1-02-code-injection-py
    code = compile(source=request.form["expr"], filename="<expr>", mode="eval")
    # ruleid: mois-1-02-code-injection-py
    driver = __import__(name="drivers." + request.form["driver"])
    # ruleid: mois-1-02-code-injection-py
    plugin = importlib.import_module(name="plugins." + request.form["plugin"])
    # 상대 import 의 기준 패키지도 어느 모듈을 실행할지 정한다
    # ruleid: mois-1-02-code-injection-py
    hook = importlib.import_module(".hooks", package=request.form["package"])
    # ruleid: mois-1-02-code-injection-py
    hook2 = importlib.import_module(".hooks", request.form["package"])
    # ruleid: mois-1-02-code-injection-py
    first = Template(source="Hello " + body).render()
    # ruleid: mois-1-02-code-injection-py
    second = MakoTemplate(text="Hello " + body).render()
    # ruleid: mois-1-02-code-injection-py
    third = render_template_string(source="<h1>Hello " + body + "</h1>")
    return {"code": repr(code), "names": [m.__name__ for m in (driver, plugin, hook, hook2)], "html": first + second + third}


def django_preview_by_keyword(request):
    # ruleid: mois-1-02-code-injection-py
    first = django_template.Template(template_string=request.POST["body"]).render(django_template.Context({}))
    # ruleid: mois-1-02-code-injection-py
    second = engines["django"].from_string(template_code="<p>" + request.POST["body"] + "</p>").render({})
    return HttpResponse(first + second)


@app.route("/kw/jinja", methods=["POST"])
def jinja_from_string_shapes():
    body = request.form["body"]
    # 환경을 만들자마자 호출 — 변수에 담지 않아도 템플릿 환경이다
    # ruleid: mois-1-02-code-injection-py
    first = jinja2.Environment().from_string(body).render()
    # ruleid: mois-1-02-code-injection-py
    second = renderer.from_string(source="Hello " + body).render()
    # 원문 키워드 이름은 엔진마다 다르다 (Jinja2 source, Django template_code)
    # ruleid: mois-1-02-code-injection-py
    third = app.jinja_env.from_string(template_code=body, globals={"site": "demo"}).render()
    return first + second + third
