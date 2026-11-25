import pickle
import socket

import requests
import torch
import yaml


def load_settings(path):
    with open(path, encoding="utf-8") as f:
        # ruleid: mois-5-05-unsafe-deserializer-py
        return yaml.load(f, Loader=yaml.UnsafeLoader)  # 임의 객체를 만드는 Loader


def load_legacy(text):
    # ruleid: mois-5-05-unsafe-deserializer-py
    return yaml.unsafe_load(text)  # 임의 객체 생성 허용


def load_model(path):
    # ruleid: mois-5-05-unsafe-deserializer-py
    return torch.load(path)  # weights_only 없이 pickle 로 읽음


def receive_job(host, port):
    with socket.create_connection((host, port), timeout=5) as conn:
        # ruleid: mois-5-05-unsafe-deserializer-py
        return pickle.loads(conn.recv(65536))  # 소켓으로 받은 데이터를 pickle 로 역직렬화


def fetch_snapshot(url):
    resp = requests.get(url, timeout=5)
    data = resp.content
    # ruleid: mois-5-05-unsafe-deserializer-py
    return pickle.loads(data)  # HTTP 로 받은 데이터를 pickle 로 역직렬화
