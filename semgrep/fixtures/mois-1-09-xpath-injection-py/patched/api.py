import re
import xml.etree.ElementTree as ET

from fastapi import FastAPI, HTTPException

app = FastAPI()
CATALOG_XML = "/srv/data/catalog.xml"
CATEGORY_RE = re.compile(r"[A-Za-z0-9_-]{1,40}")


@app.get("/products")
def products(category: str):
    # ok: mois-1-09-xpath-injection-py ElementTree 는 XPath 변수가 없으므로 허용 문자만 받는다 (전체 일치 실패 시 예외)
    if not CATEGORY_RE.fullmatch(category):
        raise HTTPException(status_code=400, detail="invalid category")
    root = ET.parse(CATALOG_XML).getroot()
    query = f".//product[@category='{category}']"
    items = root.findall(query)
    return {"names": [item.findtext("name") for item in items]}


@app.get("/stores")
def stores(city: str):
    if not city.isalnum():
        raise HTTPException(status_code=400, detail="invalid city")
    root = ET.parse(CATALOG_XML).getroot()
    # ok: mois-1-09-xpath-injection-py
    return {"count": len(root.findall(".//store[city='" + city + "']"))}
