from flask import Flask, render_template_string, request

app = Flask(__name__)


@app.route("/hello")
def hello():
    name = request.args.get("name", "guest")
    # ok: mois-1-02-code-injection-py 템플릿은 고정하고 입력은 변수로 전달 (자동 이스케이프)
    return render_template_string("<h1>Hello {{ name }}</h1>", name=name)
