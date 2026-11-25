import os
import shlex
import subprocess
import sys

import flask
from django.http import HttpResponse, HttpResponseBadRequest
from flask import abort

ALLOWED_HOSTS = ("intra.example.go.kr", "mail.example.go.kr")
ALLOWED_UNITS = frozenset({"nginx", "gunicorn"})
ALLOWED_FORMATS = {"png", "jpg", "webp"}
ALLOWED_ACTIONS = ["start", "stop", "reload"]

app = flask.Flask(__name__)


def quoted(request):
    name = request.GET.get("name", "")
    # ok: mois-1-05-os-command-injection-py shlex.quote 로 셸 인자 하나로 묶음
    os.system("ls -l /srv/data/" + shlex.quote(name))
    return HttpResponse("ok")


def allowlist_guard(request):
    host = request.GET.get("host", "")
    if host not in ALLOWED_HOSTS:
        return HttpResponseBadRequest("unknown host")
    # ok: mois-1-05-os-command-injection-py 목록에 없으면 위에서 빠져나감
    os.system("ping -c 1 " + host)
    return HttpResponse("ok")


def allowlist_guard_raise(request):
    unit = request.POST.get("unit", "")
    if unit not in ALLOWED_UNITS:
        raise ValueError("unknown unit")
    # ok: mois-1-05-os-command-injection-py
    subprocess.run("systemctl status " + unit, shell=True, check=False)
    return HttpResponse("ok")


def inside_positive_branch(request):
    host = request.GET.get("host", "")
    if host in ALLOWED_HOSTS:
        # ok: mois-1-05-os-command-injection-py 허용 목록 조건 안에서만 사용 (else 없음)
        os.system("ping -c 1 " + host)
    return HttpResponse("ok")


def restart_all(request):
    for unit in request.POST.getlist("unit"):
        if unit not in ALLOWED_UNITS:
            continue
        # ok: mois-1-05-os-command-injection-py 목록에 없는 값은 건너뜀
        subprocess.run("systemctl restart " + unit, shell=True, check=False)
    return HttpResponse("ok")


def allowlist_guard_with_empty_check(request):
    host = request.GET.get("host")
    if host is None or host not in ALLOWED_HOSTS:
        return HttpResponseBadRequest("unknown host")
    # ok: mois-1-05-os-command-injection-py 값이 없거나 목록에 없으면 위에서 빠져나감
    os.system("ping -c 1 " + host)
    return HttpResponse("ok")


# ---- (공통 2) 실패 시 중단: 빠져나가는 방법별 ----


def guard_abort(request):
    host = request.args.get("host", "")
    if host not in ALLOWED_HOSTS:
        abort(400)
    # ok: mois-1-05-os-command-injection-py 목록에 없으면 abort 로 중단
    os.system("ping -c 1 " + host)
    return "ok"


def guard_flask_abort(request):
    host = request.args.get("host", "")
    if host not in ALLOWED_HOSTS:
        flask.abort(404)
    # ok: mois-1-05-os-command-injection-py 목록에 없으면 flask.abort 로 중단
    os.system("traceroute " + host)
    return "ok"


def guard_sys_exit():
    # 라우트가 아닌 일괄 작업용 보조 함수 (요청 문맥 안에서 호출된다)
    host = flask.request.args.get("host", "")
    if host not in ALLOWED_HOSTS:
        sys.exit(2)
    # ok: mois-1-05-os-command-injection-py 목록에 없으면 sys.exit 로 종료
    os.system("dig +short " + host)


def guard_not_x_in(request):
    host = request.GET.get("host", "")
    if not host in ALLOWED_HOSTS:
        return HttpResponseBadRequest("unknown host")
    # ok: mois-1-05-os-command-injection-py `not x in 목록` 으로 쓴 같은 검사
    os.system("nslookup " + host)
    return HttpResponse("ok")


# ---- (공통 2) 허용 목록의 리터럴 종류별: set · list (tuple·frozenset 은 위) ----


def guard_set_literal(request):
    fmt = request.GET.get("format", "")
    if fmt not in ALLOWED_FORMATS:
        return HttpResponseBadRequest("unknown format")
    # ok: mois-1-05-os-command-injection-py set 리터럴 허용 목록
    os.system("convert /srv/in/a.bmp /srv/out/a." + fmt)
    return HttpResponse("ok")


def guard_list_literal(request):
    action = request.POST.get("action", "")
    if action not in ALLOWED_ACTIONS:
        return HttpResponseBadRequest("unknown action")
    # ok: mois-1-05-os-command-injection-py list 리터럴 허용 목록
    os.system("systemctl " + action + " nginx")
    return HttpResponse("ok")


# ---- (공통 2) 목록에 없으면 고정된 기본값으로 바꾸는 형태 ----


