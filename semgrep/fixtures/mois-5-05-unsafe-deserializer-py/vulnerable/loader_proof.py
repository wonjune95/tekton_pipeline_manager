import pickle

import numpy as np
import torch
import yaml
import yaml.loader
from yaml import FullLoader
from yaml import UnsafeLoader as UL


class PluginLoader(yaml.Loader):
    """yaml.Loader 를 상속 — 이름에 Unsafe 가 없어도 임의 객체를 만든다"""


class TaggedSafeLoader(yaml.SafeLoader):
    """SafeLoader 를 상속했지만 생성자를 더할 수 있다"""


def load_plugins(text, safe, **options):
    # 위험한 이름 목록에 없다고 안전한 것이 아니다
    # ruleid: mois-5-05-unsafe-deserializer-py
    a = yaml.load(text, Loader=PluginLoader)
    # import 별칭
    # ruleid: mois-5-05-unsafe-deserializer-py
    b = yaml.load(text, Loader=UL)
    # 하위 모듈 경로
    # ruleid: mois-5-05-unsafe-deserializer-py
    c = yaml.load(text, yaml.loader.UnsafeLoader)
    # ruleid: mois-5-05-unsafe-deserializer-py
    d = yaml.load(text, Loader=getattr(yaml, "CLoader", yaml.Loader))
    # 변수에 담은 Loader
    loader = yaml.Loader
    # ruleid: mois-5-05-unsafe-deserializer-py
    e = yaml.load(text, Loader=loader)
    # 식 안에 SafeLoader 가 들어 있을 뿐이다
    # ruleid: mois-5-05-unsafe-deserializer-py
    f = yaml.load(text, Loader=yaml.SafeLoader if safe else yaml.Loader)
    # ruleid: mois-5-05-unsafe-deserializer-py
    g = list(yaml.load_all(text, Loader=TaggedSafeLoader))
    # ruleid: mois-5-05-unsafe-deserializer-py
    h = yaml.load(text, **options)
    # 키워드 인자만 쓴 호출
    # ruleid: mois-5-05-unsafe-deserializer-py
    i = yaml.load(stream=text, Loader=yaml.Loader)
    # ruleid: mois-5-05-unsafe-deserializer-py
    j = yaml.load(stream=text)
    return a, b, c, d, e, f, g, h, i, j


def load_full(text):
    # FullLoader 는 SafeLoader 가 아니다 (PyYAML 5.4 미만은 임의 코드 실행: CVE-2020-1747, CVE-2020-14343)
    # ruleid: mois-5-05-unsafe-deserializer-py
    a = yaml.load(text, Loader=FullLoader)
    # ruleid: mois-5-05-unsafe-deserializer-py
    b = yaml.full_load(text)
    # ruleid: mois-5-05-unsafe-deserializer-py
    c = list(yaml.full_load_all(text))
    return a, b, c


def load_arrays(path, trusted, **options):
    # allow_pickle 이 False 로 확인되지 않는다
    # ruleid: mois-5-05-unsafe-deserializer-py
    a = np.load(path, allow_pickle=trusted)
    # 세 번째 위치 인자가 allow_pickle 이다
    # ruleid: mois-5-05-unsafe-deserializer-py
    b = np.load(path, None, True)
    # ruleid: mois-5-05-unsafe-deserializer-py
    c = np.load(path, **options)
    # ruleid: mois-5-05-unsafe-deserializer-py
    d = torch.load(f=path, weights_only=trusted)
    return a, b, c, d


def receive_stream(conn):
    # 키워드 인자로 넘긴 소켓 파일
    # ruleid: mois-5-05-unsafe-deserializer-py
    return pickle.load(file=conn.makefile("rb"))


def receive_buffered(conn):
    stream = conn.makefile("rb")
    # ruleid: mois-5-05-unsafe-deserializer-py
    return pickle.load(file=stream)
