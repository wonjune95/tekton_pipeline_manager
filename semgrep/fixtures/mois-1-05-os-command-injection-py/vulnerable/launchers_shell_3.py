"""실행 파일이 고정이어도 "인자를 다시 명령 · 코드로 실행하는 프로그램"이면 탐지되어야 한다 (셸 문자열 3/3).

규칙의 프로그램 목록 한 항목마다 한 줄씩 둔다 — 가지별 변이 시험이 항목 하나를 지우면 그 줄이 빠진다.
한 파일에 줄이 너무 많으면 변이 시험이 "Too many matches" 로 실패하므로 파일을 나눴다.
"""
import os
import shlex

from flask import Flask, request

app = Flask(__name__)


@app.route("/launch/shell3", methods=["POST"])
def launcher_shell_3():
    arg = request.form["arg"]
    # shlex.quote 로 묶은 낱말도 아래 명령은 다시 명령 · 코드로 실행한다 (셸 내장 명령 포함)
    # ruleid: mois-1-05-os-command-injection-py
    os.system("perl " + shlex.quote(arg))
    # ruleid: mois-1-05-os-command-injection-py
    os.system("ruby " + shlex.quote(arg))
    # ruleid: mois-1-05-os-command-injection-py
    os.system("node " + shlex.quote(arg))
    # ruleid: mois-1-05-os-command-injection-py
    os.system("php " + shlex.quote(arg))
    # ruleid: mois-1-05-os-command-injection-py
    os.system("lua " + shlex.quote(arg))
    # ruleid: mois-1-05-os-command-injection-py
    os.system("awk " + shlex.quote(arg))
    # ruleid: mois-1-05-os-command-injection-py
    os.system("gawk " + shlex.quote(arg))
    # ruleid: mois-1-05-os-command-injection-py
    os.system("sed " + shlex.quote(arg))
    # ruleid: mois-1-05-os-command-injection-py
    os.system("find " + shlex.quote(arg))
    # ruleid: mois-1-05-os-command-injection-py
    os.system("parallel " + shlex.quote(arg))
    # ruleid: mois-1-05-os-command-injection-py
    os.system("osascript " + shlex.quote(arg))
    # ruleid: mois-1-05-os-command-injection-py
    os.system("eval " + shlex.quote(arg))
    # ruleid: mois-1-05-os-command-injection-py
    os.system("exec " + shlex.quote(arg))
    # ruleid: mois-1-05-os-command-injection-py
    os.system("command " + shlex.quote(arg))
    # ruleid: mois-1-05-os-command-injection-py
    os.system("source " + shlex.quote(arg))
    # ruleid: mois-1-05-os-command-injection-py
    os.system(". " + shlex.quote(arg))
    # ruleid: mois-1-05-os-command-injection-py
    os.system("trap " + shlex.quote(arg))
    return {"ok": True}
