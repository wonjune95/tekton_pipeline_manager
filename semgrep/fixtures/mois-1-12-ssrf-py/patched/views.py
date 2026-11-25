import requests
from django.http import HttpResponse, HttpResponseBadRequest

ALLOWED_FEEDS = {
    "notice": "https://www.example.go.kr/notice/rss.xml",
    "press": "https://www.example.go.kr/press/rss.xml",
}


def fetch_feed(request):
    # 허용 목록에 있는 주소로만 요청
    url = ALLOWED_FEEDS.get(request.GET.get("feed", ""))
    if url is None:
        return HttpResponseBadRequest("unknown feed")
    # ok: mois-1-12-ssrf-py 같은 파일의 dict 에서 꺼낸 주소
    resp = requests.get(url, timeout=5)
    return HttpResponse(resp.content, content_type="application/xml")
