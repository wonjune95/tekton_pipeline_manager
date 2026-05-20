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

인터넷이 되는 환경에서는 pip로 직접 설치합니다.

```bash
pip install -r python-package/requirements.txt
```

---

## 폴더 구조

```
tekton_pipeline_manager/
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
│   └── {env}-{tier}-cluster.yaml       ← 앱 클러스터 초기 namespace/secret/SC 템플릿
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
│   ├── menu5_reset_cache.py
│   └── util/
│       ├── component_api.py            ← Harbor, Nexus, SonarQube, Gitea API
│       └── ui.py                       ← 메뉴 렌더링, 입력 검증
│
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

`00.reset/tekton_init.toml` 을 **그 자리에서 직접 수정**합니다. 복사할 필요 없습니다.  
`yaml_maker.py`는 실행 시 `00.reset/tekton_init.toml`을 자동으로 읽습니다.

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
cd tekton_pipeline_manager/
python3 yaml_maker.py
```

```
  ╔════════════════════════════════════════════════════════════════╗
  ║                                                                ║
  ║  TEKTON  PIPELINE  MANAGER                                     ║
  ║  project : MY_PROJECT_NAME                                     ║
  ║                                                                ║
  ╠════════════════════════════════════════════════════════════════╣
  ║                                                                ║
  ║  [ 1 ]  초기화      Tekton 인프라 초기 설정                    ║
  ║  [ 2 ]  조직 추가   새 조직 및 네임스페이스 생성               ║
  ║  [ 3 ]  파이프라인  앱 CI/CD 파이프라인 러너 생성              ║
  ║  [ 4 ]  GitOps      GitOps 레포 생성 및 초기화                 ║
  ║  [ 5 ]  캐시 초기화 캐시 노드 폴더 초기화                      ║
  ║                                                                ║
  ║  [ 9 ]  종료                                                   ║
  ║                                                                ║
  ╚════════════════════════════════════════════════════════════════╝
```

또는 메뉴 번호를 직접 지정하여 실행할 수도 있습니다.

```bash
python3 yaml_maker.py 1   # 초기화 바로 실행
python3 yaml_maker.py 2   # 조직추가 바로 실행
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
   - `01-1.init-basic.yaml` — Tekton 기본 리소스 (RBAC, ServiceAccount 등)
   - `01-2.init-pipeline.yaml` — Tekton Catalog (공통 Task, Pipeline)
   - `01-3.init-oauth.yaml` — OAuth 설정
   - `01-4.init-argo.yaml` — ArgoCD 설정
   - `01-5.init-tekton-group-role.yaml` — Tekton 그룹 롤
   - `01-6.init-cluster.yaml` — 앱 클러스터(dev/stg/prod be·fe) 초기 namespace·SC·secret
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

# 4. 앱 클러스터(dev/stg/prod be·fe)에는 01-6.init-cluster.yaml 을 컨텍스트 전환 후 적용
kubectl config use-context dev-be-cluster
kubectl apply -f result/{project_name}/01-6.init-cluster.yaml
# ... stg, prod, frontend 클러스터도 동일
```

> **참고**: Tekton에 RBAC가 적용된 경우 CoreDNS hosts에 Gitea 도메인을 등록해야 합니다.

---

## 메뉴 2: 조직 추가

새로운 팀/프로젝트 단위의 **조직(네임스페이스)** 을 추가합니다.

### 네임스페이스 명명 규칙

Gitea의 조직명을 기준으로, 각 클러스터에 생성되는 네임스페이스가 결정됩니다.

> **입력 제약 (조직명·앱명·환경명 공통)**: 소문자·숫자·하이픈(`-`)만 허용. 시작과 끝은 영문 소문자나 숫자여야 합니다. 최대 53자. 한글·공백·언더스코어·대문자는 거부됩니다 (RFC 1123 DNS label).

예를 들어 Gitea 조직명이 `sample`이면:

| 클러스터 | 네임스페이스 |
|----------|-------------|
| CI/CD (ND) 클러스터 | `sample-cicd` |
| 개발(dev) 클러스터 | `sample-dev` |
| 검증(stg) 클러스터 | `sample-stg` |
| 운영(prod) 클러스터 | `sample-prod` |

> **사전 조건**: 메뉴 2 실행 전에 Gitea에 해당 조직이 먼저 생성되어 있어야 합니다.

### 사전 준비

```bash
# 현재 클러스터의 RBAC 파일 추출
kubectl get ClusterRoleBinding cicdbot -o yaml > ./02-2.add-organization/rbac.yaml
```

### 하위 메뉴

| 번호 | 기능 |
|------|------|
| 1 | 설정값 화면 확인 (캐시 노드 IP 등) |
| 2 | **조직추가 실행** |

### 실행 시 처리 내용

1. `02-1.add-storage-in-organization/` → 클러스터별 스토리지 YAML 생성
2. `02-2.add-organization/` → 네임스페이스 + RBAC YAML 생성
3. `result/{project_name}/` 아래에 `.pem` 파일이 있으면 캐시 노드에 SSH 접속하여 `/CICD-DATA/local/{조직명}-cicd`, `/CICD-DATA/store/{조직명}-cicd` 폴더 자동 생성
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

> **주의**: 네이버와 NHN 환경의 RBAC 구조가 다를 수 있으므로, 적용 전 반드시 내용을 확인하세요.  
> 사용 완료된 `./02-2.add-organization/rbac.yaml` 파일은 직접 삭제하세요.  
> `02-1.add-storage-in-organization` 파일은 **각 어플리케이션 클러스터에서 나눠서 실행**하세요.

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
| 7 | Library — build(maven-library, nexus 배포) |

### 추가 입력 항목

