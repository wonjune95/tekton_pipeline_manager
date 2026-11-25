import os
import stat
import subprocess
from pathlib import Path

from django.conf import settings


def save_config(text):
    path = os.path.join(settings.BASE_DIR, "conf", "app.conf")
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    # 모든 사용자가 읽고 쓸 수 있다
    # ruleid: mois-2-03-insecure-permission-py
    os.chmod(path, 0o777)


def prepare_upload_dir():
    # 이후 만드는 파일의 권한을 전혀 가리지 않는다
    # ruleid: mois-2-03-insecure-permission-py
    os.umask(0)
    # ruleid: mois-2-03-insecure-permission-py
    os.makedirs(settings.MEDIA_ROOT, mode=0o777, exist_ok=True)
    # ruleid: mois-2-03-insecure-permission-py
    Path(settings.MEDIA_ROOT, "keys").chmod(0o666)


def open_token_file(path):
    # ruleid: mois-2-03-insecure-permission-py
    fd = os.open(path, os.O_WRONLY | os.O_CREAT, 0o666)
    return os.fdopen(fd, "w")


def share_log(path):
    # ruleid: mois-2-03-insecure-permission-py
    os.chmod(path, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)
    # ruleid: mois-2-03-insecure-permission-py
    subprocess.run(["chmod", "-R", "777", os.path.dirname(path)], check=True)
