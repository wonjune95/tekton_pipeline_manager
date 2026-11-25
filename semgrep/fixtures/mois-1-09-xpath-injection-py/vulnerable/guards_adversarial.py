"""guard 를 속이는 경우 — 모두 탐지되어야 한다.

종료처럼 보이는 호출(exit·quit·이름만 abort), 검사식을 다른 식으로 감싼 조건(&·|·not not·비교·호출 인자),
검사 뒤·조건 안의 재대입, 아무것이나 통과시키는 정규식.
"""
import re

from django.http import HttpResponse, HttpResponseBadRequest
from lxml import etree
from .patterns import TOKEN_PATTERN

USERS_XML = "/srv/data/users.xml"
PARSER = etree.XMLParser(resolve_entities=False, no_network=True)
GOOD_RE = re.compile(r"[A-Za-z0-9_]{1,40}")
SWAPPED_RE = re.compile(r"[A-Za-z0-9_]{1,40}")
ANY_RE = re.compile(r".*")
REDEFINED_RE = re.compile(r"[A-Za-z0-9_]{1,40}")
REDEFINED_RE = re.compile(r".*")
PLUS_TO_Z_RE = re.compile(r"[+-z]+")
UPPER_TO_LOWER_RE = re.compile(r"[A-z]+")


def abort(code):
    print("rejected", code)


def audit(result):
    print("check", result)
    return False


def builtin_exit(request):
    name = request.GET.get("name", "")
    tree = etree.parse(USERS_XML, PARSER)
    if not name.isalnum():
        exit(2)
    # 내장 exit() 는 site 모듈이 넣어 주는 대화형 도우미다 (python -S·임베디드 환경에는 없다) — import 로 확인되는 sys.exit 만 종료로 본다
    # ruleid: mois-1-09-xpath-injection-py
    tree.xpath("//user[@name='" + name + "']")
    return HttpResponse("ok")


def builtin_quit(request):
    name = request.GET.get("name", "")
    tree = etree.parse(USERS_XML, PARSER)
    if not name.isalnum():
        quit()
    # 내장 quit() 도 같다
    # ruleid: mois-1-09-xpath-injection-py
    tree.xpath("//user[@name='" + name + "']")
    return HttpResponse("ok")


def local_abort(request):
    name = request.GET.get("name", "")
    tree = etree.parse(USERS_XML, PARSER)
    if not name.isalnum():
        abort(400)
    # 이 파일의 abort 는 기록만 하고 돌아온다 — 이름이 abort 일 뿐 중단하지 않는다
    # ruleid: mois-1-09-xpath-injection-py
    tree.xpath("//user[@name='" + name + "']")
    return HttpResponse("ok")


def check_joined_with_bitand(request, strict):
    name = request.GET.get("name", "")
    tree = etree.parse(USERS_XML, PARSER)
    if (not name.isalnum()) & strict:
        return HttpResponseBadRequest("invalid")
    # & 로 묶이면 strict 가 거짓일 때 검사에 실패한 값이 그대로 내려온다
    # ruleid: mois-1-09-xpath-injection-py
    tree.xpath("//user[@name='" + name + "']")
    return HttpResponse("ok")


def double_negation(request):
    name = request.GET.get("name", "")
    tree = etree.parse(USERS_XML, PARSER)
    if not (not re.fullmatch(r"[A-Za-z0-9_]{1,40}", name)):
        return HttpResponseBadRequest("invalid")
    # not (not …) 은 뜻이 뒤집힌다: 형식이 맞으면 빠져나가고 틀린 값이 내려온다
    # ruleid: mois-1-09-xpath-injection-py
    tree.xpath("//user[@name='" + name + "']")
    return HttpResponse("ok")


def check_compared_with_flag(request, strict):
    name = request.GET.get("name", "")
    tree = etree.parse(USERS_XML, PARSER)
    if (not GOOD_RE.fullmatch(name)) == strict:
        return HttpResponseBadRequest("invalid")
    # 검사 결과를 다른 값과 비교하면 strict 가 거짓일 때 틀린 값이 내려온다
    # ruleid: mois-1-09-xpath-injection-py
    tree.xpath("//user[@name='" + name + "']")
    return HttpResponse("ok")


