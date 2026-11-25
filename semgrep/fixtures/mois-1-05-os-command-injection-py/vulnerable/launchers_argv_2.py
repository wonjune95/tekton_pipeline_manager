"""실행 파일이 고정이어도 "인자를 다시 명령 · 코드로 실행하는 프로그램"이면 탐지되어야 한다 (인자 목록 2/2).

규칙의 프로그램 목록 한 항목마다 한 줄씩 둔다 — 가지별 변이 시험이 항목 하나를 지우면 그 줄이 빠진다.
한 파일에 줄이 너무 많으면 변이 시험이 "Too many matches" 로 실패하므로 파일을 나눴다.
"""
import subprocess

from flask import Flask, request

app = Flask(__name__)


@app.route("/launch/argv2", methods=["POST"])
def launcher_argv_2():
    arg = request.form["arg"]
    # 인자 목록의 첫 원소가 아래 프로그램이면 뒤의 인자를 명령 · 코드 · 실행할 프로그램으로 받는다
    # ruleid: mois-1-05-os-command-injection-py
    subprocess.run(["setsid", arg])
    # ruleid: mois-1-05-os-command-injection-py
    subprocess.run(["chroot", arg])
    # ruleid: mois-1-05-os-command-injection-py
    subprocess.run(["flock", arg])
    # ruleid: mois-1-05-os-command-injection-py
    subprocess.run(["stdbuf", arg])
    # ruleid: mois-1-05-os-command-injection-py
    subprocess.run(["strace", arg])
    # ruleid: mois-1-05-os-command-injection-py
    subprocess.run(["ssh", arg])
    # ruleid: mois-1-05-os-command-injection-py
    subprocess.run(["sshpass", arg])
    # ruleid: mois-1-05-os-command-injection-py
    subprocess.run(["docker", arg])
    # ruleid: mois-1-05-os-command-injection-py
    subprocess.run(["podman", arg])
    # ruleid: mois-1-05-os-command-injection-py
    subprocess.run(["kubectl", arg])
    # ruleid: mois-1-05-os-command-injection-py
    subprocess.run(["nsenter", arg])
    # ruleid: mois-1-05-os-command-injection-py
    subprocess.run(["python3", arg])
    # ruleid: mois-1-05-os-command-injection-py
    subprocess.run(["perl", arg])
    # ruleid: mois-1-05-os-command-injection-py
    subprocess.run(["ruby", arg])
    # ruleid: mois-1-05-os-command-injection-py
    subprocess.run(["node", arg])
    # ruleid: mois-1-05-os-command-injection-py
    subprocess.run(["php", arg])
    # ruleid: mois-1-05-os-command-injection-py
    subprocess.run(["lua", arg])
    # ruleid: mois-1-05-os-command-injection-py
    subprocess.run(["awk", arg])
    # ruleid: mois-1-05-os-command-injection-py
    subprocess.run(["gawk", arg])
    # ruleid: mois-1-05-os-command-injection-py
    subprocess.run(["sed", arg])
    # ruleid: mois-1-05-os-command-injection-py
    subprocess.run(["find", arg])
    # ruleid: mois-1-05-os-command-injection-py
    subprocess.run(["parallel", arg])
    # ruleid: mois-1-05-os-command-injection-py
    subprocess.run(["osascript", arg])
    return {"ok": True}
