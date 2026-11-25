from django.http import JsonResponse


class ConnectionPool:
    def __init__(self):
        self._conns = {}

    def release(self, name):
        # read·close 는 HTTP 응답만의 이름이 아니다: dict 에서 꺼낸 값이 없으면 None 이다
        # ruleid: mois-5-01-null-dereference-py
        self._conns.get(name).close()


def upload(request):
    # 파일을 첨부하지 않은 요청이면 None 이다
    # ruleid: mois-5-01-null-dereference-py
    data = request.FILES.get("attachment").read()
    return JsonResponse({"size": len(data)})
