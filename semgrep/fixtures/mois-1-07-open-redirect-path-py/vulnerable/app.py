"""요청의 "경로" 값으로 만든 리다이렉트 (Flask)."""
import flask
from flask import Flask, redirect, request

app = Flask(__name__)


@app.route("/same-page")
def same_page():
    # ruleid: mois-1-07-open-redirect-path-py
    return redirect(request.path)


@app.route("/same-page-query")
def same_page_query():
    # 경로와 질의 문자열
    # ruleid: mois-1-07-open-redirect-path-py
    return redirect(request.full_path)


@app.route("/reload")
def reload_page():
    # `import flask` 뒤 flask.request 로 쓴 요청
    # ruleid: mois-1-07-open-redirect-path-py
    return flask.redirect(flask.request.path)
