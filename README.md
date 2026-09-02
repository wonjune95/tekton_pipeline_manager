# Tekton Pipeline Manager

Kubernetes 환경에서 Tekton CI/CD 파이프라인을 **CLI 메뉴 기반으로 자동 설치·구성**하는 도구입니다.

복잡한 YAML을 직접 작성하지 않고, 메뉴를 따라가면 아래 작업을 일괄 처리합니다.

- Tekton · ArgoCD · Harbor · Nexus · Gitea · SonarQube 초기 설정
- 조직(네임스페이스) · RBAC · 스토리지 리소스 생성
- 앱 빌드/배포 파이프라인 YAML 생성 및 클러스터 적용
- GitOps 저장소 자동 생성 및 초기 매니페스트 push

---

## 사전 준비

### 필요 환경

| 항목 | 버전 |
|------|------|
| Python | 3.8 이상 |
| kubectl | 클러스터 접근 가능 상태 |

### Python 패키지 설치

**인터넷 환경**

```bash
pip install -r python-package/requirements.txt
```

설치되는 패키지: `tomli, Jinja2, inquirer, paramiko, pexpect, requests`

**폐쇄망 환경 — 2단계**

#### Step 1. 인터넷 PC에서 패키지 다운로드 (Docker 필요)

Docker Desktop이 설치된 Windows PC에서 Git Bash로 실행:

```bash
cd python-package/
bash download_docker.sh
```

자동 다운로드 위치:

- `rocky/rpms/rocky8/`, `rocky/rpms/rocky9/` — 시스템 RPM
- `rocky/packages/rocky8/`, `rocky/packages/rocky9/` — Python wheel

> **Ubuntu의 경우** `download_docker.sh` 대신 인터넷 되는 Ubuntu 머신에서 `ubuntu/download.sh` 를 실행하세요.

완료 후 `python-package/` 폴더 전체를 폐쇄망 서버에 복사합니다.

#### Step 2. 폐쇄망 서버에서 설치

```bash
cd python-package/
chmod +x install.sh && sudo ./install.sh
```

OS(Rocky 8 / 9, Ubuntu 22 / 24)를 자동 감지합니다.

---

## 폴더 구조

```
tekton_pipeline_manager/
├── yaml_maker.py                       ← 실행 진입점
│
├── 00.reset/
│   └── tekton_init.toml                ← 전체 설정 원본 (최초 1회 작성)
│
├── 01.init/                            ← Tekton 초기화 YAML 템플릿
│   ├── tekton-catalog/                 ← 공통 Task / Pipeline
│   │   ├── tasks/        (16개: build-1~6, deploy, kubernetes-cli 등)
│   │   └── pipelines/    (11개: build-{maven,gradle,npm}-*, deploy-argocd 등)
│   ├── tekton-with-role/               ← Tekton 기본 RBAC / ServiceAccount
│   ├── tekton-group-role/              ← Tekton 그룹 롤
│   ├── argocd/                         ← ArgoCD 설정
│   ├── oauth/                          ← OIDC OAuth 설정
│   └── {env}-{tier}-cluster.yaml       ← 앱 클러스터 초기 namespace/SC/secret
│
├── 02-1.add-storage-in-organization/   ← 조직별 스토리지 (dev/stg/prod × be/fe)
├── 02-2.add-organization/              ← 조직 네임스페이스 · RBAC 템플릿
│
├── 03.add-app-in-organization/         ← 앱 파이프라인 템플릿
│   ├── app-rbac.yaml
│   ├── sample-npm-argo-pipeline/
│   ├── sample-maven-boot-argo-pipeline/
│   ├── sample-maven-tomcat-argo-pipeline/
│   ├── sample-maven-spring-vm-pipeline/
│   ├── sample-gradle-boot-argo-pipeline/
│   ├── sample-gradle-tomcat-argo-pipeline/
│   └── sample-spring-library-pipeline/
│       └── build-{el,pr,tt}.yaml, deploy-{el,pr,tt}.yaml
│
├── 04.gitea-source/                    ← GitOps 매니페스트 템플릿 (kustomize 구조)
│   ├── sample-frontend-{ing,svc,hpa-bluegreen,hpa-canary,istio}-gitops/
│   └── sample-backend-{ing,svc,hpa-bluegreen,hpa-canary,istio}-gitops/
│       └── base/ + overlays/{dev,stg,prod}/
│
├── menu/                               ← 메뉴별 Python 로직
│   ├── menu1_init.py
│   ├── menu2_add_org.py
│   ├── menu3_add_pipeline_runner.py
│   ├── menu4_add_gitops.py
│   ├── menu5_reset_cache.py
│   └── util/
│       ├── component_api.py            ← Harbor/Nexus/SonarQube/Gitea API
│       └── ui.py                       ← 메뉴 박스 렌더링, 입력 검증
│
├── python-package/                     ← 오프라인 설치 패키지
│   ├── download_docker.sh              ← 인터넷 PC에서 실행 (Docker 사용)
│   ├── install.sh                      ← 폐쇄망 서버에서 실행 (OS 자동 감지)
│   ├── requirements.txt
│   ├── ubuntu/  (debs/, packages/, download.sh, install.sh)
│   └── rocky/   (rpms/{rocky8,9}/, packages/{rocky8,9}/, docker_inner.sh, ...)
│
└── result/                             ← 생성된 YAML 결과물 (자동 생성)
```

