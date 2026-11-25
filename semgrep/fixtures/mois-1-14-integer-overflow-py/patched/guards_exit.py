"""guard 형태별 안전한 예제 — import 로 확인되는 종료 호출(flask.abort·sys.exit).

내장 exit()·quit() 와 이름만 abort 인 함수는 vulnerable/ 쪽에 있다 (종료로 보지 않는다).
"""
import sys

import flask
from flask import Flask, request

app = Flask(__name__)
MAX_SIZE = 1024 * 1024


@app.route("/guard/flask_abort")
def guard_flask_abort():
    size = int(request.args.get("size", "0"))
    if size >= MAX_SIZE:
        flask.abort(400)
    # ok: mois-1-14-integer-overflow-py 실패하면 flask.abort
    buf = bytearray(size)
    return bytes(buf)


def guard_sys_exit():
    # 라우트가 아닌 일괄 작업용 보조 함수 (요청 문맥 안에서 호출된다)
    size = int(request.args.get("size", "0"))
    if size >= MAX_SIZE:
        sys.exit(2)
    # ok: mois-1-14-integer-overflow-py 실패하면 sys.exit
    buf = bytearray(size)
    return bytes(buf)
