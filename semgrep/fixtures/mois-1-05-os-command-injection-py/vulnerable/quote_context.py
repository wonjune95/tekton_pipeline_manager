"""shlex.quote 를 썼지만 막지 못하는 문맥 — 모두 탐지되어야 한다.

shlex.quote 는 값을 "셸 낱말 하나"로 묶을 뿐이다. 그 낱말이 어디에 놓이는지는 보장하지 않는다.
"""
import os
import shlex
import subprocess

from flask import Flask, request

app = Flask(__name__)


@app.route("/quote/reparsed", methods=["POST"])
def quote_reparsed():
    x = request.form["x"]
    # 묶은 낱말 전체가 sh -c 의 스크립트가 된다
    # ruleid: mois-1-05-os-command-injection-py
    os.system("sh -c " + shlex.quote(x))
    # ssh 는 인자를 이어 붙여 원격 셸에 다시 넘긴다
    # ruleid: mois-1-05-os-command-injection-py
    os.system("ssh backup@host " + shlex.quote(x))
    # eval 은 인자를 다시 해석한다
    # ruleid: mois-1-05-os-command-injection-py
    os.system("eval " + shlex.quote(x))
    # 경로로 적은 실행 파일도 같다
    # ruleid: mois-1-05-os-command-injection-py
    os.system("/usr/bin/env " + shlex.quote(x))
    # ruleid: mois-1-05-os-command-injection-py
    os.system("python3 -m tools.report " + shlex.quote(x))
    return {"ok": True}


@app.route("/quote/position", methods=["POST"])
def quote_position():
    x = request.form["x"]
    # 실행 파일 자리: 어떤 프로그램을 실행할지 입력이 정한다
    # ruleid: mois-1-05-os-command-injection-py
    os.system(shlex.quote(x))
    # 명령 이름에 그대로 붙는다 (/opt/tools/'x')
    # ruleid: mois-1-05-os-command-injection-py
    os.system("/opt/tools/" + shlex.quote(x))
    # ruleid: mois-1-05-os-command-injection-py
    os.system("ls" + shlex.quote(x))
    # ; | 뒤는 새 명령의 실행 파일 자리다
    # ruleid: mois-1-05-os-command-injection-py
    os.system("cd /srv/data; " + shlex.quote(x))
    # ruleid: mois-1-05-os-command-injection-py
    os.system("cat /srv/data/list | " + shlex.quote(x))
    # ruleid: mois-1-05-os-command-injection-py
    os.system("cd /srv/data && " + shlex.quote(x))
    # 출력 방향 바꾸기의 대상 파일을 입력이 정한다
    # ruleid: mois-1-05-os-command-injection-py
    os.system("sort /srv/data/list > " + shlex.quote(x))
    # 묶은 값을 출력해 다시 셸에 넘긴다
    # ruleid: mois-1-05-os-command-injection-py
    os.system("echo " + shlex.quote(x) + " | sh")
    # 환경 변수 대입 자리 (첫 낱말이 명령이 아니다)
    # ruleid: mois-1-05-os-command-injection-py
    os.system("LD_PRELOAD=" + shlex.quote(x) + " ls")
    # -c 류 옵션의 값은 그 프로그램이 명령 · 스크립트로 해석한다
    # ruleid: mois-1-05-os-command-injection-py
    os.system("/opt/tools/runner -c " + shlex.quote(x))
    # ruleid: mois-1-05-os-command-injection-py
    os.system(f"/opt/tools/runner -c {shlex.quote(x)}")
    # ruleid: mois-1-05-os-command-injection-py
    os.system("/opt/tools/runner -c %s" % shlex.quote(x))
    # ruleid: mois-1-05-os-command-injection-py
    os.system("/opt/tools/runner -c {}".format(shlex.quote(x)))
    # ruleid: mois-1-05-os-command-injection-py
    os.system('/opt/tools/runner -c ' + shlex.quote(x))
    return {"ok": True}


@app.route("/quote/inside-quotes", methods=["POST"])
def quote_inside_quotes():
    x = request.form["x"]
    # 이미 따옴표 안이면 shlex.quote 가 붙인 따옴표가 바깥 따옴표를 닫는다
    # ruleid: mois-1-05-os-command-injection-py
    os.system("grep '" + shlex.quote(x) + "' /var/log/app.log")
    # ruleid: mois-1-05-os-command-injection-py
    os.system("echo \"" + shlex.quote(x) + "\"")
    # 명령 치환 안은 실행 파일 자리다
    # ruleid: mois-1-05-os-command-injection-py
    os.system("echo $(" + shlex.quote(x) + ")")
    # ruleid: mois-1-05-os-command-injection-py
    os.system("echo `" + shlex.quote(x) + "`")
    return {"ok": True}


@app.route("/quote/no-shell", methods=["POST"])
def quote_without_shell():
    x = request.form["x"]
    # 셸을 거치지 않는 인자 목록에서는 따옴표가 그대로 값이 될 뿐이고, 실행 파일은 여전히 입력이 정한다
    # ruleid: mois-1-05-os-command-injection-py
    subprocess.run([shlex.quote(x), "--version"])
    # ruleid: mois-1-05-os-command-injection-py
    subprocess.run(["sh", "-c", shlex.quote(x)])
    # shell=True 가 없으면 문자열 전체가 실행 파일 이름이다
    # ruleid: mois-1-05-os-command-injection-py
    subprocess.run("ls " + shlex.quote(x))
    return {"ok": True}


@app.route("/quote/mixed", methods=["POST"])
def quote_mixed():
    x = request.form["x"]
    y = request.form["y"]
    # 한 값만 묶고 다른 값은 그대로 붙였다
    # ruleid: mois-1-05-os-command-injection-py
    os.system("cp " + shlex.quote(x) + " " + y)
    # ruleid: mois-1-05-os-command-injection-py
    os.system(f"cp {shlex.quote(x)} {y}")
    # ruleid: mois-1-05-os-command-injection-py
    os.system("cp %s %s" % (shlex.quote(x), y))
    # ruleid: mois-1-05-os-command-injection-py
    os.system("cp {} {}".format(shlex.quote(x), y))
    # ruleid: mois-1-05-os-command-injection-py
    os.system(y + " " + shlex.quote(x))
    # 묶은 뒤 따옴표를 다시 벗겼다
    # ruleid: mois-1-05-os-command-injection-py
    os.system("ls " + shlex.quote(x).strip("'"))
    # !r 은 묶은 결과를 다시 Python 따옴표로 감싼다
    # ruleid: mois-1-05-os-command-injection-py
    os.system(f"ls {shlex.quote(x)!r}")
    # 조건식의 다른 가지는 묶지 않았다
    # ruleid: mois-1-05-os-command-injection-py
    os.system("ls " + shlex.quote(x) if y else y)
    # 묶은 문자열을 괄호로 만들어 다른 명령(ssh)에 다시 감쌌다
    # ruleid: mois-1-05-os-command-injection-py
    os.system("ssh backup@host " + ("ls " + shlex.quote(x)))
    return {"ok": True}


@app.route("/quote/variable", methods=["POST"])
def quote_in_variable():
    x = request.form["x"]
    cmd = "ls -l " + shlex.quote(x)
    # 변수에 담은 명령 문자열은 인정하지 않는다 — 아래처럼 다시 감싸는 것과 구분할 수 없다
    # ruleid: mois-1-05-os-command-injection-py
    os.system(cmd)
    # ruleid: mois-1-05-os-command-injection-py
    os.system("ssh backup@host " + cmd)
    return {"ok": True}
