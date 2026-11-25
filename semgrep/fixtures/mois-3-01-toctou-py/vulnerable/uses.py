import os
import shutil
import threading
from pathlib import Path

COUNTER_FILE = "/var/app/counter.txt"


def os_uses(src, dest, spool, lock_dir, pidfile, uid, gid):
    if os.path.exists(src):
        # ruleid: mois-3-01-toctou-py
        os.rename(src, dest)
    if os.path.isfile(dest):
        # ruleid: mois-3-01-toctou-py
        os.replace(dest, dest + ".bak")
    if os.path.isdir(spool):
        # ruleid: mois-3-01-toctou-py
        os.rmdir(spool)
    if not os.path.exists(lock_dir):
        # ruleid: mois-3-01-toctou-py
        os.mkdir(lock_dir)
    if os.path.exists(pidfile):
        # ruleid: mois-3-01-toctou-py
        os.chown(pidfile, uid, gid)
    if not os.path.exists(pidfile):
        # ruleid: mois-3-01-toctou-py
        return os.open(pidfile, os.O_WRONLY | os.O_CREAT)
    return None


def shutil_uses(work_dir, report, backup_dir):
    if os.path.isdir(work_dir):
        # ruleid: mois-3-01-toctou-py
        shutil.rmtree(work_dir)
    if os.path.isfile(report):
        # ruleid: mois-3-01-toctou-py
        shutil.copy(report, backup_dir)
    if os.path.exists(report):
        # ruleid: mois-3-01-toctou-py
        shutil.copy2(report, backup_dir)
    if os.access(report, os.R_OK):
        # ruleid: mois-3-01-toctou-py
        shutil.copyfile(report, backup_dir + "/latest")


def pathlib_uses(base, data):
    spool = Path(base) / "spool"
    if spool.is_dir():
        # ruleid: mois-3-01-toctou-py
        spool.rmdir()
    if not spool.exists():
        # ruleid: mois-3-01-toctou-py
        spool.mkdir()
    current = Path(base) / "current.json"
    previous = Path(base) / "previous.json"
    if current.exists():
        # ruleid: mois-3-01-toctou-py
        current.rename(previous)
    if previous.is_file():
        # ruleid: mois-3-01-toctou-py
        previous.replace(Path(base) / "archive.json")
    marker = Path(base) / "ready"
    if not marker.exists():
        # ruleid: mois-3-01-toctou-py
        marker.touch()
    note = Path(base) / "note.txt"
    if not note.exists():
        # ruleid: mois-3-01-toctou-py
        note.write_text("created", encoding="utf-8")
    blob = Path(base) / "blob.bin"
    if not blob.exists():
        # ruleid: mois-3-01-toctou-py
        blob.write_bytes(data)
    if blob.is_file():
        # ruleid: mois-3-01-toctou-py
        data = blob.read_bytes()
    if note.is_file():
        # ruleid: mois-3-01-toctou-py
        with note.open(encoding="utf-8") as f:
            return f.read(), data
    return "", data


def bump_counter():
    # 읽고 쓰는 모드("r+")도 쓰기다
    with open(COUNTER_FILE, "r+") as f:
        n = int(f.read() or 0)
        f.seek(0)
        f.write(str(n + 1))


def start_counters(count):
    for _ in range(count):
        # ruleid: mois-3-01-toctou-py
        threading.Thread(target=bump_counter).start()
