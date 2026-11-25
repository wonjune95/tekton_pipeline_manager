import collections

from django.http import HttpRequest, JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

visit_count = 0
quota_left = 1000
last_member = None


def counter(request: HttpRequest):
    global visit_count, quota_left
    # ruleid: mois-6-01-shared-field-in-singleton-py
    visit_count += 1
    # ruleid: mois-6-01-shared-field-in-singleton-py
    quota_left -= 1
    return JsonResponse({"visits": visit_count})


class ProfileView(APIView):
    history = list()
    by_user = collections.defaultdict(list)
    seen = set()
    cache = dict()
    current = None

    def get(self, request):
        global last_member
        # 뷰 클래스 메서드에서 전역 변수에 저장
        # ruleid: mois-6-01-shared-field-in-singleton-py
        last_member = request.user.username
        # 클래스 이름으로 변경
        # ruleid: mois-6-01-shared-field-in-singleton-py
        ProfileView.history.extend([request.user.username])
        # ruleid: mois-6-01-shared-field-in-singleton-py
        ProfileView.cache[request.user.pk] = request.query_params.get("tab")
        # ruleid: mois-6-01-shared-field-in-singleton-py
        self.by_user.setdefault(request.user.pk, []).append(request.path)
        # ruleid: mois-6-01-shared-field-in-singleton-py
        self.seen.add(request.user.pk)
        return Response({"history": self.history})

    def post(self, request):
        # ruleid: mois-6-01-shared-field-in-singleton-py
        self.__class__.current = request.user
        return Response(status=204)


class MemberViewSet(ModelViewSet):
    selected = None

    def retrieve(self, request, pk=None):
        # ruleid: mois-6-01-shared-field-in-singleton-py
        type(self).selected = pk
        return Response({"id": pk})
