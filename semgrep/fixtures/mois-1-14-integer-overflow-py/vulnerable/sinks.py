import ctypes
import os
import struct
from typing import Annotated

import numpy as np
from fastapi import FastAPI, Query, UploadFile

app = FastAPI()


@app.get("/fixed-width")
def fixed_width(count: int, offset: int):
    # 고정 폭 정수형으로 변환 (범위를 넘으면 값이 잘린다)
    # ruleid: mois-1-14-integer-overflow-py
    a = np.uint16(count)
    # ruleid: mois-1-14-integer-overflow-py
    b = ctypes.c_int32(offset)
    # ruleid: mois-1-14-integer-overflow-py
    c = ctypes.c_size_t(count)
    return {"a": int(a), "b": b.value, "c": c.value}


@app.get("/fixed-width/table")
def fixed_width_table(n: int):
    # 고정 폭 정수형마다 한 줄 (numpy · ctypes)
    # ruleid: mois-1-14-integer-overflow-py
    np.int8(n)
    # ruleid: mois-1-14-integer-overflow-py
    np.uint64(n)
    # ruleid: mois-1-14-integer-overflow-py
    np.intc(n)
    # ruleid: mois-1-14-integer-overflow-py
    ctypes.c_ubyte(n)
    # ruleid: mois-1-14-integer-overflow-py
    ctypes.c_short(n)
    # ruleid: mois-1-14-integer-overflow-py
    ctypes.c_uint(n)
    # ruleid: mois-1-14-integer-overflow-py
    ctypes.c_long(n)
    # ruleid: mois-1-14-integer-overflow-py
    ctypes.c_ulonglong(n)
    # ruleid: mois-1-14-integer-overflow-py
    ctypes.c_int8(n)
    # ruleid: mois-1-14-integer-overflow-py
    ctypes.c_uint16(n)
    # ruleid: mois-1-14-integer-overflow-py
    ctypes.c_int64(n)
    return {"ok": True}


@app.get("/record")
def record(seq: int, length: int):
    # 여러 필드 가운데 하나라도 외부 입력이면 탐지
    # ruleid: mois-1-14-integer-overflow-py
    return {"hex": struct.pack(">HI", 1, seq).hex() + struct.pack("<q", length).hex()}


@app.get("/allocate")
def allocate(n: int):
    # 외부에서 받은 수만큼 메모리를 잡는다
    # ruleid: mois-1-14-integer-overflow-py
    zeros = [0] * n
    # ruleid: mois-1-14-integer-overflow-py
    pad = " " * n
    # ruleid: mois-1-14-integer-overflow-py
    ones = np.ones(n)
    # ruleid: mois-1-14-integer-overflow-py
    empty = np.empty(n, dtype=np.uint8)
    # ruleid: mois-1-14-integer-overflow-py
    full = np.full(n, 7)
    # ruleid: mois-1-14-integer-overflow-py
    token = os.urandom(n)
    return {"sizes": [len(zeros), len(pad), ones.size, empty.size, full.size, len(token)]}


@app.post("/head")
async def head(file: UploadFile, limit: int = Query(1024, ge=1)):
    # 하한(ge)만 있고 상한이 없는 매개변수
    # ruleid: mois-1-14-integer-overflow-py
    return {"head": file.file.read(limit).hex()}


@app.get("/blank")
def blank(lines: Annotated[int, Query(ge=1)]):
    # Annotated 로 선언했지만 상한이 없다
    # ruleid: mois-1-14-integer-overflow-py
    return {"text": "\n" * lines}
