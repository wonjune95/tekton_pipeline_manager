"""실행 파일이 고정이어도 "인자를 다시 명령 · 코드로 실행하는 프로그램"이면 탐지되어야 한다 (인자 목록 1/2).

규칙의 프로그램 목록 한 항목마다 한 줄씩 둔다 — 가지별 변이 시험이 항목 하나를 지우면 그 줄이 빠진다.
한 파일에 줄이 너무 많으면 변이 시험이 "Too many matches" 로 실패하므로 파일을 나눴다.
"""
import subprocess

from flask import Flask, request

app = Flask(__name__)


@app.route("/launch/argv1", methods=["POST"])
def launcher_argv_1():
    arg = request.form["arg"]
    # 인자 목록의 첫 원소가 아래 프로그램이면 뒤의 인자를 명령 · 코드 · 실행할 프로그램으로 받는다
    # ruleid: mois-1-05-os-command-injection-py
    subprocess.run(["sh", arg])
    # ruleid: mois-1-05-os-command-injection-py
    subprocess.run(["bash", arg])
    # ruleid: mois-1-05-os-command-injection-py
    subprocess.run(["dash", arg])
    # ruleid: mois-1-05-os-command-injection-py
    subprocess.run(["zsh", arg])
    # ruleid: mois-1-05-os-command-injection-py
    subprocess.run(["ksh", arg])
    # ruleid: mois-1-05-os-command-injection-py
    subprocess.run(["csh", arg])
    # ruleid: mois-1-05-os-command-injection-py
    subprocess.run(["tcsh", arg])
    # ruleid: mois-1-05-os-command-injection-py
    subprocess.run(["fish", arg])
    # ruleid: mois-1-05-os-command-injection-py
    subprocess.run(["ash", arg])
    # ruleid: mois-1-05-os-command-injection-py
    subprocess.run(["busybox", arg])
    # ruleid: mois-1-05-os-command-injection-py
    subprocess.run(["cmd", arg])
    # ruleid: mois-1-05-os-command-injection-py
    subprocess.run(["powershell", arg])
    # ruleid: mois-1-05-os-command-injection-py
    subprocess.run(["pwsh", arg])
    # ruleid: mois-1-05-os-command-injection-py
    subprocess.run(["env", arg])
    # ruleid: mois-1-05-os-command-injection-py
    subprocess.run(["sudo", arg])
    # ruleid: mois-1-05-os-command-injection-py
    subprocess.run(["su", arg])
    # ruleid: mois-1-05-os-command-injection-py
    subprocess.run(["doas", arg])
    # ruleid: mois-1-05-os-command-injection-py
    subprocess.run(["runuser", arg])
    # ruleid: mois-1-05-os-command-injection-py
    subprocess.run(["nohup", arg])
    # ruleid: mois-1-05-os-command-injection-py
    subprocess.run(["nice", arg])
    # ruleid: mois-1-05-os-command-injection-py
    subprocess.run(["timeout", arg])
    # ruleid: mois-1-05-os-command-injection-py
    subprocess.run(["time", arg])
    # ruleid: mois-1-05-os-command-injection-py
    subprocess.run(["xargs", arg])
    # ruleid: mois-1-05-os-command-injection-py
    subprocess.run(["watch", arg])
    return {"ok": True}
