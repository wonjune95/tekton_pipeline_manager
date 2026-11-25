import re
import subprocess

from django.http import HttpResponse, HttpResponseBadRequest

ALLOWED_TOOLS = {"convert": "/opt/tools/convert", "resize": "/opt/tools/resize"}
HOST_RE = re.compile(r"^[A-Za-z0-9.-]{1,253}$")


def ping(request):
    host = request.GET.get("host", "")
    if not HOST_RE.fullmatch(host):
        return HttpResponseBadRequest("invalid host")
    # ok: mois-1-05-os-command-injection-py 셸을 거치지 않고 인자 목록으로 실행 (실행 파일은 고정)
    subprocess.run(["ping", "-c", "1", host], check=False, timeout=5)
    return HttpResponse("ok")


def run_tool(request):
    path = ALLOWED_TOOLS.get(request.POST.get("tool", ""))
    if path is None:
        return HttpResponseBadRequest("unknown tool")
    # ok: mois-1-05-os-command-injection-py 같은 파일의 dict 에서 꺼낸 경로
    out = subprocess.check_output([path, "--version"])
    return HttpResponse(out)


def tool_version(request):
    try:
        # ok: mois-1-05-os-command-injection-py 같은 파일의 dict 를 키로 조회 (없는 키는 KeyError)
        path = ALLOWED_TOOLS[request.POST["tool"]]
    except KeyError:
        return HttpResponseBadRequest("unknown tool")
    out = subprocess.check_output(path + " --version", shell=True)
    return HttpResponse(out)


def tool_help(request):
    path = ALLOWED_TOOLS.get(request.POST.get("tool", ""), None)
    if path is None:
        return HttpResponseBadRequest("unknown tool")
    # ok: mois-1-05-os-command-injection-py dict.get(키, None)
    out = subprocess.check_output(path + " --help", shell=True)
    return HttpResponse(out)


def tool_or_default(request):
    path = ALLOWED_TOOLS.get(request.POST.get("tool", ""), "/opt/tools/convert")
    # ok: mois-1-05-os-command-injection-py dict.get(키, 고정 문자열) — 없는 키면 고정 경로
    out = subprocess.check_output(path + " --list", shell=True)
    return HttpResponse(out)


# ---- 조건에 바로 적은 허용 목록 ----
def convert_inline_allowlist(request):
    fmt = request.GET.get("format", "")
    if fmt not in ("png", "jpg"):
        return HttpResponseBadRequest("unsupported format")
    # ok: mois-1-05-os-command-injection-py — 문자열만 든 목록을 조건에 바로 적었다
    subprocess.run("convert in.dat out." + fmt, shell=True, check=False)
    return HttpResponse("ok")


def convert_inline_positive(request):
    fmt = request.GET.get("format", "")
    if fmt in {"png", "jpg"}:
        # ok: mois-1-05-os-command-injection-py
        subprocess.run("convert in.dat out." + fmt, shell=True, check=False)
    return HttpResponse("ok")


def convert_inline_default(request):
    fmt = request.GET.get("format", "")
    if fmt not in ["png", "jpg"]:
        fmt = "png"
    # ok: mois-1-05-os-command-injection-py — 목록에 없으면 기본값으로 바꿨다
    subprocess.run("convert in.dat out." + fmt, shell=True, check=False)
    return HttpResponse("ok")
