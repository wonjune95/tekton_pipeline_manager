#!/bin/bash
# ════════════════════════════════════════════════════════════════
#  Ubuntu 패키지 다운로드 스크립트
# ════════════════════════════════════════════════════════════════
#  실행 환경 : 인터넷 연결된 Ubuntu 머신
#              (폐쇄망 대상과 동일한 Ubuntu 버전 / x86_64 권장)
#
#  다운로드 결과 :
#    packages/  ─ Python wheel (.whl) 파일
#    debs/      ─ git, python3, python3-pip .deb 패키지 및 의존성
#
#  다음 단계 :
#    ubuntu/ 폴더 전체를 폐쇄망으로 복사 후 install.sh 실행
# ════════════════════════════════════════════════════════════════

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REQ_FILE="$SCRIPT_DIR/../requirements.txt"

# Ubuntu 버전 감지 (22 / 24 / 26)
UBUNTU_VER=$(grep '^VERSION_ID=' /etc/os-release 2>/dev/null | cut -d'=' -f2 | tr -d '"' | cut -d'.' -f1 || echo "22")
DEB_DIR="$SCRIPT_DIR/debs/ubuntu${UBUNTU_VER}"
PY_PKG_DIR="$SCRIPT_DIR/packages/ubuntu${UBUNTU_VER}"

echo "════════════════════════════════════════════════"
echo "  Ubuntu 패키지 다운로드"
echo "════════════════════════════════════════════════"
echo "  OS    : $(grep '^PRETTY_NAME=' /etc/os-release 2>/dev/null | cut -d'=' -f2 | tr -d '"' || echo '확인불가')"
echo "  버전  : Ubuntu ${UBUNTU_VER}"
echo "  아키텍처: $(uname -m)"
echo ""

# ── Python 확인 ──────────────────────────────────────
PYTHON=$(command -v python3 || true)
if [ -z "$PYTHON" ]; then
    echo "[ERROR] python3가 없습니다."
    echo "        sudo apt-get install -y python3 python3-pip"
    exit 1
fi
PY_VERSION=$($PYTHON --version)
echo "[INFO] Python: $PY_VERSION"

if ! $PYTHON -m pip --version &>/dev/null; then
    echo "[ERROR] pip가 없습니다."
    echo "        sudo apt-get install -y python3-pip"
    exit 1
fi

# ── [1/2] Python 패키지 다운로드 ─────────────────────
mkdir -p "$PY_PKG_DIR"
echo ""
echo "[1/2] Python 패키지 다운로드 ..."
echo "      경로: $PY_PKG_DIR (ubuntu${UBUNTU_VER})"

$PYTHON -m pip download \
    -r "$REQ_FILE" \
    -d "$PY_PKG_DIR" \
    --prefer-binary

PY_COUNT=$(ls "$PY_PKG_DIR" | wc -l)
echo "      완료: ${PY_COUNT}개 파일"

# ── [2/2] 시스템 패키지 다운로드 (git + python3-pip) ──
mkdir -p "$DEB_DIR"
echo ""
echo "[2/2] 시스템 패키지 .deb 다운로드 ..."
echo "      경로: $DEB_DIR (ubuntu${UBUNTU_VER})"

sudo apt-get update -qq

# 설치 여부와 무관하게 강제 다운로드 (--reinstall --download-only)
# python3-distutils: Ubuntu 22 전용 (24+에서 제거됨)
PKGS="git python3 python3-pip"
if [ "$UBUNTU_VER" -le 22 ] 2>/dev/null; then
    PKGS="$PKGS python3-distutils"
fi
# shellcheck disable=SC2086
sudo apt-get install --reinstall --download-only -y $PKGS 2>/dev/null || true

# /var/cache/apt/archives/ 에서 복사
sudo cp -n /var/cache/apt/archives/*.deb "$DEB_DIR/" 2>/dev/null || true
sudo chown "$(id -u):$(id -g)" "$DEB_DIR"/*.deb 2>/dev/null || true
DEB_COUNT=$(ls "$DEB_DIR" 2>/dev/null | wc -l)
echo "      완료: ${DEB_COUNT}개 파일"

# ── 결과 요약 ────────────────────────────────────────
echo ""
echo "════════════════════════════════════════════════"
echo "  다운로드 완료"
echo "════════════════════════════════════════════════"
echo "  Python 패키지 : packages/ubuntu${UBUNTU_VER}/  (${PY_COUNT}개)"
echo "  시스템 패키지 : debs/ubuntu${UBUNTU_VER}/    (${DEB_COUNT}개)"
echo ""
echo "  [다음 단계]"
echo "  ubuntu/ 폴더 전체를 폐쇄망 서버에 복사 후:"
echo "    chmod +x install.sh && sudo ./install.sh"
echo "════════════════════════════════════════════════"
