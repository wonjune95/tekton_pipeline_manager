import pickle
import shelve

import _pickle
import cloudpickle
import dill
import joblib
import jsonpickle
import numpy as np
import pandas as pd
import torch
import yaml
from flask import Flask, request

app = Flask(__name__)


@app.post("/restore")
def restore():
    upload = request.files["state"].stream
    blob = request.get_data()
    text = request.form["state"]
    # 첫 인자를 이름으로 넘겨도 같은 호출이다
    # ruleid: mois-5-05-insecure-deserialization-py
    a = pickle.load(file=upload)
    # ruleid: mois-5-05-insecure-deserialization-py
    b = _pickle.load(file=upload)
    # ruleid: mois-5-05-insecure-deserialization-py
    c = cloudpickle.load(file=upload)
    # ruleid: mois-5-05-insecure-deserialization-py
    d = dill.load(file=upload)
    # ruleid: mois-5-05-insecure-deserialization-py
    e = dill.loads(str=blob)
    # ruleid: mois-5-05-insecure-deserialization-py
    f = pickle.Unpickler(file=upload).load()
    # ruleid: mois-5-05-insecure-deserialization-py
    g = jsonpickle.decode(string=text)
    # ruleid: mois-5-05-insecure-deserialization-py
    h = jsonpickle.loads(string=text, keys=True)
    return {"n": len([a, b, c, d, e, f, g, h])}


@app.post("/restore/yaml")
def restore_yaml():
    text = request.get_data(as_text=True)
    # ruleid: mois-5-05-insecure-deserialization-py
    a = yaml.load(stream=text, Loader=yaml.Loader)
    # 인자 순서를 바꿔도 같다
    # ruleid: mois-5-05-insecure-deserialization-py
    b = yaml.load(Loader=yaml.FullLoader, stream=text)
    # Loader 없이 stream 만
    # ruleid: mois-5-05-insecure-deserialization-py
    c = yaml.load(stream=text)
    # ruleid: mois-5-05-insecure-deserialization-py
    d = yaml.unsafe_load(stream=text)
    # ruleid: mois-5-05-insecure-deserialization-py
    e = list(yaml.full_load_all(stream=text))
    return {"n": len([a, b, c, d, e])}


@app.get("/models/load")
def load_model(**options):
    path = request.args["path"]
    # ruleid: mois-5-05-insecure-deserialization-py
    a = joblib.load(filename=path)
    # ruleid: mois-5-05-insecure-deserialization-py
    b = pd.read_pickle(filepath_or_buffer=path)
    # ruleid: mois-5-05-insecure-deserialization-py
    c = torch.load(f=path, map_location="cpu")
    # ruleid: mois-5-05-insecure-deserialization-py
    d = np.load(file=path, allow_pickle=True)
    # ruleid: mois-5-05-insecure-deserialization-py
    with shelve.open(filename=path, flag="r") as db:
        return {"keys": list(db), "n": len([a, b, c, d])}


@app.get("/arrays/load")
def load_arrays(**options):
    path = request.args["path"]
    # allow_pickle 이 True 리터럴이 아니어도 False 로 확인되지 않으면 pickle 을 읽을 수 있다
    # ruleid: mois-5-05-insecure-deserialization-py
    a = np.load(path, allow_pickle=request.args.get("pickle") == "1")
    # 세 번째 위치 인자가 allow_pickle 이다
    # ruleid: mois-5-05-insecure-deserialization-py
    b = np.load(path, None, True)
    # 무엇이 들어올지 알 수 없는 **옵션
    # ruleid: mois-5-05-insecure-deserialization-py
    c = np.load(path, **options)
    return {"n": len([a, b, c])}