---

## 전체 사용 흐름

```
1단계: 00.reset/tekton_init.toml 작성
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
`yaml_maker.py` 가 실행 시 자동으로 읽습니다.

설정 파일은 14개 섹션입니다.

| 섹션 | 내용 |
|------|------|
| 1. 프로젝트 기본 정보 | `project_name` |
| 2. Kubernetes 클러스터 | `nks_master_server`, `node_selector`, `nnd_cluster_name`, `cicdbot_token` 등 |
| 3. OAuth | Gitea OAuth2 App 클라이언트 ID/Secret |
| 4. Harbor | `image_registry`, `harbor_admin_pw` 등 |
| 5. 컴포넌트 관리자 계정 | Gitea/Nexus/ArgoCD/SonarQube admin |
| 6. CICD 봇 서비스 계정 | `cicdbot`, `devopsadmin`, `cicdmanager` |
| 7. 외부 접속 URL | ArgoCD/Tekton/Gitea/Nexus/SonarQube 도메인 |
| 8. 클러스터 내부 서비스 URL | 기본값 유지 권장 |
| 9. 배포 대상 클러스터 | dev/stg/prod × be/fe 클러스터 API |
| 10. NAS 스토리지 | 환경별 NFS 서버 IP·경로 |
| 11. 애플리케이션 도메인 | nip.io 도메인, LB IP, Istio egress 대상 호스트 |
| 12. VM SSH 배포 | VM 호스트 목록, SSH 키 |
| 13. 캐시 노드 | SSH 접속 정보, PEM 파일명 |
| 14. SSL 인증서 | 와일드카드 dev/prod SSL 인증서·키 |

> **자동 채워지는 값** (직접 입력 불필요):
> - `harbor_robot_pw`, `harbor_robot_auth`, `sonar_token` → 메뉴 1 초기화 시
> - `harbor_auth`, `harbor_admin_auth`, `git_cicd_auth` → `(id:pw)` base64 인코딩으로 매 실행 시
>
> **수동으로 채워야 하는 값**:
> - `cicdbot_token` → 메뉴 1 실행 + `kubectl apply 01-1.init-basic.yaml` 후 별도 취득

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

메뉴 번호를 인자로 주면 해당 메뉴로 바로 진입합니다.

```bash
python3 yaml_maker.py 1   # 초기화 바로 실행
python3 yaml_maker.py 2   # 조직추가 바로 실행
```

---

## 메뉴 1: Tekton 초기화 — **최초 1회만 실행**

Tekton/ArgoCD/Harbor/Nexus/Gitea/SonarQube의 계정·저장소를 자동 생성하고, 클러스터 적용용 YAML을 만듭니다.

### 하위 메뉴

| 번호 | 기능 |
|------|------|
| 1 | `tekton_init.toml` 설정값 확인 (20개씩 페이징) |
| 2 | **초기화 실행** |
| 3 | ArgoCD 관리자 비밀번호 일괄 변경 |

### 초기화 실행 시 처리 내용

**A. `01.init/` 템플릿 렌더링** → `result/{project_name}/`에 6개 YAML 분리 저장:

| 파일 | 내용 |
|------|------|
| `01-1.init-basic.yaml` | Tekton 기본 (RBAC, ServiceAccount 등) |
| `01-2.init-pipeline.yaml` | Tekton Catalog 전체 (공통 Task + Pipeline) |
| `01-3.init-oauth.yaml` | OAuth 설정 |
| `01-4.init-argo.yaml` | ArgoCD 설정 |
| `01-5.init-tekton-group-role.yaml` | Tekton 그룹 롤 |
| `01-6.init-cluster.yaml` | 앱 클러스터(dev/stg/prod × be/fe) 초기 namespace/SC/secret |

**B. 외부 컴포넌트 자동 프로비저닝**

- Harbor robot 계정 생성 (Harbor 사용 시)
- Gitea CICD 서비스 계정 생성 (cicdbot, devopsadmin, cicdmanager)
- Nexus 계정 + 저장소 자동 생성 (maven-default / -release / -snapshot / -group, npm-default / -group, raw-default / -group)
- SonarQube 토큰 발급

**C. 결과 저장** → `{project_name}-init_result.json`
(이후 모든 메뉴의 입력 기준값)

### 실행 후 후속 작업

```bash
# 1. 기본 리소스 적용 후 cicdbot token 취득 → init_result.json에 반영
kubectl config use-context {nnd_cluster_name}
kubectl apply -f result/{project_name}/01-1.init-basic.yaml

