# Tekton Pipeline Manager

Kubernetes 환경에서 Tekton CI/CD 파이프라인을 **자동으로 설치·구성**하는 CLI 도구입니다.

복잡한 YAML을 직접 작성하지 않고, 메뉴를 따라가면 다음을 자동으로 처리합니다.

- Tekton, ArgoCD, Harbor, Nexus, Gitea, SonarQube 초기 설정
- 조직(네임스페이스) 및 RBAC 생성
- 앱 빌드/배포 파이프라인 YAML 생성
- GitOps 저장소 생성 및 초기 파일 푸시

---

## 사전 준비

### 필요 환경

| 항목 | 버전 |
|------|------|
| Python | 3.8 이상 |
| kubectl | 클러스터 접근 가능 상태 |

### Python 패키지 설치 (오프라인)

폐쇄망 환경에서는 `python-package/` 폴더 안의 스크립트로 설치합니다.

```bash
# Ubuntu
cd python-package/ubuntu/
chmod +x install.sh && sudo ./install.sh

# Rocky Linux 8 / 9 (버전 자동 감지)
cd python-package/rocky/
chmod +x install.sh && sudo ./install.sh
```

---

## 폴더 구조

```
gitops/
├── yaml_maker.py                       ← 실행 진입점
│
├── 00.reset/
│   └── tekton_init.toml                ← 전체 인프라 설정값 (최초 1회 작성)
│
├── 01.init/                            ← Tekton 초기화 YAML 템플릿
│   ├── tekton-catalog/
│   ├── tekton-group-role/
│   ├── tekton-with-role/
│   ├── argocd/
│   ├── oauth/
│   └── {env}-{tier}-cluster.yaml       ← 클러스터별 스토리지 초기화 템플릿
│
├── 02-1.add-storage-in-organization/   ← 조직별 스토리지 YAML 템플릿
├── 02-2.add-organization/              ← 조직 네임스페이스·RBAC 템플릿
│
├── 03.add-app-in-organization/         ← 앱 파이프라인 템플릿
│   ├── sample-npm-argo-pipeline/
│   ├── sample-maven-boot-argo-pipeline/
│   ├── sample-maven-tomcat-argo-pipeline/
│   ├── sample-maven-spring-vm-pipeline/
│   ├── sample-gradle-boot-argo-pipeline/
│   ├── sample-gradle-tomcat-argo-pipeline/
│   └── sample-spring-library-pipeline/
│
├── 04.gitea-source/                    ← GitOps 저장소 YAML 템플릿
│   ├── sample-backend-{type}-gitops/
│   └── sample-frontend-{type}-gitops/
│
├── menu/                               ← 메뉴별 Python 로직
│   ├── menu1_init.py
│   ├── menu2_add_org.py
│   ├── menu3_add_pipeline_runner.py
│   ├── menu4_add_gitops.py
│   └── util/
│       ├── component_api.py            ← Harbor, Nexus, SonarQube API
│       ├── gitea_api.py                ← Gitea API
│       └── ui.py
│
├── tekton-rbac/                        ← Tekton 직접 적용용 YAML
├── python-package/                     ← 오프라인 설치 패키지 모음
│   ├── ubuntu/  (debs/ + packages/)
│   └── rocky/   (rpms/rocky8|9/ + packages/)
│
└── result/                             ← 생성된 YAML 결과물 저장
```

---

## 전체 사용 흐름

```
1단계: tekton_init.toml 작성
         ↓
2단계: 메뉴 1 — Tekton 초기화 (최초 1회)
         ↓
3단계: 메뉴 2 — 조직 추가
         ↓
4단계: 메뉴 3 — 앱 파이프라인 생성
         ↓
5단계: 메뉴 4 — 앱 GitOps 저장소 생성
```

---

## 1단계: 설정 파일 작성

`00.reset/tekton_init.toml` 을 복사하여 프로젝트 루트에 `tekton_init.toml` 파일을 만들고 실제 환경값으로 채웁니다.

```
gitops/
├── tekton_init.toml   ← 여기에 위치해야 함
└── yaml_maker.py
```

설정 파일은 14개 섹션으로 구성됩니다.

| 섹션 | 내용 |
|------|------|
| 1. 프로젝트 기본 정보 | `project_name` |
| 2. Kubernetes 클러스터 | `nks_master_server`, `nnd_cluster_name`, `cicdbot_token` 등 |
| 3. OAuth 설정 | Gitea OAuth2 App 클라이언트 ID/Secret |
| 4. Harbor | `image_registry`, `harbor_admin_pw` 등 |
| 5. 컴포넌트 관리자 계정 | Gitea, Nexus, ArgoCD, SonarQube admin 계정 |
| 6. CICD 봇 서비스 계정 | `cicdbot`, `devopsadmin`, `cicdmanager` 계정 |
| 7. 외부 접속 URL | ArgoCD, Tekton, Gitea, Nexus, SonarQube 도메인 |
| 8. 클러스터 내부 서비스 URL | 기본값 유지 권장 |
| 9. 배포 대상 클러스터 | dev/stg/prod별 back/front 클러스터 API 주소 |
| 10. NAS 스토리지 | 환경별 NFS 서버 IP·경로 |
| 11. 애플리케이션 도메인 | nip.io 도메인, LB IP |
| 12. VM SSH 배포 | VM 호스트 목록, SSH 키 |
| 13. 캐시 노드 | SSH 접속 정보, PEM 파일명 |
| 14. SSL 인증서 | 와일드카드 dev/prod SSL 인증서·키 |

