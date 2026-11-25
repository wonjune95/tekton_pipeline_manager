import re
from urllib.parse import quote, quote_plus, urlencode

from django.http import HttpResponse
from django.utils.text import slugify
from werkzeug.utils import secure_filename

NEWLINES = re.compile(r"[\r\n]+")
DROP_NEWLINES = str.maketrans("", "", "\r\n")


def replace_both(request):
    name = request.GET.get("name", "")
    response = HttpResponse("ok")
    # ok: mois-1-13-http-response-splitting-py \r 과 \n 을 모두 지움
    response["X-File-Name"] = name.replace("\r", "").replace("\n", "")
    # ok: mois-1-13-http-response-splitting-py 순서가 바뀌어도 같다
    response["X-File-Alias"] = name.replace("\n", " ").replace("\r", " ")
    return response


def sub_newlines(request):
    name = request.GET.get("name", "")
    response = HttpResponse("ok")
    # ok: mois-1-13-http-response-splitting-py 정규식에 \r·\n 이 모두 있다
    response["X-A"] = re.sub(r"[\r\n]", "", name)
    # ok: mois-1-13-http-response-splitting-py raw 문자열이 아니어도 같다
    response["X-B"] = re.sub("\r|\n", "", name)
    # ok: mois-1-13-http-response-splitting-py raw 문자열로 적은 \r|\n
    response["X-B2"] = re.sub(r"\n|\r", "", name)
    # ok: mois-1-13-http-response-splitting-py 실제 개행 글자가 든 집합 (raw 가 아닌 문자열)
    response["X-B3"] = re.sub("[\r\n]+", " ", name)
    # ok: mois-1-13-http-response-splitting-py \s 는 CR·LF 를 포함한다
    response["X-C"] = re.sub(r"\s+", " ", name)
    # ok: mois-1-13-http-response-splitting-py 허용 문자만 남기는 부정 집합
    response["X-D"] = re.sub(r"[^A-Za-z0-9_.-]", "_", name)
    # ok: mois-1-13-http-response-splitting-py 같은 파일에서 컴파일한 정규식
    response["X-E"] = NEWLINES.sub("", name)
    return response


def translate_newlines(request):
    name = request.GET.get("name", "")
    response = HttpResponse("ok")
    # ok: mois-1-13-http-response-splitting-py 삭제 문자에 \r·\n 이 있다
    response["X-A"] = name.translate(str.maketrans("", "", "\r\n"))
    # ok: mois-1-13-http-response-splitting-py 같은 파일에 정의한 변환표
    response["X-B"] = name.translate(DROP_NEWLINES)
    return response


def encoded(request):
    name = request.GET.get("name", "")
    response = HttpResponse("ok")
    # ok: mois-1-13-http-response-splitting-py URL 인코딩하면 개행이 %0D%0A 가 된다
    response["Content-Disposition"] = "attachment; filename*=UTF-8''" + quote(name)
    # ok: mois-1-13-http-response-splitting-py
    response["X-Query"] = quote_plus(name)
    # ok: mois-1-13-http-response-splitting-py
    response["X-Next"] = "/search?" + urlencode({"q": name})
    # ok: mois-1-13-http-response-splitting-py 영문·숫자·-·_ 만 남긴다
    response["X-Slug"] = slugify(name)
    # ok: mois-1-13-http-response-splitting-py
    response["X-Stored-As"] = secure_filename(name)
    # ok: mois-1-13-http-response-splitting-py 정수로 바꾼 값
    response.set_cookie("page", int(request.GET.get("page", "1")))
    return response