TOKEN=$(kubectl describe secret cicdbot -n default | grep token: | awk '{print $2}')
sed -i "s/\"cicdbot_token\": \"\"/\"cicdbot_token\": \"$TOKEN\"/" \
  result/{project_name}/{project_name}-init_result.json

# 2. PEM 키 파일을 result/{project_name}/ 폴더에 복사
cp {your_key}.pem result/{project_name}/
chmod 600 result/{project_name}/{your_key}.pem

# 3. 나머지 YAML 순서대로 적용 (ND 클러스터)
kubectl apply -f result/{project_name}/01-2.init-pipeline.yaml
kubectl apply -f result/{project_name}/01-3.init-oauth.yaml
kubectl apply -f result/{project_name}/01-4.init-argo.yaml
kubectl apply -f result/{project_name}/01-5.init-tekton-group-role.yaml

# 4. 앱 클러스터마다 컨텍스트 전환 후 01-6 적용
kubectl config use-context dev-be-cluster
kubectl apply -f result/{project_name}/01-6.init-cluster.yaml
# stg, prod, frontend 클러스터도 동일
```

> Tekton RBAC가 적용된 환경에서는 CoreDNS에 Gitea 도메인 hosts 등록이 필요할 수 있습니다.

---

## 메뉴 2: 조직 추가

새로운 팀/프로젝트 단위의 **조직(네임스페이스)** 을 추가합니다.

### 네임스페이스 명명 규칙

Gitea의 조직명을 기준으로 클러스터별 네임스페이스가 결정됩니다.

> **입력 제약 (조직명·앱명·환경명 공통)**: 소문자·숫자·하이픈(`-`)만 허용. 시작·끝은 소문자/숫자. 최대 53자. RFC 1123 DNS label.

예) Gitea 조직명이 `sample`이면:

| 클러스터 | 네임스페이스 |
|----------|-------------|
| CICD (ND) 클러스터 | `sample-cicd` |
| 개발 (dev) 클러스터 | `sample-dev` |
| 검증 (stg) 클러스터 | `sample-stg` |
| 운영 (prod) 클러스터 | `sample-prod` |

> **사전 조건**: Gitea에 해당 조직이 먼저 생성되어 있어야 합니다.

### 사전 준비 — RBAC 파일 추출

```bash
kubectl get ClusterRoleBinding cicdbot -o yaml > ./02-2.add-organization/rbac.yaml
```

이 파일은 메뉴 2 실행 시 자동으로 정규화(kubectl 메타필드 제거)되고 `subjects`가 `{org}-cicd` 네임스페이스의 `cicdbot` ServiceAccount로 치환됩니다.

### 하위 메뉴

| 번호 | 기능 |
|------|------|
| 1 | 설정값 확인 (캐시 노드 IP 등) |
| 2 | **조직추가 실행** |

### 실행 시 처리 내용

1. Gitea에서 조직 목록 조회 → 선택 (`cicd`가 포함된 조직은 제외)
2. 선택한 조직명을 K8s namespace 규칙으로 검증
3. `02-1.add-storage-in-organization/` → 클러스터별 storage YAML 6개 생성
4. `02-2.add-organization/` → Namespace + RBAC 단일 YAML 생성
5. `result/{project_name}/` 또는 `result/`의 `.pem` 파일 탐색 (앞의 경로 우선)
6. PEM 발견 시 → `cicd_cache_node_ip` 각 노드에 SSH로 `/CICD-DATA/local/{org}-cicd`, `/CICD-DATA/store/{org}-cicd` 폴더 자동 생성
7. **선택**: 자동 적용 — dev 앱 클러스터(`02-1.dev*.yaml`) + ND 클러스터(`02-2.add-organization.yaml`)에 한해 `kubectl apply` 자동 실행

> **주의**: stg/prod 클러스터는 자동 적용 대상에서 빠져 있으므로 수동으로 적용해야 합니다.

### 산출물

```
result/{project_name}/{org}-cicd/
├── 02-1.dev-be-cluster.yaml
├── 02-1.dev-fe-cluster.yaml
├── 02-1.stg-be-cluster.yaml
├── 02-1.stg-fe-cluster.yaml
├── 02-1.prod-be-cluster.yaml
├── 02-1.prod-fe-cluster.yaml
└── 02-2.add-organization.yaml
```

### 수동 적용

```bash
# 각 앱 클러스터에 스토리지 적용
kubectl config use-context dev-be-cluster
kubectl apply -f result/{project_name}/{org}-cicd/02-1.dev-be-cluster.yaml
# stg, prod, frontend 클러스터도 동일

