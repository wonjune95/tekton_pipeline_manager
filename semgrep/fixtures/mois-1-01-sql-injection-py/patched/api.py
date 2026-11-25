from fastapi import Depends, FastAPI
from sqlalchemy import text
from sqlalchemy.orm import Session

from .db import get_db

app = FastAPI()


@app.get("/orders")
def orders(status: str, db: Session = Depends(get_db)):
    # ok: mois-1-01-sql-injection-py 값은 바인딩 매개변수로 전달
    rows = db.execute(text("SELECT id FROM orders WHERE status = :status"), {"status": status}).all()
    return {"count": len(rows)}
