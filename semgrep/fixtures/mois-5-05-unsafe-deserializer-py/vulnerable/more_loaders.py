import pickle
import socket
import urllib.request

import numpy as np
import requests
import yaml
from yaml import CLoader, Loader


def load_pipeline(path):
    with open(path, encoding="utf-8") as f:
        # Loader 를 주지 않은 yaml.load
        # ruleid: mois-5-05-unsafe-deserializer-py
        return yaml.load(f)


def load_documents(text):
    # ruleid: mois-5-05-unsafe-deserializer-py
    a = list(yaml.load_all(text))
    # ruleid: mois-5-05-unsafe-deserializer-py
    b = list(yaml.unsafe_load_all(text))
    # 위치 인자로 준 Loader
    # ruleid: mois-5-05-unsafe-deserializer-py
    c = yaml.load(text, Loader)
    # ruleid: mois-5-05-unsafe-deserializer-py
    d = list(yaml.load_all(text, Loader=CLoader))
    return a, b, c, d


def load_arrays(path):
    # ruleid: mois-5-05-unsafe-deserializer-py
    return np.load(path, allow_pickle=True)


def receive_datagram(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("0.0.0.0", port))
    # ruleid: mois-5-05-unsafe-deserializer-py
    return pickle.loads(sock.recvfrom(65536)[0])


def receive_stream(conn):
    # ruleid: mois-5-05-unsafe-deserializer-py
    return pickle.load(conn.makefile("rb"))


def fetch_direct(url):
    # ruleid: mois-5-05-unsafe-deserializer-py
    return pickle.loads(requests.get(url, timeout=5).content)


def fetch_urllib(url):
    # ruleid: mois-5-05-unsafe-deserializer-py
    a = pickle.loads(urllib.request.urlopen(url).read())
    # ruleid: mois-5-05-unsafe-deserializer-py
    b = pickle.load(urllib.request.urlopen(url))
    return a, b


def receive_buffered(conn):
    payload = conn.recv(1 << 20)
    # 변수에 담았다가 읽는 경우
    # ruleid: mois-5-05-unsafe-deserializer-py
    return pickle.loads(payload)
