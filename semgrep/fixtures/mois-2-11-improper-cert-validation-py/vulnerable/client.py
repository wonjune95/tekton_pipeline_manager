import ssl
import urllib.request

import httpx
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def fetch_member(member_id):
    # 서버 인증서를 검증하지 않는다
    # ruleid: mois-2-11-improper-cert-validation-py
    return requests.get("https://api.example.org/members/%d" % member_id, verify=False, timeout=5)


def api_client():
    # ruleid: mois-2-11-improper-cert-validation-py
    return httpx.Client(base_url="https://api.example.org", verify=False)


def session_client():
    session = requests.Session()
    # ruleid: mois-2-11-improper-cert-validation-py
    session.verify = False
    return session


def fetch_notice():
    # ruleid: mois-2-11-improper-cert-validation-py
    context = ssl._create_unverified_context()
    with urllib.request.urlopen("https://notice.example.org/latest", context=context) as resp:
        return resp.read()


def legacy_context():
    context = ssl.create_default_context()
    # 호스트 이름과 인증서 검증을 끈다
    # ruleid: mois-2-11-improper-cert-validation-py
    context.check_hostname = False
    # ruleid: mois-2-11-improper-cert-validation-py
    context.verify_mode = ssl.CERT_NONE
    return context
