import os
from pathlib import Path

from django.conf import settings


def save_config(text):
    path = os.path.join(settings.BASE_DIR, "conf", "app.conf")
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    # 소유자만 읽고 쓴다
    os.chmod(path, 0o600)


def prepare_upload_dir():
    os.umask(0o077)
    os.makedirs(settings.MEDIA_ROOT, mode=0o750, exist_ok=True)
    Path(settings.MEDIA_ROOT, "keys").chmod(0o700)
