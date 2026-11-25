"""검증·정화처럼 보이지만 CR·LF 가 남는 경우 — 모두 탐지되어야 한다."""
import re

from django.http import HttpResponse, HttpResponseBadRequest

SEPARATORS = re.compile(r"[;,=]")
DROP_QUOTES = str.maketrans("", "", "\"'")
TOKEN_RE = re.compile(r"[A-Za-z0-9_.-]{1,64}")


def replace_other_characters(request):
    name = request.GET.get("name", "")
    response = HttpResponse("ok")
    # 공백만 바꾼다 — 개행은 그대로
    # ruleid: mois-1-13-http-response-splitting-py
    response["X-File-Name"] = name.replace(" ", "_")
    return response


def removes_cr_only(request):
    name = request.GET.get("name", "")
    response = HttpResponse("ok")
    # \r 만 지우면 \n 한 글자로도 헤더가 나뉜다
    # ruleid: mois-1-13-http-response-splitting-py
    response["X-File-Name"] = name.replace("\r", "")
    return response


def replace_result_discarded(request):
    name = request.GET.get("name", "")
    response = HttpResponse("ok")
    name.replace("\r", "").replace("\n", "")
    # ruleid: mois-1-13-http-response-splitting-py
    response["X-File-Name"] = name
    return response


def sub_other_characters(request):
    name = request.GET.get("name", "")
    response = HttpResponse("ok")
    # ruleid: mois-1-13-http-response-splitting-py
    response["X-File-Name"] = re.sub(r"[;=]", "", name)
    # 미리 컴파일한 정규식도 개행을 지우지 않는다
    # ruleid: mois-1-13-http-response-splitting-py
    response["X-File-Alias"] = SEPARATORS.sub("", name)
    return response


def sub_keeps_only_newlines(request):
    name = request.GET.get("name", "")
    response = HttpResponse("ok")
    # [^\r\n] 은 개행이 아닌 문자를 지운다 — 개행만 남는다
    # ruleid: mois-1-13-http-response-splitting-py
    response["X-File-Name"] = re.sub(r"[^\r\n]", "", name)
    # \s 가 들어 있어도 부정 집합이면 공백·개행이 남는다
    # ruleid: mois-1-13-http-response-splitting-py
    response["X-File-Alias"] = re.sub(r"[^\w\s]", "", name)
    return response


def translate_other_characters(request):
    name = request.GET.get("name", "")
    response = HttpResponse("ok")
    # ruleid: mois-1-13-http-response-splitting-py
    response["X-File-Name"] = name.translate(DROP_QUOTES)
    # ruleid: mois-1-13-http-response-splitting-py
    response["X-File-Alias"] = name.translate(str.maketrans("", "", ";,"))
    # raw 문자열의 \r\n 은 역슬래시·r·n 세 글자다 — 개행은 지워지지 않는다
    # ruleid: mois-1-13-http-response-splitting-py
    response["X-File-Raw"] = name.translate(str.maketrans("", "", r"\r\n"))
    return response


def prefix_match_only(request):
    lang = request.GET.get("lang", "")
    # re.match + $ 는 끝의 개행 앞에서도 맞는다: "ko\n" 통과
    if not re.match(r"^[a-z]{2}$", lang):
        return HttpResponseBadRequest("invalid lang")
    response = HttpResponse("ok")
    # ruleid: mois-1-13-http-response-splitting-py
    response.set_cookie("lang", lang)
    return response


def check_result_ignored(request):
    token = request.GET.get("token", "")
    TOKEN_RE.fullmatch(token)
    response = HttpResponse("ok")
    # ruleid: mois-1-13-http-response-splitting-py
    response["X-Token"] = token
    return response


def failure_does_not_exit(request):
    token = request.GET.get("token", "")
    if not TOKEN_RE.fullmatch(token):
        print("suspicious token")
    response = HttpResponse("ok")
    # ruleid: mois-1-13-http-response-splitting-py
    response["X-Token"] = token
    return response


def opposite_branch(request):
    token = request.GET.get("token", "")
    response = HttpResponse("ok")
    if token.isalnum():
        pass
    else:
        # ruleid: mois-1-13-http-response-splitting-py
        response["X-Token"] = token
    return response


def used_when_check_fails(request):
    token = request.GET.get("token", "")
    response = HttpResponse("ok")
    if not TOKEN_RE.fullmatch(token):
        # ruleid: mois-1-13-http-response-splitting-py
        response["X-Rejected-Token"] = token
    return response


