import sqlite3

import pandas as pd
from django.db.models.expressions import RawSQL
from flask import Flask, request
from sqlalchemy import create_engine, text

from .models import Member

app = Flask(__name__)
engine = create_engine("postgresql+psycopg2://app@db/app")
ORDER_COLUMNS = {"name": "name", "joined": "joined_at"}


@app.route("/bound")
def bound_parameters():
    name = request.args["name"]
    with sqlite3.connect("/srv/app.db") as link:
        # ok: mois-1-01-sql-injection-py 값은 바인딩 매개변수로 전달
        link.execute("SELECT * FROM member WHERE name = ?", (name,))
    # ok: mois-1-01-sql-injection-py
    stmt = text("SELECT * FROM member WHERE name = :name").bindparams(name=name)
    # ok: mois-1-01-sql-injection-py
    annotated = Member.objects.annotate(rank=RawSQL("SELECT rank FROM score WHERE name = %s", [name]))
    # ok: mois-1-01-sql-injection-py
    filtered = Member.objects.extra(where=["name = %s"], params=[name])
    # ok: mois-1-01-sql-injection-py
    frame = pd.read_sql("SELECT * FROM member WHERE name = %(name)s", engine, params={"name": name})
    # ok: mois-1-01-sql-injection-py
    members = Member.objects.raw("SELECT * FROM member WHERE name = %s", [name])
    return {"n": len(frame) + len(list(members)), "stmt": str(stmt), "q": str(annotated.query) + str(filtered.query)}


@app.route("/sorted")
def sorted_list():
    # ok: mois-1-01-sql-injection-py 정렬 컬럼은 같은 파일의 dict 에서 고른다 (식별자는 바인딩할 수 없으므로)
    column = ORDER_COLUMNS.get(request.args.get("sort", "name"))
    if column is None:
        return {"error": "unknown sort"}, 400
    with engine.connect() as conn:
        rows = conn.execute(text("SELECT id, name FROM member ORDER BY " + column)).all()
    return {"n": len(rows)}
