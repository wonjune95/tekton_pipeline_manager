"""guard 형태별 안전한 예제 (Flask)."""
import os
import sys

from pathlib import Path

import flask
from flask import Flask, abort, request

app = Flask(__name__)
MEDIA_DIR = "/srv/media"
BASE = Path("/srv/media")


@app.route("/guard/abort")
def guard_abort():
    name = request.args.get("name", "")
    target = os.path.realpath(os.path.join(MEDIA_DIR, name))
    if not target.startswith(MEDIA_DIR + os.sep):
        abort(400)
    # ok: mois-1-03-path-traversal-py 실패하면 abort
    os.remove(target)
    return "ok"


@app.route("/guard/abort_empty")
def guard_abort_empty():
    name = request.args.get("name", "")
    target = os.path.realpath(os.path.join(MEDIA_DIR, name))
    if name.startswith(".") or os.path.commonpath([target, MEDIA_DIR]) != MEDIA_DIR:
        abort(400)
    # ok: mois-1-03-path-traversal-py 값이 없거나 실패하면 abort
    os.remove(target)
    return "ok"


@app.route("/guard/flask_abort")
def guard_flask_abort():
    target = os.path.realpath(os.path.join(MEDIA_DIR, request.args.get("name", "")))
    if not target.startswith(MEDIA_DIR + os.sep):
        flask.abort(404)
    # ok: mois-1-03-path-traversal-py 실패하면 flask.abort
    os.remove(target)
    return "ok"


def cleanup_job_sys_exit():
    # 라우트가 아닌 일괄 작업용 보조 함수 (요청 문맥 안에서 호출된다)
    target = os.path.realpath(os.path.join(MEDIA_DIR, request.args.get("name", "")))
    if not target.startswith(MEDIA_DIR + os.sep):
        sys.exit(2)
    # ok: mois-1-03-path-traversal-py 실패하면 sys.exit
    os.remove(target)


@app.route("/guard/relative_to")
def relative_to_except_aborts():
    target = (BASE / request.args.get("name", "")).resolve()
    try:
        target.relative_to(BASE)
    except ValueError:
        abort(404)
    # ok: mois-1-03-path-traversal-py 기준 밖이면 except 에서 flask.abort 로 끝난다
    os.remove(target)
    return "ok"
