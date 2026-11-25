import os
import threading
from pathlib import Path

from flask import Flask

app = Flask(__name__)
STATE_FILE = "/var/app/state.txt"
state_lock = threading.Lock()


def write_state(content):
    # 같은 잠금 안에서 검사와 쓰기를 함께 수행
    with state_lock:
        if os.path.isfile(STATE_FILE):
            with open(STATE_FILE, "w") as f:
                f.write(content)


@app.route("/rotate")
def rotate():
    Path("/var/app/rotate.marker").unlink(missing_ok=True)
    t = threading.Thread(target=write_state, args=("rotated",))
    t.start()
    return "ok"
