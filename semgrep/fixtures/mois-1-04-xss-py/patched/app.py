from flask import Flask, request
from markupsafe import escape

app = Flask(__name__)


@app.route("/greet")
def greet():
    name = request.args.get("name", "")
    # ok: mois-1-04-xss-py markupsafe.escape 로 이스케이프
    return f"<h1>안녕하세요 {escape(name)}</h1>"
