from django.http import JsonResponse
from django.views import View

current_user = None


def greeting(request):
    global current_user
    # 전역 변수에 요청별 사용자 저장: 다른 요청이 덮어써 남의 정보가 보일 수 있음
    # ruleid: mois-6-01-shared-field-in-singleton-py
    current_user = request.GET.get("name", "")
    return JsonResponse({"name": current_user})


class CartView(View):
    items = []
    last_buyer = None

    def post(self, request):
        # ruleid: mois-6-01-shared-field-in-singleton-py
        self.items.append(request.POST.get("item", ""))  # 클래스 속성은 모든 요청이 공유
        # ruleid: mois-6-01-shared-field-in-singleton-py
        CartView.last_buyer = request.user.username  # 클래스 속성에 요청별 데이터 저장
        return JsonResponse({"items": self.items})