def default_string_tuple(request):
    host = request.GET.get("host", "")
    if host not in ALLOWED_HOSTS:
        host = "intra.example.go.kr"
    # ok: mois-1-05-os-command-injection-py 목록에 없으면 고정 문자열로 바꿈
    os.system("ping -c 1 " + host)
    return HttpResponse("ok")


def default_none_set(request):
    fmt = request.GET.get("format", "")
    if not fmt in ALLOWED_FORMATS:
        fmt = None
    if fmt is None:
        return HttpResponseBadRequest("unknown format")
    # ok: mois-1-05-os-command-injection-py 목록에 없으면 None 으로 바꾸고, None 이면 실행하지 않음
    os.system("convert /srv/in/b.bmp /srv/out/b." + fmt)
    return HttpResponse("ok")


def default_string_list(request):
    action = request.POST.get("action", "")
    if action not in ALLOWED_ACTIONS:
        action = "reload"
    # ok: mois-1-05-os-command-injection-py list 리터럴 허용 목록 + 고정 기본값
    os.system("systemctl " + action + " gunicorn")
    return HttpResponse("ok")


def default_string_frozenset(request):
    unit = request.POST.get("unit", "")
    if unit not in ALLOWED_UNITS:
        unit = "nginx"
    # ok: mois-1-05-os-command-injection-py frozenset 허용 목록 + 고정 기본값
    os.system("systemctl is-active " + unit)
    return HttpResponse("ok")


# ---- (공통 3) 조건 안에서만 사용: 허용 목록의 리터럴 종류별 (tuple 은 위) ----


def inside_positive_branch_set(request):
    fmt = request.GET.get("format", "")
    if fmt in ALLOWED_FORMATS:
        # ok: mois-1-05-os-command-injection-py set 리터럴 허용 목록 조건 안
        os.system("convert /srv/in/c.bmp /srv/out/c." + fmt)
    return HttpResponse("ok")


def inside_positive_branch_list(request):
    action = request.POST.get("action", "")
    if action in ALLOWED_ACTIONS:
        # ok: mois-1-05-os-command-injection-py list 리터럴 허용 목록 조건 안
        os.system("systemctl " + action + " celery")
    return HttpResponse("ok")


def inside_positive_branch_frozenset(request):
    unit = request.POST.get("unit", "")
    if unit in ALLOWED_UNITS:
        # ok: mois-1-05-os-command-injection-py frozenset 허용 목록 조건 안
        os.system("journalctl -n 20 -u " + unit)
    return HttpResponse("ok")


# ================= 공통 sanitizer 의 가지별 예제 =================
# (공통 1) 리터럴 dict — 작은따옴표 키, 작은따옴표 값, 숫자 값
TOOL_PATHS = {'convert': "/opt/tools/convert", 'resize': "/opt/tools/resize"}
UNIT_NAMES = {"web": 'nginx.service', "app": 'gunicorn.service'}
NICE_LEVELS = {"low": 10, "high": -5}
# (공통 2-가 · 3) 이름 붙은 목록 — set([...]), 작은따옴표, 숫자
ALLOWED_SIGNALS = set(["HUP", "TERM"])
ALLOWED_MODES = ['fast', 'slow']
ALLOWED_COUNTS = (1, 3, 5)


def dict_single_quoted_key(request):
    # ok: mois-1-05-os-command-injection-py 문자열만 든 dict 에서 꺼낸 값
    subprocess.run(TOOL_PATHS[request.GET.get("tool", "")] + " in.png out.png", shell=True, check=False)
    return HttpResponse("ok")


def dict_single_quoted_value(request):
    # ok: mois-1-05-os-command-injection-py
    os.system("systemctl status " + UNIT_NAMES.get(request.GET.get("unit", "")))
    return HttpResponse("ok")


def dict_number_value(request):
    # ok: mois-1-05-os-command-injection-py 숫자 값만 든 dict
    os.system("nice -n %d /opt/batch/run.sh" % NICE_LEVELS[request.GET.get("priority", "")])
    return HttpResponse("ok")


def named_set_call(request):
    sig = request.GET.get("signal", "")
    if sig not in ALLOWED_SIGNALS:
        return HttpResponseBadRequest("unsupported signal")
    # ok: mois-1-05-os-command-injection-py set([...]) 로 만든 목록
    os.system("systemctl kill -s " + sig + " nginx")
    return HttpResponse("ok")


def named_single_quoted(request):
    mode = request.GET.get("mode", "")
    if mode not in ALLOWED_MODES:
        return HttpResponseBadRequest("unsupported mode")
    # ok: mois-1-05-os-command-injection-py
    os.system("/opt/batch/run.sh --mode " + mode)
    return HttpResponse("ok")


@app.route("/ping", methods=["POST"])
def named_numbers():
    count = flask.request.json.get("count")
    if count not in ALLOWED_COUNTS:
        abort(400)
    # ok: mois-1-05-os-command-injection-py 숫자만 든 목록
    os.system("ping -c %s intra.example.go.kr" % count)
    return "ok"


