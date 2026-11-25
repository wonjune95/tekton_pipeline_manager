import urllib.request

import aiohttp
import httpx
import requests
import urllib3
from flask import Flask, request

app = Flask(__name__)
SESSION = requests.Session()


@app.route("/fetch")
def fetch():
    url = request.args["url"]
    # requests·httpx 모듈 함수
    # ruleid: mois-1-12-ssrf-py
    a = requests.post(url=url, json={}, timeout=5)
    # ruleid: mois-1-12-ssrf-py
    b = httpx.get(url, timeout=5)
    # ruleid: mois-1-12-ssrf-py
    c = httpx.head(url=url)
    # request(method, url) 모양
    # ruleid: mois-1-12-ssrf-py
    d = requests.request("GET", url, timeout=5)
    # ruleid: mois-1-12-ssrf-py
    e = requests.request(method="GET", url=url, timeout=5)
    # ruleid: mois-1-12-ssrf-py
    f = httpx.request("GET", url)
    # ruleid: mois-1-12-ssrf-py
    g = httpx.request(method="GET", url=url)
    # ruleid: mois-1-12-ssrf-py
    h = urllib3.request("GET", url)
    return {"status": [x.status_code for x in (a, b, c, d, e, f, g)], "raw": h.status}


@app.route("/download")
def download():
    url = request.args["url"]
    # ruleid: mois-1-12-ssrf-py
    req = urllib.request.Request(url, headers={"User-Agent": "portal"})
    # ruleid: mois-1-12-ssrf-py
    path, _ = urllib.request.urlretrieve(url)
    # ruleid: mois-1-12-ssrf-py
    with httpx.stream("GET", url) as resp:
        size = sum(len(chunk) for chunk in resp.iter_bytes())
    return {"req": req.full_url, "path": path, "size": size}


@app.route("/aio")
async def aio():
    url = request.args["url"]
    # ruleid: mois-1-12-ssrf-py
    async with aiohttp.request("GET", url) as resp:
        first = await resp.text()
    async with aiohttp.ClientSession() as http:
        # 같은 함수에서 만든 ClientSession
        # ruleid: mois-1-12-ssrf-py
        async with http.get(url) as resp:
            second = await resp.text()
    return {"len": len(first) + len(second)}


@app.route("/session")
def session_calls():
    url = request.args["url"]
    # 파일 위쪽에서 만든 Session
    # ruleid: mois-1-12-ssrf-py
    a = SESSION.get(url, timeout=5)
    s = requests.session()
    # ruleid: mois-1-12-ssrf-py
    b = s.post(url=url, data={})
    # ruleid: mois-1-12-ssrf-py
    c = s.request("PUT", url)
    # ruleid: mois-1-12-ssrf-py
    d = s.request(method="DELETE", url=url)
    with httpx.Client(timeout=5) as client:
        # ruleid: mois-1-12-ssrf-py
        with client.stream("GET", url) as resp:
            size = len(resp.read())
    return {"status": [a.status_code, b.status_code, c.status_code, d.status_code], "size": size}


@app.route("/webhook/test", methods=["POST"])
def webhook_test():
    url = request.form["url"]
    # 나머지 HTTP 메서드 (모듈 함수)
    # ruleid: mois-1-12-ssrf-py
    a = requests.put(url, json={"ping": True}, timeout=5)
    # ruleid: mois-1-12-ssrf-py
    b = requests.patch(url, json={"ping": True}, timeout=5)
    # ruleid: mois-1-12-ssrf-py
    c = httpx.delete(url, timeout=5)
    # ruleid: mois-1-12-ssrf-py
    d = httpx.options(url, timeout=5)
    return {"status": [a.status_code, b.status_code, c.status_code, d.status_code]}


@app.route("/webhook/probe", methods=["POST"])
def webhook_probe():
    url = request.form["url"]
    # 나머지 HTTP 메서드 (Session·Client 객체)
    # ruleid: mois-1-12-ssrf-py
    a = SESSION.put(url, json={"ping": True}, timeout=5)
    # ruleid: mois-1-12-ssrf-py
    b = SESSION.patch(url, json={"ping": True}, timeout=5)
    # ruleid: mois-1-12-ssrf-py
    c = SESSION.delete(url, timeout=5)
    with httpx.Client(timeout=5) as client:
        # ruleid: mois-1-12-ssrf-py
        d = client.head(url)
        # ruleid: mois-1-12-ssrf-py
        e = client.options(url)
    return {"status": [a.status_code, b.status_code, c.status_code, d.status_code, e.status_code]}


@app.route("/keyword")
def keyword_url():
    url = request.args["url"]
    # url= 키워드 인자로 넘겨도 같은 sink 다
    # ruleid: mois-1-12-ssrf-py
    a = urllib.request.urlopen(url=url, timeout=5)
    # ruleid: mois-1-12-ssrf-py
    req = urllib.request.Request(url=url, headers={"User-Agent": "portal"})
    # ruleid: mois-1-12-ssrf-py
    path, _ = urllib.request.urlretrieve(url=url)
    # ruleid: mois-1-12-ssrf-py
    with httpx.stream("GET", url=url) as resp:
        size = len(resp.read())
    # ruleid: mois-1-12-ssrf-py
    b = urllib3.request("GET", url=url)
    with httpx.Client(timeout=5) as client:
        # ruleid: mois-1-12-ssrf-py
        with client.stream(method="GET", url=url) as resp:
            size += len(resp.read())
    return {"a": a.status, "req": req.full_url, "path": path, "size": size, "b": b.status}


@app.route("/keyword/aio")
async def keyword_url_aio():
    url = request.args["url"]
    # ruleid: mois-1-12-ssrf-py
    async with aiohttp.request("GET", url=url) as resp:
        return {"len": len(await resp.text())}


@app.route("/pool")
def pool_manager():
    url = request.args["url"]
    pool = urllib3.PoolManager()
    # urllib3 연결 풀 객체의 request(method, url)
    # ruleid: mois-1-12-ssrf-py
    resp = pool.request("GET", url)
    return {"status": resp.status}
