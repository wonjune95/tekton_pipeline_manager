"""sink 목록의 나머지 함수·메서드를 하나씩 확인하는 예제 (os·shutil)."""
import os
import shutil

from flask import Flask, request

app = Flask(__name__)
DATA_DIR = "/srv/data"


@app.route("/manage/os", methods=["POST"])
def manage_os():
    target = os.path.join(DATA_DIR, request.form["name"])
    # os 모듈의 나머지 파일·디렉터리 함수
    # ruleid: mois-1-03-path-traversal-py
    os.rmdir(target)
    # ruleid: mois-1-03-path-traversal-py
    os.removedirs(target)
    # ruleid: mois-1-03-path-traversal-py
    os.mkdir(target)
    # ruleid: mois-1-03-path-traversal-py
    os.makedirs(target, exist_ok=True)
    # ruleid: mois-1-03-path-traversal-py
    names = [entry.name for entry in os.scandir(target)]
    # ruleid: mois-1-03-path-traversal-py
    for _root, _dirs, files in os.walk(target):
        names += files
    # ruleid: mois-1-03-path-traversal-py
    size = os.stat(target).st_size
    # ruleid: mois-1-03-path-traversal-py
    os.chmod(target, 0o644)
    # ruleid: mois-1-03-path-traversal-py
    os.chown(target, 1000, 1000)
    # ruleid: mois-1-03-path-traversal-py
    fd = os.open(target, os.O_RDONLY)
    os.close(fd)
    # ruleid: mois-1-03-path-traversal-py
    os.truncate(target, 0)
    # 두 번째 인자(만들어지는 링크 경로)
    # ruleid: mois-1-03-path-traversal-py
    os.symlink(DATA_DIR + "/current", target)
    # ruleid: mois-1-03-path-traversal-py
    os.link(DATA_DIR + "/current", target)
    return {"names": names, "size": size}


@app.route("/manage/shutil", methods=["POST"])
def manage_shutil():
    target = os.path.join(DATA_DIR, request.form["name"])
    # shutil 의 나머지 복사·이동·압축 함수
    # ruleid: mois-1-03-path-traversal-py
    shutil.copy2(DATA_DIR + "/template.docx", target)
    # ruleid: mois-1-03-path-traversal-py
    shutil.copyfile(DATA_DIR + "/template.docx", target)
    # ruleid: mois-1-03-path-traversal-py
    shutil.copytree(target, DATA_DIR + "/backup")
    # ruleid: mois-1-03-path-traversal-py
    shutil.move(target, DATA_DIR + "/trash")
    # ruleid: mois-1-03-path-traversal-py
    shutil.make_archive(target, "zip", DATA_DIR)
    # ruleid: mois-1-03-path-traversal-py
    shutil.unpack_archive(target, DATA_DIR + "/unpacked")
    return {"ok": True}

