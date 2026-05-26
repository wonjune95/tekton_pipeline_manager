Rocky Linux 10용 시스템 패키지 (.rpm) 디렉토리

이 폴더는 현재 비어 있습니다.
아래 절차로 Rocky Linux 10 환경에서 패키지를 다운로드한 뒤 이 폴더에 복사하세요.

  # 인터넷 연결된 Rocky Linux 10 머신에서 실행
  cd python-package/rocky
  chmod +x download.sh && ./download.sh

  # 생성된 rpms/rocky10/*.rpm 파일을 폐쇄망 서버에 복사 후
  sudo ./install.sh  (또는 상위 python-package/install.sh)

참고:
  Rocky Linux 10은 Python 3.12를 기본으로 사용합니다.
  현재 rocky/packages/ 의 wheel 중 cp39-cp39 태그 파일은
  Python 3.12에서 호환되지 않으므로, 필요 시
  rocky/packages/rocky10/ 에 Python 3.12용 wheel을 별도 추가하세요.
