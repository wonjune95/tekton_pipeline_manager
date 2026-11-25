from django.urls import path
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from . import views


# 클래스 기반 뷰 전체를 CSRF 검사에서 제외
# ruleid: mois-1-11-csrf-py
@method_decorator(csrf_exempt, name="dispatch")
class ProfileView(View):
    def post(self, request):
        return views.change_email(request)


urlpatterns = [
    # URL 설정에서 뷰를 감싸 제외
    # ruleid: mois-1-11-csrf-py
    path("profile/email/", csrf_exempt(views.change_email)),
    path("profile/", ProfileView.as_view()),
]
