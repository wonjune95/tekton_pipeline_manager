import socket


def db_is_up(host, port):
    try:
        # ruleid: mois-5-02-resource-leak-py
        s = socket.create_connection((host, port), timeout=2)  # 닫지 않음
        s.sendall(b"\x00")
    except OSError:
        return False
    return True