> **주의**: `cicdbot_token`은 메뉴 1 초기화 실행 및 `kubectl apply` 후 별도로 채워야 합니다.  
> `harbor_robot_pw`, `harbor_robot_auth`, `sonar_token`은 메뉴 1 초기화 실행 시 자동 생성됩니다.

---

## 2단계: 프로그램 실행

```bash
cd gitops/
python yaml_maker.py
```

```
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃                    Tekton Pipeline Manager                          ┃
┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
┃ 1. Tekton 초기화                                                    ┃
┃ 2. 조직추가                                                         ┃
┃ 3. 앱 파이프라인                                                    ┃
┃ 4. 앱 GitOps                                                        ┃
┃ 9. 종료                                                             ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
```

---

## 메뉴 1: Tekton 초기화

**최초 1회만 실행합니다.**

Tekton, ArgoCD, Harbor, Nexus, Gitea, SonarQube의 계정·저장소를 자동 생성하고, 클러스터에 적용할 YAML을 만듭니다.

### 하위 메뉴

| 번호 | 기능 |
|------|------|
| 1 | `tekton_init.toml` 설정값 화면 확인 |
| 2 | **초기화 실행** — YAML 생성 + 각 컴포넌트 계정 자동 생성 |
| 3 | ArgoCD 관리자 비밀번호 일괄 변경 |

### 초기화 실행 시 처리 내용

1. `01.init/` 템플릿을 렌더링하여 `result/{project_name}/`에 생성
   - `01-1.init-basic.yaml` — Tekton 기본 리소스
   - `01-2.init-pipeline.yaml` — Tekton Catalog (공통 Task)
   - `01-3.init-oauth.yaml` — OAuth 설정
   - `01-4.init-argo.yaml` — ArgoCD 설정
   - `01-5.init-tekton-group-role.yaml` — Tekton 그룹 롤
2. Harbor robot 계정 자동 생성
3. Gitea CI/CD 서비스 계정 자동 생성
4. Nexus 계정 및 저장소(maven, npm, raw) 자동 생성
5. SonarQube 토큰 자동 생성
6. 결과를 `{project_name}-init_result.json`으로 저장

### 실행 후 해야 할 일

```bash
# 1. cicdbot token 취득 후 init_result.json에 채우기
kubectl config use-context {nnd_cluster_name}
kubectl apply -f result/{project_name}/01-1.init-basic.yaml

TOKEN=$(kubectl describe secret cicdbot -n default | grep token: | awk '{print $2}')
sed -i "s/\"cicdbot_token\": \"\"/\"cicdbot_token\": \"$TOKEN\"/" \
  result/{project_name}/{project_name}-init_result.json

# 2. PEM 키 파일을 result/{project_name}/ 폴더에 복사
cp {your_key}.pem result/{project_name}/

# 3. 나머지 YAML 순서대로 적용
kubectl apply -f result/{project_name}/01-2.init-pipeline.yaml
kubectl apply -f result/{project_name}/01-3.init-oauth.yaml
kubectl apply -f result/{project_name}/01-4.init-argo.yaml
kubectl apply -f result/{project_name}/01-5.init-tekton-group-role.yaml
```

> **참고**: Tekton에 RBAC가 적용된 경우 CoreDNS hosts에 Gitea 도메인을 등록해야 합니다.

---

## 메뉴 2: 조직 추가

새로운 팀/프로젝트 단위의 **조직(네임스페이스)** 을 추가합니다.

### 사전 준비

```bash
# 현재 클러스터의 RBAC 파일 추출
kubectl get ClusterRoleBinding cicdbot -o yaml > ./02-2.add-organization/rbac.yaml
```

### 하위 메뉴

| 번호 | 기능 |
|------|------|
| 1 | 설정값 화면 확인 |
| 2 | **조직추가 실행** |
| 3 | CICD 캐시 폴더 재생성 (SSH) |

### 실행 시 처리 내용

1. `02-1.add-storage-in-organization/` → 클러스터별 스토리지 YAML 생성
2. `02-2.add-organization/` → 네임스페이스 + RBAC YAML 생성
3. CICD 캐시 노드에 SSH 접속하여 `/CICD-DATA/local/{조직명}-cicd` 폴더 생성 (PEM 키 있을 때)
4. 결과 경로: `result/{project_name}/{조직명}-cicd/`

### 적용

```bash
# 각 앱 클러스터에 스토리지 적용
kubectl config use-context dev-be-cluster
kubectl apply -f result/{project_name}/{조직명}-cicd/02-1.dev-be-cluster.yaml

# ... stg, prod 클러스터도 동일하게 적용

# CICD(ND) 클러스터에 조직 리소스 적용
kubectl config use-context {nnd_cluster_name}
kubectl apply -f result/{project_name}/{조직명}-cicd/02-2.add-organization.yaml
```

