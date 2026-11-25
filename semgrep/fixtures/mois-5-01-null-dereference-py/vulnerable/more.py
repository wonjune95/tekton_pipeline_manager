import logging
import os
import re
import sys

from bs4 import BeautifulSoup
from flask import Flask, request

from .models import Member, db, mongo

app = Flask(__name__)
logger = logging.getLogger(__name__)
VERSION = re.compile(r"v(\d+)\.(\d+)")


def direct(text, headers, config):
    # ruleid: mois-5-01-null-dereference-py
    a = VERSION.fullmatch(text).groups()
    # ruleid: mois-5-01-null-dereference-py
    b = re.search(r"(\d+)", text)[0]
    # ruleid: mois-5-01-null-dereference-py
    c = headers.get("Content-Type").lower()
    # ruleid: mois-5-01-null-dereference-py
    d = config.get("peers")[0]
    # ruleid: mois-5-01-null-dereference-py
    e = os.getenv("REGION").upper()
    # ruleid: mois-5-01-null-dereference-py
    f = os.getenv("PEERS")[0]
    return a, b, c, d, e, f


def direct_orm(session, email, html):
    # ruleid: mois-5-01-null-dereference-py
    a = session.query(Member).filter_by(email=email).one_or_none().id
    # ruleid: mois-5-01-null-dereference-py
    b = Member.objects.last().name
    # ruleid: mois-5-01-null-dereference-py
    c = Member.query.first().name
    # ruleid: mois-5-01-null-dereference-py
    d = mongo.db.members.find_one({"email": email}).get("name")
    # ruleid: mois-5-01-null-dereference-py
    e = mongo.db.members.find_one({"email": email})["name"]
    # ruleid: mois-5-01-null-dereference-py
    f = BeautifulSoup(html, "html.parser").find("a").get("href")
    return a, b, c, d, e, f


@app.route("/members")
def by_variable():
    page = request.args.get("page")
    # ruleid: mois-5-01-null-dereference-py
    size = page.strip()
    home = os.environ.get("APP_HOME")
    # ruleid: mois-5-01-null-dereference-py
    conf = home.rstrip("/") + "/conf"
    member = db.session.query(Member).filter_by(email=request.args["email"]).one_or_none()
    # ruleid: mois-5-01-null-dereference-py
    name = member.name
    newest = Member.objects.last()
    # ruleid: mois-5-01-null-dereference-py
    joined = newest.joined_at
    oldest = Member.query.first()
    # ruleid: mois-5-01-null-dereference-py
    first_joined = oldest.joined_at
    doc = mongo.db.members.find_one({"email": request.args["email"]})
    # ruleid: mois-5-01-null-dereference-py
    return {"size": size, "conf": conf, "name": name, "joined": joined, "first": first_joined, "doc": doc["name"]}


def check_does_not_exit(email):
    member = Member.objects.filter(email=email).first()
    # None 이어도 기록만 하고 계속 진행한다
    if member is None:
        logger.warning("member not found: %s", email)
    # ruleid: mois-5-01-null-dereference-py
    return member.name


def use_inside_failing_branch(text):
    m = re.match(r"(\d+)", text)
    if m is None:
        # None 인 분기 안에서 쓴다
        # ruleid: mois-5-01-null-dereference-py
        return m.group(0)
    return m.group(1)


def check_joined_with_and(text, strict):
    m = re.match(r"(\d+)", text)
    # strict 가 아니면 None 이어도 통과한다
    if m is None and strict:
        return None
    # ruleid: mois-5-01-null-dereference-py
    return m.group(1)


def nested_conditional_exit(text, strict):
    m = re.match(r"(\d+)", text)
    if m is None:
        if strict:
            return None
    # ruleid: mois-5-01-null-dereference-py
    return m.group(1)


def condition_is_the_dereference(text):
    m = VERSION.search(text)
    # 조건식 자체가 역참조다
    # ruleid: mois-5-01-null-dereference-py
    if m.group(1) == "2":
        # ruleid: mois-5-01-null-dereference-py
        return m.group(2)
    return None


def opposite_branch(text):
    m = VERSION.search(text)
    if m:
        return "ok"
    else:
        # 값이 없는 쪽에서 쓴다
        # ruleid: mois-5-01-null-dereference-py
        return m.group(1)


def opposite_ternary(text):
    m = VERSION.search(text)
    # ruleid: mois-5-01-null-dereference-py
    return None if m else m.group(1)


def exit_without_check(text):
    m = VERSION.search(text)
    if not text:
        sys.exit(1)
    # 다른 값을 검사하고 빠져나갔다
    # ruleid: mois-5-01-null-dereference-py
    return m.group(1)


def reassigned_after_check(text, other):
    m = VERSION.search(text)
    if m is None:
        return None
    # 검사한 뒤에 None 일 수 있는 값으로 다시 대입했다
    m = VERSION.search(other)
    # ruleid: mois-5-01-null-dereference-py
    return m.group(1)


def initialised_then_assigned(email):
    member = None
    member = Member.objects.filter(email=email).first()
    # 처음에 None 으로 둔 변수에 조회 결과를 넣은 것은 "다시 대입해서 안전해진" 것이 아니다
    # ruleid: mois-5-01-null-dereference-py
    return member.name
