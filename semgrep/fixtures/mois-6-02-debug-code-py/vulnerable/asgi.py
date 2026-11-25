from starlette.applications import Starlette
from starlette.responses import PlainTextResponse
from starlette.routing import Route


async def health(request):
    # ruleid: mois-6-02-debug-code-py
    print("health check from", request.client.host)
    return PlainTextResponse("ok")


app = Starlette(routes=[Route("/health", health)])

# Starlette 모듈에 남은 확인용 블록
# ruleid: mois-6-02-debug-code-py
if __name__ == "__main__":
    response = health(None)
    assert response is not None
