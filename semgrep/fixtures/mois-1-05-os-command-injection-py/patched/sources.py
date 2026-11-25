"""공통 source 블록이 외부 입력으로 보지 않는 것 — 프레임워크가 넣어 주는 객체와 숫자형 매개변수."""
import subprocess
from typing import Annotated

from fastapi import Depends, FastAPI, Path
from sqlalchemy.orm import Session

from .database import get_db
from .deps import CurrentUser, SessionDep

app = FastAPI()


@app.get("/me/quota")
def my_quota(current_user: CurrentUser):
    # ok: mois-1-05-os-command-injection-py 의존성 별칭(Current…)으로 주입된 로그인 사용자 객체
    out = subprocess.check_output("quota -u " + current_user.login, shell=True)
    return {"out": out.decode()}


@app.post("/db/vacuum")
def vacuum(session: SessionDep):
    # ok: mois-1-05-os-command-injection-py 의존성 별칭(…Dep)으로 주입된 DB 세션
    subprocess.run("vacuumdb " + session.bind.url.database, shell=True, check=False)
    return {"ok": True}


@app.post("/db/dump")
def dump(db: Annotated[Session, Depends(get_db)]):
    # ok: mois-1-05-os-command-injection-py Annotated[..., Depends(...)] 로 주입된 객체
    subprocess.run("pg_dump " + db.bind.url.database, shell=True, check=False)
    return {"ok": True}


@app.get("/logs/{n}")
def tail(n: Annotated[int, Path()]):
    # ok: mois-1-05-os-command-injection-py 정수형 경로 매개변수
    out = subprocess.check_output(f"tail -n {n} /var/log/app/app.log", shell=True)
    return {"out": out.decode()}