# CICD(ND) 클러스터에 조직 리소스 적용
kubectl config use-context {nnd_cluster_name}
kubectl apply -f result/{project_name}/{org}-cicd/02-2.add-organization.yaml
```

> 사용 완료된 `./02-2.add-organization/rbac.yaml` 파일은 직접 삭제하세요.
> 네이버와 NHN 환경의 RBAC 구조가 다를 수 있으므로, 적용 전 반드시 내용을 확인하세요.

### ⚠️ ClusterRoleBinding `cicdbot` 덮어쓰기 주의

`02-2.add-organization.yaml` 안의 ClusterRoleBinding `cicdbot` 은 **전역 단일 객체** 입니다.
조직마다 새로 생성되는 게 아니라 `subjects` 리스트에 ServiceAccount 가 누적되어야 합니다.

하지만 도구는 매 조직마다 `subjects` 를 **해당 조직 1개로 통째 교체** 한 YAML을 만들어 둡니다.
다음 두 시나리오 모두에서 **기존 조직들의 ClusterRoleBinding subjects 가 모두 사라집니다.**

- 과거에 만든 조직의 `02-2.add-organization.yaml` 을 다시 `kubectl apply` 하는 경우
- 새 조직 추가 시 추출한 `rbac.yaml` 의 subjects 를 그대로 두고 도구가 가공한 결과를 그대로 적용하는 경우

**안전하게 적용하는 방법**

1. 이미 운영 중인 조직이 있다면, `02-2.add-organization.yaml` 의 ClusterRoleBinding `cicdbot` 섹션을
   현재 클러스터의 ClusterRoleBinding 과 머지(기존 subjects + 신규 조직 subject)한 뒤 적용
2. **과거 조직의 `02-2.add-organization.yaml` 은 재적용하지 말 것** (스토리지 `02-1.*` 만 필요 시 재적용)
3. 적용 직전 현재 상태 백업 권장:
   ```bash
   kubectl get ClusterRoleBinding cicdbot -o yaml > cicdbot-crb-backup-$(date +%F).yaml
   ```

---

## 메뉴 3: 앱 파이프라인 생성

앱별 빌드/배포 파이프라인 YAML(EventListener, PipelineRun, TriggerTemplate)을 생성합니다.

### 입력 모드

| 모드 | 설명 |
|------|------|
| 자동선택 | Gitea API로 조직·앱 목록을 가져와 선택 |
| 수동입력 | 조직명·앱명 직접 입력 |

### 파이프라인 유형

| 번호 | 빌드 | 배포 |
|------|------|------|
| 1 | npm-nginx | ArgoCD |
| 2 | maven-spring-boot | ArgoCD |
| 3 | maven-spring + tomcat | ArgoCD |
| 4 | maven-spring | VM SSH |
| 5 | gradle-spring-boot | ArgoCD |
| 6 | gradle-spring + tomcat | ArgoCD |
| 7 | maven-spring-library | Nexus 배포 (배포 클러스터 선택 없음) |

### 추가 입력

- **환경명**: `dev` / `stg` / `prod` (자유 입력, k8s 명명 규칙 적용)
- **브랜치명**: 트리거할 git 브랜치 (예: `dev`, `main`)
- **배포 클러스터**: 목록에서 선택 (유형 4, 7은 제외)

### 실행 후

생성된 YAML을 ND 클러스터에 자동 적용할지 선택할 수 있습니다.

```
result/{project_name}/{org}-cicd/{app}/
└── 03.add-app-in-organization-{app}-{env}.yaml
```

```bash
# 수동 적용 시
kubectl config use-context {nnd_cluster_name}
kubectl apply -f result/{project_name}/{org}-cicd/{app}/03.add-app-in-organization-{app}-{env}.yaml
```

---

## 메뉴 4: 앱 GitOps 저장소 생성

Gitea에 GitOps 저장소와 환경별 소스 저장소를 자동 생성하고, 매니페스트 템플릿을 push 합니다.

### GitOps 유형

| 번호 | 유형 | 트래픽 진입 |
|------|------|-------------|
| 1 | Frontend | Ingress |
| 2 | Frontend | Service (LoadBalancer) |
| 3 | Frontend | Ingress + blue/green (Argo Rollouts) |
| 4 | Frontend | Ingress + canary (Argo Rollouts) |
| 5 | Frontend | Istio ingress gateway |
| 6 | Backend | Ingress |
| 7 | Backend | Service (LoadBalancer) |
| 8 | Backend | Ingress + blue/green (Argo Rollouts) |
| 9 | Backend | Ingress + canary (Argo Rollouts) |
| 10 | Backend | Istio ingress + egress gateway |

**5·10번 (Istio)** — Istio 가 설치된 클러스터 전용입니다.

- Ingress 대신 `Gateway` + `VirtualService` + `DestinationRule` 을 생성합니다. 10번은 여기에
  `ServiceEntry` + egress gateway 라우팅이 추가됩니다. 전 구간 평문 HTTP 입니다.
- 사이드카 주입은 네임스페이스 라벨 `istio-injection: enabled` 로 켜지며,
  `01.init/` 와 `02-1.add-storage-in-organization/` 의 `{env}-{tier}-cluster.yaml` 에 반영되어 있습니다.
- egress 대상은 `tekton_init.toml` 의 `{dev|stg|prod}_egress_hosts` 에 지정합니다. 메시가 기본값
  `ALLOW_ANY` 이면 나열한 호스트만 egress gateway 를 경유하고 나머지는 그대로 나갑니다.

### 처리 내용

1. Gitea에 `{org}-cicd` 조직 생성 (없을 때만)
2. Gitea에 4개 저장소 자동 생성
   - `{app}-gitops` — ArgoCD가 바라보는 GitOps 매니페스트 저장소
   - `{app}-dev` / `{app}-stg` / `{app}-prod` — 환경별 앱 소스 저장소
3. `04.gitea-source/sample-{frontend|backend}-*-gitops/` 템플릿 렌더링
   (`.yaml`, `.yml`, `.j2`, `.tpl` 확장자 지원, `.j2`/`.tpl` suffix는 산출물명에서 제거)
4. `{app}-gitops` 저장소 clone → 렌더된 매니페스트 커밋 → push
5. 로컬 작업 폴더 자동 정리

> 자체서명 인증서 환경을 고려해 `git -c http.sslVerify=false` 와 verify=False fallback이 적용되어 있습니다.

---

## 메뉴 5: 캐시 초기화

CICD 캐시 노드의 특정 조직 폴더를 **삭제 후 재생성**합니다. 빌드 캐시 오염 시 사용합니다.

### 동작 방식

1. 프로젝트 선택 → 조직명 입력 (k8s 명명 규칙 검증)
2. `yes` 정확히 입력해야만 진행 (이중 확인)
3. `result/{project_name}/` 또는 `result/`에서 `.pem` 파일 자동 탐색
4. PEM 있음 → `cicd_cache_node_ip` 각 노드에 SSH로 자동 실행
5. PEM 없음 → 수동 실행 명령어 출력

- 템플릿 렌더에 쓰는 값은 `init_result.json` 을 먼저 읽고, 거기 없는 키만 `tekton_init.toml`
  에서 보충합니다. 그래서 toml 에 키를 추가한 뒤 메뉴 1 을 다시 돌리지 않아도 반영됩니다.
```bash
# 수동 실행 (각 캐시 노드에서)
sudo rm -rf /CICD-DATA/local/{org}-cicd /CICD-DATA/store/{org}-cicd
sudo mkdir -p /CICD-DATA/local/{org}-cicd /CICD-DATA/store/{org}-cicd
```

---

## Task / Pipeline 커스텀

`01-2.init-pipeline.yaml`에는 모든 Task와 Pipeline이 묶여 있습니다. 일부만 수정하려면 해당 부분만 별도 파일로 만들어 적용합니다.

**원본 템플릿 위치**

```
01.init/tekton-catalog/
├── tasks/         (build-1~6 단계별 task, deploy-{vm-ssh,zap}, kubernetes-cli)
└── pipelines/     (build-{maven,gradle,npm}-*, deploy-argocd, deploy-artifact-via-openssh-sftp)
```

**커스텀 절차**

1. 수정할 파일을 복사
2. 파일명과 내부 `metadata.name`을 새 이름으로 변경
3. 필요한 부분(Dockerfile 경로, 이미지, 파라미터 등) 수정
4. 적용

```bash
kubectl apply -f my-sonarqube-scanner-custom.yaml -n tekton-catalog
```

> `metadata.name`을 기본값과 다르게 지정했다면, 이 Task를 참조하는 Pipeline의 `taskRef.name`도 함께 수정해야 합니다.

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
    ├── cicd-key.pem                              ← (사용자가 복사)
    └── sample-cicd/                              ← 조직명
        ├── 02-1.dev-be-cluster.yaml
        ├── 02-1.dev-fe-cluster.yaml
        ├── 02-1.stg-be-cluster.yaml
        ├── 02-1.stg-fe-cluster.yaml
        ├── 02-1.prod-be-cluster.yaml
        ├── 02-1.prod-fe-cluster.yaml
        ├── 02-2.add-organization.yaml
        └── sample-app/                           ← 앱명
            ├── 03.add-app-in-organization-sample-app-dev.yaml
            └── 03.add-app-in-organization-sample-app-prod.yaml
```

