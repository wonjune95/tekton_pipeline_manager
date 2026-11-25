import pickle

import numpy as np
import torch
import yaml
import yaml.cyaml
import yaml.loader

try:
    from yaml import CSafeLoader as SafeLoader
except ImportError:
    from yaml import SafeLoader


def load_documents(text):
    # ok: mois-5-05-unsafe-deserializer-py C 구현이 없으면 SafeLoader 로 바꿔 import 하는 흔한 형태
    a = yaml.load(text, Loader=SafeLoader)
    # ok: mois-5-05-unsafe-deserializer-py
    b = yaml.load(text, Loader=yaml.CBaseLoader)
    # ok: mois-5-05-unsafe-deserializer-py 클래스가 정의된 하위 모듈 경로
    c = yaml.load(text, yaml.loader.SafeLoader)
    # ok: mois-5-05-unsafe-deserializer-py
    d = list(yaml.load_all(text, Loader=yaml.loader.BaseLoader))
    # ok: mois-5-05-unsafe-deserializer-py
    e = yaml.load(stream=text, Loader=yaml.cyaml.CSafeLoader)
    # ok: mois-5-05-unsafe-deserializer-py
    f = yaml.load(text, yaml.cyaml.CBaseLoader)
    return a, b, c, d, e, f


def load_arrays(path):
    # ok: mois-5-05-unsafe-deserializer-py allow_pickle 이 False 로 확인된다
    a = np.load(path, allow_pickle=False)
    # ok: mois-5-05-unsafe-deserializer-py 세 번째 위치 인자 False
    b = np.load(path, None, False)
    # ok: mois-5-05-unsafe-deserializer-py
    c = torch.load(f=path, weights_only=True)
    return a, b, c


def load_local_cache(path):
    with open(path, "rb") as f:
        # ok: mois-5-05-unsafe-deserializer-py 네트워크가 아니라 프로그램이 직접 쓴 로컬 캐시 파일
        return pickle.load(file=f)
