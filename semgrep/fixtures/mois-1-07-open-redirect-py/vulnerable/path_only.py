"""요청의 "경로" 값으로 만든 리다이렉트 — 이 규칙(block)은 보고하지 않는다.

//evil.example/x 로 들어온 요청이면 다른 호스트로 갈 수 있지만 흔한 관용구라 block 하지 않고,
warn 규칙 mois-1-07-open-redirect-path-py 가 보고한다 (fixtures/mois-1-07-open-redirect-path-py).
아래 줄에는 이 규칙의 ruleid 표시가 없다 — 이 규칙이 탐지하면 회귀시험이 실패한다.
"""
import flask
from django.shortcuts import redirect
from django.views import View


def back_to_same_path(request):
    # ok: mois-1-07-open-redirect-py 경로와 질의 문자열만 담는 값 (warn 규칙이 맡는다)
    return redirect(request.get_full_path())


def back_after_save(req):
    # ok: mois-1-07-open-redirect-py 요청 객체 이름이 req 인 경우
    return redirect(req.path)


class SaveDraftView(View):
    def post(self, request, *args, **kwargs):
        # ok: mois-1-07-open-redirect-py 클래스 기반 뷰의 self.request
        return redirect(self.request.get_full_path())


def same_page_query():
    # ok: mois-1-07-open-redirect-py Flask 의 full_path, `import flask` 뒤 flask.request 로 쓴 요청
    return flask.redirect(flask.request.full_path)
