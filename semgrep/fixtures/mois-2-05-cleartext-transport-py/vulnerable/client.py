import ftplib
import smtplib

import httpx
import requests

PAY_API = "http://pay.example.org/api/v1/approve"


def approve(card_no, amount):
    # 카드번호를 암호화되지 않은 http:// 로 보낸다
    # ruleid: mois-2-05-cleartext-transport-py
    return requests.post("http://pay.example.org/api/v1/approve", json={"card": card_no, "amount": amount}, timeout=5)


def approve_again(card_no):
    # ruleid: mois-2-05-cleartext-transport-py
    return requests.post(PAY_API, json={"card": card_no}, timeout=5)


def member_client():
    # ruleid: mois-2-05-cleartext-transport-py
    return httpx.Client(base_url="http://member.example.org", timeout=5)


def send_mail(sender, to, message, user, pw):
    # TLS 없이 SMTP 로그인
    # ruleid: mois-2-05-cleartext-transport-py
    with smtplib.SMTP("smtp.example.org", 25) as smtp:
        smtp.login(user, pw)
        smtp.sendmail(sender, [to], message)


def upload_report(path, user, pw):
    # ruleid: mois-2-05-cleartext-transport-py
    ftp = ftplib.FTP("ftp.example.org")
    ftp.login(user, pw)
    with open(path, "rb") as f:
        ftp.storbinary("STOR report.csv", f)
    ftp.quit()
