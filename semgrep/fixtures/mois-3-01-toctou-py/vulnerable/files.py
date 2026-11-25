import fcntl
import os
import shutil
import threading
from pathlib import Path

lock = threading.Lock()


def read_or_404(path):
    # 먼저 빠져나가는 검사 뒤에 여는 경우도 같다
    if not os.path.exists(path):
        return None
    # ruleid: mois-3-01-toctou-py
    with open(path, "rb") as f:
        return f.read()


def archive(src, dest_dir):
    if os.path.isdir(src):
        # ruleid: mois-3-01-toctou-py
        shutil.move(src, dest_dir)


def clean_link(link, stale):
    if os.path.islink(link):
        # ruleid: mois-3-01-toctou-py
        os.unlink(link)
    if os.path.lexists(stale):
        # ruleid: mois-3-01-toctou-py
        os.unlink(stale)


def make_writable(path):
    if not os.access(path, os.W_OK):
        return False
    # ruleid: mois-3-01-toctou-py
    os.chmod(path, 0o640)
    return True


def read_config(base):
    conf = Path(base) / "app.conf"
    if conf.is_file():
        # ruleid: mois-3-01-toctou-py
        with open(conf, encoding="utf-8") as f:
            return f.read()
    return ""


def read_template(base):
    template = Path(base) / "mail.html"
    if not template.exists():
        return ""
    # ruleid: mois-3-01-toctou-py
    return template.read_text(encoding="utf-8")


def remove_checked_then_locked(path):
    if os.path.exists(path):
        # 검사한 뒤에 잠근다 — 검사는 잠금 밖이다
        with lock:
            # ruleid: mois-3-01-toctou-py
            os.remove(path)


def remove_acquire_after_check(path):
    if os.path.exists(path):
        lock.acquire()
        # ruleid: mois-3-01-toctou-py
        os.remove(path)
        lock.release()


def truncate_flock_after_check(path, fd):
    if os.path.isfile(path):
        fcntl.flock(fd, fcntl.LOCK_EX)
        # ruleid: mois-3-01-toctou-py
        os.truncate(path, 0)


def remove_other_block_locked(path, stats):
    # 다른 일을 하는 잠금 블록이 있어도 파일 검사·삭제는 잠금 밖이다
    with lock:
        stats["removed"] = stats.get("removed", 0) + 1
    if os.path.exists(path):
        # ruleid: mois-3-01-toctou-py
        os.remove(path)
