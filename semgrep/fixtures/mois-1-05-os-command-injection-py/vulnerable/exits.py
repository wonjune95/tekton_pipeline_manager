"""끝내는 것처럼 보이지만 끝난다고 확인할 수 없는 호출 — 모두 탐지되어야 한다.

종료 함수는 import 로 확인되는 flask.abort · sys.exit 만 인정한다.
이 파일의 abort 는 직접 만든 함수이고, 내장 exit()/quit() 은 다른 정의로 가려질 수 있다.
"""
import logging
import os

import flask

ALLOWED_HOSTS = ("intra.example.go.kr", "mail.example.go.kr")
log = logging.getLogger(__name__)


def abort(code):
    # 기록만 하고 돌아온다 — 요청 처리는 계속된다
    log.warning("rejected with %s", code)


def named_fake_abort():
    host = flask.request.args.get("host", "")
    if host not in ALLOWED_HOSTS:
        abort(400)
    # ruleid: mois-1-05-os-command-injection-py
    os.system("traceroute " + host)


def named_builtin_exit():
    host = flask.request.args.get("host", "")
    if host not in ALLOWED_HOSTS:
        exit(2)
    # ruleid: mois-1-05-os-command-injection-py
    os.system("host " + host)


def named_builtin_quit():
    host = flask.request.args.get("host", "")
    if host not in ALLOWED_HOSTS:
        quit()
    # ruleid: mois-1-05-os-command-injection-py
    os.system("whois " + host)


def inline_fake_abort():
    fmt = flask.request.args.get("format", "")
    if fmt not in ("png", "jpg"):
        abort(400)
    # ruleid: mois-1-05-os-command-injection-py
    os.system("convert in.dat out." + fmt)


def inline_builtin_exit():
    fmt = flask.request.args.get("format", "")
    if fmt not in ("png", "jpg"):
        exit(2)
    # ruleid: mois-1-05-os-command-injection-py
    os.system("convert in.dat out." + fmt)
