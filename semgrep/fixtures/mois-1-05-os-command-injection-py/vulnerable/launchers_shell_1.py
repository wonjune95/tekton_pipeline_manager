"""실행 파일이 고정이어도 "인자를 다시 명령 · 코드로 실행하는 프로그램"이면 탐지되어야 한다 (셸 문자열 1/3).

규칙의 프로그램 목록 한 항목마다 한 줄씩 둔다 — 가지별 변이 시험이 항목 하나를 지우면 그 줄이 빠진다.
한 파일에 줄이 너무 많으면 변이 시험이 "Too many matches" 로 실패하므로 파일을 나눴다.
"""
import os
import shlex

from flask import Flask, request

app = Flask(__name__)


@app.route("/launch/shell1", methods=["POST"])
def launcher_shell_1():
    arg = request.form["arg"]
    # shlex.quote 로 묶은 낱말도 아래 명령은 다시 명령 · 코드로 실행한다 (셸 내장 명령 포함)
    # ruleid: mois-1-05-os-command-injection-py
    os.system("sh " + shlex.quote(arg))
    # ruleid: mois-1-05-os-command-injection-py
    os.system("bash " + shlex.quote(arg))
    # ruleid: mois-1-05-os-command-injection-py
    os.system("dash " + shlex.quote(arg))
    # ruleid: mois-1-05-os-command-injection-py
    os.system("zsh " + shlex.quote(arg))
    # ruleid: mois-1-05-os-command-injection-py
    os.system("ksh " + shlex.quote(arg))
    # ruleid: mois-1-05-os-command-injection-py
    os.system("csh " + shlex.quote(arg))
    # ruleid: mois-1-05-os-command-injection-py
    os.system("tcsh " + shlex.quote(arg))
    # ruleid: mois-1-05-os-command-injection-py
    os.system("fish " + shlex.quote(arg))
    # ruleid: mois-1-05-os-command-injection-py
    os.system("ash " + shlex.quote(arg))
    # ruleid: mois-1-05-os-command-injection-py
    os.system("busybox " + shlex.quote(arg))
    # ruleid: mois-1-05-os-command-injection-py
    os.system("cmd " + shlex.quote(arg))
    # ruleid: mois-1-05-os-command-injection-py
    os.system("powershell " + shlex.quote(arg))
    # ruleid: mois-1-05-os-command-injection-py
    os.system("pwsh " + shlex.quote(arg))
    # ruleid: mois-1-05-os-command-injection-py
    os.system("env " + shlex.quote(arg))
    # ruleid: mois-1-05-os-command-injection-py
    os.system("sudo " + shlex.quote(arg))
    # ruleid: mois-1-05-os-command-injection-py
    os.system("su " + shlex.quote(arg))
    # ruleid: mois-1-05-os-command-injection-py
    os.system("doas " + shlex.quote(arg))
    # ruleid: mois-1-05-os-command-injection-py
    os.system("runuser " + shlex.quote(arg))
    return {"ok": True}
