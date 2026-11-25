import sqlite3

import pandas as pd
import psycopg2
from django.db import connection
from django.db.models.expressions import RawSQL
from flask import Flask, g, request
from sqlalchemy import create_engine, text

from .models import Member

app = Flask(__name__)
engine = create_engine("postgresql+psycopg2://app@db/app")


@app.route("/typed")
def typed_apis():
    name = request.args["name"]
    # SQLAlchemy text() — 어디에 넘기든 질의문이 된다
    # ruleid: mois-1-01-sql-injection-py
    stmt = text("SELECT * FROM member WHERE name = '%s'" % name)
    # Django RawSQL·extra(where=[…])
    # ruleid: mois-1-01-sql-injection-py
    annotated = Member.objects.annotate(rank=RawSQL("SELECT rank FROM score WHERE name = '" + name + "'", []))
    # ruleid: mois-1-01-sql-injection-py
    filtered = Member.objects.extra(where=["name = '" + name + "'"])
    # pandas
    # ruleid: mois-1-01-sql-injection-py
    frame = pd.read_sql("SELECT * FROM member WHERE name = '" + name + "'", engine)
    # ruleid: mois-1-01-sql-injection-py
    frame2 = pd.read_sql_query(f"SELECT * FROM member WHERE name = '{name}'", engine)
    return {"n": len(frame) + len(frame2), "stmt": str(stmt), "q": str(annotated.query) + str(filtered.query)}


@app.route("/created")
def created_in_this_function():
    name = request.args["name"]
    # .connect(...) 로 만든 객체 (이름과 무관)
    link = sqlite3.connect("/srv/app.db")
    # ruleid: mois-1-01-sql-injection-py
    link.execute("SELECT * FROM member WHERE name = '" + name + "'")
    # .cursor() 로 만든 객체
    c = link.cursor()
    # ruleid: mois-1-01-sql-injection-py
    c.executescript("DELETE FROM audit WHERE who = '" + name + "'; VACUUM;")
    # with … .cursor() as …
    with psycopg2.connect("dbname=app") as pg:
        # ruleid: mois-1-01-sql-injection-py
        pg.execute(f"SELECT 1 FROM member WHERE name = '{name}'")
        with pg.cursor() as handle:
            # ruleid: mois-1-01-sql-injection-py
            handle.executemany("INSERT INTO log(who) VALUES ('" + name + "')", [()])
    # 커서를 만들자마자 실행
    # ruleid: mois-1-01-sql-injection-py
    connection.cursor().execute("SELECT * FROM member WHERE name = '%s'" % name)
    return {"ok": True}


@app.route("/named")
def named_handles():
    name = request.args["name"]
    # 이름이 DB 핸들인 객체 (만든 곳은 보이지 않음)
    # ruleid: mois-1-01-sql-injection-py
    g.db.execute("SELECT * FROM member WHERE name = '" + name + "'")
    # ruleid: mois-1-01-sql-injection-py
    rows = engine.execute("SELECT * FROM member WHERE name = '" + name + "'")
    return {"n": len(list(rows))}


class MemberRepository:
    def __init__(self, session, conn):
        self.session = session
        self._conn = conn

    def search(self, request):
        keyword = request.GET["q"]
        # ruleid: mois-1-01-sql-injection-py
        self.session.execute("SELECT * FROM member WHERE name LIKE '%" + keyword + "%'")
        # 바인딩 인자가 있어도 질의문 자체에 입력을 이어 붙이면 탐지
        # ruleid: mois-1-01-sql-injection-py
        self._conn.execute("SELECT * FROM member WHERE dept = ? AND name = '" + keyword + "'", (1,))


class AuditRepository:
    def __init__(self, cursor, connection):
        self.cursor = cursor
        self.connection = connection

    def by_actor(self, request):
        actor = request.GET.get("actor", "")
        # 만든 곳은 보이지 않지만 이름이 cursor·connection 인 객체
        # ruleid: mois-1-01-sql-injection-py
        self.cursor.execute("SELECT * FROM audit WHERE actor = '" + actor + "'")
        # ruleid: mois-1-01-sql-injection-py
        self.connection.execute("DELETE FROM audit_cache WHERE actor = '" + actor + "'")
        return self.cursor.fetchall()


@app.route("/audit/count")
def audit_count():
    actor = request.args["actor"]
    # 요청마다 g 에 넣어 둔 커서 (이름 cur)
    # ruleid: mois-1-01-sql-injection-py
    g.cur.execute("SELECT count(*) FROM audit WHERE actor = '%s'" % actor)
    return {"count": g.cur.fetchone()[0]}
