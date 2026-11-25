"""검증처럼 보이지만 검증이 아닌 경우 — 모두 탐지되어야 한다."""
import os
import shlex
import subprocess

from django.http import HttpResponse, HttpResponseBadRequest

from .policy import REMOTE_TOOLS

ALLOWED_TOOLS = {"convert": "/opt/tools/convert", "resize": "/opt/tools/resize"}
ALLOWED_HOSTS = ("intra.example.go.kr", "mail.example.go.kr")


def quote_result_discarded(request):
    host = request.GET.get("host", "")
    # 이스케이프한 결과를 쓰지 않음
    shlex.quote(host)
    # ruleid: mois-1-05-os-command-injection-py
    os.system("ping -c 1 " + host)
    return HttpResponse("ok")


def check_result_ignored(request):
    host = request.GET.get("host", "")
    # 허용 목록 검사 결과를 쓰지 않음
    host in ALLOWED_HOSTS
    # ruleid: mois-1-05-os-command-injection-py
    os.system("ping -c 1 " + host)
    return HttpResponse("ok")


def failure_does_not_exit(request):
    host = request.GET.get("host", "")
    if host not in ALLOWED_HOSTS:
        # 기록만 하고 계속 진행
        print("unexpected host", host)
    # ruleid: mois-1-05-os-command-injection-py
    os.system("ping -c 1 " + host)
    return HttpResponse("ok")


def opposite_branch(request):
    host = request.GET.get("host", "")
    if host in ALLOWED_HOSTS:
        return HttpResponse("skipped")
    else:
        # 허용 목록에 없는 값이 쓰이는 분기
        # ruleid: mois-1-05-os-command-injection-py
        os.system("ping -c 1 " + host)
    return HttpResponse("ok")


def negated_condition(request):
    host = request.GET.get("host", "")
    if host not in ALLOWED_HOSTS:
        # ruleid: mois-1-05-os-command-injection-py
        os.system("ping -c 1 " + host)
    return HttpResponse("ok")


def imported_allowlist(request):
    tool = request.POST.get("tool", "")
    # 다른 모듈의 목록은 내용을 볼 수 없어 인정하지 않는다
    if tool not in REMOTE_TOOLS:
        return HttpResponseBadRequest("unknown tool")
    # ruleid: mois-1-05-os-command-injection-py
    out = subprocess.check_output(f"/opt/tools/{tool} --version", shell=True)
    return HttpResponse(out)


def lookup_with_input_default(request):
    tool = request.POST.get("tool", "")
    # 목록에 없으면 입력값을 그대로 돌려준다
    path = ALLOWED_TOOLS.get(tool, tool)
    # ruleid: mois-1-05-os-command-injection-py
    out = subprocess.check_output([path, "--version"])
    return HttpResponse(out)


def other_variable_checked(request):
    host = request.GET.get("host", "")
    target = request.GET.get("target", "")
    if host not in ALLOWED_HOSTS:
        return HttpResponseBadRequest("unknown host")
    # 검사한 변수(host)와 쓰는 변수(target)가 다르다
    # ruleid: mois-1-05-os-command-injection-py
    os.system("ping -c 1 " + target)
    return HttpResponse("ok")


# ---- 공통 허용 목록 guard (공통 2)·(공통 3): 속이는 형태는 탐지되어야 한다 ----


def reassigned_after_check(request):
    host = request.GET.get("host", "")
    if host not in ALLOWED_HOSTS:
        return HttpResponseBadRequest("unknown host")
    # 검사한 뒤에 다른 입력으로 바꿔 넣는다
    host = request.GET.get("alias", "")
    # ruleid: mois-1-05-os-command-injection-py
    os.system("ping -c 1 " + host)
    return HttpResponse("ok")


def sink_inside_failing_branch(request):
    host = request.GET.get("host", "")
    if host not in ALLOWED_HOSTS:
        # 허용 목록에 없는 값으로 실행하고 빠져나간다
        # ruleid: mois-1-05-os-command-injection-py
        os.system("ping -c 1 " + host)
        return HttpResponseBadRequest("unknown host")
    return HttpResponse("ok")


def nested_conditional_exit(request):
    host = request.GET.get("host", "")
    if host not in ALLOWED_HOSTS:
        if request.GET.get("strict"):
            return HttpResponseBadRequest("unknown host")
    # 엄격 모드가 아니면 목록에 없는 값이 그대로 내려온다
    # ruleid: mois-1-05-os-command-injection-py
    os.system("ping -c 1 " + host)
    return HttpResponse("ok")


