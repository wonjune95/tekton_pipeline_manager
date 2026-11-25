from typing import Optional


class RateLimiter:
    def __init__(self, routes: list, quotas: dict[str, int], blocked: Optional[set] = None):
        # 내장 타입으로 표기한 인자
        # ruleid: mois-6-04-public-data-to-private-array-py
        self._routes = routes
        # ruleid: mois-6-04-public-data-to-private-array-py
        self._quotas = quotas
        # ruleid: mois-6-04-public-data-to-private-array-py
        self._blocked = blocked
        self._exempt = list()
        self._weights = dict()
        self._roles = set()
        self._window = 60

    def set_exempt(self, exempt=None):
        # 기본값이 있는 인자 (타입 표기 없음)
        # ruleid: mois-6-04-public-data-to-private-array-py
        self._exempt = exempt

    def set_weights(self, weights):
        # ruleid: mois-6-04-public-data-to-private-array-py
        self._weights = weights

    def set_roles(self, roles):
        # ruleid: mois-6-04-public-data-to-private-array-py
        self._roles = roles
