"""다시 대입한 값이 또 None 을 돌려줄 수 있는 호출이면 "다시 대입해서 안전해진" 것이 아니다 (호출 이름마다 한 묶음)."""
import re

from sqlalchemy import select

from .models import Member, mongo

CODE = re.compile(r"[A-Z]{2}-\d{4}")


def then_match(text):
    m = None
    m = re.match(r"(\d+)", text)
    # ruleid: mois-5-01-null-dereference-py
    return m.group(1)


def then_fullmatch(text):
    m = None
    m = CODE.fullmatch(text)
    # ruleid: mois-5-01-null-dereference-py
    return m.group(0)


def then_last(email):
    member = None
    member = Member.objects.filter(email=email).last()
    # ruleid: mois-5-01-null-dereference-py
    return member.name


def then_one_or_none(session, email):
    member = None
    member = session.query(Member).filter_by(email=email).one_or_none()
    # ruleid: mois-5-01-null-dereference-py
    return member.name


def then_scalar_one_or_none(session, email):
    member = None
    member = session.execute(select(Member).where(Member.email == email)).scalar_one_or_none()
    # ruleid: mois-5-01-null-dereference-py
    return member.name


def then_find_one(email):
    doc = None
    doc = mongo.db.members.find_one({"email": email})
    # ruleid: mois-5-01-null-dereference-py
    return doc["name"]
