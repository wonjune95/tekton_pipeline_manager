import base64
import io
import logging
import os
import pickle
import shelve

import _pickle
import cloudpickle
import dill
import joblib
import jsonpickle
import marshal
import numpy as np
import pandas as pd
import torch
import yaml
from flask import Flask, abort, request
from six.moves import cPickle
from yaml import FullLoader, Loader, UnsafeLoader

app = Flask(__name__)
logger = logging.getLogger(__name__)
MODEL_DIR = "/var/app/models"
MODELS = {"churn", "fraud"}
MODEL_FILES = {"churn": "churn-v3.joblib", "fraud": "fraud-v1.joblib"}


@app.post("/state/pickle")
def pickle_variants():
    raw = base64.b64decode(request.form["state"])
    # ruleid: mois-5-05-insecure-deserialization-py
    a = _pickle.loads(raw)
    # ruleid: mois-5-05-insecure-deserialization-py
    b = cPickle.loads(raw)
    # ruleid: mois-5-05-insecure-deserialization-py
    c = dill.loads(raw)
    # ruleid: mois-5-05-insecure-deserialization-py
    d = cloudpickle.loads(raw)
    # ruleid: mois-5-05-insecure-deserialization-py
    e = marshal.load(io.BytesIO(raw))
    # ruleid: mois-5-05-insecure-deserialization-py
    f = dill.load(request.files["state"].stream)
    # ruleid: mois-5-05-insecure-deserialization-py
    g = pickle.Unpickler(io.BytesIO(raw)).load()
    # ruleid: mois-5-05-insecure-deserialization-py
    h = jsonpickle.loads(request.form["json_state"])
    return {"n": len([a, b, c, d, e, f, g, h])}


@app.post("/state/yaml")
def yaml_variants():
    text = request.get_data(as_text=True)
    # ruleid: mois-5-05-insecure-deserialization-py
    a = yaml.unsafe_load(text)
    # ruleid: mois-5-05-insecure-deserialization-py
    b = list(yaml.unsafe_load_all(text))
    # ruleid: mois-5-05-insecure-deserialization-py
    c = yaml.full_load(text)
    # ruleid: mois-5-05-insecure-deserialization-py
    d = list(yaml.full_load_all(text))
    # Loader 를 주지 않은 yaml.load
    # ruleid: mois-5-05-insecure-deserialization-py
    e = yaml.load(text)
    # ruleid: mois-5-05-insecure-deserialization-py
    f = list(yaml.load_all(text))
    # 위치 인자로 준 Loader
    # ruleid: mois-5-05-insecure-deserialization-py
    g = yaml.load(text, Loader)
    # ruleid: mois-5-05-insecure-deserialization-py
    h = yaml.load(text, Loader=UnsafeLoader)
    # ruleid: mois-5-05-insecure-deserialization-py
    i = yaml.load(text, Loader=FullLoader)
    # ruleid: mois-5-05-insecure-deserialization-py
    j = list(yaml.load_all(text, Loader=yaml.CLoader))
    return {"n": len([a, b, c, d, e, f, g, h, i, j])}


@app.get("/models/<name>")
def model_files(name):
    path = os.path.join(MODEL_DIR, name)
    # 요청으로 고른 경로의 파일을 pickle 계열로 읽는다
    # ruleid: mois-5-05-insecure-deserialization-py
    a = joblib.load(path)
    # ruleid: mois-5-05-insecure-deserialization-py
    b = pd.read_pickle(path)
    # ruleid: mois-5-05-insecure-deserialization-py
    c = torch.load(path)
    # ruleid: mois-5-05-insecure-deserialization-py
    d = np.load(path, allow_pickle=True)
    # ruleid: mois-5-05-insecure-deserialization-py
    with shelve.open(path) as db:
        return {"keys": list(db), "n": len([a, b, c, d])}


@app.get("/models/checked")
def allowlist_not_enforced():
    name = request.args.get("model", "")
    # 허용 목록에 없어도 기록만 하고 계속 진행한다
    if name not in MODELS:
        logger.warning("unknown model: %s", name)
    # ruleid: mois-5-05-insecure-deserialization-py
    return {"model": str(joblib.load(os.path.join(MODEL_DIR, name)))}


@app.get("/models/ignored")
def allowlist_result_ignored():
    name = request.args.get("model", "")
    # 검사 결과를 쓰지 않는다
    name in MODELS
    # ruleid: mois-5-05-insecure-deserialization-py
    return {"model": str(joblib.load(os.path.join(MODEL_DIR, name)))}


@app.get("/models/else")
def allowlist_opposite_branch():
    name = request.args.get("model", "")
    if name in MODELS:
        return {"model": "builtin"}
    else:
        # 허용 목록에 없는 쪽에서 읽는다
        # ruleid: mois-5-05-insecure-deserialization-py
        return {"model": str(joblib.load(os.path.join(MODEL_DIR, name)))}


@app.get("/models/default")
def lookup_with_input_default():
    name = request.args.get("model", "")
    # 표에 없으면 입력을 그대로 돌려주는 조회
    filename = MODEL_FILES.get(name, name)
    # ruleid: mois-5-05-insecure-deserialization-py
    return {"model": str(joblib.load(os.path.join(MODEL_DIR, filename)))}


@app.get("/models/abort-late")
def allowlist_checks_other_value():
    name = request.args.get("model", "")
    kind = request.args.get("kind", "")
    # 다른 값을 검사한다
    if kind not in MODELS:
        abort(400)
    # ruleid: mois-5-05-insecure-deserialization-py
    return {"model": str(joblib.load(os.path.join(MODEL_DIR, name)))}
