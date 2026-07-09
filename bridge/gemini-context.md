# Gemini Context — tekton_pipeline_manager

> 이 파일은 Claude가 Gemini에게 요청할 때 자동으로 포함되는 프로젝트 컨텍스트입니다.
> `/gemini init` 시 자동 생성되며, 프로젝트가 발전하면 Claude가 자동 업데이트합니다.

## 프로젝트 개요
Kubernetes 환경에서 Tekton CI/CD 파이프라인을 CLI 메뉴 기반으로 자동 설치·구성하는 Python 도구.
Tekton/ArgoCD/Harbor/Nexus/Gitea/SonarQube 초기 설정, 조직(네임스페이스)/RBAC/스토리지 생성,
앱 빌드/배포 파이프라인 YAML 생성, GitOps 저장소 자동 생성을 메뉴(1~5)로 처리한다.

## 기술 스택
Python 3.8+, Jinja2(YAML 템플릿 렌더링), inquirer(대화형 메뉴), paramiko(SSH), requests(Harbor/Nexus/Gitea/SonarQube REST API), tomllib/tomli(설정 파싱), kubectl(subprocess 호출).

## 디자인 시스템
해당 없음 (CLI 도구, ANSI 컬러 코드로 터미널 UI 구성)

## Gemini 주 역할
코드 리뷰 의견 교환 — 보안/설계 관점에서 발견한 이슈에 대한 세컨 오피니언

## 현재 상태
사용자가 프로젝트를 처음 훑어보는 단계. Claude가 코드 리뷰 후 발견한 이슈 2가지를 Gemini와 논의 예정.
