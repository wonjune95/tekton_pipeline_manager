import socket


def db_is_up(host, port):
    s = None
    try:
        s = socket.create_connection((host, port), timeout=2)
        s.sendall(b"\x00")
    except OSError:
        return False
    finally:
        if s is not None:
            s.close()
    return True
