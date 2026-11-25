import os
import re
import sys

import requests
from flask import Flask, abort, request

from .models import Member, mongo

app = Flask(__name__)
VERSION = re.compile(r"v(\d+)\.(\d+)")


def guards(text, strict):
    m = VERSION.search(text)
    # ok: mois-5-01-null-dereference-py None 이면 빠져나간다 (다른 조건과 or 로 묶여도 같다)
    if strict or m is None:
        raise ValueError("no version")
    major = m.group(1)
    n = re.match(r"(\d+)", text)
    if not n:
        sys.exit(2)
    # ok: mois-5-01-null-dereference-py
    return major, n.group(1)


def inside_condition(text, strict):
    m = VERSION.search(text)
    if strict and m is not None and text:
        # ok: mois-5-01-null-dereference-py 값이 있을 때만 들어오는 분기
        return m.group(1)
    if m is None:
        value = ""
    else:
        # ok: mois-5-01-null-dereference-py None 검사의 else 쪽
        value = m.group(2)
    # ok: mois-5-01-null-dereference-py 조건식·and
    return value or (m and m.group(1)) or (m.group(2) if m is not None else "")


def loop(lines):
    out = []
    for line in lines:
        m = VERSION.search(line)
        if m is None:
            continue
        # ok: mois-5-01-null-dereference-py None 이면 다음 줄로 넘어갔다
        out.append(m.group(1))
    return out


def asserted(text):
    m = VERSION.search(text)
    assert m is not None, "version missing"
    # ok: mois-5-01-null-dereference-py
    return m.group(1)


def eafp(text):
    m = VERSION.search(text)
    try:
        # ok: mois-5-01-null-dereference-py AttributeError 를 잡아 처리한다
        return m.group(1)
    except AttributeError:
        return None


@app.route("/members/<email>")
def member(email):
    found = Member.query.filter_by(email=email).first()
    if found is None:
        abort(404)
    doc = mongo.db.members.find_one({"email": email}) or {}
    # ok: mois-5-01-null-dereference-py None 이면 abort, 기본값으로 바꾼 dict
    return {"name": found.name, "nick": doc.get("nick", ""), "page": request.args.get("page", "1").strip()}


def http_and_env():
    # ok: mois-5-01-null-dereference-py HTTP 클라이언트의 get 은 None 을 돌려주지 않는다
    body = requests.get("https://api.example.org/v1/health", timeout=3).json()
    region = os.environ.get("REGION")
    region = region or "kr"
    # ok: mois-5-01-null-dereference-py 기본값으로 다시 대입했다
    return body, region.upper()


def default_then_index(email):
    doc = mongo.db.members.find_one({"email": email})
    doc = doc or {"name": ""}
    # ok: mois-5-01-null-dereference-py 기본값으로 다시 대입한 뒤의 [] 접근
    return doc["name"]
