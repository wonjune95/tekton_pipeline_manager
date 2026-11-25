from flask import Flask, request

app = Flask(__name__)


@app.route("/greet")
def greet():
    name = request.args.get("name", "")
    # Flask 는 반환한 문자열을 text/html 로 응답
    # ruleid: mois-1-04-xss-py
    return f"<h1>안녕하세요 {name}</h1>"
