# 공통 source 블록 시험 (감사 사례). `# CASE` 표시만 있고 ruleid 가 없는 줄은 알려진 미탐 — 공통 source 가 보지 않는 형태다.
import os
from typing import Annotated

from fastapi import APIRouter, Body, Depends, FastAPI, Header, Path, Query, Request, UploadFile, WebSocket
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBasic,
    HTTPBasicCredentials,
    HTTPBearer,
    OAuth2PasswordBearer,
    OAuth2PasswordRequestForm,
)
from fastapi_cache.decorator import cache
from pydantic import BaseModel
from starlette.requests import HTTPConnection

from . import schemas

app = FastAPI()
router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
basic = HTTPBasic()
bearer = HTTPBearer()


class WebhookConfig(BaseModel):
    url: str


class ApiClient(BaseModel):
    name: str


class CurrentAddress(BaseModel):
    street: str


class UserSettings(BaseModel):
    theme: str


class GitRepo(BaseModel):
    url: str


class LoginSession(BaseModel):
    device: str


class PrintService(BaseModel):
    printer: str


class FilterParams(BaseModel):
    q: str


class Item(BaseModel):
    name: str


def common_parameters(q: str | None = None):
    return {"q": q}


@app.get("/c1")
def ctl_str(cmd: str):
    # ruleid: mois-1-05-os-command-injection-py — ctl-fastapi-str
    os.system(cmd)


@router.api_route("/c2", methods=["GET"])
def ctl_api_route(cmd: str):
    # ruleid: mois-1-05-os-command-injection-py — ctl-fastapi-api_route
    os.system(cmd)


@app.get("/c3")
async def ctl_async(cmd: str):
    # ruleid: mois-1-05-os-command-injection-py — ctl-fastapi-async
    os.system(cmd)


@router.get("/c4")
@cache(expire=60)
async def ctl_stacked(cmd: str):
    # ruleid: mois-1-05-os-command-injection-py — ctl-fastapi-stacked-decorator
    os.system(cmd)


@app.post("/c5")
def ctl_body_model(item: Item):
    # ruleid: mois-1-05-os-command-injection-py — ctl-fastapi-body-model-Item
    os.system(item.name)


@app.post("/c6")
def ctl_annotated_body(cfg: Annotated[WebhookConfig, Body()]):
    # ruleid: mois-1-05-os-command-injection-py — ctl-fastapi-Annotated[WebhookConfig,Body()]
    os.system("curl " + cfg.url)


@app.post("/c7")
def ctl_qualified(cfg: schemas.WebhookConfig):
    # ruleid: mois-1-05-os-command-injection-py — ctl-fastapi-schemas.WebhookConfig
    os.system("curl " + cfg.url)


@app.get("/c8")
def ctl_header(x_cmd: Annotated[str, Header()]):
    # ruleid: mois-1-05-os-command-injection-py — ctl-fastapi-Annotated-Header
    os.system(x_cmd)


@app.post("/c9")
def ctl_upload(file: UploadFile):
    # ruleid: mois-1-05-os-command-injection-py — ctl-fastapi-UploadFile
    os.system("file " + file.filename)


@app.get("/c10")
async def ctl_request(request: Request):
    # ruleid: mois-1-05-os-command-injection-py — ctl-fastapi-request-query_params
    os.system(request.query_params["c"])


@app.post("/c11")
async def ctl_request_json(request: Request):
    data = await request.json()
    # ruleid: mois-1-05-os-command-injection-py — ctl-fastapi-request-json
    os.system(data["c"])


@app.websocket("/c12")
async def ctl_ws_untyped(websocket):
    data = await websocket.receive_text()
    # ruleid: mois-1-05-os-command-injection-py — ctl-fastapi-websocket-untyped
    os.system(data)


@app.get("/c13")
def ctl_kwonly(*, cmd: str):
    # ruleid: mois-1-05-os-command-injection-py — ctl-fastapi-kwonly
    os.system(cmd)


@app.get("/c14")
def ctl_untyped_default(cmd=None):
    # ruleid: mois-1-05-os-command-injection-py — ctl-fastapi-untyped-default-None
    os.system(cmd)


@app.get("/c15/{n}")
def ok_int(n: int):
    os.system(f"kill {n}")  # CASE ok-fastapi-int (sound exclusion, expect no finding)


# ---- name-suffix exclusions hitting request bodies ----
@app.post("/m1")
def miss_config(cfg: WebhookConfig):
    # ruleid: mois-1-05-os-command-injection-py — fastapi-body-WebhookConfig
    os.system("curl " + cfg.url)


@app.post("/m2")
def miss_client(client: ApiClient):
    # ruleid: mois-1-05-os-command-injection-py — fastapi-body-ApiClient
    os.system("register " + client.name)


@app.post("/m3")
def miss_current(addr: CurrentAddress):
    # ruleid: mois-1-05-os-command-injection-py — fastapi-body-CurrentAddress
    os.system("geocode " + addr.street)


@app.put("/m4")
def miss_settings(settings: UserSettings = Body(...)):
    # ruleid: mois-1-05-os-command-injection-py — fastapi-body-UserSettings=Body(...)
    os.system("set-theme " + settings.theme)