def check_passed_to_call(request):
    name = request.GET.get("name", "")
    tree = etree.parse(USERS_XML, PARSER)
    if audit(not name.isalnum()):
        return HttpResponseBadRequest("invalid")
    # 검사 결과를 다른 함수에 넘기면 그 함수가 무엇을 돌려주는지 알 수 없다
    # ruleid: mois-1-09-xpath-injection-py
    tree.xpath("//user[@name='" + name + "']")
    return HttpResponse("ok")


def tuple_reassigned_after_check(request):
    name = request.GET.get("name", "")
    tree = etree.parse(USERS_XML, PARSER)
    if not name.isalnum():
        return HttpResponseBadRequest("invalid")
    name, mode = request.GET.get("alias", "").split(":")
    # 검사한 뒤에 튜플 풀기 대입으로 다른 입력을 넣는다
    # ruleid: mois-1-09-xpath-injection-py
    tree.xpath("//user[@name='" + name + "']")
    return HttpResponse("ok")


def check_joined_with_bitor(request, strict):
    name = request.GET.get("name", "")
    tree = etree.parse(USERS_XML, PARSER)
    if strict | name.isalnum():
        # | 로 묶이면 strict 가 참일 때 검사를 통과하지 않은 값도 들어온다
        # ruleid: mois-1-09-xpath-injection-py
        tree.xpath("//user[@name='" + name + "']")
    return HttpResponse("ok")


def positive_check_is_none(request):
    name = request.GET.get("name", "")
    tree = etree.parse(USERS_XML, PARSER)
    if GOOD_RE.fullmatch(name) is None:
        # is None 과 비교하면 뜻이 뒤집힌다: 형식이 틀렸을 때만 들어온다
        # ruleid: mois-1-09-xpath-injection-py
        tree.xpath("//user[@name='" + name + "']")
    return HttpResponse("ok")


def positive_inline_check_is_none(request):
    name = request.GET.get("name", "")
    tree = etree.parse(USERS_XML, PARSER)
    if re.fullmatch(r"[A-Za-z0-9_]{1,40}", name) is None:
        # 조건에 적은 정규식도 마찬가지다: is None 이면 형식이 틀렸을 때만 들어온다
        # ruleid: mois-1-09-xpath-injection-py
        tree.xpath("//user[@name='" + name + "']")
    return HttpResponse("ok")


def positive_check_passed_to_call(request):
    name = request.GET.get("name", "")
    tree = etree.parse(USERS_XML, PARSER)
    if audit(name.isalnum()):
        # 검사 결과를 다른 함수에 넘긴 조건은 검사가 아니다
        # ruleid: mois-1-09-xpath-injection-py
        tree.xpath("//user[@name='" + name + "']")
    return HttpResponse("ok")


def used_in_condition_before_check(request):
    name = request.GET.get("name", "")
    tree = etree.parse(USERS_XML, PARSER)
    # 조건식 안에서 검사보다 먼저 쓴다 (and 는 왼쪽부터 실행한다)
    # ruleid: mois-1-09-xpath-injection-py
    if tree.xpath("//user[@name='" + name + "']") and name.isalnum():
        pass
    return HttpResponse("ok")


def reassigned_inside_if(request):
    name = request.GET.get("name", "")
    tree = etree.parse(USERS_XML, PARSER)
    if name.isalnum():
        name = request.GET.get("alias", "")
        # 검사를 통과한 조건 안에서 다른 입력으로 바꿔 넣는다
        # ruleid: mois-1-09-xpath-injection-py
        tree.xpath("//user[@name='" + name + "']")
    return HttpResponse("ok")


def appended_inside_if(request):
    name = request.GET.get("name", "")
    tree = etree.parse(USERS_XML, PARSER)
    if GOOD_RE.fullmatch(name):
        name += request.GET.get("suffix", "")
        # 검사를 통과한 조건 안에서 검사하지 않은 입력을 덧붙인다
        # ruleid: mois-1-09-xpath-injection-py
        tree.xpath("//user[@name='" + name + "']")
    return HttpResponse("ok")


def tuple_reassigned_inside_if(request):
    name = request.GET.get("name", "")
    tree = etree.parse(USERS_XML, PARSER)
    if name.isalnum():
        name, mode = request.GET.get("alias", "").split(":")
        # 검사를 통과한 조건 안에서 튜플 풀기 대입으로 다른 입력을 넣는다
        # ruleid: mois-1-09-xpath-injection-py
        tree.xpath("//user[@name='" + name + "']")
    return HttpResponse("ok")


