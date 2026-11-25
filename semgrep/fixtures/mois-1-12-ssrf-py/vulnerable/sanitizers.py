"""고정 주소처럼 보이지만 요청 대상 호스트를 바꿀 수 있는 경우 — 모두 탐지되어야 한다."""
from urllib.parse import urljoin

import requests
from django.http import HttpResponse


def host_from_format(request):
    host = request.GET.get("host", "")
    # 호스트 자리가 % 서식
    # ruleid: mois-1-12-ssrf-py
    resp = requests.get("https://%s/api/status" % host, timeout=5)
    return HttpResponse(resp.content)


def host_concatenated(request):
    host = request.GET.get("host", "")
    # ruleid: mois-1-12-ssrf-py
    resp = requests.get("https://" + host + "/api/status", timeout=5)
    return HttpResponse(resp.content)


def host_without_terminator(request):
    path = request.GET.get("path", "")
    # 호스트 뒤에 구분자가 없다: path=.evil.example/x 또는 @evil.example/x 로 다른 호스트가 된다
    # ruleid: mois-1-12-ssrf-py
    resp = requests.get("https://api.example.go.kr" + path, timeout=5)
    return HttpResponse(resp.content)


def userinfo_prefix(request):
    host = request.GET.get("host", "")
    # "@" 앞은 호스트가 아니라 사용자 정보다
    # ruleid: mois-1-12-ssrf-py
    resp = requests.get("https://svc-account@" + host + "/api/status", timeout=5)
    return HttpResponse(resp.content)


def subdomain_from_input(request):
    tenant = request.GET.get("tenant", "")
    # tenant=evil.example/ 이면 evil.example 로 간다
    # ruleid: mois-1-12-ssrf-py
    resp = requests.get(f"https://{tenant}.example.go.kr/api/status", timeout=5)
    return HttpResponse(resp.content)


def literal_first_but_not_prefix(request, use_default, mirror):
    url = request.GET.get("url", "")
    # 리터럴로 시작하지만 값은 입력에서 올 수 있는 식
    # ruleid: mois-1-12-ssrf-py
    a = requests.get("https://api.example.go.kr/status" if use_default else url, timeout=5)
    # ruleid: mois-1-12-ssrf-py
    b = requests.get("https://api.example.go.kr/".join([url, "status"]), timeout=5)
    # ruleid: mois-1-12-ssrf-py
    c = requests.get("https://api.example.go.kr/" + mirror and url, timeout=5)
    # ruleid: mois-1-12-ssrf-py
    d = requests.get("https://api.example.go.kr/" * use_default or url, timeout=5)
    return HttpResponse(a.content + b.content + c.content + d.content)


def host_in_placeholder(request):
    host = request.GET.get("host", "")
    port = request.GET.get("port", "")
    url = request.GET.get("url", "")
    # 호스트 자리가 .format 자리표시
    # ruleid: mois-1-12-ssrf-py
    a = requests.get("https://{}/api/status".format(host), timeout=5)
    # 포트 자리: 호스트는 같아도 내부 관리 포트로 간다
    # ruleid: mois-1-12-ssrf-py
    b = requests.get(f"https://api.example.go.kr:{port}/api/status", timeout=5)
    # urljoin 은 둘째 인자가 절대 주소나 //host 이면 기준 주소의 호스트를 버린다
    # ruleid: mois-1-12-ssrf-py
    c = requests.get(urljoin("https://api.example.go.kr/v1/", url), timeout=5)
    return HttpResponse(a.content + b.content + c.content)


