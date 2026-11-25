import xml.etree.ElementTree as ET

from fastapi import FastAPI

app = FastAPI()
CATALOG_XML = "/srv/data/catalog.xml"


@app.get("/products")
def products(category: str):
    root = ET.parse(CATALOG_XML).getroot()
    # 외부 입력으로 ElementTree 경로식을 만듦
    query = f".//product[@category='{category}']"
    # ruleid: mois-1-09-xpath-injection-py
    items = root.findall(query)
    return {"names": [item.findtext("name") for item in items]}


@app.get("/stores")
def stores(city: str):
    root = ET.parse(CATALOG_XML).getroot()
    # ruleid: mois-1-09-xpath-injection-py
    return {"count": len(root.findall(".//store[city='" + city + "']"))}
