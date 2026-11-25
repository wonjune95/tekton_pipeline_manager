from typing import Annotated

import numpy as np
from fastapi import FastAPI, Path, Query

app = FastAPI()
MAX_ITEMS = 10_000


@app.get("/annotated")
def annotated(count: Annotated[int, Query(ge=0, le=MAX_ITEMS)], page: Annotated[int, Path(lt=1000)]):
    # ok: mois-1-14-integer-overflow-py Annotated 로 상한(le·lt)이 걸린 매개변수
    return {"cells": int(np.zeros(count).size), "page": int(np.int16(page))}


@app.get("/default-bound")
def default_bound(depth: int = Query(1, lt=64), width: int = Query(8, le=4096)):
    # ok: mois-1-14-integer-overflow-py 기본값 Query(lt=…)·Query(le=…) 로 상한이 걸린 매개변수
    return {"cells": len([0] * depth) + len(bytearray(width))}


@app.get("/clamped")
def clamped(count: int, level: int):
    # ok: mois-1-14-integer-overflow-py min·clip 으로 상한을 정한 값
    limited = min(count, MAX_ITEMS)
    clipped = np.clip(level, 0, 255)
    return {"cells": len(bytearray(limited)), "level": int(np.uint8(clipped))}
