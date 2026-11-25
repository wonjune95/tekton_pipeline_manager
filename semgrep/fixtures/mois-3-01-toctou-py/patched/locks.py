import os
import threading
from pathlib import Path

state_mutex = threading.RLock()
write_semaphore = threading.BoundedSemaphore(1)
lock = threading.Lock()
LOG_FILE = "/var/app/audit.log"


def remove_with_mutex(path):
    # ok: mois-3-01-toctou-py 검사와 삭제가 같은 잠금(mutex) 안에 있다
    with state_mutex:
        if os.path.exists(path):
            os.remove(path)


def rotate_with_semaphore(base):
    current = Path(base) / "current.log"
    # ok: mois-3-01-toctou-py 검사와 이름 변경이 같은 세마포어 안에 있다
    with write_semaphore:
        if current.exists():
            current.rename(Path(base) / "previous.log")


def clear_marker(base):
    marker = Path(base) / "ready"
    if marker.exists():
        # ok: mois-3-01-toctou-py 이미 없어도 실패하지 않는다
        marker.unlink(missing_ok=True)


def append_acquired(line):
    lock.acquire()
    try:
        # ok: mois-3-01-toctou-py 잠금을 잡은 뒤에 with 로 연다
        with open(LOG_FILE, "a") as f:
            f.write(line + "\n")
    finally:
        lock.release()


def append_with_mutex(line):
    # ok: mois-3-01-toctou-py
    with state_mutex:
        with open(LOG_FILE, "a") as f:
            f.write(line + "\n")


def append_with_semaphore(line):
    # ok: mois-3-01-toctou-py
    with write_semaphore:
        with open(LOG_FILE, "a") as f:
            f.write(line + "\n")


def assign_with_mutex(line):
    # ok: mois-3-01-toctou-py
    with state_mutex:
        fh = open(LOG_FILE, "a")
        try:
            fh.write(line + "\n")
        finally:
            fh.close()


def assign_with_semaphore(line):
    # ok: mois-3-01-toctou-py
    with write_semaphore:
        fh = open(LOG_FILE, "a")
        try:
            fh.write(line + "\n")
        finally:
            fh.close()


def start_workers(line):
    threading.Thread(target=append_acquired, args=(line,)).start()
    threading.Thread(target=append_with_mutex, args=(line,)).start()
    threading.Thread(target=append_with_semaphore, args=(line,)).start()
    threading.Thread(target=assign_with_mutex, args=(line,)).start()
    threading.Thread(target=assign_with_semaphore, args=(line,)).start()