---

## 메뉴 3: 앱 파이프라인 생성

앱별 빌드/배포 파이프라인 YAML을 생성합니다.

### 입력 모드

| 모드 | 설명 |
|------|------|
| 자동선택 | Gitea API로 조직·앱 목록을 가져와 선택 |
| 수동입력 | 조직명·앱명 직접 입력 |

### 파이프라인 유형

| 번호 | 설명 |
|------|------|
| 1 | Frontend — build(npm-nginx) + deploy(ArgoCD) |
| 2 | Backend — build(maven-boot) + deploy(ArgoCD) |
| 3 | Backend — build(maven-tomcat) + deploy(ArgoCD) |
| 4 | Backend — build(maven-spring) + deploy(VM SSH) |
| 5 | Backend — build(gradle-boot) + deploy(ArgoCD) |
| 6 | Backend — build(gradle-tomcat) + deploy(ArgoCD) |
| 7 | Library — build(maven-library) |

### 추가 입력 항목

- **환경명**: `dev` / `stg` / `prod`
- **브랜치명**: 트리거할 git 브랜치 (예: `dev`, `main`)
- **배포 클러스터**: 목록에서 선택

### 결과물 및 적용

```
result/{project_name}/{조직명}-cicd/{앱명}/
└── 03.add-app-in-organization-{앱명}-{환경명}.yaml
```

```bash
kubectl config use-context {nnd_cluster_name}
kubectl apply -f result/{project_name}/{조직명}-cicd/{앱명}/03.add-app-in-organization-{앱명}-{환경명}.yaml
```

---

## 메뉴 4: 앱 GitOps 저장소 생성

Gitea에 GitOps 저장소를 만들고 배포용 YAML 템플릿을 자동으로 푸시합니다.

### GitOps 유형

| 번호 | 설명 |
|------|------|
| 1 | Frontend — svc |
| 2 | Frontend — ing (Ingress) |
| 3 | Frontend — hpa-bluegreen |
| 4 | Frontend — hpa-canary |
| 5 | Backend — svc |
| 6 | Backend — ing |
| 7 | Backend — hpa-bluegreen |
| 8 | Backend — hpa-canary |

### 처리 내용

1. Gitea에 조직(`{조직명}-cicd`) 자동 생성
2. Gitea에 저장소 자동 생성
   - `{앱명}-gitops` — ArgoCD가 바라보는 GitOps 저장소
   - `{앱명}-dev` — 앱 소스 저장소 (dev)
   - `{앱명}-prod` — 앱 소스 저장소 (prod)
3. `04.gitea-source/` 템플릿을 렌더링하여 `{앱명}-gitops` 저장소에 push

---

## 결과물 구조 예시

```
result/
└── gov24/                                        ← project_name
    ├── gov24-init_result.json                    ← 초기화 결과 (이후 모든 작업의 기준값)
    ├── 01-1.init-basic.yaml
    ├── 01-2.init-pipeline.yaml
    ├── 01-3.init-oauth.yaml
    ├── 01-4.init-argo.yaml
    ├── 01-5.init-tekton-group-role.yaml
    └── sample-cicd/                              ← 조직명
        ├── 02-1.dev-be-cluster.yaml
        ├── 02-1.dev-fe-cluster.yaml
        ├── 02-2.add-organization.yaml
        └── sample-app/                           ← 앱명
            ├── 03.add-app-in-organization-sample-app-dev.yaml
            └── 03.add-app-in-organization-sample-app-prod.yaml
```

---

## 자주 발생하는 문제

### rbac.yaml 없음 오류 (메뉴 2)

```bash
kubectl get ClusterRoleBinding cicdbot -o yaml > ./02-2.add-organization/rbac.yaml
```

### 초기화 파일 없음 오류

`result/{project_name}/{project_name}-init_result.json`이 없는 경우입니다.  
메뉴 1 초기화를 먼저 실행하세요.

### ArgoCD 비밀번호 변경 실패 (메뉴 1-3)

ArgoCD ConfigMap이 등록되어 있어야 합니다.

```bash
kubectl get cm argocd-cm -n argocd
```

하위 경로(sub-path) 사용 시 `--grpc-web-root-path argocd` 옵션이 추가로 필요합니다.

### Gitea 접근 불가 (폐쇄망)

CoreDNS에 Gitea 호스트를 등록해야 합니다. Tekton RBAC 적용 환경에서 필수입니다.

### SSH 접속 실패 (메뉴 2, 캐시 노드 폴더 생성)

PEM 파일이 `result/{project_name}/` 폴더에 없는 경우입니다.  
파일이 없으면 자동 생성을 건너뛰므로, 아래 명령어를 수동으로 실행하세요.

```bash
ssh -i {pem_file} {cicd_cache_node_id}@{cicd_cache_node_ip} \
  "sudo mkdir -p /CICD-DATA/local/{조직명}-cicd"
```