def wildcard_pattern(request):
    name = request.GET.get("name", "")
    tree = etree.parse(USERS_XML, PARSER)
    if not re.fullmatch(r".+", name):
        return HttpResponseBadRequest("invalid")
    # . 은 (개행을 뺀) 모든 글자에 맞는다 — fullmatch 여도 아무 값이나 통과한다
    # ruleid: mois-1-09-xpath-injection-py
    tree.xpath("//user[@name='" + name + "']")
    return HttpResponse("ok")


def negated_class_pattern(request):
    name = request.GET.get("name", "")
    tree = etree.parse(USERS_XML, PARSER)
    if re.fullmatch(r"[^<>]+", name):
        # [^<>] 는 < > 만 빼고 따옴표·괄호·개행까지 모두 통과시킨다
        # ruleid: mois-1-09-xpath-injection-py
        tree.xpath("//user[@name='" + name + "']")
    return HttpResponse("ok")


def wide_range_pattern(request):
    name = request.GET.get("name", "")
    tree = etree.parse(USERS_XML, PARSER)
    if not re.fullmatch(r"[!-~]+", name):
        return HttpResponseBadRequest("invalid")
    # [!-~] 는 따옴표·괄호·역슬래시를 포함한 모든 ASCII 기호에 맞는다 (범위는 a-z·A-Z·0-9 안에서만 인정한다)
    # ruleid: mois-1-09-xpath-injection-py
    tree.xpath("//user[@name='" + name + "']")
    return HttpResponse("ok")


def class_with_whitespace_escape(request):
    name = request.GET.get("name", "")
    tree = etree.parse(USERS_XML, PARSER)
    if not re.fullmatch(r"[\w\s]+", name):
        return HttpResponseBadRequest("invalid")
    # [\w\s] 의 \s 는 공백과 개행(CR·LF)에 맞는다 — 집합 안의 이스케이프도 \w·\d·\.·\- 만 인정한다
    # ruleid: mois-1-09-xpath-injection-py
    tree.xpath("//user[@name='" + name + "']")
    return HttpResponse("ok")


def range_from_symbol(request):
    name = request.GET.get("name", "")
    tree = etree.parse(USERS_XML, PARSER)
    if not PLUS_TO_Z_RE.fullmatch(name):
        return HttpResponseBadRequest("invalid")
    # [+-z] 는 + 부터 z 까지의 범위다: , / : ; < = > ? @ [ \ ] ^ ` 가 모두 통과한다
    # ruleid: mois-1-09-xpath-injection-py
    tree.xpath("//user[@name='" + name + "']")
    return HttpResponse("ok")


def range_to_symbol(request):
    name = request.GET.get("name", "")
    tree = etree.parse(USERS_XML, PARSER)
    if re.fullmatch(r"[A-_]+", name):
        # [A-_] 는 A 부터 _ 까지의 범위다: [ \ ] ^ 가 통과한다
        # ruleid: mois-1-09-xpath-injection-py
        tree.xpath("//user[@name='" + name + "']")
    return HttpResponse("ok")


def range_upper_to_lower(request):
    name = request.GET.get("name", "")
    tree = etree.parse(USERS_XML, PARSER)
    if UPPER_TO_LOWER_RE.fullmatch(name):
        # [A-z] 는 대문자와 소문자 사이의 [ \ ] ^ _ ` 까지 통과시킨다 (흔한 실수)
        # ruleid: mois-1-09-xpath-injection-py
        tree.xpath("//user[@name='" + name + "']")
    return HttpResponse("ok")


def range_digit_to_upper(request):
    name = request.GET.get("name", "")
    tree = etree.parse(USERS_XML, PARSER)
    if not re.fullmatch(r"[0-Z]+", name):
        return HttpResponseBadRequest("invalid")
    # [0-Z] 는 숫자와 대문자 사이의 : ; < = > ? @ 까지 통과시킨다
    # ruleid: mois-1-09-xpath-injection-py
    tree.xpath("//user[@name='" + name + "']")
    return HttpResponse("ok")


