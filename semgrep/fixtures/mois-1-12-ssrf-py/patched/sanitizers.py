import requests
from django.http import JsonResponse


def fixed_host(request):
    item = request.GET.get("item", "")
    # ok: mois-1-12-ssrf-py 스킴과 호스트가 리터럴로 고정되고 입력은 경로·질의에만 쓰인다
    a = requests.get("https://api.example.go.kr/items/" + item, timeout=5)
    # ok: mois-1-12-ssrf-py
    b = requests.get("https://api.example.go.kr/items/%s/detail" % item, timeout=5)
    # ok: mois-1-12-ssrf-py
    c = requests.get("https://api.example.go.kr/items/{}".format(item), timeout=5)
    # ok: mois-1-12-ssrf-py
    d = requests.get(f"https://api.example.go.kr/search?q={item}", timeout=5)
    return JsonResponse({"sizes": [len(r.content) for r in (a, b, c, d)]})


def fixed_host_more(request):
    item = request.GET.get("item", "")
    page = request.GET.get("page", "1")
    # ok: mois-1-12-ssrf-py 나란히 적어 이어 붙인 리터럴 — 첫 리터럴이 호스트를 고정한다
    a = requests.get("https://api.example.go.kr/items/" f"{item}/detail", timeout=5)
    # ok: mois-1-12-ssrf-py 뒤쪽 값에 건 연산(메서드·슬라이스·조건식)은 맨 앞 리터럴을 바꾸지 못한다
    b = requests.get("https://api.example.go.kr/items/" + item.strip().split("/")[0] + "?tag=" + (item[1:] or "all"), timeout=5)
    # ok: mois-1-12-ssrf-py 정수로 바꾼 값을 경로·질의 자리에만 쓴다 (호스트·포트 자리의 int() 는 vulnerable/ 참고)
    c = requests.get("https://api.example.go.kr/items/%d" % int(page), timeout=5)
    # ok: mois-1-12-ssrf-py
    d = requests.get(f"https://api.example.go.kr/items?page={int(page)}", timeout=5)
    return JsonResponse({"sizes": [len(r.content) for r in (a, b, c, d)]})


def not_http_clients(request, cache, registry):
    key = request.GET.get("key", "")
    # ok: mois-1-12-ssrf-py dict·캐시의 get, 임의 객체의 request 는 HTTP 요청이 아니다
    value = cache.get(key)
    ticket = registry.request("reserve", key)
    return JsonResponse({"value": value, "ticket": ticket})
