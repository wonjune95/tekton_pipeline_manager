import os
import ssl

import aiohttp
import boto3
import ldap
import requests
import urllib3

CA_BUNDLE = os.environ.get("INTERNAL_CA_BUNDLE", "/etc/pki/tls/certs/ca-bundle.crt")


def post_with_session(payload):
    session = requests.Session()
    # ok: mois-2-11-improper-cert-validation-py 사설 CA 번들로 검증
    session.verify = CA_BUNDLE
    return session.post("https://api.example.org/v1/members", json=payload)


def s3_client():
    # ok: mois-2-11-improper-cert-validation-py
    return boto3.client("s3", endpoint_url="https://s3.example.org", verify=CA_BUNDLE)


async def aiohttp_calls(url):
    context = ssl.create_default_context(cafile=CA_BUNDLE)
    # ok: mois-2-11-improper-cert-validation-py 검증하는 컨텍스트를 넘긴다
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=context)) as session:
        async with session.get(url) as resp:
            return await resp.text()


def urllib3_pool():
    # ok: mois-2-11-improper-cert-validation-py
    return urllib3.PoolManager(cert_reqs="CERT_REQUIRED", ca_certs=CA_BUNDLE)


def strict_context():
    context = ssl.create_default_context(cafile=CA_BUNDLE)
    # ok: mois-2-11-improper-cert-validation-py 호스트 이름 검증을 켠다
    context.check_hostname = True
    context.verify_mode = ssl.CERT_REQUIRED
    return context


def ldap_connect(url):
    # ok: mois-2-11-improper-cert-validation-py 서버 인증서를 요구한다
    ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_DEMAND)
    ldap.set_option(ldap.OPT_X_TLS_CACERTFILE, CA_BUNDLE)
    return ldap.initialize(url)


def check_signature(verifier, document, signature):
    # ok: mois-2-11-improper-cert-validation-py 인증서와 무관한 verify 메서드
    return verifier.verify(document, signature)
