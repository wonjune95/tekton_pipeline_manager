"""주문 건수를 출력하는 명령행 스크립트 (웹 모듈 아님)."""
import argparse
import csv
import sys


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("path")
    args = parser.parse_args()
    with open(args.path, newline="", encoding="utf-8") as f:
        rows = list(csv.reader(f))
    if not rows:
        print("empty file", file=sys.stderr)
        return 1
    # 명령행 도구의 결과 출력
    print(len(rows))
    return 0


if __name__ == "__main__":
    sys.exit(main())
