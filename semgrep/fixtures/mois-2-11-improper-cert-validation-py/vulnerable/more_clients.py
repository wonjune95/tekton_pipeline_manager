import ssl
import urllib.request

import aiohttp
import boto3
import httpx
import ldap
import requests
import urllib3
from httpx import AsyncClient

# 모듈 전체의 기본 컨텍스트를 검증 없는 것으로 바꾼다
# ruleid: mois-2-11-improper-cert-validation-py
ssl._create_default_https_context = ssl._create_unverified_context


def post_with_session(payload):
    session = requests.Session()
    # 같은 함수에서 만든 세션
    # ruleid: mois-2-11-improper-cert-validation-py
    return session.post("https://api.example.org/v1/members", json=payload, verify=False)


def get_with_context_manager():
    with requests.Session() as s:
        # ruleid: mois-2-11-improper-cert-validation-py
        return s.get("https://api.example.org/v1/members", verify=False)


def session_attribute():
    with requests.Session() as web:
        # 이름이 세션처럼 보이지 않아도 같은 함수에서 만든 세션
        # ruleid: mois-2-11-improper-cert-validation-py
        web.verify = False
        return web.get("https://api.example.org/v1/members")


def httpx_stream(url):
    # ruleid: mois-2-11-improper-cert-validation-py
    return httpx.stream("GET", url, verify=False)


def configure(http_session):
    # 인자로 받은 세션: 이름으로 세션임을 알아본다
    # ruleid: mois-2-11-improper-cert-validation-py
    http_session.verify = False
    return http_session


async def httpx_async(url):
    # ruleid: mois-2-11-improper-cert-validation-py
    async with AsyncClient(verify=False) as client:
        return await client.get(url)


def s3_client():
    # ruleid: mois-2-11-improper-cert-validation-py
    return boto3.client("s3", endpoint_url="https://s3.example.org", verify=False)


def s3_resource():
    session = boto3.session.Session()
    # ruleid: mois-2-11-improper-cert-validation-py
    return session.resource("s3", endpoint_url="https://s3.example.org", verify=False)


def sqs_client():
    aws = boto3.Session(profile_name="ops")
    # ruleid: mois-2-11-improper-cert-validation-py
    return aws.client("sqs", verify=False)


async def aiohttp_calls(url):
    # ruleid: mois-2-11-improper-cert-validation-py
    connector = aiohttp.TCPConnector(ssl=False)
    async with aiohttp.ClientSession(connector=connector) as session:
        # ruleid: mois-2-11-improper-cert-validation-py
        async with session.get(url, ssl=False) as resp:
            return await resp.text()


def aiohttp_legacy_connector():
    # ruleid: mois-2-11-improper-cert-validation-py
    return aiohttp.TCPConnector(verify_ssl=False)


async def aiohttp_legacy_call(session, url):
    # ruleid: mois-2-11-improper-cert-validation-py
    async with session.post(url, verify_ssl=False) as resp:
        return resp.status


def urllib3_pool():
    # ruleid: mois-2-11-improper-cert-validation-py
    return urllib3.PoolManager(cert_reqs="CERT_NONE")


def urllib3_pool_no_hostname():
    # ruleid: mois-2-11-improper-cert-validation-py
    return urllib3.HTTPSConnectionPool("api.example.org", 443, assert_hostname=False)


def wrap(sock):
    # ruleid: mois-2-11-improper-cert-validation-py
    return ssl.wrap_socket(sock, cert_reqs=ssl.CERT_NONE)


def ldap_connect(url):
    # LDAPS 서버 인증서를 요구하지 않는다
    # ruleid: mois-2-11-improper-cert-validation-py
    ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_NEVER)
    return ldap.initialize(url)


def urlopen_unverified(url):
    # ruleid: mois-2-11-improper-cert-validation-py
    return urllib.request.urlopen(url, context=ssl._create_unverified_context())


def partner_api():
    api = requests.Session()
    # with 없이 같은 함수에서 만든 세션 (이름이 세션처럼 보이지 않는 경우)
    # ruleid: mois-2-11-improper-cert-validation-py
    api.verify = False
    return api


# 인자·속성으로 받은 세션: 같은 함수에서 만들지 않았으므로 이름으로 알아본다 (이름마다 하나씩)
def relax(s):
    # ruleid: mois-2-11-improper-cert-validation-py
    s.verify = False
    return s


def relax_sess(sess):
    # ruleid: mois-2-11-improper-cert-validation-py
    sess.verify = False
    return sess


class PartnerApi:
    def __init__(self, client, http, connection):
        self.client = client
        self.http = http
        self.connection = connection
        self.requests = requests.Session()

    def allow_self_signed(self):
        # ruleid: mois-2-11-improper-cert-validation-py
        self.client.verify = False
        # ruleid: mois-2-11-improper-cert-validation-py
        self.http.verify = False
        # ruleid: mois-2-11-improper-cert-validation-py
        self.connection.verify = False
        # 다른 메서드에서 만든 세션
        # ruleid: mois-2-11-improper-cert-validation-py
        self.requests.verify = False
