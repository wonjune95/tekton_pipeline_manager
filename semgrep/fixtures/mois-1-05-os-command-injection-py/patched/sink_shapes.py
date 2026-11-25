"""실행 파일이 고정된 리스트 리터럴 — 입력은 인자로만 들어간다."""
import asyncio
import subprocess

from flask import Flask, request

app = Flask(__name__)

FFPROBE = "/usr/bin/ffprobe"


@app.route("/probe", methods=["POST"])
async def probe():
    name = request.form["name"]
    # ok: mois-1-05-os-command-injection-py shell=False 를 명시한 리스트 리터럴
    subprocess.run(["ls", "-l", name], shell=False, check=False)
    # ok: mois-1-05-os-command-injection-py 같은 파일의 문자열 상수가 실행 파일
    subprocess.run([FFPROBE, "-hide_banner", name], check=False)
    # ok: mois-1-05-os-command-injection-py 입력이 표준 입력으로만 들어간다
    subprocess.run(["wc", "-l"], input=name, text=True, check=False)
    # ok: mois-1-05-os-command-injection-py -c 바로 뒤는 고정 값
    subprocess.run(["grep", "-c", "ERROR", name], check=False)
    # ok: mois-1-05-os-command-injection-py 프로그램이 문자열 리터럴이고 셸 · 실행기가 아니다
    proc = await asyncio.create_subprocess_exec("ffprobe", "-hide_banner", name)
    await proc.wait()
    return {"ok": True}