def positive_named_set_call(request):
    sig = request.GET.get("signal", "")
    if sig in ALLOWED_SIGNALS:
        # ok: mois-1-05-os-command-injection-py
        os.system("systemctl kill -s " + sig + " nginx")
    return HttpResponse("ok")


def positive_named_single_quoted(request):
    mode = request.GET.get("mode", "")
    if mode in ALLOWED_MODES:
        # ok: mois-1-05-os-command-injection-py
        os.system("/opt/batch/run.sh --mode " + mode)
    return HttpResponse("ok")


@app.route("/ping2", methods=["POST"])
def positive_named_numbers():
    count = flask.request.json.get("count")
    if count in ALLOWED_COUNTS:
        # ok: mois-1-05-os-command-injection-py
        os.system("ping -c %s intra.example.go.kr" % count)
    return "ok"


# ---- (공통 2-나) 조건에 바로 적은 목록: 빠져나가는 방법마다 ----
def inline_raise(request):
    fmt = request.GET.get("format", "")
    if fmt not in ("png", "jpg"):
        raise ValueError("unsupported format")
    # ok: mois-1-05-os-command-injection-py
    os.system("convert in.dat out." + fmt)
    return HttpResponse("ok")


def inline_continue(request):
    for fmt in request.GET.getlist("format"):
        if fmt not in ("png", "jpg"):
            continue
        # ok: mois-1-05-os-command-injection-py
        os.system("convert in.dat out." + fmt)
    return HttpResponse("ok")


@app.route("/convert/a")
def inline_abort():
    fmt = flask.request.args.get("format", "")
    if fmt not in ("png", "jpg"):
        abort(400)
    # ok: mois-1-05-os-command-injection-py
    os.system("convert in.dat out." + fmt)
    return "ok"


@app.route("/convert/b")
def inline_flask_abort():
    fmt = flask.request.args.get("format", "")
    if fmt not in ("png", "jpg"):
        flask.abort(400)
    # ok: mois-1-05-os-command-injection-py
    os.system("convert in.dat out." + fmt)
    return "ok"


def inline_sys_exit():
    # 라우트가 아닌 일괄 작업용 보조 함수 (요청 문맥 안에서 호출된다)
    fmt = flask.request.args.get("format", "")
    if fmt not in ("png", "jpg"):
        sys.exit(2)
    # ok: mois-1-05-os-command-injection-py
    os.system("convert in.dat out." + fmt)


def inline_default_none(request):
    fmt = request.GET.get("format", "")
    if fmt not in ("png", "jpg"):
        fmt = None
    # ok: mois-1-05-os-command-injection-py 목록에 없으면 None 으로 바꿨다
    os.system("convert in.dat out.%s" % (fmt or "png"))
    return HttpResponse("ok")


def inline_not_x_in(request):
    fmt = request.GET.get("format", "")
    if not fmt in ("png", "jpg"):
        return HttpResponseBadRequest("unsupported format")
    # ok: mois-1-05-os-command-injection-py
    os.system("convert in.dat out." + fmt)
    return HttpResponse("ok")


def inline_single_quoted(request):
    fmt = request.GET.get("format", "")
    if fmt not in ['png', 'jpg']:
        return HttpResponseBadRequest("unsupported format")
    # ok: mois-1-05-os-command-injection-py
    os.system("convert in.dat out." + fmt)
    return HttpResponse("ok")


@app.route("/ping3", methods=["POST"])
def inline_numbers():
    count = flask.request.json.get("count")
    if count not in (1, 3, 5):
        abort(400)
    # ok: mois-1-05-os-command-injection-py
    os.system("ping -c %s intra.example.go.kr" % count)
    return "ok"


# ---- (공통 3) 조건에 바로 적은 목록 안에서만 사용 ----
def positive_inline_single_quoted(request):
    fmt = request.GET.get("format", "")
    if fmt in ('png', 'jpg'):
        # ok: mois-1-05-os-command-injection-py
        os.system("convert in.dat out." + fmt)
    return HttpResponse("ok")


@app.route("/ping4", methods=["POST"])
def positive_inline_numbers():
    count = flask.request.json.get("count")
    if count in [1, 3, 5]:
        # ok: mois-1-05-os-command-injection-py
        os.system("ping -c %s intra.example.go.kr" % count)
    return "ok"


def inline_not_x_in_single_quoted(request):
    fmt = request.GET.get("format", "")
    if not fmt in ('png', 'jpg'):
        return HttpResponseBadRequest("unsupported format")
    # ok: mois-1-05-os-command-injection-py 작은따옴표 목록
    os.system("convert in.dat out." + fmt)
    return HttpResponse("ok")


@app.route("/ping5", methods=["POST"])
def inline_not_x_in_numbers():
    count = flask.request.json.get("count")
    if not count in (1, 3, 5):
        abort(400)
    # ok: mois-1-05-os-command-injection-py 숫자 목록
    os.system("ping -c %s intra.example.go.kr" % count)
    return "ok"
