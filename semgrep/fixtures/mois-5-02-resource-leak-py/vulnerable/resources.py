import codecs
import gzip
import io
import socket
import tarfile
import urllib.request
import zipfile

import cx_Oracle
import MySQLdb
import oracledb
import psycopg2
import pymysql


def read_files(path):
    # ruleid: mois-5-02-resource-leak-py
    a = io.open(path, encoding="utf-8")
    # ruleid: mois-5-02-resource-leak-py
    b = codecs.open(path, "r", "euc-kr")
    # ruleid: mois-5-02-resource-leak-py
    c = gzip.open(path + ".gz", "rt")
    return a.read() + b.read() + c.read()


def list_archives(path):
    # ruleid: mois-5-02-resource-leak-py
    tar = tarfile.open(path + ".tar.gz")
    # ruleid: mois-5-02-resource-leak-py
    zf = zipfile.ZipFile(path + ".zip")
    return tar.getnames() + zf.namelist()


def probe(host, port, url):
    # ruleid: mois-5-02-resource-leak-py
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    # ruleid: mois-5-02-resource-leak-py
    resp = urllib.request.urlopen(url, timeout=3)
    return resp.status


def count_members(dsn):
    # ruleid: mois-5-02-resource-leak-py
    pg = psycopg2.connect(dsn)
    # ruleid: mois-5-02-resource-leak-py
    my = pymysql.connect(host="db", user="app", database="portal")
    # ruleid: mois-5-02-resource-leak-py
    legacy = MySQLdb.connect(host="db", user="app", db="portal")
    # ruleid: mois-5-02-resource-leak-py
    ora = cx_Oracle.connect(dsn=dsn)
    # ruleid: mois-5-02-resource-leak-py
    ora2 = oracledb.connect(dsn=dsn)
    return [c.cursor() for c in (pg, my, legacy, ora, ora2)]


def close_only_on_error(path):
    # 예외가 났을 때만 닫는다 — 정상 흐름에서는 열린 채로 남는다
    # ruleid: mois-5-02-resource-leak-py
    f = open(path, encoding="utf-8")
    try:
        return f.read()
    except UnicodeDecodeError:
        f.close()
        return ""


def close_other_resource(src, dst):
    # ruleid: mois-5-02-resource-leak-py
    fin = open(src, "rb")
    fout = open(dst, "wb")
    try:
        fout.write(fin.read())
    finally:
        # 다른 자원만 닫는다
        fout.close()


def with_other_resource(src, dst):
    # ruleid: mois-5-02-resource-leak-py
    fin = open(src, "rb")
    fout = open(dst, "wb")
    with fout:
        fout.write(fin.read())
