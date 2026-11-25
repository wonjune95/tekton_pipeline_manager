from django.http import HttpResponse
from django.template import Context, Template, engines
from flask import Flask, request
from jinja2 import Environment
from mako.template import Template as MakoTemplate

app = Flask(__name__)
renderer = Environment(autoescape=True)


@app.route("/run", methods=["POST"])
def run_snippet():
    source = request.form["source"]
    scope = {}
    # ruleid: mois-1-02-code-injection-py
    exec(source, scope)
    # ruleid: mois-1-02-code-injection-py
    code = compile(request.form["expr"], "<expr>", "eval")
    # ruleid: mois-1-02-code-injection-py
    driver = __import__("drivers." + request.form["driver"])
    return {"keys": sorted(scope), "code": repr(code), "driver": driver.__name__}


def django_preview(request):
    # 템플릿 원문이 외부 입력 (SSTI)
    # ruleid: mois-1-02-code-injection-py
    first = Template(request.POST["body"]).render(Context({}))
    # ruleid: mois-1-02-code-injection-py
    second = engines["django"].from_string("<p>" + request.POST["body"] + "</p>").render({})
    return HttpResponse(first + second)


@app.route("/mako", methods=["POST"])
def mako_preview():
    # ruleid: mois-1-02-code-injection-py
    return MakoTemplate(request.form["body"]).render()


@app.route("/jinja", methods=["POST"])
def jinja_preview():
    body = request.form["body"]
    # 같은 파일에서 jinja2.Environment 로 만든 객체
    # ruleid: mois-1-02-code-injection-py
    first = renderer.from_string(body).render()
    # 이름이 템플릿 환경인 객체 (Flask 의 app.jinja_env)
    # ruleid: mois-1-02-code-injection-py
    second = app.jinja_env.from_string("Hello " + body).render()
    return first + second


class MailRenderer:
    """템플릿 환경을 밖에서 받아 쓰는 클래스 — 만든 곳은 보이지 않지만 이름이 템플릿 환경이다."""

    def __init__(self, env, environment, template_engine, jinja):
        self.env = env
        self.environment = environment
        self.template_engine = template_engine
        self.jinja = jinja

    def preview(self, request):
        body = request.POST["body"]
        # ruleid: mois-1-02-code-injection-py
        subject = self.env.from_string(request.POST["subject"]).render()
        # ruleid: mois-1-02-code-injection-py
        html = self.environment.from_string(body).render()
        # ruleid: mois-1-02-code-injection-py
        text = self.template_engine.from_string(body).render({})
        # ruleid: mois-1-02-code-injection-py
        footer = self.jinja.from_string(request.POST["footer"]).render()
        return HttpResponse(subject + html + text + footer)
