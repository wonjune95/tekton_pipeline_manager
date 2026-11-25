from flask import Flask, render_template_string, request

app = Flask(__name__)


@app.route("/hello")
def hello():
    name = request.args.get("name", "guest")
    # 외부 입력을 템플릿 원문에 이어 붙임 (SSTI)
    # ruleid: mois-1-02-code-injection-py
    return render_template_string("<h1>Hello " + name + "</h1>")
