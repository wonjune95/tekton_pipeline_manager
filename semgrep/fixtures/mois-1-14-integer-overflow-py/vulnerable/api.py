import numpy as np
from fastapi import FastAPI

app = FastAPI()


@app.get("/matrix")
def matrix(rows: int, cols: int):
    # 외부 입력값을 범위 검사 없이 배열 크기로 사용
    # ruleid: mois-1-14-integer-overflow-py
    grid = np.zeros(rows * cols)
    return {"cells": int(grid.size)}


@app.get("/scale")
def scale(value: int, factor: int = 2):
    # int32 로 바꾼 뒤 곱하면 넘친 값이 그대로 남음
    # ruleid: mois-1-14-integer-overflow-py
    scaled = np.int32(value) * np.int32(factor)
    return {"scaled": int(scaled)}
