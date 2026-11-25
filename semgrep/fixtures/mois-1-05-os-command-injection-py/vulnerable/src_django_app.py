# 공통 source 블록 시험 (감사 사례). `# CASE` 표시만 있고 ruleid 가 없는 줄은 알려진 미탐 — 공통 source 가 보지 않는 형태다.
import os

from django.http import HttpResponse
from django.views import View
from rest_framework.decorators import action, api_view
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet


def ctl_get(request):
    x = request.GET["x"]
    # ruleid: mois-1-05-os-command-injection-py — ctl-django-GET
    os.system(x)
    return HttpResponse()


def ctl_meta(request):
    x = request.META["HTTP_X_CMD"]
    # ruleid: mois-1-05-os-command-injection-py — ctl-django-META
    os.system(x)
    return HttpResponse()


def ctl_files(request):
    x = request.FILES["f"].name
    # ruleid: mois-1-05-os-command-injection-py — ctl-django-FILES-name
    os.system(x)
    return HttpResponse()


def ctl_headers(request):
    x = request.headers.get("X-Cmd")
    # ruleid: mois-1-05-os-command-injection-py — ctl-django-headers
    os.system(x)
    return HttpResponse()


def miss_name_r(r):
    x = r.GET["x"]
    os.system(x)  # CASE django-request-named-r
    return HttpResponse()


def miss_name_http_request(http_request):
    x = http_request.POST["x"]
    os.system(x)  # CASE django-request-named-http_request
    return HttpResponse()


def miss_url_kwarg(request, filename):
    # ruleid: mois-1-05-os-command-injection-py — django-urlconf-kwarg-function-view
    os.system("cat /srv/files/" + filename)
    return HttpResponse()


def miss_get_host(request):
    x = request.get_host()
    os.system(x)  # CASE django-get_host
    return HttpResponse()


def miss_build_absolute_uri(request):
    x = request.build_absolute_uri()
    os.system(x)  # CASE django-build_absolute_uri
    return HttpResponse()


def miss_path_info(request):
    x = request.path_info
    os.system(x)  # CASE django-path_info
    return HttpResponse()


def miss_resolver_match(request):
    x = request.resolver_match.kwargs["name"]
    # ruleid: mois-1-05-os-command-injection-py — django-resolver_match-kwargs
    os.system(x)
    return HttpResponse()


def miss_content_type(request):
    x = request.content_type
    # ruleid: mois-1-05-os-command-injection-py — django-content_type
    os.system(x)
    return HttpResponse()


def miss_readline(request):
    x = request.readline()
    # ruleid: mois-1-05-os-command-injection-py — django-readline
    os.system(x)
    return HttpResponse()


class CbvView(View):
    def get(self, request, name):
        # ruleid: mois-1-05-os-command-injection-py — django-cbv-method-kwarg
        os.system(name)
        return HttpResponse()

    def post(self, request, *args, **kwargs):
        # ruleid: mois-1-05-os-command-injection-py — django-cbv-self.kwargs
        os.system(self.kwargs["name"])
        return HttpResponse()

    def put(self, request, *args, **kwargs):
        os.system(kwargs["name"])  # CASE django-cbv-kwargs
        return HttpResponse()

    def delete(self, request):
        x = self.request.GET.get("x")
        # ruleid: mois-1-05-os-command-injection-py — ctl-django-self.request-GET
        os.system(x)
        return HttpResponse()


class DrfView(APIView):
    def post(self, request):
        x = self.request.data["x"]
        # ruleid: mois-1-05-os-command-injection-py — ctl-drf-self.request-data
        os.system(x)
        return HttpResponse()

    def get(self, request):
        x = request.query_params.get("x")
        # ruleid: mois-1-05-os-command-injection-py — ctl-drf-query_params
        os.system(x)
        return HttpResponse()


class DrfViewSet(ViewSet):
    @action(detail=True, methods=["post"])
    def run(self, request, pk=None):
        # ruleid: mois-1-05-os-command-injection-py — drf-action-pk
        os.system("run-job " + pk)
        return HttpResponse()


@api_view(["POST"])
def miss_api_view(request, name):
    # ruleid: mois-1-05-os-command-injection-py — drf-api_view-url-kwarg
    os.system(name)
    return HttpResponse()


class Query:
    def resolve_ping(root, info, host):
        os.system("ping " + host)  # CASE graphene-resolver-arg
        return ""

    def resolve_whoami(root, info):
        x = info.context.GET["x"]
        os.system(x)  # CASE graphene-info.context
        return ""
