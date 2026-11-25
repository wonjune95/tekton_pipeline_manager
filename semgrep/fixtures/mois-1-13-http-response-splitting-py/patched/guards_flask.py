"""guard 형태별 안전한 예제 (Flask)."""
import re

from flask import Flask, abort, make_response, request

app = Flask(__name__)
TOKEN_RE = re.compile(r"[A-Za-z0-9_.-]{1,64}")


@app.route("/guard/abort")
def guard_abort():
    token = request.args.get("token", "")
    if not re.fullmatch(r"[A-Za-z0-9_.-]{1,64}", token):
        abort(400)
    resp = make_response("ok")
    # ok: mois-1-13-http-response-splitting-py 실패하면 abort
    resp.headers["X-Token"] = token
    return "ok"


@app.route("/guard/abort_empty")
def guard_abort_empty():
    token = request.args.get("token", "")
    if not token or not token.isalnum():
        abort(400)
    resp = make_response("ok")
    # ok: mois-1-13-http-response-splitting-py 값이 없거나 실패하면 abort
    resp.headers["X-Token"] = token
    return "ok"
