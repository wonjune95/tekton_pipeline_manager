#!/bin/bash
# ════════════════════════════════════════════════════════════════
#  Ubuntu 오프라인 설치 스크립트 (폐쇄망용)
# ════════════════════════════════════════════════════════════════
#  실행 전 준비 : ubuntu/ 폴더 전체가 이 머신에 복사되어 있어야 함
#  실행 방법   : sudo ./install.sh
# ════════════════════════════════════════════════════════════════

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REQ_FILE="$SCRIPT_DIR/../requirements.txt"

# Ubuntu 버전 감지 (22 / 24 / 26)
UBUNTU_VER=$(grep '^VERSION_ID=' /etc/os-release 2>/dev/null | cut -d'=' -f2 | tr -d '"' | cut -d'.' -f1 || echo "22")

# 버전별 debs 디렉토리 우선, 없으면 debs/ (레거시) 로 fallback
DEB_DIR="$SCRIPT_DIR/debs/ubuntu${UBUNTU_VER}"
if [ ! -d "$DEB_DIR" ] || [ -z "$(find "$DEB_DIR" -maxdepth 1 -name '*.deb' 2>/dev/null | head -1)" ]; then
    DEB_DIR="$SCRIPT_DIR/debs"
fi

echo "════════════════════════════════════════════════"
echo "  Ubuntu 오프라인 설치"
echo "════════════════════════════════════════════════"
echo "  OS    : $(grep '^PRETTY_NAME=' /etc/os-release 2>/dev/null | cut -d'=' -f2 | tr -d '"' || echo '확인불가')"
echo ""

# ── [1/2] 시스템 패키지 설치 (git, python3-pip) ──────
echo "[1/2] 시스템 패키지 설치 ..."

DEB_COUNT=$(find "$DEB_DIR" -maxdepth 1 -name '*.deb' 2>/dev/null | wc -l)
if [ "$DEB_COUNT" -gt 0 ]; then
    echo "      경로   : $DEB_DIR ($DEB_COUNT개)"
    dpkg -i "$DEB_DIR"/*.deb 2>/dev/null || true
    apt-get install -f -y 2>/dev/null || true
    echo "      git    : $(git --version 2>/dev/null || echo '확인 필요')"
    echo "      python3: $(python3 --version 2>/dev/null || echo '확인 필요')"
    echo "      pip    : $(python3 -m pip --version 2>/dev/null | cut -d' ' -f1-2 || echo '확인 필요')"
else
    echo "      [WARN] debs/ubuntu${UBUNTU_VER}/ 및 debs/ 폴더 없음 또는 비어 있음 — 시스템 패키지 건너뜀"
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

# 버전별 디렉토리 우선, 없으면 공통 디렉토리 fallback
VERSIONED_PKG="$SCRIPT_DIR/packages/ubuntu${UBUNTU_VER}"
COMMON_PKG="$SCRIPT_DIR/packages"
PY_PKG_DIR=""
if [ -d "$VERSIONED_PKG" ] && [ -n "$(find "$VERSIONED_PKG" -maxdepth 1 -name '*.whl' 2>/dev/null | head -1)" ]; then
    PY_PKG_DIR="$VERSIONED_PKG"
elif [ -d "$COMMON_PKG" ] && [ -n "$(find "$COMMON_PKG" -maxdepth 1 -name '*.whl' 2>/dev/null | head -1)" ]; then
    PY_PKG_DIR="$COMMON_PKG"
else
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
