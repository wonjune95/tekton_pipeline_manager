import sys

import uvicorn
from django.core.management import execute_from_command_line
from fastapi import FastAPI

app = FastAPI()


def export(path, rows):
    with open(path, "w", encoding="utf-8") as f:
        for row in rows:
            # ok: mois-6-02-debug-code-py 파일로 쓰는 print 는 디버그 출력이 아니다
            print(",".join(row), file=f)


def main(argv):
    uvicorn.run(app)
    return 0


# ok: mois-6-02-debug-code-py main() 을 부르는 시작 블록
if __name__ == "__main__":
    sys.exit(main(sys.argv))