def check_joined_with_and(request):
    host = request.GET.get("host", "")
    if request.GET.get("strict") and host not in ALLOWED_HOSTS:
        return HttpResponseBadRequest("unknown host")
    # 엄격 모드일 때만 검사한다
    # ruleid: mois-1-05-os-command-injection-py
    os.system("ping -c 1 " + host)
    return HttpResponse("ok")


def check_joined_with_or(request):
    host = request.GET.get("host", "")
    if request.user.is_staff or host in ALLOWED_HOSTS:
        # or 로 묶이면 목록에 없는 값도 들어온다
        # ruleid: mois-1-05-os-command-injection-py
        os.system("ping -c 1 " + host)
    return HttpResponse("ok")


def negated_with_not_operator(request):
    host = request.GET.get("host", "")
    if not host in ALLOWED_HOSTS:
        # `not x in 목록` 이 참인 분기 = 목록에 없는 값
        # ruleid: mois-1-05-os-command-injection-py
        os.system("ping -c 1 " + host)
    return HttpResponse("ok")


def imported_dict_lookup(request):
    # 다른 모듈의 dict 는 내용을 볼 수 없어 인정하지 않는다
    path = REMOTE_TOOLS.get(request.POST.get("tool", ""))
    # ruleid: mois-1-05-os-command-injection-py
    out = subprocess.check_output(path + " --version", shell=True)
    return HttpResponse(out)


# ---- (공통 2) "고정된 기본값으로 바꾸는" 형태를 흉내 낸 것 ----


def default_is_another_input(request):
    host = request.GET.get("host", "")
    if host not in ALLOWED_HOSTS:
        # 기본값이 고정 문자열이 아니라 또 다른 입력
        host = request.GET.get("fallback", "")
    # ruleid: mois-1-05-os-command-injection-py
    os.system("ping -c 1 " + host)
    return HttpResponse("ok")


def default_used_before_replaced(request):
    host = request.GET.get("host", "")
    if host not in ALLOWED_HOSTS:
        # 기본값으로 바꾸기 전에 목록에 없는 값으로 실행한다
        # ruleid: mois-1-05-os-command-injection-py
        os.system("logger rejected " + host)
        host = "intra.example.go.kr"
    return HttpResponse(host)


def default_then_reassigned(request):
    host = request.GET.get("host", "")
    if host not in ALLOWED_HOSTS:
        host = "intra.example.go.kr"
    # 기본값으로 바꾼 뒤에 다른 입력으로 다시 바꿔 넣는다
    host = request.GET.get("alias", "")
    # ruleid: mois-1-05-os-command-injection-py
    os.system("ping -c 1 " + host)
    return HttpResponse("ok")


def default_joined_with_and(request):
    host = request.GET.get("host", "")
    if request.GET.get("strict") and host not in ALLOWED_HOSTS:
        host = "intra.example.go.kr"
    # 엄격 모드일 때만 기본값으로 바꾼다
    # ruleid: mois-1-05-os-command-injection-py
    os.system("ping -c 1 " + host)
    return HttpResponse("ok")


def used_outside_positive_branch(request):
    host = request.GET.get("host", "")
    if host in ALLOWED_HOSTS:
        print("known host", host)
    # 검사한 if 문 밖에서 쓴다
    # ruleid: mois-1-05-os-command-injection-py
    os.system("ping -c 1 " + host)
    return HttpResponse("ok")


# ---- 공통 sanitizer 를 고친 뒤에 탐지되어야 하는 예제 (지금 규칙으로는 미탐) ----


def allowlist_from_request(request):
    # 허용 목록 자체가 요청에서 온다 (리터럴 목록이 아니다)
    allowed = request.GET.getlist("allowed")
    host = request.GET.get("host", "")
    if host not in allowed:
        return HttpResponseBadRequest("unknown host")
    # ruleid: mois-1-05-os-command-injection-py
    os.system("ping -c 1 " + host)
    return HttpResponse("ok")


def allowlist_loaded_at_runtime(request):
    # 실행 중에 불러오는 목록은 내용을 볼 수 없다
    allowed = load_allowed_hosts()
    host = request.GET.get("host", "")
    if host in allowed:
        # ruleid: mois-1-05-os-command-injection-py
        os.system("ping -c 1 " + host)
    return HttpResponse("ok")


