import smtplib
import telnetlib
import urllib.request

import aiohttp
import httpx
import requests


def call_requests(payload):
    # ruleid: mois-2-05-cleartext-transport-py
    return requests.request("POST", "http://api.example.org/v1/members", json=payload, timeout=5)


def call_httpx(payload):
    # ruleid: mois-2-05-cleartext-transport-py
    a = httpx.post("http://api.example.org/v1/members", json=payload)
    # ruleid: mois-2-05-cleartext-transport-py
    b = httpx.request("PUT", "http://api.example.org/v1/members/1", json=payload)
    return a, b


def call_urllib(body):
    # ruleid: mois-2-05-cleartext-transport-py
    req = urllib.request.Request("http://api.example.org/v1/login", data=body, method="POST")
    # ruleid: mois-2-05-cleartext-transport-py
    with urllib.request.urlopen("http://api.example.org/v1/session", timeout=5) as resp:
        return req, resp.read()


async def call_aiohttp(payload):
    # ruleid: mois-2-05-cleartext-transport-py
    async with aiohttp.request("POST", "http://api.example.org/v1/pay", json=payload) as resp:
        return await resp.json()


def call_session(token, payload):
    session = requests.Session()
    session.headers["Authorization"] = "Bearer " + token
    # 세션·클라이언트 객체로 부르는 경우
    # ruleid: mois-2-05-cleartext-transport-py
    a = session.get("http://api.example.org/v1/me")
    # ruleid: mois-2-05-cleartext-transport-py
    b = session.post("http://api.example.org/v1/me", json=payload)
    # ruleid: mois-2-05-cleartext-transport-py
    c = session.put("http://api.example.org/v1/me", json=payload)
    # ruleid: mois-2-05-cleartext-transport-py
    d = session.patch("http://api.example.org/v1/me", json=payload)
    # ruleid: mois-2-05-cleartext-transport-py
    e = session.delete("http://api.example.org/v1/me")
    return a, b, c, d, e


def notify(sender, to, message, user, pw):
    # TLS 없이 로그인 (starttls 호출 없음)
    # ruleid: mois-2-05-cleartext-transport-py
    smtp = smtplib.SMTP("mail.example.org", 587)
    smtp.login(user, pw)
    smtp.sendmail(sender, [to], message)
    smtp.quit()


def notify_late_tls(sender, to, message, user, pw):
    smtp = smtplib.SMTP("mail.example.org", 587)
    # starttls() 가 로그인 뒤에 있다 — 계정은 이미 평문으로 지나갔다
    # ruleid: mois-2-05-cleartext-transport-py
    smtp.login(user, pw)
    smtp.starttls()
    smtp.sendmail(sender, [to], message)
    smtp.quit()


def notify_other_object(sender, to, message, user, pw):
    relay = smtplib.SMTP_SSL("relay.example.org", 465)
    # 다른 객체의 starttls() 는 이 연결을 지켜 주지 않는다
    # ruleid: mois-2-05-cleartext-transport-py
    smtp = smtplib.SMTP("mail.example.org", 25)
    relay.starttls()
    smtp.login(user, pw)
    smtp.sendmail(sender, [to], message)


def router_command(host, user, pw, command):
    # ruleid: mois-2-05-cleartext-transport-py
    tn = telnetlib.Telnet(host, 23, timeout=5)
    tn.read_until(b"login: ")
    tn.write(user.encode() + b"\n")
    tn.write(pw.encode() + b"\n")
    tn.write(command.encode() + b"\n")
    return tn.read_all()


def export_exists(token):
    # get·post 말고 다른 메서드(head 등)도 같은 채널이다 — 토큰이 평문으로 지나간다
    # ruleid: mois-2-05-cleartext-transport-py
    a = requests.head("http://files.example.org/export/members.csv", headers={"Authorization": "Bearer " + token})
    # ruleid: mois-2-05-cleartext-transport-py
    b = httpx.head("http://files.example.org/export/members.csv", headers={"Authorization": "Bearer " + token})
    return a.ok and b.is_success


def call_lookalike_host(payload):
    # localhost 로 시작할 뿐 다른 호스트다
    # ruleid: mois-2-05-cleartext-transport-py
    return requests.post("http://localhost.example.org/v1/members", json=payload)


def call_keyword_url(session, payload, body):
    # URL 을 url= 키워드로 넘겨도 같은 호출이다
    # ruleid: mois-2-05-cleartext-transport-py
    a = requests.get(url="http://api.example.org/v1/members", timeout=5)
    # ruleid: mois-2-05-cleartext-transport-py
    b = requests.post(url="http://api.example.org/v1/members", json=payload)
    # ruleid: mois-2-05-cleartext-transport-py
    c = httpx.put(url="http://api.example.org/v1/members/1", json=payload)
    # ruleid: mois-2-05-cleartext-transport-py
    d = httpx.patch(url="http://api.example.org/v1/members/1", json=payload)
    # ruleid: mois-2-05-cleartext-transport-py
    e = session.delete(url="http://api.example.org/v1/members/1")
    # ruleid: mois-2-05-cleartext-transport-py
    f = requests.request(method="POST", url="http://api.example.org/v1/login", json=payload)
    # ruleid: mois-2-05-cleartext-transport-py
    req = urllib.request.Request(url="http://api.example.org/v1/login", data=body, method="POST")
    # ruleid: mois-2-05-cleartext-transport-py
    with urllib.request.urlopen(url="http://api.example.org/v1/session", timeout=5) as resp:
        return a, b, c, d, e, f, req, resp.read()


def call_userinfo_host():
    # localhost 로 시작하지만 @ 앞은 계정 정보이고 실제 호스트는 files.example.org 다
    # ruleid: mois-2-05-cleartext-transport-py
    return requests.get("http://localhost:x@files.example.org/export/members.csv")


def notify_optional_tls(sender, to, message, user, pw, use_tls):
    # 설정에 따라 starttls() 를 건너뛴다 — TLS 가 보장되지 않는다
    # ruleid: mois-2-05-cleartext-transport-py
    smtp = smtplib.SMTP("mail.example.org", 587)
    if use_tls:
        smtp.starttls()
    smtp.login(user, pw)
    smtp.sendmail(sender, [to], message)
    smtp.quit()


def notify_best_effort_tls(sender, to, message, user, pw):
    # starttls() 가 실패해도 그대로 로그인한다
    # ruleid: mois-2-05-cleartext-transport-py
    with smtplib.SMTP("mail.example.org", 587) as smtp:
        try:
            smtp.starttls()
        except smtplib.SMTPException:
            pass
        smtp.login(user, pw)
        smtp.sendmail(sender, [to], message)


def login_then_optional_tls(smtp, user, pw, use_tls):
    # 넘겨받은 연결: 뒤의 starttls() 가 if 안에 있어도 계정은 이미 평문으로 지나갔다
    # ruleid: mois-2-05-cleartext-transport-py
    smtp.login(user, pw)
    if use_tls:
        smtp.starttls()


def send_then_tls(sender, to, message):
    smtp = smtplib.SMTP("mail.example.org", 587)
    # 로그인 없이 보내도 내용은 평문으로 지나갔다 — 뒤의 starttls() 는 이미 늦었다
    # ruleid: mois-2-05-cleartext-transport-py
    smtp.sendmail(sender, [to], message)
    smtp.starttls()
    smtp.quit()


def send_message_then_tls(msg):
    smtp = smtplib.SMTP("mail.example.org", 587)
    # ruleid: mois-2-05-cleartext-transport-py
    smtp.send_message(msg)
    smtp.starttls()
    smtp.quit()
