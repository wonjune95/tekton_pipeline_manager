import json
import pickle

import numpy as np
import yaml
from yaml import CSafeLoader


def load_documents(text):
    # ok: mois-5-05-unsafe-deserializer-py SafeLoader 계열
    a = list(yaml.safe_load_all(text))
    # ok: mois-5-05-unsafe-deserializer-py
    b = yaml.load(text, CSafeLoader)
    # ok: mois-5-05-unsafe-deserializer-py 기본 자료형만 만드는 BaseLoader
    c = yaml.load(text, Loader=yaml.BaseLoader)
    return a, b, c


def load_arrays(path):
    # ok: mois-5-05-unsafe-deserializer-py allow_pickle 기본값은 False
    return np.load(path)


def load_local_cache(path):
    with open(path, "rb") as f:
        # ok: mois-5-05-unsafe-deserializer-py 네트워크가 아니라 프로그램이 직접 쓴 로컬 캐시 파일
        return pickle.load(f)


def receive_json(conn):
    # ok: mois-5-05-unsafe-deserializer-py
    return json.loads(conn.recv(65536))
