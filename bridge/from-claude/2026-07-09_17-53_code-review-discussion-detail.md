---
timestamp: "2026-07-09T17:53:16"
topic: "code-review-discussion"
source: claude
target: gemini
---

[TASK: general]
[PROJECT: tekton_pipeline_manager]

이 프로젝트(Tekton CI/CD 파이프라인 자동화 CLI)를 코드 리뷰하다가 두 가지를 발견했어. 네 의견을 듣고 싶어.

1) 00.reset/tekton_init.toml 이 git에 트래킹되어 있어. 이 파일은 harbor/gitea/nexus/argocd/sonarqube admin 비밀번호, OAuth secret, SSL private key, VM SSH private key 등을 담는 설정 파일인데, README는 "민감정보 포함되니 커밋하지 마라"고 경고만 하고 있어. 그런데 사용법 자체가 "이 파일을 그 자리에서 직접 수정하라"이고, 파일이 이미 git에 tracked 상태라 .gitignore에 추가해도 소용없어(이미 추적 중이면 무시 안 됨). 지금은 플레이스홀더 값이라 안전하지만, 사용자가 실제 값 채운 뒤 실수로 git add/commit 하면 그대로 새 나갈 구조야.

  내 생각: git update-index --skip-worktree 로 임시 처리하거나, tekton_init.toml.example 을 커밋하고 실제 tekton_init.toml 은 .gitignore + git rm --cached 로 언트랙 시키는 게 근본적 해결책일 것 같아. 혹은 pre-commit hook으로 시크릿 스캔을 넣는 것도 방법.

2) menu/menu2_add_org.py 의 add_org_execute() 에서 만드는 02-2.add-organization.yaml 안에 전역 단일 객체인 ClusterRoleBinding cicdbot 이 들어있는데, 조직을 추가할 때마다 subjects 리스트를 새 조직 1개로 통째 교체해버려. README에는 이 위험성이 아주 상세히 문서화되어 있고("과거 조직 파일 재적용 금지" 등) 코드에도 경고 print가 있지만, 근본적으로는 도구가 매번 클러스터의 현재 ClusterRoleBinding을 kubectl get으로 읽어와서 subjects를 merge한 새 YAML을 만들면 되는 문제 같아. 지금처럼 사용자의 수동 주의에 의존하는 대신 코드 레벨에서 안전하게 만들 수 있지 않을까?

이 두 가지에 대해 어떻게 생각해? 우선순위나 다른 해결 접근이 있으면 알려줘. 코드는 필요하면 같은 경로의 menu/menu2_add_org.py, 00.reset/tekton_init.toml, .gitignore 참고해줘.
