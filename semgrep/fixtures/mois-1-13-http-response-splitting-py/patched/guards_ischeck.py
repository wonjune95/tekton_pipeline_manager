"""guard 형태별 안전한 예제 — 문자 종류 검사별(isdigit·isdecimal·isalpha·isidentifier)."""
from flask import Flask, make_response, request

app = Flask(__name__)


@app.route("/guard/isdigit")
def guard_isdigit():
    token = request.args.get("token", "")
    if not token.isdigit():
        return "invalid", 400
    resp = make_response("ok")
    # ok: mois-1-13-http-response-splitting-py 숫자만 통과 (실패하면 return)
    resp.headers["X-Token"] = token
    return resp


@app.route("/inside/isdigit")
def inside_isdigit():
    token = request.args.get("token", "")
    if token.isdigit():
        resp = make_response("ok")
        # ok: mois-1-13-http-response-splitting-py 숫자만 통과한 조건 안에서만 사용
        resp.headers["X-Token"] = token
    return "ok"


@app.route("/guard/isdecimal")
def guard_isdecimal():
    token = request.args.get("token", "")
    if not token.isdecimal():
        return "invalid", 400
    resp = make_response("ok")
    # ok: mois-1-13-http-response-splitting-py 10진 숫자만 통과 (실패하면 return)
    resp.headers["X-Token"] = token
    return resp


@app.route("/inside/isdecimal")
def inside_isdecimal():
    token = request.args.get("token", "")
    if token.isdecimal():
        resp = make_response("ok")
        # ok: mois-1-13-http-response-splitting-py 10진 숫자만 통과한 조건 안에서만 사용
        resp.headers["X-Token"] = token
    return "ok"


@app.route("/guard/isalpha")
def guard_isalpha():
    token = request.args.get("token", "")
    if not token.isalpha():
        return "invalid", 400
    resp = make_response("ok")
    # ok: mois-1-13-http-response-splitting-py 글자만 통과 (실패하면 return)
    resp.headers["X-Token"] = token
    return resp


@app.route("/inside/isalpha")
def inside_isalpha():
    token = request.args.get("token", "")
    if token.isalpha():
        resp = make_response("ok")
        # ok: mois-1-13-http-response-splitting-py 글자만 통과한 조건 안에서만 사용
        resp.headers["X-Token"] = token
    return "ok"


@app.route("/guard/isidentifier")
def guard_isidentifier():
    token = request.args.get("token", "")
    if not token.isidentifier():
        return "invalid", 400
    resp = make_response("ok")
    # ok: mois-1-13-http-response-splitting-py 식별자 문자만 통과 (실패하면 return)
    resp.headers["X-Token"] = token
    return resp


@app.route("/inside/isidentifier")
def inside_isidentifier():
    token = request.args.get("token", "")
    if token.isidentifier():
        resp = make_response("ok")
        # ok: mois-1-13-http-response-splitting-py 식별자 문자만 통과한 조건 안에서만 사용
        resp.headers["X-Token"] = token
    return "ok"
