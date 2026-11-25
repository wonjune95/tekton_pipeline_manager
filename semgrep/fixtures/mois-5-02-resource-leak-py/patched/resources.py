import atexit
import gzip
import socket
import sqlite3
import tarfile
import urllib.request
import zipfile
from contextlib import ExitStack, closing

import psycopg2
import pymysql


def read_gzip(path):
    # ok: mois-5-02-resource-leak-py with 문
    with gzip.open(path, "rt") as f:
        return f.read()


def list_archives(path):
    tar = tarfile.open(path + ".tar.gz")
    zf = zipfile.ZipFile(path + ".zip")
    # ok: mois-5-02-resource-leak-py 연 뒤에 with 로 감싼다
    with tar, zf:
        return tar.getnames() + zf.namelist()


def probe(host, port, url):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((host, port))
    finally:
        # ok: mois-5-02-resource-leak-py finally 에서 닫는다
        sock.close()
    # ok: mois-5-02-resource-leak-py closing() 으로 감싼다
    resp = urllib.request.urlopen(url, timeout=3)
    with closing(resp):
        return resp.status


def open_connection(dsn):
    # ok: mois-5-02-resource-leak-py 연결을 돌려주면 닫는 것은 받는 쪽 몫
    conn = psycopg2.connect(dsn)
    conn.autocommit = True
    return conn


def stream_rows(dsn):
    conn = pymysql.connect(host="db", user="app", database="portal")
    try:
        # ok: mois-5-02-resource-leak-py 제너레이터가 끝나면 finally 에서 닫는다
        yield from conn.cursor()
    finally:
        conn.close()


class Exporter:
    def __init__(self, path):
        # ok: mois-5-02-resource-leak-py 필드에 보관 (close() 메서드에서 닫는다)
        fh = open(path, "w", encoding="utf-8")
        self.fh = fh

    def close(self):
        self.fh.close()


def open_many(paths):
    stack = ExitStack()
    files = []
    for path in paths:
        # ok: mois-5-02-resource-leak-py ExitStack 이 닫는다
        f = open(path, encoding="utf-8")
        stack.enter_context(f)
        files.append(f)
    return stack, files


def open_log(path):
    # ok: mois-5-02-resource-leak-py 프로세스 종료 때 닫도록 등록
    log = open(path, "a", encoding="utf-8")
    atexit.register(log.close)
    log.write("started\n")


def open_with_callback(path, stack):
    # ok: mois-5-02-resource-leak-py ExitStack.callback 으로 닫는다
    f = open(path, encoding="utf-8")
    stack.callback(f.close)
    return f.readline()


def checksum_all(paths):
    total = 0
    for path in paths:
        # ok: mois-5-02-resource-leak-py 연 뒤에 with 로 감싼다 (반복문 안)
        fh = open(path, "rb")
        with fh:
            total += len(fh.read())
    return total


def tail_log(path):
    try:
        # ok: mois-5-02-resource-leak-py try 안에서 열고 finally 에서 닫는다
        log = open(path, encoding="utf-8")
        return log.readlines()[-10:]
    finally:
        log.close()


def temp_database(path):
    # ok: mois-5-02-resource-leak-py 제너레이터로 넘겨준 쪽(fixture·의존성 주입)이 끝나면 닫는다
    conn = sqlite3.connect(path)
    yield conn
    conn.close()
