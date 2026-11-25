"""회귀 시험 — 괄호 친 수신 객체의 메서드 호출이 조건에 있는 파일.

Semgrep 1.180 은 metavariable-pattern 안에서 metavariable-regex 를 평가할 때, 조건식이
`if(a.b(k=v)).exists():` 처럼 괄호로 감싼 수신 객체의 메서드 호출이면 내부 오류
(Invalid_argument: String.sub / Bytes.sub)를 낸다. 이 오류는 규칙 하나의 문제가 아니라
그 파일에 대한 **모든 규칙의 탐지**를 버리게 만든다 (django.nV taskManager/views.py 에서 실제로 일어났다).

이 파일은 그 모양을 그대로 담고 있다. 아래의 표시한 줄이 탐지되지 않으면 내부 오류가 다시 생긴 것이다.
오류는 파일 앞부분이 어느 정도 길어야(조건식의 위치가 뒤쪽이어야) 나타나므로 이 설명과 import 를 줄이지 말 것.

규칙을 쓸 때 지킬 것: metavariable-regex 는 metavariable-pattern 바깥에 둔다
(안쪽 patterns 로 한 겹 감싸고 정규식은 그 바깥에 건다 — docs/rule-conventions.md 4절).
"""
import datetime
import mimetypes
import os
import codecs

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.utils import timezone
from django.db import connection
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth.models import Group, User

from .models import Project, Task


def index(request):
    sorted_projects = Project.objects.order_by('-start_date')
    list_to_show = []
    for project in sorted_projects:
        if(project.users_assigned.filter(username=request.user.username)).exists():
            list_to_show.append(project)
    if request.user.is_authenticated():
        return redirect("/dashboard")
    return render(request, 'index.html', {'project_list': list_to_show})


def download(request):
    response = HttpResponse("ok")
    # ruleid: mois-1-13-http-response-splitting-py
    response["Content-Disposition"] = "attachment; filename=" + request.GET.get("name", "")
    return response