---

## 자주 발생하는 문제

### `rbac.yaml` 없음 오류 (메뉴 2)

```bash
kubectl get ClusterRoleBinding cicdbot -o yaml > ./02-2.add-organization/rbac.yaml
```

### 다른 조직의 Tekton 권한이 갑자기 사라짐 (메뉴 2 — 가장 흔한 함정)

ClusterRoleBinding `cicdbot` 은 전역 단일이라, 도구가 만든 `02-2.add-organization.yaml` 을 그대로 적용하면 `subjects` 가 **해당 조직 1개로 덮어써져** 다른 조직 ServiceAccount 가 사라집니다.
**과거 조직의 `02-2.add-organization.yaml` 은 절대 재적용하지 말 것.** 자세한 안전 적용법은 "메뉴 2: 조직 추가 — ClusterRoleBinding `cicdbot` 덮어쓰기 주의" 항목 참고.

### 초기화 파일 없음 오류 (메뉴 2~5)

`result/{project_name}/{project_name}-init_result.json` 이 없는 경우입니다. 메뉴 1 초기화를 먼저 실행하세요.

### ArgoCD 비밀번호 변경 실패 (메뉴 1-3)

ArgoCD ConfigMap이 등록되어 있어야 합니다.

```bash
kubectl get cm argocd-cm -n argocd
```