def allowlist_is_a_string(request):
    # 문자열에 대한 in 은 부분 문자열 검사다 ("" 나 "example" 도 통과)
    allowed = "intra.example.go.kr mail.example.go.kr"
    host = request.GET.get("host", "")
    if host not in allowed:
        host = "intra.example.go.kr"
    # ruleid: mois-1-05-os-command-injection-py
    os.system("ping -c 1 " + host)
    return HttpResponse("ok")


def dict_literal_built_from_request(request):
    # 함수 안에서 요청 값으로 만든 dict — 꺼낸 값은 그대로 외부 입력이다
    opts = {"host": request.GET.get("host", ""), "count": "1"}
    # ruleid: mois-1-05-os-command-injection-py
    os.system("ping -c " + opts["count"] + " " + opts["host"])
    return HttpResponse("ok")


def appended_after_check(request):
    host = request.GET.get("host", "")
    if host not in ALLOWED_HOSTS:
        return HttpResponseBadRequest("unknown host")
    # 검사한 뒤에 다른 입력을 덧붙인다 (+=)
    host += request.GET.get("options", "")
    # ruleid: mois-1-05-os-command-injection-py
    os.system("ping -c 1 " + host)
    return HttpResponse("ok")


def default_then_appended(request):
    host = request.GET.get("host", "")
    if host not in ALLOWED_HOSTS:
        host = "intra.example.go.kr"
    # 기본값으로 바꾼 뒤에 다른 입력을 덧붙인다 (+=)
    host += request.GET.get("options", "")
    # ruleid: mois-1-05-os-command-injection-py
    os.system("ping -c 1 " + host)
    return HttpResponse("ok")


# ================= 조건에 바로 적은 목록 — 검증처럼 보이지만 아닌 경우 =================
def inline_used_in_failing_branch(request):
    fmt = request.GET.get("format", "")
    if fmt not in ("png", "jpg"):
        # ruleid: mois-1-05-os-command-injection-py
        os.system("logger unsupported format " + fmt)
        return HttpResponseBadRequest("unsupported format")
    return HttpResponse("ok")


def inline_reassigned_after_check(request):
    fmt = request.GET.get("format", "")
    if fmt not in ("png", "jpg"):
        return HttpResponseBadRequest("unsupported format")
    fmt = request.GET.get("override", fmt)
    # ruleid: mois-1-05-os-command-injection-py
    os.system("convert in.dat out." + fmt)
    return HttpResponse("ok")


def inline_appended_after_check(request):
    fmt = request.GET.get("format", "")
    if fmt not in ("png", "jpg"):
        return HttpResponseBadRequest("unsupported format")
    fmt += request.GET.get("suffix", "")
    # ruleid: mois-1-05-os-command-injection-py
    os.system("convert in.dat out." + fmt)
    return HttpResponse("ok")


def inline_check_only_when_strict(request):
    fmt = request.GET.get("format", "")
    if request.GET.get("strict") and fmt not in ("png", "jpg"):
        return HttpResponseBadRequest("unsupported format")
    # ruleid: mois-1-05-os-command-injection-py
    os.system("convert in.dat out." + fmt)
    return HttpResponse("ok")


def inline_negated_positive(request):
    fmt = request.GET.get("format", "")
    if not (fmt in ("png", "jpg")):
        # ruleid: mois-1-05-os-command-injection-py
        os.system("logger unsupported format " + fmt)
    return HttpResponse("ok")


def inline_or_bypass(request):
    fmt = request.GET.get("format", "")
    if fmt in ("png", "jpg") or request.user.is_staff:
        # ruleid: mois-1-05-os-command-injection-py
        os.system("convert in.dat out." + fmt)
    return HttpResponse("ok")


def inline_else_branch(request):
    fmt = request.GET.get("format", "")
    if fmt in ("png", "jpg"):
        pass
    else:
        # ruleid: mois-1-05-os-command-injection-py
        os.system("logger unsupported format " + fmt)
    return HttpResponse("ok")


def inline_list_has_variable(request):
    extra = request.GET.get("extra", "")
    fmt = request.GET.get("format", "")
    if fmt not in ("png", extra):
        return HttpResponseBadRequest("unsupported format")
    # ruleid: mois-1-05-os-command-injection-py
    os.system("convert in.dat out." + fmt)
    return HttpResponse("ok")
