import requests
from django.http import HttpResponse


def fetch_feed(request):
    url = request.GET.get("url", "")
    # 외부 입력 URL 로 서버가 요청을 보냄 (내부망·메타데이터 주소 접근 가능)
    # ruleid: mois-1-12-ssrf-py
    resp = requests.get(url, timeout=5)
    return HttpResponse(resp.content, content_type="application/xml")
