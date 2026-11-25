"""빠져나가는 것처럼 보이지만 끝난다고 확인할 수 없는 호출 — 모두 탐지되어야 한다."""
import os

from flask import request

MEDIA_DIR = "/srv/media"


def abort(code):
    # 이름만 abort 인 함수: 기록만 하고 돌아온다
    print("abort requested", code)


def fake_abort():
    target = os.path.realpath(os.path.join(MEDIA_DIR, request.args.get("name", "")))
    if not target.startswith(MEDIA_DIR + os.sep):
        abort(400)
    # flask.abort 가 아니라 이 파일의 abort — 실패해도 계속 진행한다
    # ruleid: mois-1-03-path-traversal-py
    os.remove(target)


def builtin_exit():
    target = os.path.realpath(os.path.join(MEDIA_DIR, request.args.get("name", "")))
    if not target.startswith(MEDIA_DIR + os.sep):
        exit(2)
    # 내장 exit() 는 site 모듈이 넣어 주는 대화형 도우미라 없을 수도, 다른 함수로 가려질 수도 있다 (sys.exit 만 인정)
    # ruleid: mois-1-03-path-traversal-py
    os.remove(target)


def builtin_quit():
    target = os.path.realpath(os.path.join(MEDIA_DIR, request.args.get("name", "")))
    if not target.startswith(MEDIA_DIR + os.sep):
        quit()
    # 내장 quit() 도 같다
    # ruleid: mois-1-03-path-traversal-py
    os.remove(target)
