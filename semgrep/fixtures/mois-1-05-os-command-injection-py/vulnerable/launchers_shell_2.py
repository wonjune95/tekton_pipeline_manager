"""실행 파일이 고정이어도 "인자를 다시 명령 · 코드로 실행하는 프로그램"이면 탐지되어야 한다 (셸 문자열 2/3).

규칙의 프로그램 목록 한 항목마다 한 줄씩 둔다 — 가지별 변이 시험이 항목 하나를 지우면 그 줄이 빠진다.
한 파일에 줄이 너무 많으면 변이 시험이 "Too many matches" 로 실패하므로 파일을 나눴다.
"""
import os
import shlex

from flask import Flask, request

app = Flask(__name__)


@app.route("/launch/shell2", methods=["POST"])
def launcher_shell_2():
    arg = request.form["arg"]
    # shlex.quote 로 묶은 낱말도 아래 명령은 다시 명령 · 코드로 실행한다 (셸 내장 명령 포함)
    # ruleid: mois-1-05-os-command-injection-py
    os.system("nohup " + shlex.quote(arg))
    # ruleid: mois-1-05-os-command-injection-py
    os.system("nice " + shlex.quote(arg))
    # ruleid: mois-1-05-os-command-injection-py
    os.system("timeout " + shlex.quote(arg))
    # ruleid: mois-1-05-os-command-injection-py
    os.system("time " + shlex.quote(arg))
    # ruleid: mois-1-05-os-command-injection-py
    os.system("xargs " + shlex.quote(arg))
    # ruleid: mois-1-05-os-command-injection-py
    os.system("watch " + shlex.quote(arg))
    # ruleid: mois-1-05-os-command-injection-py
    os.system("setsid " + shlex.quote(arg))
    # ruleid: mois-1-05-os-command-injection-py
    os.system("chroot " + shlex.quote(arg))
    # ruleid: mois-1-05-os-command-injection-py
    os.system("flock " + shlex.quote(arg))
    # ruleid: mois-1-05-os-command-injection-py
    os.system("stdbuf " + shlex.quote(arg))
    # ruleid: mois-1-05-os-command-injection-py
    os.system("strace " + shlex.quote(arg))
    # ruleid: mois-1-05-os-command-injection-py
    os.system("ssh " + shlex.quote(arg))
    # ruleid: mois-1-05-os-command-injection-py
    os.system("sshpass " + shlex.quote(arg))
    # ruleid: mois-1-05-os-command-injection-py
    os.system("docker " + shlex.quote(arg))
    # ruleid: mois-1-05-os-command-injection-py
    os.system("podman " + shlex.quote(arg))
    # ruleid: mois-1-05-os-command-injection-py
    os.system("kubectl " + shlex.quote(arg))
    # ruleid: mois-1-05-os-command-injection-py
    os.system("nsenter " + shlex.quote(arg))
    # ruleid: mois-1-05-os-command-injection-py
    os.system("python3 " + shlex.quote(arg))
    return {"ok": True}
