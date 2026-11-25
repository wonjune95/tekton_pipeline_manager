"""명령 인자의 여러 모양 — 리스트 리터럴이 아니거나, 고정된 실행 파일이 인자를 다시 실행하는 경우."""
import asyncio
import os
import pty
import shlex
import subprocess

from flask import Flask, request

app = Flask(__name__)


@app.route("/shape/variable", methods=["POST"])
def list_in_variable():
    x = request.form["x"]
    cmd = ["sh", "-c", x]
    # 변수에 담은 목록은 모양을 알 수 없으므로 통째로 본다
    # ruleid: mois-1-05-os-command-injection-py
    subprocess.run(cmd)
    exe = [x, "--version"]
    # ruleid: mois-1-05-os-command-injection-py
    subprocess.check_call(exe)
    return {"ok": True}


@app.route("/shape/built", methods=["POST"])
def list_built_later():
    x = request.form["x"]
    a = ["sh", "-c"]
    a.append(x)
    # 나중에 append 한 값
    # ruleid: mois-1-05-os-command-injection-py
    subprocess.run(a)
    b = ["sh", "-c"]
    b.extend([x])
    # ruleid: mois-1-05-os-command-injection-py
    subprocess.run(b)
    c = ["--version"]
    c.insert(0, x)
    # ruleid: mois-1-05-os-command-injection-py
    subprocess.run(c)
    return {"ok": True}


@app.route("/shape/expression", methods=["POST"])
def not_a_list_literal():
    x = request.form["x"]
    # 입력을 나눈 목록: 첫 낱말이 실행 파일이 된다
    # ruleid: mois-1-05-os-command-injection-py
    subprocess.run(x.split())
    # ruleid: mois-1-05-os-command-injection-py
    subprocess.run(shlex.split(x))
    # shell=True 없이 넘긴 문자열은 그대로 실행 파일 이름이다
    # ruleid: mois-1-05-os-command-injection-py
    subprocess.run(x)
    # 튜플
    # ruleid: mois-1-05-os-command-injection-py
    subprocess.run(("sh", "-c", x))
    # 목록 연결
    # ruleid: mois-1-05-os-command-injection-py
    subprocess.run(["sh", "-c"] + [x])
    # 첫 원소가 문자열 리터럴이 아닌 목록 (f-string · 풀어 넣기)
    # ruleid: mois-1-05-os-command-injection-py
    subprocess.run([f"/opt/tools/{x}", "--version"])
    # ruleid: mois-1-05-os-command-injection-py
    subprocess.run([*x.split(), "--version"])
    return {"ok": True}


@app.route("/shape/keyword", methods=["POST"])
def keyword_arguments():
    x = request.form["x"]
    # 명령을 args= 키워드로 넘긴다
    # ruleid: mois-1-05-os-command-injection-py
    subprocess.run(args="ls " + x, shell=True)
    # ruleid: mois-1-05-os-command-injection-py
    subprocess.Popen(args=[x])
    # executable= 은 첫 인자와 무관하게 실행할 프로그램을 정한다
    # ruleid: mois-1-05-os-command-injection-py
    subprocess.run(["ls", "-l"], executable=x)
    # 호출 전체를 보는 sink 는 키워드 이름과 무관하다
    # ruleid: mois-1-05-os-command-injection-py
    os.system(command="ls " + x)
    return {"ok": True}


@app.route("/shape/shell-flag", methods=["POST"])
def shell_flag():
    x = request.form["x"]
    # shell=1 도 참이다
    # ruleid: mois-1-05-os-command-injection-py
    subprocess.run("ls " + x, shell=1)
    # 리스트 리터럴이어도 shell 을 켜면 Windows 에서는 cmd.exe 가 해석한다
    # ruleid: mois-1-05-os-command-injection-py
    subprocess.run(["dir", x], shell=True)
    return {"ok": True}


@app.route("/shape/dash-c", methods=["POST"])
def dash_c_option():
    x = request.form["x"]
    # 셸이 아니어도 -c 류 옵션 바로 뒤의 값은 명령 · 스크립트로 해석된다
    # ruleid: mois-1-05-os-command-injection-py
    subprocess.run(["psql", "-c", x])
    # ruleid: mois-1-05-os-command-injection-py
    subprocess.run(["/opt/tools/runner", "--quiet", "-xc", x])
    return {"ok": True}


@app.route("/shape/launcher", methods=["POST"])
def launcher_arguments():
    x = request.form["x"]
    # -c 바로 뒤가 아니어도, 옵션이 붙어 있어도 셸의 인자는 모두 본다
    # ruleid: mois-1-05-os-command-injection-py
    subprocess.run(["bash", "-lc", x])
    # ruleid: mois-1-05-os-command-injection-py
    subprocess.run(["/usr/bin/sudo", "-u", "www", x])
    # ruleid: mois-1-05-os-command-injection-py
    subprocess.run(["ssh", "backup@host", x])
    # ruleid: mois-1-05-os-command-injection-py
    subprocess.run(["CMD.EXE", "/c", x])
    return {"ok": True}


@app.route("/shape/async", methods=["POST"])
async def async_exec():
    x = request.form["x"]
    # ruleid: mois-1-05-os-command-injection-py
    await asyncio.create_subprocess_exec("sh", "-c", x)
    # -c 가 없어도 sudo 뒤의 인자는 실행할 명령이다
    # ruleid: mois-1-05-os-command-injection-py
    await asyncio.create_subprocess_exec("sudo", "systemctl", "restart", x)
    # ruleid: mois-1-05-os-command-injection-py
    await asyncio.create_subprocess_exec("psql", "-c", x)
    # 프로그램이 입력
    # ruleid: mois-1-05-os-command-injection-py
    await asyncio.create_subprocess_exec(x, "--version")
    return {"ok": True}


@app.route("/shape/os", methods=["POST"])
def os_exec_family():
    x = request.form["x"]
    # os.exec* · os.spawn* · os.posix_spawn* 은 실행 파일이 고정이어도 인자 목록까지 본다
    # ruleid: mois-1-05-os-command-injection-py
    os.execv("/bin/sh", ["sh", "-c", x])
    # ruleid: mois-1-05-os-command-injection-py
    os.spawnv(os.P_WAIT, "/bin/sh", ["sh", "-c", x])
    # ruleid: mois-1-05-os-command-injection-py
    os.posix_spawn(x, [x], os.environ)
    # ruleid: mois-1-05-os-command-injection-py
    pty.spawn(["sh", "-c", x])
    return {"ok": True}
