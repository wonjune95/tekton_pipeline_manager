from flask import Flask, render_template_string, request
from jinja2 import Environment, Template

app = Flask(__name__)
renderer = Environment(autoescape=True)


@app.route("/kw/hello")
def hello_by_keyword():
    name = request.args.get("name", "guest")
    # ok: mois-1-02-code-injection-py 원문(source)은 고정이고 입력은 템플릿 변수로만 전달
    first = render_template_string(source="<h1>Hello {{ name }}</h1>", name=name)
    # ok: mois-1-02-code-injection-py
    second = Template(source="Hello {{ name }}", autoescape=True).render(name=name)
    # ok: mois-1-02-code-injection-py from_string 의 globals 는 템플릿 변수 자리다
    third = renderer.from_string(source="Hello {{ name }}", globals={"name": name}).render()
    return {"first": first, "second": second, "third": third}
