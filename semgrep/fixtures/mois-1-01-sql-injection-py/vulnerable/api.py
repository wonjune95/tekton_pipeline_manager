from fastapi import Depends, FastAPI
from sqlalchemy import text
from sqlalchemy.orm import Session

from .db import get_db

app = FastAPI()


@app.get("/orders")
def orders(status: str, db: Session = Depends(get_db)):
    # f-string 으로 만든 질의문
    # ruleid: mois-1-01-sql-injection-py
    rows = db.execute(text(f"SELECT id FROM orders WHERE status = '{status}'")).all()
    return {"count": len(rows)}
