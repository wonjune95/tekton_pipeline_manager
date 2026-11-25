import logging
import time

logger = logging.getLogger(__name__)


def poll_queue(queue, handler):
    # while 1 로 쓴 무한 반복
    # ruleid: mois-3-02-infinite-loop-recursion-py
    while 1:
        handler(queue.get())


def heartbeat(client):
    # 주석에 적은 break·return 은 탈출 조건이 아니다
    # ruleid: mois-3-02-infinite-loop-recursion-py
    while True:
        client.ping()  # TODO: 실패하면 break
        time.sleep(5)


def countdown(n):
    # 빠져나가지 않는 조건문(로그)은 기저 조건이 아니다
    if n % 100 == 0:
        logger.info("countdown %d", n)
    # ruleid: mois-3-02-infinite-loop-recursion-py
    return countdown(n - 1)


class Category:
    def full_name(self):
        if self.parent is None:
            logger.debug("root category")
        # 부모가 아니라 자기 자신을 다시 부른다
        # ruleid: mois-3-02-infinite-loop-recursion-py
        return self.full_name() + "/" + self.name
