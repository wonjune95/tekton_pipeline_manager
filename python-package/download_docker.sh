#!/bin/bash
# ════════════════════════════════════════════════════════════════
#  폐쇄망 오프라인 설치용 패키지 다운로드
#
#  사전 조건 : Docker Desktop 설치 및 실행 중
#  실행 방법 : Git Bash에서  bash download_docker.sh
#
#  다운로드 결과 :
#    rocky/rpms/rocky8/     ← Rocky 8 시스템 RPM
#    rocky/rpms/rocky9/     ← Rocky 9 시스템 RPM
#    rocky/packages/rocky8/ ← Rocky 8용 Python wheel
#    rocky/packages/rocky9/ ← Rocky 9용 Python wheel
#
#  다음 단계 :
#    python-package/ 폴더 전체를 폐쇄망 서버에 복사 후
#    chmod +x install.sh && sudo ./install.sh
# ════════════════════════════════════════════════════════════════

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# ── Docker 확인 ──────────────────────────────────────────────────
if ! command -v docker &>/dev/null; then
    echo "[ERROR] Docker가 설치되어 있지 않습니다."
    echo "        https://www.docker.com/products/docker-desktop/ 에서 설치 후 재실행하세요."
    exit 1
fi

if ! docker info &>/dev/null 2>&1; then
    echo "[ERROR] Docker Desktop이 실행 중이지 않습니다. 시작 후 재실행하세요."
    exit 1
fi

# ── Rocky Linux 버전별 다운로드 ──────────────────────────────────
run_rocky() {
    local VER="$1"
    echo ""
    echo "━━ Rocky Linux ${VER} ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "   이미지 pull 중 (rockylinux:${VER}) ..."

    # MSYS_NO_PATHCONV=1 : Git Bash가 Linux 경로를 Windows 경로로 변환하는 것 방지
    MSYS_NO_PATHCONV=1 docker run --rm \
        -v "${SCRIPT_DIR}:/pkg" \
        "rockylinux:${VER}" \
        bash /pkg/rocky/docker_inner.sh "$VER"

    local RPM_COUNT WHL_COUNT
    RPM_COUNT=$(ls "${SCRIPT_DIR}/rocky/rpms/rocky${VER}" 2>/dev/null | wc -l)
    WHL_COUNT=$(ls "${SCRIPT_DIR}/rocky/packages/rocky${VER}" 2>/dev/null | wc -l)
    echo ""
    echo "   Rocky ${VER} 완료 — RPM: ${RPM_COUNT}개 / WHL: ${WHL_COUNT}개"
}

# ════════════════════════════════════════════════════════════════
echo "════════════════════════════════════════════════"
echo "  폐쇄망 오프라인 패키지 다운로드 (Docker 사용)"
echo "════════════════════════════════════════════════"

# 인자 없으면 8, 9 모두 / 인자 있으면 해당 버전만  예) bash download_docker.sh 8
VERSIONS="${*:-8 9}"
for VER in $VERSIONS; do
    run_rocky "$VER"
done

echo ""
echo "════════════════════════════════════════════════"
echo "  다운로드 완료"
echo ""
echo "  [다음 단계]"
echo "  python-package/ 폴더 전체를 폐쇄망 서버에 복사 후:"
echo "    chmod +x install.sh && sudo ./install.sh"
echo "════════════════════════════════════════════════"