def prefix_literal_rewritten(request, keep):
    host = request.GET.get("host", "")
    # 글자는 고정 주소 리터럴로 시작하지만 그 리터럴을 고쳐 쓴다 — 값의 맨 앞에 리터럴이 남는다는 증명이 못 된다
    # HOST 자리에 입력이 들어간다
    # ruleid: mois-1-12-ssrf-py
    a = requests.get("https://HOST/api/status".replace("HOST", host), timeout=5)
    # 끝의 "/" 를 떼면 호스트 구분자가 사라진다: host=.evil.example/x
    # ruleid: mois-1-12-ssrf-py
    b = requests.get("https://api.example.go.kr/".rstrip("/") + host, timeout=5)
    # .format 으로 만든 뒤에 호스트를 바꾼다
    # ruleid: mois-1-12-ssrf-py
    c = requests.get("https://HOST/items/{}".format("status").replace("HOST", host), timeout=5)
    # keep=0 이면 리터럴이 빈 문자열이 된다
    # ruleid: mois-1-12-ssrf-py
    d = requests.get("https://api.example.go.kr/" * keep + host, timeout=5)
    # Python 은 (리터럴 % 값) * keep 으로 계산한다 (Semgrep 은 리터럴 % (값 * keep) 으로 읽는다)
    # ruleid: mois-1-12-ssrf-py
    e = requests.get("https://api.example.go.kr/%s" % "status" * keep + host, timeout=5)
    # 글자 하나만 꺼낸다: "h" + host
    # ruleid: mois-1-12-ssrf-py
    f = requests.get("https://api.example.go.kr/"[keep] + host, timeout=5)
    return HttpResponse(a.content + b.content + c.content + d.content + e.content + f.content)


def prefix_literal_sliced(request, i, j, k):
    host = request.GET.get("host", "")
    # 잘라낸 리터럴은 호스트를 고정하지 않는다 (슬라이스 모양마다 하나씩)
    # ruleid: mois-1-12-ssrf-py
    a = requests.get("https://api.example.go.kr/"[:-1] + host, timeout=5)
    # ruleid: mois-1-12-ssrf-py
    b = requests.get("https://api.example.go.kr/"[i:] + host, timeout=5)
    # ruleid: mois-1-12-ssrf-py
    c = requests.get("https://api.example.go.kr/"[i:j] + host, timeout=5)
    # ruleid: mois-1-12-ssrf-py
    d = requests.get("https://api.example.go.kr/"[::k] + host, timeout=5)
    # ruleid: mois-1-12-ssrf-py
    e = requests.get("https://api.example.go.kr/"[i::k] + host, timeout=5)
    # ruleid: mois-1-12-ssrf-py
    f = requests.get("https://api.example.go.kr/"[:j:k] + host, timeout=5)
    # ruleid: mois-1-12-ssrf-py
    g = requests.get("https://api.example.go.kr/"[i:j:k] + host, timeout=5)
    return HttpResponse(b"".join(r.content for r in (a, b, c, d, e, f, g)))


def literal_first_in_a_container(request):
    url = request.GET.get("url", "")
    # 리터럴로 시작하는 묶음·dict 항목은 고정 접두가 아니다: 둘째 값이 입력이다
    out = []
    for target in "https://api.example.go.kr/status", url:
        # ruleid: mois-1-12-ssrf-py
        out.append(requests.get(target, timeout=5).content)
    first, second = "https://api.example.go.kr/" + "status", url
    # ruleid: mois-1-12-ssrf-py
    out.append(requests.get(second, timeout=5).content)
    table = {"https://api.example.go.kr/": url}
    # ruleid: mois-1-12-ssrf-py
    out.append(requests.get(table["https://api.example.go.kr/"], timeout=5).content)
    return HttpResponse(b"".join(out))


def integer_in_host_position(request):
    n = request.GET.get("n", "")
    # int() 로 바꿔도 호스트·포트·옥텟 자리에서는 요청 대상을 고른다
    # 10진수 IP: n=2130706433 은 127.0.0.1
    # ruleid: mois-1-12-ssrf-py
    a = requests.get("http://" + str(int(n)) + "/", timeout=2)
    # 포트: 같은 호스트의 다른 내부 서비스
    # ruleid: mois-1-12-ssrf-py
    b = requests.get("http://127.0.0.1:%d/health" % int(n), timeout=2)
    # ruleid: mois-1-12-ssrf-py
    c = requests.get("http://10.0.0.5:" + str(int(n)), timeout=2)
    # 마지막 옥텟: 내부망의 다른 장비
    # ruleid: mois-1-12-ssrf-py
    d = requests.get("http://10.0.0." + str(int(n)) + ":8080/metrics", timeout=2)
    return HttpResponse(a.content + b.content + c.content + d.content)
