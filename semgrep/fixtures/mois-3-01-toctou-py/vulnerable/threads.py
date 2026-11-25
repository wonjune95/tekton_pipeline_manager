import threading

LOG_FILE = "/var/app/audit.log"
counter_lock = threading.Lock()
counter = {"n": 0}


def append_audit(line):
    fh = open(LOG_FILE, "a")
    fh.write(line + "\n")
    fh.close()


def write_report(text):
    with open("/var/app/report.txt", "w") as f:
        f.write(text)
    # 다른 값을 지키는 잠금은 파일 쓰기를 지켜 주지 않는다
    with counter_lock:
        counter["n"] += 1


def write_then_lock(text):
    with open("/var/app/late.txt", "w") as f:
        f.write(text)
    # 파일을 다 쓴 뒤에 잠근다
    counter_lock.acquire()
    counter["n"] += 1
    counter_lock.release()


def start_workers(lines):
    for line in lines:
        # ruleid: mois-3-01-toctou-py
        threading.Thread(target=append_audit, args=(line,)).start()
    # ruleid: mois-3-01-toctou-py
    threading.Thread(target=write_report, args=("done",)).start()
    # ruleid: mois-3-01-toctou-py
    threading.Thread(target=write_then_lock, args=("done",)).start()
