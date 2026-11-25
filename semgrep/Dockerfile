# Semgrep 점검 이미지 = Semgrep CE 1.180.0 + 이 저장소의 규칙. 폐쇄망에서는 이 이미지 하나로 점검한다 (규칙 저장소 접근 불필요)
#   docker build --build-arg RULESET_VERSION="$(git describe --tags --exact-match 2>/dev/null || echo untagged) $(git rev-parse --short HEAD)" -t <레지스트리>/semgrep-mois:<태그> .
# 규칙은 /semgrep-rules/rules, 보고서 스크립트는 /semgrep-rules/scripts/report.py 에 있다.
FROM semgrep/semgrep:1.180.0@sha256:dffc9caeecc924370d30f9187b6edf10949600d3ef5f69ef5c359074d8fc7d2d
ARG RULESET_VERSION="untagged unknown"
COPY rules/ /semgrep-rules/rules/
COPY scripts/report.py /semgrep-rules/scripts/report.py
RUN printf '%s\n' "$RULESET_VERSION" > /semgrep-rules/VERSION
