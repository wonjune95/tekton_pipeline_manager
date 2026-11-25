"""요청의 "경로" 값으로 만든 리다이렉트 (Django).

//evil.example/x 로 들어온 요청은 request.path 가 "//evil.example/x" 다. 이것을 Location 에 그대로 넣으면
브라우저는 스킴만 이어받아 evil.example 로 간다. /\\evil.example 도 브라우저는 같은 뜻으로 읽는다.
"""
import re

from django.http import HttpResponse, HttpResponsePermanentRedirect, HttpResponseRedirect
from django.shortcuts import redirect
from django.views import View


def back_to_same_path(request):
    # ruleid: mois-1-07-open-redirect-path-py
    return redirect(request.path)


def back_with_query(request):
    # 경로와 질의 문자열
    # ruleid: mois-1-07-open-redirect-path-py
    return HttpResponseRedirect(request.get_full_path())


def back_after_save(req):
    # 요청 객체 이름이 req 인 경우
    # ruleid: mois-1-07-open-redirect-path-py
    return HttpResponsePermanentRedirect(req.path)


class SaveDraftView(View):
    def post(self, request, *args, **kwargs):
        # 클래스 기반 뷰의 self.request
        # ruleid: mois-1-07-open-redirect-path-py
        return redirect(self.request.get_full_path())


def location_header(request):
    response = HttpResponse(status=302)
    # Location 헤더를 직접 넣음
    # ruleid: mois-1-07-open-redirect-path-py
    response["Location"] = request.path
    return response


def path_with_suffix_removed(request):
    path = request.path
    # 뒤쪽만 잘라 낸 경로 — 앞쪽은 그대로다
    # ruleid: mois-1-07-open-redirect-path-py
    return redirect(path.removesuffix("index/"))


def slashes_collapsed(request):
    # 겹친 슬래시를 하나로 줄인 경로. "//" 는 사라지지만 규칙은 이것을 검증으로 인정하지 않는다 (확인 대상으로 남는다)
    normalized = re.sub(r"/{2,}", "/", request.path)
    # ruleid: mois-1-07-open-redirect-path-py
    return HttpResponsePermanentRedirect(normalized)
