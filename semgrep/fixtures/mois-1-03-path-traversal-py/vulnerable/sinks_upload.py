"""sink 목록의 나머지 함수·메서드를 하나씩 확인하는 예제 (이름으로 알아보는 업로드 객체의 save, pathlib)."""
import os
from pathlib import Path

from flask import Flask, request

app = Flask(__name__)
DATA_DIR = "/srv/data"


@app.route("/upload/form", methods=["POST"])
def upload_form():
    from PIL import Image

    from .forms import AttachmentForm

    form = AttachmentForm()
    folder = request.form["folder"]
    # 이름이 upload·photo·attach·img 인 객체의 save(경로) — request.files 에서 바로 꺼낸 것이 아니어도 본다
    # ruleid: mois-1-03-path-traversal-py
    form.upload.data.save(os.path.join(DATA_DIR, folder, "upload.bin"))
    # ruleid: mois-1-03-path-traversal-py
    form.photo.data.save(os.path.join(DATA_DIR, folder, "photo.jpg"))
    attachment = form.attachment.data
    # ruleid: mois-1-03-path-traversal-py
    attachment.save(os.path.join(DATA_DIR, folder, "attachment.bin"))
    img = Image.open(form.photo.data.stream)
    # ruleid: mois-1-03-path-traversal-py
    img.save(os.path.join(DATA_DIR, folder, "thumb.png"))
    return {"ok": True}


@app.route("/notes/manage", methods=["POST"])
def notes_manage():
    target = Path(DATA_DIR) / request.form["name"]
    # pathlib 의 나머지 메서드
    # ruleid: mois-1-03-path-traversal-py
    target.write_bytes(request.get_data())
    # ruleid: mois-1-03-path-traversal-py
    with target.open("rb") as fp:
        head = fp.read(16)
    # ruleid: mois-1-03-path-traversal-py
    target.rmdir()
    # ruleid: mois-1-03-path-traversal-py
    target.mkdir(parents=True)
    # ruleid: mois-1-03-path-traversal-py
    target.touch()
    # ruleid: mois-1-03-path-traversal-py
    names = [child.name for child in target.iterdir()]
    return {"head": head.hex(), "names": names}