def sink_inside_failing_branch(request):
    token = request.GET.get("token", "")
    response = HttpResponse("ok")
    if not TOKEN_RE.fullmatch(token):
        # 형식이 틀린 값을 헤더에 넣고 빠져나간다
        # ruleid: mois-1-13-http-response-splitting-py
        response["X-Rejected-Token"] = token
        return response
    return response


def nested_conditional_exit(request):
    token = request.GET.get("token", "")
    response = HttpResponse("ok")
    if not TOKEN_RE.fullmatch(token):
        if request.GET.get("strict"):
            return response
    # 엄격 모드가 아니면 검사에 실패한 값이 그대로 내려온다
    # ruleid: mois-1-13-http-response-splitting-py
    response["X-Token"] = token
    return response


def reassigned_after_check(request):
    token = request.GET.get("token", "")
    response = HttpResponse("ok")
    if not TOKEN_RE.fullmatch(token):
        return response
    # 검사한 뒤에 다른 입력으로 바꿔 넣는다
    token = request.GET.get("alias", "")
    # ruleid: mois-1-13-http-response-splitting-py
    response["X-Token"] = token
    return response


def appended_after_check(request):
    token = request.GET.get("token", "")
    response = HttpResponse("ok")
    if not TOKEN_RE.fullmatch(token):
        return response
    # 검사한 뒤에 검사하지 않은 입력을 덧붙인다
    token += request.GET.get("suffix", "")
    # ruleid: mois-1-13-http-response-splitting-py
    response["X-Token"] = token
    return response


def check_joined_with_and(request):
    token = request.GET.get("token", "")
    response = HttpResponse("ok")
    # 엄격 모드일 때만 검사한다
    if request.GET.get("strict") and not TOKEN_RE.fullmatch(token):
        return response
    # ruleid: mois-1-13-http-response-splitting-py
    response["X-Token"] = token
    return response


def check_joined_with_or(request):
    token = request.GET.get("token", "")
    response = HttpResponse("ok")
    # or 로 묶이면 검사를 통과하지 않은 값도 들어온다
    if request.user.is_staff or TOKEN_RE.fullmatch(token):
        # ruleid: mois-1-13-http-response-splitting-py
        response["X-Token"] = token
    return response


# --- 개행을 지우는 것처럼 보이지만 남거나 다시 생기는 경우 ---

NEWLINES = re.compile(r"[\r\n]+")
SWAPPED_NEWLINES = re.compile(r"[\r\n]+")
REDEFINED_NEWLINES = re.compile(r"[\r\n]+")
REDEFINED_NEWLINES = re.compile(r"[;]+")
PIPE_TO_NEWLINE = str.maketrans("|", "\n", "\r\n")
SWAPPED_TABLE = str.maketrans("", "", "\r\n")
REDEFINED_TABLE = str.maketrans("", "", "\r\n")
REDEFINED_TABLE = str.maketrans("", "", ";")


def replace_reintroduces_newline(request):
    name = request.GET.get("name", "")
    response = HttpResponse("ok")
    # 두 번째 replace 가 개행을 다시 넣는다
    # ruleid: mois-1-13-http-response-splitting-py
    response["X-File-Name"] = name.replace("\r", "").replace("\n", "\r\n ")
    # \n 을 지운 뒤에 \r 을 \n 으로 바꾼다
    # ruleid: mois-1-13-http-response-splitting-py
    response["X-File-Alias"] = name.replace("\n", "").replace("\r", "\n")
    return response


def sub_limited_count(request):
    name = request.GET.get("name", "")
    response = HttpResponse("ok")
    # count=1 이면 첫 개행만 지운다
    # ruleid: mois-1-13-http-response-splitting-py
    response["X-File-Name"] = re.sub(r"[\r\n]", "", name, 1)
    # ruleid: mois-1-13-http-response-splitting-py
    response["X-File-Alias"] = re.sub(r"[\r\n]", "", name, count=1)
    # ruleid: mois-1-13-http-response-splitting-py
    response["X-File-Third"] = NEWLINES.sub("", name, 1)
    return response


def sub_replacement_is_newline(request):
    name = request.GET.get("name", "")
    response = HttpResponse("ok")
    # 개행을 개행으로 바꾼다
    # ruleid: mois-1-13-http-response-splitting-py
    response["X-File-Name"] = re.sub(r"[\r\n]+", "\n", name)
    # re.sub 은 바꿀 문자열의 r"\n" 을 개행으로 푼다
    # ruleid: mois-1-13-http-response-splitting-py
    response["X-File-Alias"] = re.sub(r"[\r\n]+", r"\n", name)
    # ruleid: mois-1-13-http-response-splitting-py
    response["X-File-Third"] = NEWLINES.sub("\n", name)
    return response


