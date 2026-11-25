"""명령행 도구: 요청 처리 코드가 아니므로 sys.exit 사용이 정상이다."""
import sys


def main(argv):
    if len(argv) < 2:
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
