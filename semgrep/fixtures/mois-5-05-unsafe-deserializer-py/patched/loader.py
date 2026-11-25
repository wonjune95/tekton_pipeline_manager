import json
import socket

import requests
import torch
import yaml


def load_settings(path):
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_legacy(text):
    return yaml.load(text, Loader=yaml.SafeLoader)


def load_model(path):
    return torch.load(path, weights_only=True)


def receive_job(host, port):
    with socket.create_connection((host, port), timeout=5) as conn:
        return json.loads(conn.recv(65536))


def fetch_snapshot(url):
    resp = requests.get(url, timeout=5)
    resp.raise_for_status()
    return resp.json()
