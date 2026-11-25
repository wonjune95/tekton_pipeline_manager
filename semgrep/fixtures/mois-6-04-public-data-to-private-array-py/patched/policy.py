import copy
from typing import Optional


class RateLimiter:
    def __init__(self, routes: list, quotas: dict[str, int], blocked: Optional[set] = None, window: int = 60):
        # ok: mois-6-04-public-data-to-private-array-py 복사본을 보관
        self._routes = list(routes)
        # ok: mois-6-04-public-data-to-private-array-py
        self._quotas = copy.deepcopy(quotas)
        # ok: mois-6-04-public-data-to-private-array-py
        self._blocked = set(blocked or ())
        # ok: mois-6-04-public-data-to-private-array-py 숫자 인자
        self._window = window
        self._exempt = []
        # 공개 속성은 대상이 아니다
        self.routes = routes

    def set_exempt(self, exempt):
        # ok: mois-6-04-public-data-to-private-array-py 바꿀 수 없는 튜플로 보관
        self._exempt = tuple(exempt)

    def _replace_routes(self, routes: list):
        # ok: mois-6-04-public-data-to-private-array-py 비공개 메서드
        self._routes = routes
