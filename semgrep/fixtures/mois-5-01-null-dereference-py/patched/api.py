import os
import re
import xml.etree.ElementTree as ET

from fastapi import FastAPI, HTTPException

app = FastAPI()


@app.get("/version")
def version(text: str):
    m = re.search(r"v(\d+)\.(\d+)", text)
    if not m:
        raise HTTPException(status_code=400, detail="E400")
    return {"major": m.group(1)}


@app.post("/feed")
def feed(body: str):
    root = ET.fromstring(body)
    node = root.find("channel/title")
    title = node.text if node is not None else ""
    region = os.getenv("REGION") or "kr"
    return {"title": title, "region": region.upper()}
