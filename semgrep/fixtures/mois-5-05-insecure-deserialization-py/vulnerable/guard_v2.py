# 허용 목록 guard 의 v2 기준 (docs/rule-conventions.md 1절) 을 확인하는 예제.
# 공통 sanitizer (공통 2)·(공통 3) 이 v2 형태로 바뀐 뒤의 기대 동작으로 표시했다.
import os

import joblib
from flask import Flask, request

app = Flask(__name__)
MODEL_DIR = "/var/app/models"
MODELS = {"churn", "fraud"}


@app.get("/v2/inside-failing-branch")
def inside_failing_branch():
    name = request.args.get("model", "")
    if name not in MODELS:
        # 허용 목록에 없는 분기 안에서 쓴다
        # ruleid: mois-5-05-insecure-deserialization-py
        return {"model": str(joblib.load(os.path.join(MODEL_DIR, name)))}
    return {"model": None}


@app.get("/v2/nested-return")
def nested_conditional_return():
    name = request.args.get("model", "")
    if name not in MODELS:
        if request.args.get("strict"):
            return {"model": None}
    # 안쪽 조건부 return 은 중단이 아니다
    # ruleid: mois-5-05-insecure-deserialization-py
    return {"model": str(joblib.load(os.path.join(MODEL_DIR, name)))}


@app.get("/v2/reassigned")
def reassigned_after_check():
    name = request.args.get("model", "")
    if name not in MODELS:
        return {"model": None}
    # 검사한 뒤에 다른 요청값으로 다시 대입했다
    name = request.args.get("override", name)
    # ruleid: mois-5-05-insecure-deserialization-py
    return {"model": str(joblib.load(os.path.join(MODEL_DIR, name)))}


@app.get("/v2/and")
def check_joined_with_and():
    name = request.args.get("model", "")
    strict = request.args.get("strict")
    # strict 가 아니면 목록에 없어도 통과한다
    if strict and name not in MODELS:
        return {"model": None}
    # ruleid: mois-5-05-insecure-deserialization-py
    return {"model": str(joblib.load(os.path.join(MODEL_DIR, name)))}
