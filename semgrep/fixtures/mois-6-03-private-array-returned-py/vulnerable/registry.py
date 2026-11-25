import collections
from collections import OrderedDict, defaultdict, deque


class SessionStore:
    # 클래스 속성으로 둔 비공개 컬렉션
    _sessions = {}
    _order = []

    def __init__(self, names):
        self._names = list(names)
        self._index = dict()
        self._seen = set()
        self._buffer = bytearray(16)
        self._by_user = defaultdict(list)
        self._lru = OrderedDict()
        self._recent = collections.deque(maxlen=10)

    def sessions(self):
        # ruleid: mois-6-03-private-array-returned-py
        return self._sessions

    def order(self):
        # ruleid: mois-6-03-private-array-returned-py
        return self._order

    def names(self):
        # ruleid: mois-6-03-private-array-returned-py
        return self._names

    def index(self):
        # ruleid: mois-6-03-private-array-returned-py
        return self._index

    def seen(self):
        # ruleid: mois-6-03-private-array-returned-py
        return self._seen

    def buffer(self):
        # ruleid: mois-6-03-private-array-returned-py
        return self._buffer

    def by_user(self):
        # ruleid: mois-6-03-private-array-returned-py
        return self._by_user

    def lru(self):
        # ruleid: mois-6-03-private-array-returned-py
        return self._lru

    @property
    def recent(self):
        # ruleid: mois-6-03-private-array-returned-py
        return self._recent
