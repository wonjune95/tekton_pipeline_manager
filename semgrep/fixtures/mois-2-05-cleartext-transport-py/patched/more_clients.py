import ftplib
import smtplib
import ssl
import urllib.request

import httpx
import requests


def call_requests(payload):
    # ok: mois-2-05-cleartext-transport-py https
    return requests.request("POST", "https://api.example.org/v1/members", json=payload, timeout=5)


def call_local(payload):
    # ok: mois-2-05-cleartext-transport-py 같은 호스트(루프백) 호출
    a = httpx.post("http://127.0.0.1:9000/internal/reindex", json=payload)
    # ok: mois-2-05-cleartext-transport-py
    with urllib.request.urlopen("http://localhost:9000/health", timeout=2) as resp:
        return a, resp.read()


def call_session(token):
    session = requests.Session()
    session.headers["Authorization"] = "Bearer " + token
    # ok: mois-2-05-cleartext-transport-py
    return session.get("https://api.example.org/v1/me")


def read_config(config):
    # ok: mois-2-05-cleartext-transport-py dict 의 get 은 호출이 아니다 (키가 http:// 로 시작하지 않음)
    return config.get("endpoint", "https://api.example.org")


def notify(sender, to, message, user, pw):
    smtp = smtplib.SMTP("mail.example.org", 587)
    # ok: mois-2-05-cleartext-transport-py 로그인 전에 TLS 로 올린다
    smtp.starttls(context=ssl.create_default_context())
    smtp.login(user, pw)
    smtp.sendmail(sender, [to], message)
    smtp.quit()


def notify_local(sender, to, message):
    # ok: mois-2-05-cleartext-transport-py 같은 호스트의 MTA
    with smtplib.SMTP("localhost") as smtp:
        smtp.sendmail(sender, [to], message)


def upload_report(path, user, pw):
    # ok: mois-2-05-cleartext-transport-py FTPS
    ftp = ftplib.FTP_TLS("ftp.example.org", context=ssl.create_default_context())
    ftp.login(user, pw)
    ftp.prot_p()
    with open(path, "rb") as f:
        ftp.storbinary("STOR report.csv", f)
    ftp.quit()


def notify_local_ip(sender, to, message):
    # ok: mois-2-05-cleartext-transport-py 루프백 주소의 MTA
    with smtplib.SMTP("127.0.0.1", 25) as smtp:
        smtp.sendmail(sender, [to], message)


def notify_unconnected(sender, to, message):
    # ok: mois-2-05-cleartext-transport-py 호스트 없이 만들면 아직 연결하지 않는다 (아래에서 같은 호스트로 연결)
    smtp = smtplib.SMTP()
    smtp.connect("localhost")
    smtp.sendmail(sender, [to], message)
    smtp.quit()


def call_local_bare():
    # ok: mois-2-05-cleartext-transport-py 포트·경로 없이 적은 같은 호스트
    client = httpx.Client(base_url="http://localhost")
    # ok: mois-2-05-cleartext-transport-py IPv6 루프백
    return client, requests.get("http://[::1]:8080/health", timeout=2)


def call_keyword_url(payload):
    # ok: mois-2-05-cleartext-transport-py url= 키워드로 넘긴 https
    a = requests.post(url="https://api.example.org/v1/members", json=payload, timeout=5)
    # ok: mois-2-05-cleartext-transport-py url= 키워드로 넘긴 같은 호스트
    b = requests.get(url="http://localhost:8080/health", timeout=2)
    return a, b


def relay_after_login(smtp, relay, user, pw):
    # ok: mois-2-05-cleartext-transport-py 뒤의 starttls() 는 다른 연결(relay)의 것이다 (smtp 는 TLS 로 올린 뒤 넘겨받은 연결)
    smtp.login(user, pw)
    relay.starttls()
    relay.sendmail(user, [user], "ping")
