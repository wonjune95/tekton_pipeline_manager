import smtplib
import ssl

import httpx
import requests

PAY_API = "https://pay.example.org/api/v1/approve"


def approve(card_no, amount):
    return requests.post(PAY_API, json={"card": card_no, "amount": amount}, timeout=5)


def member_client():
    return httpx.Client(base_url="https://member.example.org", timeout=5)


def health():
    # 같은 호스트 안의 호출
    return requests.get("http://localhost:8080/health", timeout=2)


def send_mail(sender, to, message, user, pw):
    context = ssl.create_default_context()
    with smtplib.SMTP("smtp.example.org", 587) as smtp:
        smtp.starttls(context=context)
        smtp.login(user, pw)
        smtp.sendmail(sender, [to], message)


def send_mail_ssl(sender, to, message, user, pw):
    with smtplib.SMTP_SSL("smtp.example.org", 465, context=ssl.create_default_context()) as smtp:
        smtp.login(user, pw)
        smtp.sendmail(sender, [to], message)
