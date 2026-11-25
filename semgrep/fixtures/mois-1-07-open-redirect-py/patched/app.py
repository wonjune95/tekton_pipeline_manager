import flask
from flask import Flask, redirect, request, url_for

app = Flask(__name__)


@app.route("/posts/<post_id>/done")
def done(post_id):
    # ok: mois-1-07-open-redirect-py url_for 로 만든 내부 주소
    return redirect(url_for("post_detail", post_id=post_id, tab=request.args.get("tab", "")))


@app.route("/search-redirect")
def search_redirect():
    q = request.args.get("q", "")
    # ok: mois-1-07-open-redirect-py — 프레임워크가 만든 경로 뒤에 "?q=" 리터럴을 두고 질의 값을 붙인다
    return redirect(url_for("search") + "?q=" + q)


@app.route("/search-redirect2")
def search_redirect2():
    # ok: mois-1-07-open-redirect-py — flask.url_for(...) 로 쓴 경우도 같다
    return flask.redirect(flask.url_for("search") + "?q=" + flask.request.args.get("q", ""))


@app.route("/search-redirect3")
def search_redirect3():
    q = request.args.get("q", "")
    page = request.args.get("page", "1")
    # ok: mois-1-07-open-redirect-py — 인자에 괄호가 든 호출, 리터럴이 f-string 인 경우
    return redirect(url_for("search", page=int(page)) + f"?q={q}")
