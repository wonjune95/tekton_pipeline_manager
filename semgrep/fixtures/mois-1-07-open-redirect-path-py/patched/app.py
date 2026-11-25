"""요청 경로를 쓰지만 주소의 맨 앞은 url_for 가 만든다 (Flask)."""
from flask import Flask, redirect, request, url_for

app = Flask(__name__)


@app.route("/members")
def members():
    # ok: mois-1-07-open-redirect-path-py url_for 의 인자(질의 문자열)로만 들어간다
    return redirect(url_for("auth.login", next=request.full_path))


@app.route("/members2")
def members2():
    # ok: mois-1-07-open-redirect-path-py url_for 로 만든 경로 뒤에 "?next=" 리터럴을 두고 붙인다
    return redirect(url_for("auth.login") + "?next=" + request.path)
