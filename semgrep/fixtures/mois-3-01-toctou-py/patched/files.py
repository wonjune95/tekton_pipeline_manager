import fcntl
import os
import threading
from pathlib import Path

lock = threading.Lock()
LOG_FILE = "/var/app/audit.log"


def remove_locked(path):
    # ok: mois-3-01-toctou-py 검사와 삭제가 같은 잠금 안에 있다
    with lock:
        if os.path.exists(path):
            os.remove(path)


def remove_acquired(path):
    lock.acquire()
    try:
        # ok: mois-3-01-toctou-py acquire() 뒤에 검사하고 삭제한다
        if os.path.exists(path):
            os.remove(path)
    finally:
        lock.release()


def truncate_flocked(path, fd):
    fcntl.flock(fd, fcntl.LOCK_EX)
    # ok: mois-3-01-toctou-py 파일 잠금을 잡은 뒤에 검사한다
    if os.path.isfile(path):
        os.truncate(path, 0)
    fcntl.flock(fd, fcntl.LOCK_UN)


def ensure_dirs(base):
    cache = Path(base) / "cache"
    if not cache.exists():
        # ok: mois-3-01-toctou-py 이미 있어도 실패하지 않는다
        cache.mkdir(parents=True, exist_ok=True)
    if not os.path.isdir(base):
        # ok: mois-3-01-toctou-py
        os.makedirs(base, exist_ok=True)


def read_other(path, other):
    if os.path.exists(path):
        # ok: mois-3-01-toctou-py 검사한 경로와 다른 파일
        with open(other, encoding="utf-8") as f:
            return f.read()
    return ""


def append_audit(line):
    lock.acquire()
    # ok: mois-3-01-toctou-py 잠금을 잡은 뒤에 쓴다
    fh = open(LOG_FILE, "a")
    try:
        fh.write(line + "\n")
    finally:
        fh.close()
        lock.release()


def read_audit():
    # ok: mois-3-01-toctou-py 읽기 전용
    with open(LOG_FILE, "r") as f:
        return f.read()


def start_workers(lines):
    for line in lines:
        threading.Thread(target=append_audit, args=(line,)).start()
    threading.Thread(target=read_audit).start()


def append_locked(line):
    # ok: mois-3-01-toctou-py with 잠금 안에서 대입식으로 연다
    with lock:
        fh = open(LOG_FILE, "a")
        try:
            fh.write(line + "\n")
        finally:
            fh.close()


def start_locked_worker(line):
    threading.Thread(target=append_locked, args=(line,)).start()