def request_supplied_pattern(request):
    name = request.GET.get("name", "")
    tree = etree.parse(USERS_XML, PARSER)
    if not re.fullmatch(request.GET.get("pattern", ""), name):
        return HttpResponseBadRequest("invalid")
    # 정규식을 요청에서 받으면 무엇이든 통과시킬 수 있다
    # ruleid: mois-1-09-xpath-injection-py
    tree.xpath("//user[@name='" + name + "']")
    return HttpResponse("ok")


def compiled_wildcard(request):
    name = request.GET.get("name", "")
    tree = etree.parse(USERS_XML, PARSER)
    if not ANY_RE.fullmatch(name):
        return HttpResponseBadRequest("invalid")
    # ANY_RE 는 .* 이다 — 이름이 정규식일 뿐 아무것도 거르지 않는다
    # ruleid: mois-1-09-xpath-injection-py
    tree.xpath("//user[@name='" + name + "']")
    return HttpResponse("ok")


def compiled_wildcard_inside_if(request):
    name = request.GET.get("name", "")
    tree = etree.parse(USERS_XML, PARSER)
    if ANY_RE.fullmatch(name):
        # 조건 안에서 써도 마찬가지다
        # ruleid: mois-1-09-xpath-injection-py
        tree.xpath("//user[@name='" + name + "']")
    return HttpResponse("ok")


def imported_pattern(request):
    name = request.GET.get("name", "")
    tree = etree.parse(USERS_XML, PARSER)
    if not TOKEN_PATTERN.fullmatch(name):
        return HttpResponseBadRequest("invalid")
    # 다른 모듈에서 가져온 정규식은 무엇을 허용하는지 볼 수 없다
    # ruleid: mois-1-09-xpath-injection-py
    tree.xpath("//user[@name='" + name + "']")
    return HttpResponse("ok")


def compiled_shadowed(request):
    name = request.GET.get("name", "")
    tree = etree.parse(USERS_XML, PARSER)
    GOOD_RE = re.compile(request.GET.get("pattern", ".*"))
    if not GOOD_RE.fullmatch(name):
        return HttpResponseBadRequest("invalid")
    # 함수 안에서 같은 이름의 지역 변수에 다른 정규식을 대입했다 — 모듈 수준의 정의는 쓰이지 않는다
    # ruleid: mois-1-09-xpath-injection-py
    tree.xpath("//user[@name='" + name + "']")
    return HttpResponse("ok")


def compiled_replaced_globally(request):
    global SWAPPED_RE
    name = request.GET.get("name", "")
    tree = etree.parse(USERS_XML, PARSER)
    SWAPPED_RE = re.compile(request.GET.get("pattern", ".*"))
    if not SWAPPED_RE.fullmatch(name):
        return HttpResponseBadRequest("invalid")
    # global 로 모듈 수준의 정규식을 요청 값으로 바꿔 넣었다
    # ruleid: mois-1-09-xpath-injection-py
    tree.xpath("//user[@name='" + name + "']")
    return HttpResponse("ok")


def compiled_replaced_globally_inside_if(request):
    global SWAPPED_RE
    name = request.GET.get("name", "")
    tree = etree.parse(USERS_XML, PARSER)
    SWAPPED_RE = re.compile(request.GET.get("pattern", ".*"))
    if SWAPPED_RE.fullmatch(name):
        # 조건 안에서 써도 마찬가지다
        # ruleid: mois-1-09-xpath-injection-py
        tree.xpath("//user[@name='" + name + "']")
    return HttpResponse("ok")


def compiled_redefined(request):
    name = request.GET.get("name", "")
    tree = etree.parse(USERS_XML, PARSER)
    if not REDEFINED_RE.fullmatch(name):
        return HttpResponseBadRequest("invalid")
    # REDEFINED_RE 는 모듈 수준에서 .* 로 다시 정의되었다
    # ruleid: mois-1-09-xpath-injection-py
    tree.xpath("//user[@name='" + name + "']")
    return HttpResponse("ok")


def compiled_redefined_inside_if(request):
    name = request.GET.get("name", "")
    tree = etree.parse(USERS_XML, PARSER)
    if REDEFINED_RE.fullmatch(name):
        # 조건 안에서 써도 마찬가지다
        # ruleid: mois-1-09-xpath-injection-py
        tree.xpath("//user[@name='" + name + "']")
    return HttpResponse("ok")
