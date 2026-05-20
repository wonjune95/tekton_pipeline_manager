#!/bin/bash
# ════════════════════════════════════════════════════════════════
#  Ubuntu 오프라인 설치 스크립트 (폐쇄망용)
# ════════════════════════════════════════════════════════════════
#  실행 전 준비 : ubuntu/ 폴더 전체가 이 머신에 복사되어 있어야 함
#  실행 방법   : sudo ./install.sh
# ════════════════════════════════════════════════════════════════

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PY_PKG_DIR="$SCRIPT_DIR/packages"
DEB_DIR="$SCRIPT_DIR/debs"
REQ_FILE="$SCRIPT_DIR/../requirements.txt"

echo "════════════════════════════════════════════════"
echo "  Ubuntu 오프라인 설치"
echo "════════════════════════════════════════════════"
echo "  OS    : $(lsb_release -d 2>/dev/null | cut -f2 || cat /etc/os-release | grep PRETTY_NAME | cut -d'"' -f2)"
echo ""

# ── [1/2] 시스템 패키지 설치 (git, python3-pip) ──────
echo "[1/2] 시스템 패키지 설치 ..."

if [ -d "$DEB_DIR" ] && [ "$(ls -A "$DEB_DIR" 2>/dev/null)" ]; then
    # 의존성 순서 무시하고 일괄 설치 후 깨진 의존성 자동 복구
    dpkg -i "$DEB_DIR"/*.deb 2>/dev/null || true
    apt-get install -f -y 2>/dev/null || true
    echo "      git    : $(git --version 2>/dev/null || echo '확인 필요')"
    echo "      python3: $(python3 --version 2>/dev/null || echo '확인 필요')"
    echo "      pip    : $(python3 -m pip --version 2>/dev/null | cut -d' ' -f1-2 || echo '확인 필요')"
else
    echo "      [WARN] debs/ 폴더 없음 또는 비어 있음 — 시스템 패키지 건너뜀"
    echo "             git, python3-pip 가 이미 설치되어 있는지 확인하세요."
fi

# ── Python 인터프리터 확인 ────────────────────────────
PYTHON=$(command -v python3 || true)
if [ -z "$PYTHON" ]; then
    echo "[ERROR] python3가 없습니다. 시스템 패키지 설치를 먼저 확인하세요."
    exit 1
fi

if ! $PYTHON -m pip --version &>/dev/null; then
    echo "[ERROR] pip가 없습니다."
    exit 1
fi

# ── [2/2] Python 패키지 설치 (오프라인) ──────────────
echo ""
echo "[2/2] Python 패키지 오프라인 설치 ..."

if [ ! -d "$PY_PKG_DIR" ] || [ -z "$(ls -A "$PY_PKG_DIR" 2>/dev/null)" ]; then
    echo "[ERROR] packages/ 폴더가 없거나 비어 있습니다."
    echo "        인터넷 연결 환경에서 download.sh 를 먼저 실행하세요."
    exit 1
fi

echo "      Python: $($PYTHON --version)"
echo "      경로  : $PY_PKG_DIR"

$PYTHON -m pip install \
    --no-index \
    --find-links "$PY_PKG_DIR" \
    -r "$REQ_FILE"

# ── 결과 확인 ────────────────────────────────────────
echo ""
echo "════════════════════════════════════════════════"
echo "  설치 완료 — 설치된 패키지"
echo "════════════════════════════════════════════════"
$PYTHON -m pip list 2>/dev/null | grep -iE \
    "tomli|jinja2|inquirer|paramiko|pexpect|requests|cryptography|blessed|bcrypt|pynacl|cffi" \
    | awk '{printf "  %-30s %s\n", $1, $2}'

echo ""
echo "  git: $(git --version 2>/dev/null || echo '미설치')"
echo "════════════════════════════════════════════════"
