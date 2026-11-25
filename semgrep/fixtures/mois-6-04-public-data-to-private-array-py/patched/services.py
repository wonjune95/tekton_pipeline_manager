from typing import Dict, List


class AccessPolicy:
    def __init__(self, allowed_ips: List[str], limits: Dict[str, int] = None, name: str = ""):
        # 복사본을 만들어 보관
        self.__allowed_ips = list(allowed_ips)
        self._limits = dict(limits or {})
        self._name = name
        self._tags = []

    def set_tags(self, tags):
        self._tags = list(tags)

    def is_allowed(self, ip):
        return ip in self.__allowed_ips
