"""shlex.quote 를 인정하는 형태 — 셸 sink 의 명령 문자열 전체가 "고정된 명령 + 리터럴 + shlex.quote(...)" 뿐일 때."""
import asyncio
import os
import shlex
import subprocess

from flask import Flask, request

app = Flask(__name__)


@app.route("/thumb", methods=["POST"])
def thumbnail():
    src = request.form["src"]
    dst = request.form["dst"]
    # ok: mois-1-05-os-command-injection-py 고정된 명령 뒤에 묶은 값과 리터럴만 이어 붙임
    os.system("cp " + shlex.quote(src) + " " + shlex.quote(dst))
    # ok: mois-1-05-os-command-injection-py f-string 의 {shlex.quote(...)} 조각
    os.system(f"convert {shlex.quote(src)} -resize 120x120 {shlex.quote(dst)}")
    # ok: mois-1-05-os-command-injection-py % 형식의 인자가 shlex.quote(...) 하나
    os.system("file --brief %s" % shlex.quote(src))
    # ok: mois-1-05-os-command-injection-py % 형식의 인자 튜플이 모두 shlex.quote(...)
    os.system("cp %s %s" % (shlex.quote(src), shlex.quote(dst)))
    # ok: mois-1-05-os-command-injection-py .format 의 인자가 모두 shlex.quote(...)
    os.system("mv {} {}".format(shlex.quote(src), shlex.quote(dst)))
    # ok: mois-1-05-os-command-injection-py -c 뒤가 고정 값이면 옵션 값 자리가 아니다
    os.system('ping -c 1 ' + shlex.quote(src))
    return {"ok": True}


@app.route("/inspect")
async def inspect():
    name = request.args["name"]
    # ok: mois-1-05-os-command-injection-py 셸 sink 마다 같은 기준
    out = os.popen("du -sh /srv/data/" + shlex.quote(name)).read()
    # ok: mois-1-05-os-command-injection-py
    kind = subprocess.getoutput("file --brief /srv/data/" + shlex.quote(name))
    # ok: mois-1-05-os-command-injection-py
    code, text = subprocess.getstatusoutput("wc -l /srv/data/" + shlex.quote(name))
    # ok: mois-1-05-os-command-injection-py
    subprocess.run("touch /srv/data/" + shlex.quote(name), shell=True, check=False)
    # ok: mois-1-05-os-command-injection-py
    proc = await asyncio.create_subprocess_shell("ls -l /srv/data/" + shlex.quote(name))
    await proc.wait()
    return {"out": out, "kind": kind, "code": code, "text": text}
