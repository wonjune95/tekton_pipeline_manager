"""이스케이프한 값을 이스케이프가 통하는 자리(태그 사이 글자, 따옴표로 감싼 속성 값)에 넣은 경우 — 탐지되면 안 된다."""
import html
from urllib.parse import quote

import bleach
import markupsafe
import nh3
from django.http import HttpResponse
from django.utils.html import escape, format_html
from django.utils.safestring import mark_safe


def escape_options(request):
    q = request.GET.get("q", "")
    # ok: mois-1-04-xss-py quote=True 는 따옴표까지 바꾼다
    a = HttpResponse('<input value="' + html.escape(q, quote=True) + '">')
    # ok: mois-1-04-xss-py 작은따옴표 리터럴도 형식 문자열 리터럴이다
    b = HttpResponse(format_html('<b>{}</b>', q))
    # ok: mois-1-04-xss-py safe="" 는 기본값보다 더 많이 인코딩한다
    c = HttpResponse("<a href='/tags/" + quote(q, safe="") + "'>태그</a>")
    # ok: mois-1-04-xss-py 리터럴 안의 \" · \' 는 리터럴을 끝내지 않는다
    d = HttpResponse(format_html("<span title=\"{}\">{}</span>", q, q))
    # ok: mois-1-04-xss-py
    e = HttpResponse(format_html('<span title=\'{}\'>{}</span>', q, q))
    return a or b or c or d or e


def quoted_attribute_and_text(request):
    q = request.GET.get("q", "")
    # ok: mois-1-04-xss-py 따옴표로 감싼 속성 값
    a = HttpResponse("<input name=q value='" + html.escape(q) + "'>")
    # ok: mois-1-04-xss-py
    b = HttpResponse('<td title="%s">…</td>' % escape(q))
    # ok: mois-1-04-xss-py
    c = HttpResponse('<abbr title="{}">?</abbr>'.format(escape(q)))
    # ok: mois-1-04-xss-py
    d = HttpResponse(f"<input name=q value='{html.escape(q)}'>")
    # ok: mois-1-04-xss-py href 가 고정된 경로로 시작한다 (스킴을 바꿀 수 없다)
    e = HttpResponse('<a href="/search?q=' + escape(q) + '">다시 검색</a>')
    # ok: mois-1-04-xss-py action 이라는 이름의 쿼리 변수일 뿐이다
    f = HttpResponse('<a href="/do?action=' + escape(q) + '">실행</a>')
    # ok: mois-1-04-xss-py format_html 의 인자가 따옴표로 감싼 속성 값에 들어간다
    g = HttpResponse(format_html('<a href="/users/{}/" title="{}">프로필</a>', q, q))
    return a or b or c or d or e or f or g


def after_closed_script_or_handler(request):
    q = request.GET.get("q", "")
    # ok: mois-1-04-xss-py <script> 가 닫힌 뒤의 글자
    a = HttpResponse("<script>var ready = true;</script><p>" + html.escape(q) + "</p>")
    # ok: mois-1-04-xss-py 중괄호가 든 스크립트가 닫힌 뒤
    b = HttpResponse("<script>function go(){ return 1 }</script><p>%s</p>" % html.escape(q))
    # ok: mois-1-04-xss-py f-string 의 {{ }} 는 글자다
    c = HttpResponse(f"<script>var o = {{}};</script><p>{html.escape(q)}</p>")
    # ok: mois-1-04-xss-py 이벤트 핸들러가 있는 태그가 닫힌 뒤의 글자
    d = HttpResponse('<button onclick="go()">' + markupsafe.escape(q) + '</button>')
    # ok: mois-1-04-xss-py
    e = HttpResponse('<a href="javascript:void(0)">' + escape(q) + '</a>')
    return a or b or c or d or e


def cleaned_between_tags(request):
    q = request.GET.get("q", "")
    # ok: mois-1-04-xss-py 정화한 HTML 을 태그 사이에 넣는다
    a = HttpResponse("<div class='comment'>" + bleach.clean(q) + "</div>")
    # ok: mois-1-04-xss-py
    b = HttpResponse("<div class='comment'>%s</div>" % nh3.clean(q))
    # ok: mois-1-04-xss-py
    c = mark_safe("<div class='comment'>{}</div>".format(bleach.clean(q)))
    # ok: mois-1-04-xss-py
    d = HttpResponse(f"<div class='comment'>{nh3.clean(q)}</div>")
    return a or b or c or d
