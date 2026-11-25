from typing import DefaultDict, Deque, MutableMapping, MutableSequence, MutableSet, Set


class EventBuffer:
    def __init__(
        self,
        payload: bytearray,
        seen: Set[str],
        queue: MutableSequence[str],
        index: MutableMapping[str, int],
        muted: MutableSet[str],
        counts: DefaultDict[str, int],
        recent: Deque[str],
    ):
        # 타입 표기별로 한 줄씩: 모두 호출자가 계속 바꿀 수 있는 가변 컬렉션이다
        # ruleid: mois-6-04-public-data-to-private-array-py
        self._payload = payload
        # ruleid: mois-6-04-public-data-to-private-array-py
        self._seen = seen
        # ruleid: mois-6-04-public-data-to-private-array-py
        self._queue = queue
        # ruleid: mois-6-04-public-data-to-private-array-py
        self._index = index
        # ruleid: mois-6-04-public-data-to-private-array-py
        self._muted = muted
        # ruleid: mois-6-04-public-data-to-private-array-py
        self._counts = counts
        # ruleid: mois-6-04-public-data-to-private-array-py
        self._recent = recent