하위 경로(sub-path) 사용 시 `--grpc-web-root-path argocd` 옵션이 추가로 필요합니다.

### Gitea 접근 불가 (폐쇄망)

Tekton RBAC가 적용된 환경에서는 CoreDNS에 Gitea 호스트를 등록해야 합니다.

```bash
kubectl edit cm coredns -n kube-system
# hosts 블록에 추가:
# {gitea_node_ip}  gitea.{your_domain}
```

### SSH 접속 실패 (메뉴 2, 5 — 캐시 노드 폴더 생성)

PEM 파일이 `result/{project_name}/` 또는 `result/` 에 없는 경우입니다. 자동 생성을 건너뛰니 수동 실행하세요.

```bash
ssh -i {pem_file} {cicd_cache_node_id}@{cicd_cache_node_ip} \
  "sudo mkdir -p /CICD-DATA/local/{org}-cicd /CICD-DATA/store/{org}-cicd"
```

### Git clone 실패 (메뉴 4)

Gitea 접속·인증·레포 존재 여부를 확인하세요. 메뉴 4는 저장소를 먼저 생성하지만, Gitea 연결 오류 시 수동 확인이 필요합니다.

```bash
curl -H "Authorization: Basic {git_cicd_auth}" \
  https://{gitea_domain}/api/v1/orgs
```

