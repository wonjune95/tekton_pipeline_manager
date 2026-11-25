"""HTTP 클라이언트·ORM 의 get() 은 None 을 돌려주지 않는다 (dict.get 과 이름만 같다)."""
import httpx
import requests
from django.db.models import Q

from .models import Member


def by_module(url):
    # ok: mois-5-01-null-dereference-py requests·httpx 모듈 함수
    encoding = requests.get(url).encoding
    # ok: mois-5-01-null-dereference-py
    success = httpx.get(url).is_success
    return encoding, success


def by_manager(email):
    # ok: mois-5-01-null-dereference-py objects.get 은 없으면 DoesNotExist 예외를 낸다
    return Member.objects.get(Q(email=email)).name


class Gateway:
    def __init__(self, client, base_url):
        self.client = client
        self.http = requests.Session()
        self.api = httpx.Client(base_url=base_url)

    def probe(self, url):
        # ok: mois-5-01-null-dereference-py 이름이 client·http·api 로 끝나는 객체는 HTTP 클라이언트로 본다
        a = self.client.get(url).data
        # ok: mois-5-01-null-dereference-py
        b = self.http.get(url).encoding
        # ok: mois-5-01-null-dereference-py
        c = self.api.get(url).is_success
        return a, b, c


def response_members(session, url):
    # ok: mois-5-01-null-dereference-py 이름으로는 알 수 없는 세션: 응답 객체에만 있는 속성으로 구분한다 (속성마다 한 줄)
    return [
        session.get(url).json(),
        session.get(url).text,
        session.get(url).content,
        session.get(url).status_code,
        session.get(url).raise_for_status(),
        session.get(url).ok,
        session.get(url).headers,
        session.get(url).cookies,
        session.get(url).url,
        session.get(url).iter_content(8192),
        session.get(url).iter_lines(),
        session.get(url).history,
        session.get(url).elapsed,
    ]
