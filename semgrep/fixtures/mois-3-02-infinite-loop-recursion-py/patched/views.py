import time

from django.http import JsonResponse

from .models import Job

MAX_WAIT_SECONDS = 30


def wait_job(request, job_id):
    waited = 0
    while True:
        job = Job.objects.get(pk=job_id)
        if job.done or waited >= MAX_WAIT_SECONDS:
            break
        time.sleep(1)
        waited += 1
    return JsonResponse({"done": job.done})


def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)


class MenuTree:
    def depth(self, node):
        return 0 if node is None else 1 + self.depth(node.parent)

    def save(self, node):
        # 같은 이름의 모듈 함수 호출은 재귀가 아님
        return save(node)


def save(node):
    node.save()
    return node


def factorial_view(request):
    n = min(int(request.GET.get("n", "1")), 100)
    return JsonResponse({"value": factorial(n)})