- **환경명**: `dev` / `stg` / `prod`
- **브랜치명**: 트리거할 git 브랜치 (예: `dev`, `main`)
- **배포 클러스터**: 목록에서 선택 (유형 4·7 제외)

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
| 1 | Frontend — ing (Ingress) |
| 2 | Frontend — svc |
| 3 | Frontend — hpa-bluegreen |
| 4 | Frontend — hpa-canary |
| 5 | Backend — ing (Ingress) |
| 6 | Backend — svc |
| 7 | Backend — hpa-bluegreen |
| 8 | Backend — hpa-canary |

### 처리 내용

1. Gitea에 조직(`{조직명}-cicd`) 자동 생성
2. Gitea에 아래 저장소 자동 생성
   - `{앱명}-gitops` — ArgoCD가 바라보는 GitOps 저장소
   - `{앱명}-dev` — 환경별 앱 소스 저장소 (dev)
   - `{앱명}-stg` — 환경별 앱 소스 저장소 (stg)
   - `{앱명}-prod` — 환경별 앱 소스 저장소 (prod)
3. `04.gitea-source/` 템플릿을 렌더링하여 `{앱명}-gitops` 저장소에 push

---

## 메뉴 5: 캐시 초기화

CICD 캐시 노드의 특정 조직 폴더를 삭제 후 재생성합니다.  
빌드 캐시 오염 등의 문제가 발생했을 때 사용합니다.

### 동작 방식

- `result/{project_name}/` 에 `.pem` 파일이 있으면 SSH로 자동 실행
- `.pem` 파일이 없으면 수동 실행 명령어를 출력

```bash
# 수동 실행 (각 캐시 노드에서)
sudo rm -rf /CICD-DATA/local/{조직명}-cicd /CICD-DATA/store/{조직명}-cicd
sudo mkdir -p /CICD-DATA/local/{조직명}-cicd /CICD-DATA/store/{조직명}-cicd
```

> **경고**: `yes`를 정확히 입력해야만 실행됩니다. 실수를 방지하기 위한 이중 확인입니다.

---

## Task / Pipeline 커스텀

`01-2.init-pipeline.yaml`에는 모든 Task와 Pipeline이 포함되어 있습니다.  
특정 Task나 Pipeline만 수정이 필요한 경우, 해당 부분만 별도 파일로 만들어 적용합니다.

**원본 템플릿 위치**

```
01.init/tekton-catalog/
├── tasks/
│   ├── build-1-deploy-git-clone.yaml
│   ├── build-2-maven.yaml
│   ├── build-2-gradle.yaml
│   ├── build-2-npm.yaml
│   ├── build-3-image-kaniko.yaml
│   ├── build-4-analyze-sonarqube.yaml
│   ├── build-4-analyze-trivy.yaml
│   ├── build-4-analyze-polaris.yaml
│   ├── build-5-gitops-git-cli.yaml
│   └── ...
└── pipelines/
    ├── build-maven-spring-boot-image.yaml
    ├── build-npm-nodejs-nginx-image.yaml
    └── ...
```

**커스텀 절차**

1. `01.init/tekton-catalog/tasks/` 또는 `pipelines/` 에서 수정할 파일을 복사
2. 파일명과 내부 `metadata.name` 을 새 이름으로 변경
3. 필요한 부분(Dockerfile 경로, 이미지, 파라미터 등) 수정
4. 클러스터에 직접 적용

```bash
# 예시: sonarqube-scanner Task를 커스텀한 경우
kubectl apply -f my-sonarqube-scanner-custom.yaml -n tekton-catalog
```

> **주의**: `metadata.name`을 기본값과 다르게 지정했다면, 이 Task를 참조하는 Pipeline에서도 `taskRef.name`을 함께 수정해야 합니다.

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
    ├── 01-6.init-cluster.yaml
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

```bash
# CoreDNS ConfigMap 수정 예시
kubectl edit cm coredns -n kube-system
# hosts 블록에 추가:
# {gitea_node_ip}  gitea.{your_domain}
```

### SSH 접속 실패 (메뉴 2, 5 — 캐시 노드 폴더 생성)

PEM 파일이 `result/{project_name}/` 폴더에 없는 경우입니다.  
파일이 없으면 자동 생성을 건너뛰므로, 아래 명령어를 수동으로 실행하세요.

```bash
ssh -i {pem_file} {cicd_cache_node_id}@{cicd_cache_node_ip} \
  "sudo mkdir -p /CICD-DATA/local/{조직명}-cicd /CICD-DATA/store/{조직명}-cicd"
```

### Git clone 실패 (메뉴 4)

Gitea에 해당 조직(`{조직명}-cicd`) 또는 저장소(`{앱명}-gitops`)가 없으면 clone이 실패합니다.  
메뉴 4는 내부적으로 저장소를 먼저 생성하지만, Gitea 연결 오류 시 수동 확인이 필요합니다.

```bash
# Gitea API로 조직 확인
curl -H "Authorization: Basic {git_cicd_auth}" \
  https://{gitea_domain}/api/v1/orgs
```

---

## 보안 유의사항

- `tekton_init.toml`과 `{project_name}-init_result.json`에는 패스워드, 토큰 등 민감 정보가 포함됩니다.  
  Git에 커밋하지 않도록 `.gitignore`에 추가하거나 별도 보안 저장소에서 관리하세요.
- `.pem` 파일은 SSH 프라이빗 키이므로 권한을 `600`으로 설정하세요.  
  `chmod 600 result/{project_name}/*.pem`
- Harbor, Nexus, Gitea API 호출 시 TLS 검증이 비활성화(`verify=False`)되어 있습니다.  
  운영 환경에서는 자체 CA 인증서를 `verify` 파라미터에 지정하는 것을 권장합니다.
