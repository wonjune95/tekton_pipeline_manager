"""템플릿으로 렌더링했지만 자동 이스케이프가 적용되지 않는 경우."""
from flask import Flask, make_response, render_template, render_template_string, request

app = Flask(__name__)


@app.route("/greeting")
def not_autoescaped_extension():
    name = request.args.get("name", "")
    # Flask 는 .html .htm .xml .xhtml .svg 템플릿만 자동 이스케이프한다
    # ruleid: mois-1-04-xss-py
    return make_response(render_template("greeting.j2", name=name))


@app.route("/mail-preview")
def text_template():
    name = request.args.get("name", "")
    # ruleid: mois-1-04-xss-py
    return make_response(render_template("mail/body.txt", name=name))


@app.route("/greeting-by-name")
def template_name_in_variable():
    name = request.args.get("name", "")
    # 템플릿 이름이 변수면 확장자를 알 수 없다
    template_name = "greeting." + ("j2" if name else "html")
    # ruleid: mois-1-04-xss-py
    return make_response(render_template(template_name, name=name))


@app.route("/inline-safe")
def inline_template_safe_filter():
    name = request.args.get("name", "")
    # ruleid: mois-1-04-xss-py
    return make_response(render_template_string("<p>{{ n|safe }}</p>", n=name))


@app.route("/inline-autoescape-off")
def inline_template_autoescape_off():
    name = request.args.get("name", "")
    # ruleid: mois-1-04-xss-py
    return make_response(render_template_string("{% autoescape false %}<p>{{ n }}</p>{% endautoescape %}", n=name))