def sub_partial_pattern(request):
    name = request.GET.get("name", "")
    response = HttpResponse("ok")
    # "\r\n" 은 짝을 이룬 CRLF 만 지운다 — \n 하나로도 헤더가 나뉜다
    # ruleid: mois-1-13-http-response-splitting-py
    response["X-A"] = re.sub(r"\r\n", "", name)
    # 끝의 공백만 지운다 (rstrip 과 같다) — 가운데 개행은 남는다
    # ruleid: mois-1-13-http-response-splitting-py
    response["X-B"] = re.sub(r"\s+$", "", name)
    # 맨 앞의 개행만 지운다
    # ruleid: mois-1-13-http-response-splitting-py
    response["X-C"] = re.sub(r"^[\r\n]+", "", name)
    # 개행 두 개가 이어진 곳만 지운다
    # ruleid: mois-1-13-http-response-splitting-py
    response["X-D"] = re.sub(r"[\r\n]{2}", "", name)
    # 끝에 실제 개행 글자가 붙은 정규식: 개행 두 개가 이어진 곳만 지운다
    # ruleid: mois-1-13-http-response-splitting-py
    response["X-E"] = re.sub("[\r\n]\n", "", name)
    return response


def sub_negated_class_keeps_newlines(request):
    name = request.GET.get("name", "")
    response = HttpResponse("ok")
    # "ASCII 가 아닌 글자를 지운다" — \r(0x0d)·\n(0x0a) 은 ASCII 라서 남는다
    # ruleid: mois-1-13-http-response-splitting-py
    response["X-A"] = re.sub(r"[^\x00-\x7f]", "", name)
    # 탭(0x09)부터 ~ 까지의 범위에는 개행이 들어 있다
    # ruleid: mois-1-13-http-response-splitting-py
    response["X-B"] = re.sub(r"[^\t-~]", "", name)
    # + 부터 z 까지처럼 기호에서 시작하는 범위는 무엇이 들어 있는지 확인하지 않는다
    # ruleid: mois-1-13-http-response-splitting-py
    response["X-C"] = re.sub(r"[^+-z]", "", name)
    # ruleid: mois-1-13-http-response-splitting-py
    response["X-D"] = re.sub(r"[^A-_]", "", name)
    # ruleid: mois-1-13-http-response-splitting-py
    response["X-E"] = re.sub(r"[^A-z]", "", name)
    # ruleid: mois-1-13-http-response-splitting-py
    response["X-F"] = re.sub(r"[^0-Z]", "", name)
    return response


def sub_compiled_replaced_globally(request):
    global SWAPPED_NEWLINES
    name = request.GET.get("name", "")
    response = HttpResponse("ok")
    # global 로 모듈 수준의 정규식을 요청 값으로 바꿔 넣었다
    SWAPPED_NEWLINES = re.compile(request.GET.get("strip", ";"))
    # ruleid: mois-1-13-http-response-splitting-py
    response["X-File-Name"] = SWAPPED_NEWLINES.sub("", name)
    return response


def sub_compiled_redefined(request):
    name = request.GET.get("name", "")
    response = HttpResponse("ok")
    # REDEFINED_NEWLINES 는 모듈 수준에서 [;]+ 로 다시 정의되었다
    # ruleid: mois-1-13-http-response-splitting-py
    response["X-File-Name"] = REDEFINED_NEWLINES.sub("", name)
    return response


def translate_maps_to_newline(request):
    name = request.GET.get("name", "")
    response = HttpResponse("ok")
    # 개행을 지우지만 | 를 개행으로 바꿔 넣는다
    # ruleid: mois-1-13-http-response-splitting-py
    response["X-File-Name"] = name.translate(str.maketrans("|", "\n", "\r\n"))
    # ruleid: mois-1-13-http-response-splitting-py
    response["X-File-Alias"] = name.translate(PIPE_TO_NEWLINE)
    return response


def translate_table_replaced_globally(request):
    global SWAPPED_TABLE
    name = request.GET.get("name", "")
    response = HttpResponse("ok")
    # global 로 모듈 수준의 변환표를 바꿔 넣었다
    SWAPPED_TABLE = str.maketrans("", "", request.GET.get("strip", ";"))
    # ruleid: mois-1-13-http-response-splitting-py
    response["X-File-Name"] = name.translate(SWAPPED_TABLE)
    return response


def translate_table_redefined(request):
    name = request.GET.get("name", "")
    response = HttpResponse("ok")
    # REDEFINED_TABLE 은 모듈 수준에서 다시 정의되었다
    # ruleid: mois-1-13-http-response-splitting-py
    response["X-File-Name"] = name.translate(REDEFINED_TABLE)
    return response
