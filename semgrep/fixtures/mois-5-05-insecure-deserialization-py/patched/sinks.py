import hashlib
import hmac
import json
import os

import joblib
import numpy as np
import torch
import yaml
from flask import Flask, abort, request

app = Flask(__name__)
MODEL_DIR = "/var/app/models"
MODELS = {"churn", "fraud"}
MODEL_FILES = {"churn": "churn-v3.joblib", "fraud": "fraud-v1.joblib"}


@app.post("/state")
def restore_state():
    # ok: mois-5-05-insecure-deserialization-py 데이터만 담는 형식
    state = json.loads(request.get_data(as_text=True))
    # ok: mois-5-05-insecure-deserialization-py SafeLoader
    extra = yaml.load(request.form.get("extra", ""), Loader=yaml.CSafeLoader)
    # ok: mois-5-05-insecure-deserialization-py
    docs = list(yaml.safe_load_all(request.form.get("docs", "")))
    return {"n": len([state, extra, docs])}


@app.get("/models/guard")
def allowlist_guard():
    name = request.args.get("model", "")
    if name not in MODELS:
        abort(404)
    # ok: mois-5-05-insecure-deserialization-py 허용 목록에 없으면 위에서 빠져나갔다
    return {"model": str(joblib.load(os.path.join(MODEL_DIR, name + ".joblib")))}


@app.get("/models/inside")
def allowlist_inside():
    name = request.args.get("model", "")
    if name in MODELS:
        # ok: mois-5-05-insecure-deserialization-py 허용 목록 조건 안에서만 쓴다
        return {"model": str(joblib.load(os.path.join(MODEL_DIR, name + ".joblib")))}
    return {"model": None}


@app.get("/models/table")
def lookup_table():
    name = request.args.get("model", "")
    # ok: mois-5-05-insecure-deserialization-py 파일 이름은 코드에 적어 둔 표에서 나온다
    filename = MODEL_FILES.get(name)
    if filename is None:
        abort(404)
    return {"model": str(joblib.load(os.path.join(MODEL_DIR, filename)))}


@app.get("/weights/<name>")
def weights(name):
    if name not in MODELS:
        abort(404)
    path = os.path.join(MODEL_DIR, name)
    # ok: mois-5-05-insecure-deserialization-py 텐서만 읽는다
    tensors = torch.load(path + ".pt", weights_only=True)
    # ok: mois-5-05-insecure-deserialization-py pickle 을 허용하지 않는 기본값
    arrays = np.load(path + ".npy")
    return {"n": len(tensors) + len(arrays)}


@app.post("/weights/preview")
def uploaded_weights():
    # ok: mois-5-05-insecure-deserialization-py 올린 파일이어도 weights_only=True 는 텐서만 읽고 pickle 코드를 실행하지 않는다
    tensors = torch.load(request.files["weights"].stream, weights_only=True)
    return {"n": len(tensors)}


def verify_signature(key, blob, signature):
    # ok: mois-5-05-insecure-deserialization-py 서명 비교 결과를 돌려준다
    return hmac.compare_digest(hmac.new(key, blob, hashlib.sha256).hexdigest(), signature)
