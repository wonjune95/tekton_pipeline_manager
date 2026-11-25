from django.core.cache import cache
from rest_framework.response import Response
from rest_framework.views import APIView

DEFAULT_TABS = ["profile", "orders"]


def read_setting(name):
    global DEFAULT_TABS
    # ok: mois-6-01-shared-field-in-singleton-py 요청 처리 함수가 아닌 초기화 코드
    DEFAULT_TABS = ["profile", "orders", name]


class ProfileView(APIView):
    # ok: mois-6-01-shared-field-in-singleton-py 읽기만 하는 클래스 속성
    tabs = ["profile", "orders"]

    def get(self, request):
        # ok: mois-6-01-shared-field-in-singleton-py 요청별 값은 인스턴스·지역 변수와 캐시에 둔다
        self.tab = request.query_params.get("tab", self.tabs[0])
        history = cache.get(f"history:{request.user.pk}", [])
        history.append(self.tab)
        cache.set(f"history:{request.user.pk}", history, 600)
        return Response({"tab": self.tab, "tabs": list(self.tabs)})


class Registry:
    items = {}

    def register(self, name, value):
        # ok: mois-6-01-shared-field-in-singleton-py 뷰 클래스가 아닌 일반 등록소
        self.items[name] = value
