!! Rocky Linux 패키지 다운로드 필요 !!
======================================

이 폴더는 비어 있습니다.
Rocky Linux .rpm 파일과 Python 휠은 반드시 Rocky 머신에서 직접 받아야 합니다.

이유:
  - .rpm 파일 : Ubuntu 환경에서 dnf 사용 불가
  - Python 휠  : Rocky 8 (glibc 2.28) / Rocky 9 (glibc 2.34) 호환성 차이
                Ubuntu에서 받은 휠은 Rocky 8에서 동작하지 않을 수 있음

준비 방법:
  1. 인터넷이 연결된 Rocky Linux 머신 (폐쇄망 대상과 동일 버전)에서:

       cd rocky/
       chmod +x download.sh
       ./download.sh

  2. rocky/ 폴더 전체를 폐쇄망 서버로 복사

  3. 폐쇄망 서버에서:

       chmod +x install.sh
       sudo ./install.sh

Ubuntu는 python-package/ubuntu/ 폴더에 패키지가 이미 준비되어 있어
install.sh 바로 실행 가능합니다.
