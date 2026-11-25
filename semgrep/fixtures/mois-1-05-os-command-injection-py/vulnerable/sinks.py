import asyncio
import os
import subprocess

from flask import Flask, request

app = Flask(__name__)


@app.route("/disk")
def disk_usage():
    path = request.args.get("path", "/")
    # ruleid: mois-1-05-os-command-injection-py
    out = os.popen("du -sh " + path).read()
    return {"out": out}


@app.route("/whois")
def whois():
    domain = request.args["domain"]
    # ruleid: mois-1-05-os-command-injection-py
    out = subprocess.getoutput(f"whois {domain}")
    # ruleid: mois-1-05-os-command-injection-py
    code, text = subprocess.getstatusoutput("dig +short " + domain)
    return {"out": out, "code": code, "text": text}


@app.route("/trace")
async def trace():
    host = request.args["host"]
    # ruleid: mois-1-05-os-command-injection-py
    proc = await asyncio.create_subprocess_shell("traceroute " + host, stdout=asyncio.subprocess.PIPE)
    out, _ = await proc.communicate()
    return {"out": out.decode()}


@app.route("/archive", methods=["POST"])
def archive():
    name = request.form["name"]
    # shell=True 로 넘기는 문자열
    # ruleid: mois-1-05-os-command-injection-py
    subprocess.Popen("tar czf /tmp/" + name + ".tgz /srv/data", shell=True)
    # ruleid: mois-1-05-os-command-injection-py
    subprocess.call("gzip /tmp/%s" % name, shell=True)
    return {"ok": True}


@app.route("/tools/run", methods=["POST"])
def run_tool():
    tool = request.form["tool"]
    # 인자 목록이어도 실행 파일 자체가 외부 입력이면 임의 프로그램이 실행된다
    # ruleid: mois-1-05-os-command-injection-py
    subprocess.run([tool, "--version"], check=False)
    # ruleid: mois-1-05-os-command-injection-py
    out = subprocess.check_output([os.path.join("/opt/tools", tool)])
    # ruleid: mois-1-05-os-command-injection-py
    code = subprocess.call([tool, "--selftest"])
    # ruleid: mois-1-05-os-command-injection-py
    subprocess.Popen([tool, "--daemon"])
    return {"out": out.decode(), "code": code}


@app.route("/script", methods=["POST"])
def run_script():
    script = request.form["script"]
    # 인자 목록의 "-c" 뒤에 오는 값은 셸이 해석한다
    # ruleid: mois-1-05-os-command-injection-py
    subprocess.check_call(["bash", "-c", script])
    return {"ok": True}


@app.route("/launch", methods=["POST"])
def launch():
    program = request.form["program"]
    # ruleid: mois-1-05-os-command-injection-py
    os.spawnlp(os.P_WAIT, program, program, "--help")
    # ruleid: mois-1-05-os-command-injection-py
    os.spawnv(os.P_NOWAIT, program, [program])
    # ruleid: mois-1-05-os-command-injection-py
    os.startfile(program)
    # ruleid: mois-1-05-os-command-injection-py
    os.execv(program, [program, "--daemon"])
    return {"ok": True}