@app.post("/m5")
def miss_repo(repo: GitRepo):
    # ruleid: mois-1-05-os-command-injection-py — fastapi-body-GitRepo
    os.system("git clone " + repo.url)


@app.post("/m6")
def miss_session(sess: LoginSession):
    # ruleid: mois-1-05-os-command-injection-py — fastapi-body-LoginSession
    os.system("notify " + sess.device)


@app.post("/m7")
def miss_service(svc: PrintService):
    # ruleid: mois-1-05-os-command-injection-py — fastapi-body-PrintService
    os.system("lp -d " + svc.printer)


# ---- Depends exclusions hitting raw request values ----
@app.get("/d1")
def miss_token_default(token: str = Depends(oauth2_scheme)):
    # ruleid: mois-1-05-os-command-injection-py — fastapi-token-str=Depends(oauth2_scheme)
    os.system("audit --token " + token)


@app.get("/d2")
def miss_token_annotated(token: Annotated[str, Depends(oauth2_scheme)]):
    # ruleid: mois-1-05-os-command-injection-py — fastapi-token-Annotated[str,Depends(oauth2_scheme)]
    os.system("audit --token " + token)


@app.post("/d3")
def miss_login_form(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    # ruleid: mois-1-05-os-command-injection-py — fastapi-Annotated[OAuth2PasswordRequestForm,Depends()]
    os.system("pam-auth " + form_data.username)


@app.post("/d4")
def miss_login_form_default(form_data: OAuth2PasswordRequestForm = Depends()):
    # ruleid: mois-1-05-os-command-injection-py — fastapi-OAuth2PasswordRequestForm=Depends()
    os.system("pam-auth " + form_data.username)


@app.get("/d5")
def miss_basic(creds: Annotated[HTTPBasicCredentials, Depends(basic)]):
    # ruleid: mois-1-05-os-command-injection-py — fastapi-Annotated[HTTPBasicCredentials,Depends(basic)]
    os.system("id " + creds.username)


@app.get("/d6")
def miss_bearer(creds: HTTPAuthorizationCredentials = Depends(bearer)):
    # ruleid: mois-1-05-os-command-injection-py — fastapi-HTTPAuthorizationCredentials=Depends(bearer)
    os.system("audit --token " + creds.credentials)


@app.get("/d7")
def miss_query_model(filters: Annotated[FilterParams, Depends()]):
    # ruleid: mois-1-05-os-command-injection-py — fastapi-Annotated[FilterParams,Depends()]-query-model
    os.system("grep " + filters.q)


@app.get("/d8")
def miss_commons(commons: Annotated[dict, Depends(common_parameters)]):
    os.system("grep " + commons["q"])  # CASE fastapi-Annotated[dict,Depends(common_parameters)]


def verify_token(x_token: str = Header()):
    # ruleid: mois-1-05-os-command-injection-py — fastapi-dependency-function-Header-param
    os.system("audit --token " + x_token)
    return x_token


@app.get("/d9")
def miss_untyped_query(cmd=Query(None)):
    # ruleid: mois-1-05-os-command-injection-py — fastapi-untyped-param=Query(None)
    os.system(cmd)


# ---- framework object types excluded, accessors not re-added ----
@app.get("/t1")
async def miss_request_other_name(r: Request):
    # ruleid: mois-1-05-os-command-injection-py — fastapi-Request-named-r
    os.system(r.query_params["c"])


@app.get("/t2")
async def miss_http_request(http_request: Request):
    # ruleid: mois-1-05-os-command-injection-py — fastapi-Request-named-http_request
    os.system(http_request.headers["x-cmd"])


@app.websocket("/t3")
async def miss_ws(websocket: WebSocket):
    await websocket.accept()
    data = await websocket.receive_text()
    # ruleid: mois-1-05-os-command-injection-py — fastapi-WebSocket-receive_text
    os.system(data)


@app.websocket("/t4")
async def miss_ws_qp(websocket: WebSocket):
    # ruleid: mois-1-05-os-command-injection-py — fastapi-WebSocket-query_params
    os.system(websocket.query_params["c"])


@app.get("/t5")
async def miss_conn(conn: HTTPConnection):
    # ruleid: mois-1-05-os-command-injection-py — fastapi-HTTPConnection-query_params
    os.system(conn.query_params["c"])


# ---- numeric prefix (\b) ----
@app.get("/n1/{ident}")
def miss_union(ident: int | str):
    # ruleid: mois-1-05-os-command-injection-py — fastapi-int|str
    os.system("lookup " + str(ident))


@app.get("/n2/{ident}")
def miss_union_annotated(ident: Annotated[int | str, Path()]):
    # ruleid: mois-1-05-os-command-injection-py — fastapi-Annotated[int|str,Path()]
    os.system("lookup " + str(ident))


@app.get("/n3/{ident}")
def ctl_union_typing(ident: str | int):
    # ruleid: mois-1-05-os-command-injection-py — ctl-fastapi-str|int
    os.system("lookup " + str(ident))
