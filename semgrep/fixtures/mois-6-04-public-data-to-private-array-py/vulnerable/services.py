from typing import Dict, List


class AccessPolicy:
    def __init__(self, allowed_ips: List[str], limits: Dict[str, int] = None):
        # 호출자가 넘긴 list 를 그대로 보관: 호출자가 나중에 바꾸면 정책이 바뀜
        # ruleid: mois-6-04-public-data-to-private-array-py
        self.__allowed_ips = allowed_ips
        # ruleid: mois-6-04-public-data-to-private-array-py
        self._limits = limits  # dict 인자를 그대로 저장
        self._tags = []
        self._headers = {}

    def set_tags(self, tags):
        # ruleid: mois-6-04-public-data-to-private-array-py
        self._tags = tags  # list 속성에 인자를 그대로 저장

    def set_headers(self, headers):
        # ruleid: mois-6-04-public-data-to-private-array-py
        self._headers = headers  # dict 속성에 인자를 그대로 저장

    def is_allowed(self, ip):
        return ip in self.__allowed_ips