### TOML 문법 오류

`tekton_init.toml` 의 따옴표/대괄호/줄바꿈을 확인하세요. 멀티라인 문자열(`\n` 포함 인증서/키)은 큰따옴표로 감싸야 합니다.

---

## 보안 유의사항

- `tekton_init.toml` 은 **git 이 추적하는 파일**이며 저장소에는 플레이스홀더만 들어 있습니다.
  여기에 실제 패스워드·토큰을 채운 뒤 커밋하면 그대로 원격 저장소에 올라갑니다.
  채워 넣기 전에 로컬 변경이 커밋 대상에서 빠지도록 처리하세요.

  ```bash
  git update-index --skip-worktree 00.reset/tekton_init.toml   # 로컬 수정을 git 이 무시
  git update-index --no-skip-worktree 00.reset/tekton_init.toml # 템플릿 자체를 고칠 때 해제
  ```

  이미 값이 채워진 상태로 커밋했다면, 커밋을 되돌리는 것만으로는 부족합니다.
  노출된 토큰·패스워드는 전부 재발급해야 합니다.
- `result/{project_name}-init_result.json` 에도 같은 민감 정보가 들어갑니다.
  `result/` 는 `.gitignore` 에 있어 추적되지 않습니다.
- `.pem` 파일은 SSH 프라이빗 키이므로 권한을 `600` 으로 설정하세요.
  `chmod 600 result/{project_name}/*.pem`
- Harbor, Nexus, Gitea, SonarQube API 호출 시 TLS 검증이 비활성화(`verify=False`)되어 있습니다.
  운영 환경에서는 자체 CA 인증서를 사용하도록 코드를 조정하는 것을 권장합니다.
- 메뉴 4의 `git clone` URL에는 `git_cicd_id:git_cicd_pw` 가 포함되므로, 오류 출력에서 전체 명령이 노출되지 않도록 처리되어 있습니다(요약만 표시).
