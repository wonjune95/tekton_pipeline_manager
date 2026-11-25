from django.http import JsonResponse
from django.views import View


def greeting(request):
    # 요청별 데이터는 지역 변수에 둔다
    current_user = request.GET.get("name", "")
    return JsonResponse({"name": current_user})


class CartView(View):
    http_method_names = ["get", "post"]

    def post(self, request):
        # 요청 간에 유지할 값은 세션에 저장
        items = request.session.get("cart_items", [])
        items.append(request.POST.get("item", ""))
        request.session["cart_items"] = items
        self.buyer = request.user.username
        return JsonResponse({"items": items})
