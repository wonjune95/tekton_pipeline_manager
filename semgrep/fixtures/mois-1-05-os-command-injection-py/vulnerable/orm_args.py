"""ORM 조회 결과만 깨끗하다 — 조회에 넣은 입력 자체를 명령에 쓰면 탐지되어야 한다."""
import os

from django.http import HttpResponse

from .models import Host


def ping_lookup_key(request, host_id):
    host = Host.objects.get(pk=host_id)
    # ruleid: mois-1-05-os-command-injection-py
    os.system("ping -c 1 " + host_id + " " + host.address)
    return HttpResponse("ok")


def ping_raw_query(request, group):
    # raw() 는 SQL 원문을 받는다 — 결과를 받는 대입문은 ORM 조회 결과로 인정하지 않는다
    hosts = Host.objects.raw("SELECT * FROM host WHERE grp = '" + group + "'")
    # ruleid: mois-1-05-os-command-injection-py
    os.system("ping -c 1 " + hosts[0].address)
    return HttpResponse("ok")


def ping_extra_query(request, group):
    hosts = Host.objects.extra(where=["grp = '" + group + "'"])
    # ruleid: mois-1-05-os-command-injection-py
    os.system("ping -c 1 " + hosts[0].address)
    return HttpResponse("ok")


def ping_rawsql_annotation(request, group):
    from django.db.models.expressions import RawSQL
    hosts = Host.objects.annotate(rank=RawSQL("SELECT rank FROM r WHERE grp = '" + group + "'", []))
    # ruleid: mois-1-05-os-command-injection-py
    os.system("ping -c 1 " + hosts[0].address)
    return HttpResponse("ok")
