import os
import re
import xml.etree.ElementTree as ET

from fastapi import FastAPI

app = FastAPI()


@app.get("/version")
def version(text: str):
    m = re.search(r"v(\d+)\.(\d+)", text)
    # ruleid: mois-5-01-null-dereference-py
    return {"major": m.group(1)}  # 매치 실패 시 None


@app.post("/feed")
def feed(body: str):
    root = ET.fromstring(body)
    # ruleid: mois-5-01-null-dereference-py
    title = root.find("channel/title").text  # 요소가 없으면 None
    region = os.getenv("REGION")
    # ruleid: mois-5-01-null-dereference-py
    return {"title": title, "region": region.upper()}  # 환경변수가 없으면 None
