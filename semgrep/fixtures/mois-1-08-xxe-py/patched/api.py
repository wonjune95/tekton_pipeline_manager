import io
import xml.sax
from xml.sax.handler import ContentHandler, feature_external_ges, feature_external_pes

from fastapi import FastAPI, Request

app = FastAPI()


class ItemCounter(ContentHandler):
    def __init__(self):
        super().__init__()
        self.count = 0

    def startElement(self, name, attrs):
        if name == "item":
            self.count += 1


@app.post("/feeds")
async def upload_feed(request: Request):
    body = await request.body()
    handler = ItemCounter()
    parser = xml.sax.make_parser()
    # ok: mois-1-08-xxe-py 외부 엔티티 처리를 끔
    parser.setFeature(feature_external_ges, False)
    parser.setFeature(feature_external_pes, False)
    parser.setContentHandler(handler)
    parser.parse(io.BytesIO(body))
    return {"items": handler.count}
