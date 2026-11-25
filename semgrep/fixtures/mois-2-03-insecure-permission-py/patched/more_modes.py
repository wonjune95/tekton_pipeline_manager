import os
import stat
import subprocess
from pathlib import Path


def publish_report(path, fd):
    # ok: mois-2-03-insecure-permission-py others 는 읽기만
    os.chmod(path, mode=0o644)
    # ok: mois-2-03-insecure-permission-py 소유자·그룹만
    os.fchmod(fd, 0o660)
    # ok: mois-2-03-insecure-permission-py 10진수 420 = 0o644
    os.chmod(path, 420)


def create_spool(base):
    # ok: mois-2-03-insecure-permission-py
    os.mkdir(os.path.join(base, "spool"), 0o750)
    # ok: mois-2-03-insecure-permission-py
    Path(base, "cache").mkdir(parents=True, mode=0o755, exist_ok=True)
    # ok: mois-2-03-insecure-permission-py
    fd = os.open(os.path.join(base, "lock"), os.O_CREAT | os.O_RDWR, 0o600)
    os.close(fd)


def tighten(path):
    target = Path(path)
    # ok: mois-2-03-insecure-permission-py others 쓰기 비트를 지운다 (S_IWOTH 를 빼는 식은 탐지 대상이 아님)
    target.chmod(stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP)
    # ok: mois-2-03-insecure-permission-py
    os.umask(0o027)


def tighten_by_shell(path):
    # ok: mois-2-03-insecure-permission-py others 쓰기 제거
    os.system("chmod o-w " + path)
    # ok: mois-2-03-insecure-permission-py 755 는 others 쓰기 없음
    subprocess.run(["chmod", "-R", "755", path], check=True)
    # ok: mois-2-03-insecure-permission-py 소유자 실행 권한만 추가
    subprocess.run(f"chmod u+x {path}", shell=True, check=True)


def drop_world_write(path):
    target = Path(path)
    # ok: mois-2-03-insecure-permission-py others 쓰기 비트를 지우는 식
    os.chmod(path, os.stat(path).st_mode & ~stat.S_IWOTH)
    # ok: mois-2-03-insecure-permission-py 그룹·others 쓰기 비트를 함께 지운다
    target.chmod(target.stat().st_mode & ~(stat.S_IWGRP | stat.S_IWOTH))
    # ok: mois-2-03-insecure-permission-py
    os.chmod(path, os.stat(path).st_mode & ~stat.S_IRWXO)
    # ok: mois-2-03-insecure-permission-py others 권한을 모두 지운다 (Path)
    target.chmod(target.stat().st_mode & ~stat.S_IRWXO)
