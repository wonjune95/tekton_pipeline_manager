from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from .models import Profile


# ok: mois-1-11-csrf-py csrf_exempt 없이 기본 CSRF 검사를 받는다
@login_required
@require_POST
def change_email(request):
    Profile.objects.filter(user=request.user).update(email=request.POST["email"])
    return JsonResponse({"ok": True})
