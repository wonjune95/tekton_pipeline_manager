import os
import stat
import subprocess
from pathlib import Path


def publish_report(path, fd):
    # 키워드 인자로 준 모드
    # ruleid: mois-2-03-insecure-permission-py
    os.chmod(path, mode=0o666)
    # 심볼릭 링크 자체의 권한
    # ruleid: mois-2-03-insecure-permission-py
    os.lchmod(path, 0o777)
    # 열린 파일 기술자
    # ruleid: mois-2-03-insecure-permission-py
    os.fchmod(fd, 0o646)
    # 10진수로 적은 0o777
    # ruleid: mois-2-03-insecure-permission-py
    os.chmod(path, 511)
    # 10진수로 적은 0o666
    # ruleid: mois-2-03-insecure-permission-py
    os.chmod(path, 438)


def create_spool(base):
    # ruleid: mois-2-03-insecure-permission-py
    os.mkdir(os.path.join(base, "spool"), 0o777)
    # ruleid: mois-2-03-insecure-permission-py
    os.mkdir(os.path.join(base, "tmp"), mode=0o777)
    # ruleid: mois-2-03-insecure-permission-py
    os.makedirs(os.path.join(base, "a", "b"), 0o777)
    # ruleid: mois-2-03-insecure-permission-py
    Path(base, "cache").mkdir(parents=True, mode=0o777, exist_ok=True)
    # ruleid: mois-2-03-insecure-permission-py
    os.mkfifo(os.path.join(base, "events"), 0o666)
    # ruleid: mois-2-03-insecure-permission-py
    fd = os.open(os.path.join(base, "lock"), os.O_CREAT | os.O_RDWR, mode=0o666)
    os.close(fd)


def loosen(path):
    target = Path(path)
    # others 쓰기 비트를 더한다
    # ruleid: mois-2-03-insecure-permission-py
    os.chmod(path, os.stat(path).st_mode | stat.S_IWOTH)
    # ruleid: mois-2-03-insecure-permission-py
    target.chmod(target.stat().st_mode | stat.S_IWOTH)
    # ruleid: mois-2-03-insecure-permission-py
    target.chmod(stat.S_IRWXU | stat.S_IRWXO)
    # ruleid: mois-2-03-insecure-permission-py
    os.umask(0o000)


def loosen_by_shell(path):
    # ruleid: mois-2-03-insecure-permission-py
    os.system("chmod 777 /var/app/upload")
    # ruleid: mois-2-03-insecure-permission-py
    os.system("chmod -R 0777 " + path)
    # ruleid: mois-2-03-insecure-permission-py
    os.system(f"chmod a+w {path}")
    # ruleid: mois-2-03-insecure-permission-py
    os.popen("umask 0; touch /var/app/run.pid")
    # ruleid: mois-2-03-insecure-permission-py
    subprocess.run("chmod 666 /etc/app/app.conf", shell=True, check=True)
    # ruleid: mois-2-03-insecure-permission-py
    subprocess.check_call(f"sudo chmod go+w {path}", shell=True)
    # ruleid: mois-2-03-insecure-permission-py
    subprocess.call(["chmod", "o+w", path])
