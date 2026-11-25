"""이스케이프 함수를 썼지만 옵션이나 출력 위치 때문에 막지 못하는 경우 — 모두 탐지되어야 한다."""
import html
from urllib.parse import quote, quote_plus

import bleach
import markupsafe
import nh3
from django.http import HttpResponse
from django.utils.html import escape, format_html
from django.utils.safestring import mark_safe


def escape_options(request):
    q = request.GET.get("q", "")
    keep_quotes = request.GET.get("raw") == "1"
    # quote=False 는 따옴표를 그대로 둔다 → 속성 값을 빠져나온다 (" onfocus=…)
    # ruleid: mois-1-04-xss-py
    a = HttpResponse('<input value="' + html.escape(q, quote=False) + '">')
    # 위치 인자로 준 False 도 같다
    # ruleid: mois-1-04-xss-py
    b = HttpResponse("<input value='" + html.escape(q, False) + "'>")
    # quote 가 변수면 따옴표를 바꾸는지 알 수 없다
    # ruleid: mois-1-04-xss-py
    c = HttpResponse('<input value="' + html.escape(q, quote=keep_quotes) + '">')
    # 허용 태그·속성을 직접 주면 script·onerror 가 남을 수 있다
    # ruleid: mois-1-04-xss-py
    d = HttpResponse(bleach.clean(q, tags=["script", "img"], attributes={"img": ["src", "onerror"]}))
    # ruleid: mois-1-04-xss-py
    e = HttpResponse(nh3.clean(q, tags={"script"}))
    # safe= 로 : 를 풀어 주면 javascript: 가 그대로 남는다
    # ruleid: mois-1-04-xss-py
    f = HttpResponse('<a href="' + quote(q, safe=":/?&=") + '">link</a>')
    # ruleid: mois-1-04-xss-py
    g = HttpResponse("<p>" + quote_plus(q, safe="<>/ =") + "</p>")
    return a or b or c or d or e or f or g


def format_html_format_string(request):
    q = request.GET.get("q", "")
    n = request.GET.get("n", "")
    # format_html 은 "인자"만 이스케이프한다. 형식 문자열에 이어 붙인 입력은 그대로 나간다
    # ruleid: mois-1-04-xss-py
    a = HttpResponse(format_html("<b>" + q + "</b>"))
    # ruleid: mois-1-04-xss-py
    b = HttpResponse(format_html(f"<b>{q}</b>"))
    # 인자가 따로 있어도 형식 문자열에 입력이 들어가면 같다
    # ruleid: mois-1-04-xss-py
    c = HttpResponse(format_html("<b>" + q + "</b> {}", n))
    # 형식 문자열이 리터럴이어도 href 자리의 값은 이스케이프로 막지 못한다 (javascript:…)
    # ruleid: mois-1-04-xss-py
    d = HttpResponse(format_html('<a href="{}">link</a>', q))
    return a or b or c or d


def escaped_into_wrong_place(request):
    q = request.GET.get("q", "")
    # <script> 안: 따옴표 없이도 코드가 된다 (alert(1))
    # ruleid: mois-1-04-xss-py
    a = HttpResponse("<script>var page = " + html.escape(q) + ";</script>")
    # href 맨 앞: javascript:alert(1) 에는 이스케이프할 글자가 없다
    # ruleid: mois-1-04-xss-py
    b = mark_safe('<a href="%s">back</a>' % escape(q))
    # ruleid: mois-1-04-xss-py
    c = HttpResponse('<img src="{}">'.format(escape(q)))
    # srcdoc 값은 속성에서 한 번 풀린 뒤 HTML 로 다시 해석된다
    # ruleid: mois-1-04-xss-py
    d = HttpResponse(f'<iframe srcdoc="{html.escape(q)}"></iframe>')
    # ruleid: mois-1-04-xss-py
    e = HttpResponse('<form method="post" action="' + escape(q) + '">')
    # ruleid: mois-1-04-xss-py
    f = HttpResponse("<object data='" + escape(q) + "'></object>")
    # 이벤트 핸들러 안: 속성 값이 풀린 뒤 스크립트로 실행된다 (&#x27; → ')
    # ruleid: mois-1-04-xss-py
    g = HttpResponse('<button onclick="go(\'' + markupsafe.escape(q) + '\')">x</button>')
    # ruleid: mois-1-04-xss-py
    h = HttpResponse('<a href="javascript:go(\'' + escape(q) + '\')">x</a>')
    # 속성 이름 앞이 공백이 아니라 줄바꿈(\n)이어도 같다
    # ruleid: mois-1-04-xss-py
    j = HttpResponse("<a\nhref='" + escape(q) + "'>back</a>")
    # ruleid: mois-1-04-xss-py
    k = HttpResponse("<img src='/logo.png'\nonerror=\"report('" + escape(q) + "')\">")
    # str() 로 감싸도 위치는 같다
    # ruleid: mois-1-04-xss-py
    i = HttpResponse("<script>var u = " + str(markupsafe.escape(q)) + "</script>")
    return a or b or c or d or e or f or g or h or i or j or k


def escaped_into_unquoted_attribute(request):
    q = request.GET.get("q", "")
    # 따옴표 없는 속성 값: 공백 하나로 새 속성을 붙일 수 있다 (x onfocus=alert(1) autofocus)
    # ruleid: mois-1-04-xss-py
    a = HttpResponse("<input name=q value=" + html.escape(q) + ">")
    # ruleid: mois-1-04-xss-py
    b = HttpResponse("<input name=q value=%s>" % html.escape(q))
    # ruleid: mois-1-04-xss-py
    c = HttpResponse("<td class=cell-{}>".format(html.escape(q)))
    # ruleid: mois-1-04-xss-py
    d = HttpResponse(f"<option value={html.escape(q)}>")
    return a or b or c or d


def cleaned_into_attribute(request):
    q = request.GET.get("q", "")
    # bleach.clean·nh3.clean 은 따옴표를 바꾸지 않는다 — 속성 값 안에서는 쓸 수 없다
    # ruleid: mois-1-04-xss-py
    a = HttpResponse('<img alt="' + bleach.clean(q) + '">')
    # ruleid: mois-1-04-xss-py
    b = HttpResponse("<img alt='%s'>" % nh3.clean(q))
    # ruleid: mois-1-04-xss-py
    c = HttpResponse('<abbr title="{}">?</abbr>'.format(bleach.clean(q)))
    # ruleid: mois-1-04-xss-py
    d = HttpResponse(f"<span title='{nh3.clean(q)}'>i</span>")
    return a or b or c or d
