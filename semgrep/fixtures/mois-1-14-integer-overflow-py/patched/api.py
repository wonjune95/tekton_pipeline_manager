import numpy as np
from fastapi import FastAPI, HTTPException, Query

app = FastAPI()
MAX_SIDE = 2000
INT32_MIN, INT32_MAX = -(2**31), 2**31 - 1


@app.get("/matrix")
def matrix(rows: int = Query(..., ge=1, le=MAX_SIDE), cols: int = Query(..., ge=1, le=MAX_SIDE)):
    # ok: mois-1-14-integer-overflow-py 상한이 걸린 값만 크기로 사용
    grid = np.zeros(rows * cols)
    return {"cells": int(grid.size)}


@app.get("/scale")
def scale(value: int, factor: int = 2):
    # 자릿수 제한이 없는 int 로 계산하고, 결과가 int32 범위인지 확인한 뒤 변환
    scaled = value * factor
    if scaled < INT32_MIN or scaled > INT32_MAX:
        raise HTTPException(status_code=400, detail="result out of range")
    # ok: mois-1-14-integer-overflow-py 범위를 벗어나면 위에서 예외
    return {"scaled": int(np.int32(scaled))}
