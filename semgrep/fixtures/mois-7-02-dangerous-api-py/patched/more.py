import socket
import sys
import tempfile

from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.views import APIView


class MaintenanceView(APIView):
    def post(self, request):
        # ok: mois-7-02-dangerous-api-py if 로 검사하고 거부한다
        if not request.user.is_superuser:
            raise PermissionDenied()
        return Response(status=202)


def health_probe(host, port):
    # ok: mois-7-02-dangerous-api-py 요청 처리 함수가 아닌 운영 도구의 소켓 사용
    with socket.create_connection((host, port), timeout=2):
        return True


def scratch_file():
    # ok: mois-7-02-dangerous-api-py 파일을 만들면서 이름을 정한다
    fd, path = tempfile.mkstemp(suffix=".csv")
    return fd, path


def check_shape(rows):
    # ok: mois-7-02-dangerous-api-py 인증·권한과 무관한 내부 불변식
    assert len(rows) > 0, "rows must not be empty"
    return rows


def run(argv):
    if not argv:
        # ok: mois-7-02-dangerous-api-py 명령행 진입점
        sys.exit(2)
    return 0
