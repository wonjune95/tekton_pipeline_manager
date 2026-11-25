"""응답 객체를 변수에 받아 헤더만 고친 뒤 반환 — 본문은 고정이므로 XSS 가 아니다 (헤더 값은 개행을 지워 응답분할도 아님)."""
import flask
from flask import Flask, jsonify, make_response, redirect, request

app = Flask(__name__)


@app.route("/r/make")
def via_make_response():
    resp = make_response("ok")
    resp.headers["X-Trace"] = request.args.get("trace", "").replace("\r", "").replace("\n", "")
    # ok: mois-1-04-xss-py 응답 객체를 변수로 반환
    return resp


@app.route("/r/response")
def via_response():
    resp = flask.Response("ok", mimetype="text/plain")
    resp.headers["Content-Language"] = request.args.get("lang", "ko").replace("\r", "").replace("\n", "")
    # ok: mois-1-04-xss-py
    return resp


@app.route("/r/json")
def via_jsonify():
    resp = jsonify(status="ok")
    resp.headers["X-Trace"] = request.args.get("trace", "").replace("\r", "").replace("\n", "")
    # ok: mois-1-04-xss-py
    return resp


@app.route("/r/redirect")
def via_redirect():
    resp = redirect("/home")
    resp.headers["X-From"] = request.args.get("from", "").replace("\r", "").replace("\n", "")
    # ok: mois-1-04-xss-py
    return resp


@app.route("/r/wrapped-redirect")
def wrapped_redirect():
    # ok: mois-1-04-xss-py 리다이렉트 응답을 make_response 로 감쌌을 뿐 (본문 없음)
    resp = make_response(redirect("/search?q=" + request.args.get("q", "")))
    return resp


@app.route("/r/wrapped-json")
def wrapped_json():
    # ok: mois-1-04-xss-py JSON 응답을 감쌌을 뿐
    return make_response(jsonify(q=request.args.get("q", "")))
