import sqlite3

import pandas as pd
import sqlalchemy
from django.db import connection
from django.db.models.expressions import RawSQL
from flask import Flask, g, request
from sqlalchemy import create_engine, text
from sqlalchemy.sql import text as sql_text
from sqlalchemy.sql.expression import text as expression_text

from .models import Member

app = Flask(__name__)
engine = create_engine("postgresql+psycopg2://app@db/app")


@app.route("/kw/typed")
def typed_apis_by_keyword():
    """질의문을 키워드 인자로 넘겨도 같은 자리다 — "첫 번째 위치 인자"만 보면 통째로 놓친다."""
    name = request.args["name"]
    # ruleid: mois-1-01-sql-injection-py
    a = text(text="SELECT * FROM member WHERE name = '" + name + "'")
    # ruleid: mois-1-01-sql-injection-py
    b = RawSQL(sql="SELECT rank FROM score WHERE name = '" + name + "'", params=[])
    # ruleid: mois-1-01-sql-injection-py
    c = pd.read_sql(sql="SELECT * FROM member WHERE name = '" + name + "'", con=engine)
    # 키워드는 순서와 무관하다
    # ruleid: mois-1-01-sql-injection-py
    d = pd.read_sql_query(con=engine, sql=f"SELECT * FROM member WHERE name = '{name}'")
    # ruleid: mois-1-01-sql-injection-py
    e = Member.objects.raw(raw_query="SELECT * FROM member WHERE name = '" + name + "'")
    return {"n": len(c) + len(d) + len(list(e)), "stmt": str(a), "rank": str(b)}


@app.route("/kw/text")
def sqlalchemy_text_import_paths():
    """sqlalchemy.text 는 sqlalchemy.sql · sqlalchemy.sql.expression 에서도 가져온다. 옛 버전은 text(질의문, bind=…) 로도 부른다."""
    name = request.args["name"]
    # ruleid: mois-1-01-sql-injection-py
    a = text("SELECT * FROM member WHERE name = '" + name + "'", bind=engine)
    # ruleid: mois-1-01-sql-injection-py
    b = sql_text("SELECT * FROM member WHERE name = '" + name + "'")
    # ruleid: mois-1-01-sql-injection-py
    c = sqlalchemy.sql.text(text="SELECT * FROM member WHERE name = '" + name + "'")
    # ruleid: mois-1-01-sql-injection-py
    d = expression_text("SELECT * FROM member WHERE name = '" + name + "'")
    # ruleid: mois-1-01-sql-injection-py
    e = expression_text(text="SELECT * FROM member WHERE name = '" + name + "'")
    return {"stmts": [str(s) for s in (a, b, c, d, e)]}


@app.route("/kw/django")
def django_manager_shapes():
    name = request.args["name"]
    # 매니저 뒤에 다른 호출이 끼어도 raw 는 raw 다
    # ruleid: mois-1-01-sql-injection-py
    a = Member.objects.using("replica").raw("SELECT * FROM member WHERE name = '" + name + "'")
    # extra(where=…) 의 리스트를 변수에 담아 넘김 — 리스트 리터럴이 아니어도 where 는 SQL 조각이다
    conditions = ["name = '" + name + "'"]
    # ruleid: mois-1-01-sql-injection-py
    b = Member.objects.extra(where=conditions)
    # extra(select={별칭: SQL 식}) — 값이 SELECT 절에 그대로 들어간다
    # ruleid: mois-1-01-sql-injection-py
    c = Member.objects.extra(select={"rank": "SELECT rank FROM score WHERE name = '" + name + "'"})
    # extra(tables=…) — 따옴표로 감싼 이름은 다시 인용하지 않고 FROM 절에 그대로 들어간다
    # ruleid: mois-1-01-sql-injection-py
    d = Member.objects.extra(tables=[request.args["table"]])
    # extra(order_by=…) — "표.컬럼" 꼴은 점 뒤를 그대로 ORDER BY 에 넣는다
    # ruleid: mois-1-01-sql-injection-py
    e = Member.objects.extra(order_by=["member." + request.args["sort"]])
    # extra 를 위치 인자로: extra(select, where, params, …)
    # ruleid: mois-1-01-sql-injection-py
    f = Member.objects.extra({"rank": "SELECT rank FROM score WHERE name = '" + name + "'"})
    # ruleid: mois-1-01-sql-injection-py
    h = Member.objects.filter(active=True).extra(None, ["name = '" + name + "'"])
    return {"n": sum(len(list(q)) for q in (a, b, c, d, e, f, h))}


@app.route("/kw/execute")
def execute_by_keyword():
    """execute 의 질의문 키워드 이름은 드라이버마다 다르다 (query · operation · statement · sql …)."""
    name = request.args["name"]
    link = sqlite3.connect("/srv/app.db")
    cur = link.cursor()
    # ruleid: mois-1-01-sql-injection-py
    cur.execute(query="SELECT * FROM member WHERE name = '" + name + "'")
    # 바인딩 인자를 함께 넘겨도 질의문에 이어 붙인 입력은 그대로다
    # ruleid: mois-1-01-sql-injection-py
    cur.execute(operation="SELECT * FROM member WHERE dept = %s AND name = '" + name + "'", params=(1,))
    # ruleid: mois-1-01-sql-injection-py
    connection.cursor().execute(sql="SELECT * FROM member WHERE name = '%s'" % name)
    # ruleid: mois-1-01-sql-injection-py
    g.session.execute(statement="SELECT * FROM member WHERE name = '" + name + "'")
    return {"ok": True}
