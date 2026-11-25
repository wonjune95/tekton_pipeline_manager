"""이름만 reverse 인 함수 — django.urls.reverse 가 아니므로 경로를 만들어 주지 않는다."""
from django.shortcuts import redirect


def reverse(text):
    # 문자열을 뒤집는 보조 함수
    return text[::-1]


def go(request):
    # ruleid: mois-1-07-open-redirect-path-py
    return redirect(reverse(request.path) + "?from=menu")
