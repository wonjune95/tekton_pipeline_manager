import os

from .services import notify, parse_row


def cleanup(paths):
    for path in paths:
        try:
            os.remove(path)
        # ruleid: mois-4-02-empty-catch-py
        except:
            pass


def import_rows(rows):
    result = []
    for row in rows:
        try:
            result.append(parse_row(row))
        # ruleid: mois-4-02-empty-catch-py
        except ValueError as exc:

            # 주석과 빈 줄만 있고 실제 처리는 없다
            continue
        # ruleid: mois-4-02-empty-catch-py
        except* TypeError:
            ...
    return result


def parse_ports(values):
    ports = []
    for value in values:
        try: ports.append(int(value))
        # ruleid: mois-4-02-empty-catch-py
        except ValueError: continue  # 한 줄로 쓴 건너뛰기
    return ports


class Notifier:
    def send(self, message):
        try:
            notify(message)
        # ruleid: mois-4-02-empty-catch-py
        except ConnectionError: ...  # 한 줄로 쓴 빈 처리
        else:
            self.sent += 1

    def close(self):
        try:
            self.conn.close()
        # ruleid: mois-4-02-empty-catch-py
        except OSError:
            pass  # 닫기 실패는 무시
        finally:
            self.conn = None
