"""URL 인자로 DB 를 조회한 결과는 요청 값이 아니라 저장된 값이다 (Django ORM)."""
import os

from django.http import HttpResponse
from django.shortcuts import get_list_or_404, get_object_or_404

from .models import Host


def ping_saved_host(request, host_id):
    host = Host.objects.get(pk=host_id)
    # ok: mois-1-05-os-command-injection-py 저장된 호스트 주소
    os.system("ping -c 1 " + host.address)
    return HttpResponse("ok")


def ping_first_match(request, group):
    host = Host.objects.filter(group=group).latest("updated_at")
    # ok: mois-1-05-os-command-injection-py
    os.system("ping -c 1 " + host.address)
    return HttpResponse("ok")


def ping_inline(request, host_id):
    # ok: mois-1-05-os-command-injection-py
    os.system("ping -c 1 " + Host.objects.get(pk=host_id).address)
    return HttpResponse("ok")


def ping_or_404(request, host_id):
    host = get_object_or_404(Host, pk=host_id)
    # ok: mois-1-05-os-command-injection-py
    os.system("ping -c 1 " + host.address)
    return HttpResponse("ok")


def ping_or_404_inline(request, host_id):
    # ok: mois-1-05-os-command-injection-py
    os.system("ping -c 1 " + get_object_or_404(Host, pk=host_id).address)
    return HttpResponse("ok")


def ping_group(request, group):
    hosts = get_list_or_404(Host, group=group)
    # ok: mois-1-05-os-command-injection-py
    os.system("ping -c 1 " + hosts[0].address)
    return HttpResponse("ok")


def ping_group_inline(request, group):
    # ok: mois-1-05-os-command-injection-py
    os.system("ping -c 1 " + get_list_or_404(Host, group=group)[0].address)
    return HttpResponse("ok")


def ping_filtered_inline(request, group):
    # ok: mois-1-05-os-command-injection-py
    os.system("ping -c 1 " + Host.objects.filter(group=group).latest("updated_at").address)
    return HttpResponse("ok")
