import os
import ssl
import urllib.request

import httpx
import requests

CA_BUNDLE = os.environ.get("INTERNAL_CA_BUNDLE", "/etc/pki/tls/certs/ca-bundle.crt")


def fetch_member(member_id):
    # 사설 인증서는 CA 번들로 검증한다
    return requests.get("https://api.example.org/members/%d" % member_id, verify=CA_BUNDLE, timeout=5)


def api_client():
    return httpx.Client(base_url="https://api.example.org", verify=CA_BUNDLE)


def fetch_notice():
    context = ssl.create_default_context(cafile=CA_BUNDLE)
    with urllib.request.urlopen("https://notice.example.org/latest", context=context) as resp:
        return resp.read()
