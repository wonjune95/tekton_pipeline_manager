import os
import subprocess

from django.http import HttpResponse


def ping(request):
    host = request.GET.get("host", "")
    # 외부 입력을 그대로 셸 명령어에 이어 붙임
    # ruleid: mois-1-05-os-command-injection-py
    os.system("ping -c 1 " + host)
    return HttpResponse("ok")


def run_tool(request):
    tool = request.POST["tool"]
    # ruleid: mois-1-05-os-command-injection-py
    out = subprocess.check_output(f"/opt/tools/{tool} --version", shell=True)
    return HttpResponse(out)
