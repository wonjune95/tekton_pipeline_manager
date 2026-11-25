from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .models import Profile


# ruleid: mois-1-11-csrf-py
@csrf_exempt  # CSRF 토큰 검사를 끔
@login_required
@require_POST
def change_email(request):
    Profile.objects.filter(user=request.user).update(email=request.POST["email"])
    return JsonResponse({"ok": True})
