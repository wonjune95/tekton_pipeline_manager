import re
import sys

import flask

from .models import Member

VERSION = re.compile(r"v(\d+)\.(\d+)")


def then_branches(text, strict):
    m = VERSION.search(text)
    out = []
    # ok: mois-5-01-null-dereference-py 아래 if 들은 모두 값이 있을 때만 들어가는 분기다
    if m:
        out.append(m.group(1))
    if m is not None:
        out.append(m.group(1))
    if m and strict:
        out.append(m.group(1))
    if strict and m:
        out.append(m.group(1))
    if strict and m and text:
        out.append(m.group(1))
    if m is not None and strict:
        out.append(m.group(1))
    if strict and m is not None:
        out.append(m.group(1))
    return out


def scan_all(text):
    out = []
    m = VERSION.search(text)
    # ok: mois-5-01-null-dereference-py 값이 있는 동안만 돈다
    while m:
        out.append(m.group(1))
        m = VERSION.search(text, m.end())
    n = VERSION.search(text)
    while n is not None:
        out.append(n.group(2))
        n = VERSION.search(text, n.end())
    return out


def else_of_not(text):
    m = VERSION.search(text)
    if not m:
        value = ""
    else:
        # ok: mois-5-01-null-dereference-py 없는 경우의 else 쪽
        value = m.group(1)
    return value


def expressions(text, strict):
    m = VERSION.search(text)
    # ok: mois-5-01-null-dereference-py None 이면 else 쪽을 계산하지 않는다
    a = "" if m is None else m.group(1)
    b = "" if not m else m.group(2)
    # ok: mois-5-01-null-dereference-py and·or 의 단락 평가
    c = strict and m and m.group(1)
    d = m is not None and m.group(1)
    e = m is None or m.group(1) == "0"
    f = not m or m.group(2) == "0"
    return a, b, c, d, e, f


def asserted_plain(text):
    m = VERSION.search(text)
    assert m
    # ok: mois-5-01-null-dereference-py
    return m.group(1)


def first_valid(lines):
    out = []
    for line in lines:
        m = VERSION.search(line)
        if m is None:
            break
        # ok: mois-5-01-null-dereference-py None 이면 반복을 끝냈다
        out.append(m.group(1))
    return out


def exits(text, email):
    m = re.match(r"v(\d+)", text)
    if m is None:
        sys.exit(2)
    found = Member.query.filter_by(email=email).first()
    if found is None:
        flask.abort(404)
    # ok: mois-5-01-null-dereference-py None 이면 프로세스·요청을 끝냈다 (import 로 확인되는 sys.exit · flask.abort)
    return m.group(1), found.name


def index_after_guard(text):
    m = re.match(r"v(\d+)", text)
    if m is None:
        return None
    # ok: mois-5-01-null-dereference-py None 이면 빠져나갔다
    return m[1]


def eafp_else(text):
    m = VERSION.search(text)
    try:
        # ok: mois-5-01-null-dereference-py AttributeError 를 잡아 처리한다 (else 가 붙은 try)
        major = m.group(1)
    except (AttributeError, TypeError):
        return None
    else:
        return int(major)


def eafp_finally(text, log):
    m = VERSION.search(text)
    try:
        # ok: mois-5-01-null-dereference-py finally 가 붙은 try
        return m.group(1)
    except AttributeError as e:
        log.warning("no version: %s", type(e).__name__)
        return None
    finally:
        log.debug("parsed")


def eafp_else_finally(text, log):
    m = VERSION.search(text)
    try:
        # ok: mois-5-01-null-dereference-py else·finally 가 모두 붙은 try
        major = m.group(1)
    except AttributeError:
        major = None
    else:
        log.debug("major=%s", major)
    finally:
        log.debug("parsed")
    return major
