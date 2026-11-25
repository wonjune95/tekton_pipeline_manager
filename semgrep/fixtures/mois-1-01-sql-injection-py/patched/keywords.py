import sqlite3

import pandas as pd
from django.db.models.expressions import RawSQL
from flask import Flask, g, request
from sqlalchemy import create_engine, text

from .codecs import wire
from .models import Member

app = Flask(__name__)
engine = create_engine("postgresql+psycopg2://app@db/app")


@app.route("/kw/typed")
def typed_apis_by_keyword():
    name = request.args["name"]
    # ok: mois-1-01-sql-injection-py 질의문은 고정, 입력은 바인딩 인자(params)로만 전달
    a = RawSQL(sql="SELECT rank FROM score WHERE name = %s", params=[name])
    # ok: mois-1-01-sql-injection-py
    b = pd.read_sql(sql="SELECT * FROM member WHERE name = %(name)s", con=engine, params={"name": name})
    # ok: mois-1-01-sql-injection-py
    c = Member.objects.raw(raw_query="SELECT * FROM member WHERE name = %s", params=[name])
    # ok: mois-1-01-sql-injection-py extra 의 params · select_params 는 바인딩 값이다
    d = Member.objects.extra(select={"hit": "name = %s"}, select_params=(name,))
    # ok: mois-1-01-sql-injection-py extra 의 세 번째 위치 인자도 params 다
    e = Member.objects.extra(None, ["name = %s"], [name])
    # ok: mois-1-01-sql-injection-py Django 매니저가 아닌 객체의 raw() 는 질의 실행이 아니다
    f = wire.raw(request.args["payload"])
    return {"n": len(b) + len(list(c)) + len(list(d)) + len(list(e)), "rank": str(a), "wire": len(f)}


@app.route("/kw/execute")
def execute_by_keyword():
    name = request.args["name"]
    with sqlite3.connect("/srv/app.db") as link:
        cur = link.cursor()
        # 키워드로만 부를 때 바인딩 인자로 인정하는 이름: …param…(params · parameters · seq_params), vars…(vars · vars_list), args, values
        # ok: mois-1-01-sql-injection-py psycopg2 execute(query, vars)
        cur.execute(query="SELECT * FROM member WHERE name = %s", vars=(name,))
        # ok: mois-1-01-sql-injection-py PyMySQL execute(query, args)
        cur.execute(query="SELECT * FROM member WHERE name = %s", args=(name,))
        # ok: mois-1-01-sql-injection-py SQLAlchemy execute(statement, parameters)
        link.execute(statement=text("SELECT * FROM member WHERE name = :name"), parameters={"name": name})
        # ok: mois-1-01-sql-injection-py databases execute(query, values)
        g.db.execute(query="SELECT * FROM member WHERE name = :name", values={"name": name})
        # ok: mois-1-01-sql-injection-py 질의문이 위치 인자면 나머지 키워드는 바인딩 값이다 (oracledb 의 이름 붙인 바인딩)
        cur.execute("SELECT * FROM member WHERE name = :name", name=name)
    return {"ok": True}
