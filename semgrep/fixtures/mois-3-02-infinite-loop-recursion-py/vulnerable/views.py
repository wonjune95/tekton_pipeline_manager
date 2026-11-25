import time

from django.http import JsonResponse

from .models import Job


def wait_job(request, job_id):
    # 탈출 조건이 없는 반복문: 요청 스레드가 끝나지 않음
    # ruleid: mois-3-02-infinite-loop-recursion-py
    while True:
        job = Job.objects.get(pk=job_id)
        job.refresh_from_db()
        time.sleep(1)


def factorial(n):
    # 기저 조건 없는 재귀
    # ruleid: mois-3-02-infinite-loop-recursion-py
    return n * factorial(n - 1)


class MenuTree:
    def depth(self, node):
        # ruleid: mois-3-02-infinite-loop-recursion-py
        return 1 + self.depth(node.parent)  # 기저 조건 없는 재귀


def factorial_view(request):
    return JsonResponse({"value": factorial(int(request.GET.get("n", "1")))})
