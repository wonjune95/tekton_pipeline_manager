import subprocess

from fastapi import FastAPI

app = FastAPI()


@app.get("/lookup")
async def lookup(domain: str):
    # 셸(-c) 인자에 외부 입력
    # ruleid: mois-1-05-os-command-injection-py
    proc = subprocess.run(["sh", "-c", "nslookup " + domain], capture_output=True, text=True)
    return {"out": proc.stdout}
