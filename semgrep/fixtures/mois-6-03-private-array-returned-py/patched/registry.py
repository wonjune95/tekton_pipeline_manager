import copy
from types import MappingProxyType


class SessionStore:
    _sessions = {}
    _timeout = 1800

    def __init__(self, names):
        self._names = list(names)
        self._count = 0

    def sessions(self):
        # ok: mois-6-03-private-array-returned-py 읽기 전용 뷰
        return MappingProxyType(self._sessions)

    def names(self):
        # ok: mois-6-03-private-array-returned-py 깊은 복사본
        return copy.deepcopy(self._names)

    def names_tuple(self):
        # ok: mois-6-03-private-array-returned-py 바꿀 수 없는 튜플
        return tuple(self._names)

    def timeout(self):
        # ok: mois-6-03-private-array-returned-py 숫자는 가변 컬렉션이 아니다
        return self._timeout

    def count(self):
        # ok: mois-6-03-private-array-returned-py
        return self._count
