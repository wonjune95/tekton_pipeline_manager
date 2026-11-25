import numpy as np
import torch
import yaml
import yaml.cyaml
import yaml.loader
from flask import Flask, request
from yaml import BaseLoader

try:
    from yaml import CSafeLoader as SafeLoader
except ImportError:
    from yaml import SafeLoader

app = Flask(__name__)


@app.post("/config/import")
def import_config():
    text = request.get_data(as_text=True)
    # ok: mois-5-05-insecure-deserialization-py PyYAML 의 SafeLoader·BaseLoader 계열로 확인되는 Loader (이름 하나, import 로 풀림)
    a = yaml.load(text, Loader=yaml.SafeLoader)
    # ok: mois-5-05-insecure-deserialization-py C 구현이 없으면 SafeLoader 로 바꿔 import 하는 흔한 형태
    b = yaml.load(text, Loader=SafeLoader)
    # ok: mois-5-05-insecure-deserialization-py 위치 인자
    c = yaml.load(text, BaseLoader)
    # ok: mois-5-05-insecure-deserialization-py
    d = yaml.load(text, Loader=yaml.CBaseLoader)
    # ok: mois-5-05-insecure-deserialization-py 클래스가 정의된 하위 모듈 경로
    e = yaml.load(text, Loader=yaml.loader.SafeLoader)
    # ok: mois-5-05-insecure-deserialization-py
    f = list(yaml.load_all(text, yaml.loader.BaseLoader))
    # ok: mois-5-05-insecure-deserialization-py
    g = yaml.load(stream=text, Loader=yaml.cyaml.CSafeLoader)
    # ok: mois-5-05-insecure-deserialization-py
    h = yaml.load(Loader=yaml.cyaml.CBaseLoader, stream=text)
    return {"n": len([a, b, c, d, e, f, g, h])}


@app.post("/arrays/preview")
def preview_arrays():
    upload = request.files["arrays"].stream
    # ok: mois-5-05-insecure-deserialization-py allow_pickle 이 False 로 확인된다
    a = np.load(upload, allow_pickle=False)
    # ok: mois-5-05-insecure-deserialization-py 세 번째 위치 인자 False
    b = np.load(upload, None, False)
    # ok: mois-5-05-insecure-deserialization-py allow_pickle 을 주지 않았다 (기본값 False)
    c = np.load(file=upload, mmap_mode=None)
    # ok: mois-5-05-insecure-deserialization-py
    d = torch.load(f=upload, weights_only=True)
    return {"n": len([a, b, c, d])}
