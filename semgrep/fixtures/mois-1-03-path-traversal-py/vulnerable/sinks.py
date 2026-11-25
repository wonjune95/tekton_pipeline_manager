import codecs
import io
import os
import shutil
import tarfile
import zipfile
from pathlib import Path

import aiofiles
import starlette.responses
from fastapi.responses import FileResponse
from flask import Flask, request, send_file, send_from_directory

app = Flask(__name__)
DATA_DIR = "/srv/data"


@app.route("/read")
def read_variants():
    name = request.args["name"]
    path = os.path.join(DATA_DIR, name)
    # ruleid: mois-1-03-path-traversal-py
    with io.open(path, encoding="utf-8") as fp:
        text = fp.read()
    # ruleid: mois-1-03-path-traversal-py
    with codecs.open(path, "r", "utf-8") as fp:
        text += fp.read()
    return {"text": text}


@app.route("/read-async")
async def read_async():
    path = DATA_DIR + "/" + request.args["name"]
    # ruleid: mois-1-03-path-traversal-py
    async with aiofiles.open(path) as fp:
        return {"text": await fp.read()}


@app.route("/archives")
def archives():
    name = request.args["name"]
    # ruleid: mois-1-03-path-traversal-py
    with zipfile.ZipFile(os.path.join(DATA_DIR, name)) as zf:
        names = zf.namelist()
    # ruleid: mois-1-03-path-traversal-py
    with tarfile.open(f"{DATA_DIR}/{name}.tar") as tf:
        names += tf.getnames()
    return {"names": names}


@app.route("/download")
def download():
    name = request.args["name"]
    # ruleid: mois-1-03-path-traversal-py
    return send_file(os.path.join(DATA_DIR, name))


@app.route("/download/<folder>/<name>")
def download_from(folder, name):
    # 디렉터리 인자가 외부 입력
    # ruleid: mois-1-03-path-traversal-py
    return send_from_directory(os.path.join(DATA_DIR, folder), name)


@app.route("/responses")
def file_responses():
    name = request.args["name"]
    # ruleid: mois-1-03-path-traversal-py
    first = FileResponse(path=DATA_DIR + "/" + name)
    # ruleid: mois-1-03-path-traversal-py
    second = starlette.responses.FileResponse(DATA_DIR + "/" + name)
    # ruleid: mois-1-03-path-traversal-py
    third = starlette.responses.FileResponse(path=DATA_DIR + "/" + name, filename="report.pdf")
    return first or second or third


@app.route("/upload", methods=["POST"])
def upload():
    folder = request.form["folder"]
    # request.files 에서 꺼낸 객체의 save(경로)
    # ruleid: mois-1-03-path-traversal-py
    request.files["doc"].save(os.path.join(DATA_DIR, folder, "doc.bin"))
    # ruleid: mois-1-03-path-traversal-py
    request.files.get("extra").save(os.path.join(DATA_DIR, folder, "extra.bin"))
    first = request.files["first"]
    # ruleid: mois-1-03-path-traversal-py
    first.save(os.path.join(DATA_DIR, folder, "first.bin"))
    second = request.files.get("second")
    # ruleid: mois-1-03-path-traversal-py
    second.save(os.path.join(DATA_DIR, folder, "second.bin"))
    for item in request.files.getlist("items"):
        # 원본 파일명을 그대로 경로에 사용
        # ruleid: mois-1-03-path-traversal-py
        item.save(os.path.join(DATA_DIR, item.filename))
    return {"ok": True}


@app.route("/thumbnail", methods=["POST"])
def thumbnail():
    from PIL import Image

    image = Image.open(request.files["photo"].stream)
    # 이름이 파일·이미지인 객체의 save(경로)
    # ruleid: mois-1-03-path-traversal-py
    image.save(os.path.join(DATA_DIR, "thumbs", request.form["name"]), "PNG")
    return {"ok": True}


@app.route("/manage", methods=["POST"])
def manage():
    name = request.form["name"]
    dest = request.form["dest"]
    # os 모듈: 첫 번째 인자
    # ruleid: mois-1-03-path-traversal-py
    os.unlink(os.path.join(DATA_DIR, name))
    # ruleid: mois-1-03-path-traversal-py
    entries = os.listdir(DATA_DIR + "/" + name)
    # os 모듈: 두 번째 인자(대상 경로)
    # ruleid: mois-1-03-path-traversal-py
    os.rename(os.path.join(DATA_DIR, "incoming.tmp"), os.path.join(DATA_DIR, dest))
    # shutil: 첫 번째·두 번째 인자
    # ruleid: mois-1-03-path-traversal-py
    shutil.rmtree(os.path.join(DATA_DIR, name))
    # ruleid: mois-1-03-path-traversal-py
    shutil.copy(os.path.join(DATA_DIR, "template.docx"), os.path.join(DATA_DIR, dest))
    return {"entries": entries}


@app.route("/notes", methods=["POST"])
def notes():
    target = Path(DATA_DIR) / request.form["name"]
    # pathlib 메서드
    # ruleid: mois-1-03-path-traversal-py
    target.write_text(request.form["body"], encoding="utf-8")
    # ruleid: mois-1-03-path-traversal-py
    target.unlink()
    return {"ok": True}
