"""호스트가 비었는지만 보는 검사 — 검증으로 인정하지 않는다. 모두 탐지되어야 한다.

urlsplit(x).netloc == "" 은 "주소에 호스트가 없다"는 뜻이 아니다.
  "///evil.example/x"  → netloc 은 "" 이지만 브라우저는 //evil.example/x 로 읽어 다른 호스트로 간다
  "\\\\evil.example"   → 역슬래시를 urlsplit 은 경로로 보지만 브라우저는 / 로 바꿔 읽는다
Django 의 url_has_allowed_host_and_scheme 는 이 두 경우를 따로 거부한다 (/// 로 시작하면 거부, 역슬래시를 / 로 바꿔 한 번 더 검사).
"""
from urllib.parse import urlparse, urlsplit

from flask import Flask, redirect, request, url_for
from werkzeug.urls import url_parse

app = Flask(__name__)


@app.route("/login-next")
def login_next():
    next_page = request.args.get("next")
    if not next_page or urlsplit(next_page).netloc != "":
        next_page = url_for("index")
    # next=///evil.example 은 netloc 이 비어 있어 그대로 남는다
    # ruleid: mois-1-07-open-redirect-py
    return redirect(next_page)


@app.route("/login-next2")
def login_next2():
    target = request.args.get("next", "")
    if urlparse(target).netloc != "":
        return redirect(url_for("index"))
    # ruleid: mois-1-07-open-redirect-py
    return redirect(target)


@app.route("/login-next3")
def login_next3():
    target = request.args.get("next", "")
    if url_parse(target).netloc != "":
        return redirect(url_for("index"))
    # ruleid: mois-1-07-open-redirect-py
    return redirect(target)


@app.route("/login-next4")
def login_next4():
    target = request.args.get("next", "")
    if urlsplit(target).netloc != "":
        return redirect(url_for("index"))
    # ruleid: mois-1-07-open-redirect-py
    return redirect(target)


@app.route("/logout-next")
def logout_next():
    target = request.args.get("next", "")
    if urlparse(target).netloc != "":
        target = "/"
    # ruleid: mois-1-07-open-redirect-py
    return redirect(target)


@app.route("/logout-next2")
def logout_next2():
    target = request.args.get("next", "")
    if url_parse(target).netloc != "":
        target = url_for("index")
    # ruleid: mois-1-07-open-redirect-py
    return redirect(target)


@app.route("/logout-next3")
def logout_next3():
    target = request.args.get("next", "")
    if urlsplit(target).netloc == "":
        # 조건 안에서만 써도 마찬가지다
        # ruleid: mois-1-07-open-redirect-py
        return redirect(target)
    return redirect(url_for("index"))
