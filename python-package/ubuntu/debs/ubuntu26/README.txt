Ubuntu 26.04용 시스템 패키지 (.deb) 디렉토리

이 폴더는 현재 비어 있습니다.
아래 절차로 Ubuntu 26.04 환경에서 패키지를 다운로드한 뒤 이 폴더에 복사하세요.

  # 인터넷 연결된 Ubuntu 26.04 머신에서 실행
  cd python-package/ubuntu
  chmod +x download.sh && ./download.sh

  # 생성된 debs/*.deb 파일을 이 폴더(ubuntu26/)에 이동
  mv debs/*.deb debs/ubuntu26/

  # 폐쇄망 서버에 복사 후
  sudo ./install.sh  (또는 상위 python-package/install.sh)

참고:
  Ubuntu 26.04는 Python 3.13을 기본으로 사용합니다.
  현재 ubuntu/packages/ 의 wheel 중 cp310-cp310 태그 파일은
  Python 3.13에서 호환되지 않으므로, 필요 시
  ubuntu/packages/ubuntu26/ 에 Python 3.13용 wheel을 별도 추가하세요.
