import re
import xml.etree.ElementTree as ET

import flask
from bs4 import BeautifulSoup
from sqlalchemy import select

from .models import Member

VERSION = re.compile(r"v(?P<major>\d+)\.(?P<minor>\d+)")


def direct_regex(text):
    # ruleid: mois-5-01-null-dereference-py
    parts = VERSION.search(text).groupdict()
    # ruleid: mois-5-01-null-dereference-py
    begin = VERSION.match(text).start()
    # ruleid: mois-5-01-null-dereference-py
    finish = VERSION.match(text).end()
    # ruleid: mois-5-01-null-dereference-py
    where = VERSION.match(text).span()
    # ruleid: mois-5-01-null-dereference-py
    major = re.match(r"v(\d+)", text)[1]
    # ruleid: mois-5-01-null-dereference-py
    whole = re.fullmatch(r"v\d+\.\d+", text)[0]
    return parts, begin, finish, where, major, whole


def direct_scalar(session, email):
    # ruleid: mois-5-01-null-dereference-py
    return session.execute(select(Member).where(Member.email == email)).scalar_one_or_none().id


def direct_xml(body):
    root = ET.fromstring(body)
    # ruleid: mois-5-01-null-dereference-py
    tail = root.find("item").tail
    # ruleid: mois-5-01-null-dereference-py
    tag = root.find("item").tag
    # ruleid: mois-5-01-null-dereference-py
    item_id = root.find("item").attrib["id"]
    # ruleid: mois-5-01-null-dereference-py
    title = root.find("channel").find("title")
    # ruleid: mois-5-01-null-dereference-py
    items = root.find("channel").findall("item")
    return tail, tag, item_id, title, items


def direct_html(html):
    soup = BeautifulSoup(html, "html.parser")
    # ruleid: mois-5-01-null-dereference-py
    attrs = soup.find("a").attrs
    # ruleid: mois-5-01-null-dereference-py
    title = soup.find("title").string
    # ruleid: mois-5-01-null-dereference-py
    body = soup.find("article").get_text()
    # ruleid: mois-5-01-null-dereference-py
    rows = soup.find("table").find_all("tr")
    return attrs, title, body, rows


def re_module_then_index(text):
    a = re.match(r"v(\d+)", text)
    b = re.search(r"(\d+)", text)
    c = re.fullmatch(r"v(?P<major>\d+)", text)
    # 매치 객체의 [] 접근도 None 이면 TypeError 다
    # ruleid: mois-5-01-null-dereference-py
    major = a[1]
    # ruleid: mois-5-01-null-dereference-py
    number = b[0]
    # ruleid: mois-5-01-null-dereference-py
    return major, number, c["major"]


def compiled_then_method(text):
    a = VERSION.match(text)
    # ruleid: mois-5-01-null-dereference-py
    groups = a.groups()
    b = VERSION.fullmatch(text)
    # ruleid: mois-5-01-null-dereference-py
    named = b.groupdict()
    c = VERSION.search(text)
    # ruleid: mois-5-01-null-dereference-py
    begin = c.start()
    # ruleid: mois-5-01-null-dereference-py
    finish = c.end()
    # ruleid: mois-5-01-null-dereference-py
    where = c.span()
    return groups, named, begin, finish, where


def handler(req):
    page = req.args.get("page")
    # ruleid: mois-5-01-null-dereference-py
    return page.strip()


def flask_module_handler():
    page = flask.request.args.get("page")
    # ruleid: mois-5-01-null-dereference-py
    return page.strip()


class MemberView:
    def get(self):
        keyword = self.request.GET.get("q")
        # ruleid: mois-5-01-null-dereference-py
        return keyword.lower()


def scalar_by_variable(session, email):
    member = session.execute(select(Member).where(Member.email == email)).scalar_one_or_none()
    # ruleid: mois-5-01-null-dereference-py
    return member.id
