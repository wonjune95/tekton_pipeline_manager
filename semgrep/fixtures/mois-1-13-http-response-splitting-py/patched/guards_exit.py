"""guard 형태별 안전한 예제 — import 로 확인되는 종료 호출(flask.abort·sys.exit).

내장 exit()·quit() 와 이름만 abort 인 함수는 vulnerable/ 쪽에 있다 (종료로 보지 않는다).
"""
import sys

import flask
from flask import Flask, make_response, request

app = Flask(__name__)


@app.route("/guard/flask_abort")
def guard_flask_abort():
    token = request.args.get("token", "")
    if not token.isalnum():
        flask.abort(400)
    resp = make_response("ok")
    # ok: mois-1-13-http-response-splitting-py 실패하면 flask.abort
    resp.headers["X-Token"] = token
    return resp


def guard_sys_exit():
    # 라우트가 아닌 일괄 작업용 보조 함수 (요청 문맥 안에서 호출된다)
    token = request.args.get("token", "")
    if not token.isalnum():
        sys.exit(2)
    resp = make_response("ok")
    # ok: mois-1-13-http-response-splitting-py 실패하면 sys.exit
    resp.headers["X-Token"] = token
    return resp
