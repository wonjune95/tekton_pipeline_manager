from fastapi import FastAPI
from pydantic import BaseModel

api = FastAPI()


class SessionState(BaseModel):
    user: str
    locale: str = "ko"


@api.post("/session/restore")
def restore(state: SessionState):
    # 스키마로 검증된 값만 사용
    return {"user": state.user}
