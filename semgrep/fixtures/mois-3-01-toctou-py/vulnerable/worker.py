import threading
from pathlib import Path

from flask import Flask

app = Flask(__name__)
STATE_FILE = "/var/app/state.txt"


def write_state(content):
    with open(STATE_FILE, "w") as f:
        f.write(content)


@app.route("/rotate")
def rotate():
    marker = Path("/var/app/rotate.marker")
    if marker.exists():
        # ruleid: mois-3-01-toctou-py
        marker.unlink()  # 검사 후 잠금 없이 삭제
    # 여러 스레드가 잠금 없이 같은 파일에 씀
    # ruleid: mois-3-01-toctou-py
    t = threading.Thread(target=write_state, args=("rotated",))
    t.start()
    return "ok"
