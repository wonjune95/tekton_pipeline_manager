import os
import sys
import time


def poll_queue(queue, handler, stop_event):
    # ok: mois-3-02-infinite-loop-recursion-py 중지 신호를 받으면 빠져나간다
    while 1:
        if stop_event.is_set():
            return
        handler(queue.get())


def heartbeat(client):
    # ok: mois-3-02-infinite-loop-recursion-py 실패가 이어지면 예외로 끝난다
    while True:
        if not client.ping():
            raise ConnectionError("heartbeat lost")
        time.sleep(5)


def serve_forever(server):
    # ok: mois-3-02-infinite-loop-recursion-py 종료 명령이 오면 프로세스를 끝낸다
    while True:
        command = server.next_command()
        if command == "quit":
            sys.exit(0)
        server.run(command)


def walk(node, visit):
    visit(node)
    # ok: mois-3-02-infinite-loop-recursion-py 자식이 없으면 재귀하지 않는다
    for child in node.children:
        walk(child, visit)


def gcd(a, b):
    # ok: mois-3-02-infinite-loop-recursion-py 조건식이 기저 조건
    return a if b == 0 else gcd(b, a % b)


def find_root(node):
    if node.parent is not None:
        # ok: mois-3-02-infinite-loop-recursion-py 조건문 안의 재귀
        return find_root(node.parent)
    return node


def checked_depth(node, limit):
    if limit < 0:
        raise RecursionError("too deep")
    # ok: mois-3-02-infinite-loop-recursion-py 한도를 넘으면 예외로 끝난다
    return 1 + checked_depth(node.parent, limit - 1)


def drain(queue, out):
    if queue:
        out.append(queue.pop())
    else:
        return out
    # ok: mois-3-02-infinite-loop-recursion-py 비어 있으면 else 쪽에서 돌려주고 끝난다
    return drain(queue, out)


def descend(node, budget):
    if budget > 0:
        budget -= 1
    else:
        raise RecursionError("too deep")
    # ok: mois-3-02-infinite-loop-recursion-py 한도를 다 쓰면 else 쪽에서 예외로 끝난다
    return descend(node.child, budget)


def expand(node, out):
    out.append(node.name)
    if node.child is not None:
        # ok: mois-3-02-infinite-loop-recursion-py 자식이 있을 때만 재귀한다 (빠져나가는 문장이 없는 if)
        expand(node.child, out)


def notify_chain(handler, event):
    # ok: mois-3-02-infinite-loop-recursion-py 다음 처리기가 없으면 and 의 단락 평가로 끝난다
    return handler is not None and notify_chain(handler.next, event)


def drained(queue):
    # ok: mois-3-02-infinite-loop-recursion-py 비어 있으면 or 의 단락 평가로 끝난다
    return not queue or drained(queue[1:])


def flatten(node, out):
    pending = list(node.children)
    while pending:
        # ok: mois-3-02-infinite-loop-recursion-py 남은 자식이 없으면 재귀하지 않는다
        flatten(pending.pop(), out)
    out.append(node.name)


def read_chain(node):
    try:
        # ok: mois-3-02-infinite-loop-recursion-py 끝에 닿으면 AttributeError 로 끝난다
        return [node.value] + read_chain(node.next)
    except (AttributeError, TypeError):
        return []


class Document:
    @classmethod
    def parse(cls, text):
        # ok: mois-3-02-infinite-loop-recursion-py 같은 이름의 모듈 함수 호출은 재귀가 아니다
        return cls(parse(text))


def parse(text):
    return text.strip().splitlines()


def ticks(interval):
    # ok: mois-3-02-infinite-loop-recursion-py 제너레이터는 받는 쪽이 멈춘다
    while True:
        yield time.monotonic()
        time.sleep(interval)


def watchdog(client):
    # ok: mois-3-02-infinite-loop-recursion-py 응답이 없으면 프로세스를 끝낸다
    while True:
        if not client.ping():
            os._exit(1)
        time.sleep(5)
