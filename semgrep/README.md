# security-rules

CI 파이프라인의 Semgrep 보안점검이 쓰는 규칙 저장소입니다.
행안부 「소프트웨어 보안약점 진단가이드(2021)」 구현단계 49개 항목을 Java 와 Python 소스에서 점검합니다.

| | |
|---|---|
| 현재 버전 | `v0.7.0` |
| 점검 엔진 | Semgrep CE 1.180.0 (폐쇄망, 외부 통신 없음) |
| Java 규칙 | 43개 — MyBatis 매퍼 XML 규칙 2개 포함 |
| Python 규칙 | 40개 — Django · DRF · Flask · FastAPI |
| JavaScript · TypeScript 규칙 | 38개 — Express · Koa · Fastify · NestJS · Next.js (서버), React · Angular · 브라우저 DOM (화면) |
| CVE 규칙 | 1개 (Log4Shell) |
| 행안부 49개 항목 | Java·Python: 탐지 33 · 위치 표시 4 · **수동 점검 9** · 해당 없음 3. JS·TS: 탐지 31 · 위치 표시 4 · 수동 점검 9 · 해당 없음 5 ([항목별 표](#행안부-49개-항목-대응표)) |

> 이 규칙은 **자체 사전 점검용**입니다. 공식 보안약점 진단을 대신하지 않습니다.
> **Semgrep 이 코드만 보고 판단할 수 있는 것만 규칙으로 둡니다.** 인증·권한·업로드 제한처럼 다른 계층(필터·설정·게이트웨이)에 있는지
> 코드 한 함수로는 알 수 없는 항목은 이름으로 추정하지 않고 규칙에서 뺐습니다 — 이 항목들은 수동 점검이 필요합니다.
> 무엇을 잡고 무엇을 놓치는지는 [얼마나 믿을 수 있나](#얼마나-믿을-수-있나)를 먼저 읽어 주세요.

---

## 파이프라인에서 쓰이는 방식

```
규칙 ─▶ Semgrep 검사 ─▶ 결과(SARIF) ─▶ SonarQube 에 함께 등록 ─▶ 품질게이트가 판정
```

규칙은 Semgrep 이미지에 넣어 배포합니다(저장소의 `Dockerfile`). 이미지 태그가 규칙 버전이고, 폐쇄망에는 이미지 하나만 가져가면 됩니다.
이미지에 넣기 전까지는 Task 가 이 저장소의 `main` 을 받아 씁니다 — **그 동안에는 `main` 에 올리는 것이 곧 모든 빌드에 반영**되므로,
회귀시험을 통과한 것만 올립니다.

Semgrep 단계는 **빌드를 막지 않습니다**. 규칙을 받지 못하거나 스캔이 실패하면 로그에 크게 알리고 Semgrep 결과 없이 SonarQube 분석을 계속합니다.
막는 판정은 SonarQube 품질게이트만 합니다.

쓰는 방법은 두 가지입니다.

| 방식 | Tekton Task | 판정하는 곳 |
|---|---|---|
| SonarQube 와 함께 (기본) | `sonarqube-scanner` 의 `semgrep-scan` 단계 | SonarQube 품질게이트. Semgrep 은 검사만 합니다 |
| Semgrep 단독 | `semgrep-security-scan` | 이 저장소의 `scripts/report.py` 가 기준치로 판정합니다 |

SonarQube 화면에서는 규칙 필터 `Semgrep OSS` 로 보이고, 심각도는 아래처럼 바뀝니다.

| 규칙의 gate | Semgrep severity | SonarQube 심각도 |
|---|---|---|
| `block` | ERROR | Critical |
| `warn` | WARNING | Major |

SonarQube 를 MQR 모드로 쓰면 같은 값이 High · Medium 으로 보입니다.

**오탐 처리**는 SonarQube 화면에서 건별로 합니다. 다시 분석해도 유지됩니다.
Semgrep 단독 방식에서는 해당 줄에 `// nosemgrep: <규칙 id>` 주석을 답니다.

---

## 저장소 구성

```
rules/
  mois/                      행안부 항목 규칙. 분류(7개)별 폴더
    01-input-validation/       입력데이터 검증 및 표현
    02-security-features/      보안기능
    03-time-and-state/         시간 및 상태
    04-error-handling/         에러처리
    05-code-errors/            코드오류
    06-encapsulation/          캡슐화
    07-api-misuse/             API 오용
  cve/                       CVE 규칙. 파일 1개 = CVE 1개
fixtures/<규칙 id>/
  vulnerable/                반드시 탐지되어야 하는 예제
  patched/                   탐지되면 안 되는 예제
coverage/
  mois-coverage.csv          Java 항목 현황표
  mois-coverage-python.csv   Python 항목 현황표
  mois-coverage-js.csv       JavaScript · TypeScript 항목 현황표
scripts/
  report.py                  규칙 검사 · 보고서 · 판정
  test.sh                    회귀시험
  expect.py                  예제에 표시한 줄과 탐지 위치 비교 (회귀시험이 씀)
  mutate.py                  가지별 변이 시험 — 규칙의 가지마다 예제가 있는지 확인
docs/
  rule-conventions.md        규칙 작성 규약 (검증으로 인정하는 것, 예제 쓰는 법, Semgrep 함정)
  how-semgrep-works.md       Semgrep 동작 원리
  python-source-block.yaml   Python 규칙 공통 입력 지점 · 공통 검증 블록
  js-source-block.yaml       JavaScript · TypeScript 규칙 공통 입력 지점
```

파일 이름과 규칙 id 는 이렇게 짓습니다.

| 언어 | 파일 | 규칙 id |
|---|---|---|
| Java | `sql-injection-jdbc.yaml` | `mois-1-01-sql-injection-jdbc` |
| Python | `sql-injection-py.yaml` | `mois-1-01-sql-injection-py` |
| JS·TS | `sql-injection-js.yaml` | `mois-1-01-sql-injection-js` (`languages: [javascript, typescript]` — .js .jsx .ts .tsx 모두) |

> 규칙 파일을 다른 폴더로 옮기거나 id 를 바꾸면 SonarQube 는 다른 규칙으로 인식합니다.
> 그동안 해 둔 오탐 처리 이력이 끊기므로, 한번 배포한 규칙의 위치와 id 는 바꾸지 않습니다.

---

## 무엇을 점검하나

### 행안부 49개 항목 대응표

| 표시 | 뜻 |
|---|---|
| 탐지 | 규칙이 있고, 정해진 형태를 잡습니다. 어떤 형태를 잡고 무엇을 놓치는지는 현황표의 `note` 에 있습니다 |
| 위치 표시 | 코드 모양은 정확히 잡지만, 그것이 실제로 문제인지는 사람이 판단해야 하는 항목입니다 (예: `printStackTrace`, 디버그 출력) |
| 수동 점검 | Semgrep 이 코드만 보고 판단할 수 없어 **규칙을 두지 않은** 항목입니다. 이유는 아래 표의 비고에 있습니다 |
| 해당 없음 | C 언어 전용 항목입니다 |

| 번호 | 항목 | Java | Python | JS·TS | 비고 |
|---|---|---|---|---|---|
| | **입력데이터 검증 및 표현** | | | | |
| 1-1 | SQL 삽입 | 탐지 | 탐지 | 탐지 |  |
| 1-2 | 코드삽입 | 탐지 | 탐지 | 탐지 |  |
| 1-3 | 경로 조작 및 자원 삽입 | 탐지 | 탐지 | 탐지 |  |
| 1-4 | 크로스사이트 스크립트 | 탐지 | 탐지 | 탐지 |  |
| 1-5 | 운영체제 명령어 삽입 | 탐지 | 탐지 | 탐지 |  |
| 1-6 | 위험한 형식 파일 업로드 | 수동 점검 | 수동 점검 | 수동 점검 | 업로드 제한(확장자·크기·저장 위치)이 있는지는 다른 함수·설정·폼 검증에 있어 Semgrep 이 판단할 수 없음 |
| 1-7 | 신뢰되지 않는 URL 주소로 자동접속 연결 | 탐지 | 탐지 | 탐지 |  |
| 1-8 | 부적절한 XML 외부개체 참조 | 탐지 | 탐지 | 탐지 |  |
| 1-9 | XML 삽입 | 탐지 | 탐지 | 탐지 |  |
| 1-10 | LDAP 삽입 | 탐지 | 탐지 | 탐지 |  |
| 1-11 | 크로스사이트 요청 위조 | 탐지 | 탐지 | 탐지 |  |
| 1-12 | 서버사이드 요청 위조 | 탐지 | 탐지 | 탐지 |  |
| 1-13 | HTTP 응답분할 | 탐지 | 탐지 | 해당 없음 | JS·TS: Node.js http 가 헤더 값의 CR·LF 를 ERR_INVALID_CHAR 로 거부한다 (Express·Koa·Fastify 의 헤더·쿠키·redirect 모두 해당) |
| 1-14 | 정수형 오버플로우 | 탐지 | 탐지 | 해당 없음 | JS·TS: JS Number 는 넘쳐서 값이 돌아가지 않음(Infinity·정밀도 손실), Buffer write* 는 범위 초과 시 RangeError |
| 1-15 | 보안기능 결정에 사용되는 부적절한 입력값 | 수동 점검 | 수동 점검 | 수동 점검 | 어떤 값이 보안 결정에 쓰이는지는 이름으로만 추정할 수 있음 |
| 1-16 | 메모리 버퍼 오버플로우 | 해당 없음 | 해당 없음 | 해당 없음 | C 언어 전용 |
| 1-17 | 포맷 스트링 삽입 | 탐지 | 탐지 | 탐지 |  |
| | **보안기능** | | | | |
| 2-1 | 적절한 인증 없는 중요기능 허용 | 수동 점검 | 수동 점검 | 수동 점검 | 인증이 필요한 기능인지, 인증이 다른 계층(필터·미들웨어·게이트웨이)에 있는지 판단할 수 없음 |
| 2-2 | 부적절한 인가 | 수동 점검 | 수동 점검 | 수동 점검 | 권한 검사가 필요한지, 다른 계층에 있는지 판단할 수 없음 |
| 2-3 | 중요한 자원에 대한 잘못된 권한 설정 | 탐지 | 탐지 | 탐지 |  |
| 2-4 | 취약한 암호화 알고리즘 사용 | 탐지 | 탐지 | 탐지 |  |
| 2-5 | 암호화되지 않은 중요정보 | 탐지 | 탐지 | 탐지 |  |
| 2-6 | 하드코드된 중요정보 | 탐지 | 탐지 | 탐지 |  |
| 2-7 | 충분하지 않은 키 길이 사용 | 탐지 | 탐지 | 탐지 |  |
| 2-8 | 적절하지 않은 난수 값 사용 | 수동 점검 | 수동 점검 | 수동 점검 | 난수가 보안 용도(토큰·OTP·세션)인지 판단할 수 없음 |
| 2-9 | 취약한 비밀번호 허용 | 수동 점검 | 수동 점검 | 수동 점검 | 비밀번호 정책 검사가 다른 계층(폼·시리얼라이저·설정)에 있는지 판단할 수 없음 |
| 2-10 | 부적절한 전자서명 확인 | 탐지 | 탐지 | 탐지 |  |
| 2-11 | 부적절한 인증서 유효성 검증 | 탐지 | 탐지 | 탐지 |  |
| 2-12 | 사용자 하드디스크에 저장되는 쿠키를 통한 정보 노출 | 탐지 | 탐지 | 탐지 |  |
| 2-13 | 주석문 안에 포함된 시스템 주요정보 | 위치 표시 | 위치 표시 | 위치 표시 |  |
| 2-14 | 솔트 없이 일방향 해쉬 함수 사용 | 수동 점검 | 수동 점검 | 수동 점검 | 해시 대상이 비밀번호인지, 솔트가 다른 곳에서 붙는지 이름으로만 추정할 수 있음 |
| 2-15 | 무결성 검사 없는 코드 다운로드 | 수동 점검 | 수동 점검 | 수동 점검 | 다운로드한 코드의 무결성 검사가 다른 함수에 있는지 판단할 수 없음 |
| 2-16 | 반복된 인증시도 제한 기능 부재 | 수동 점검 | 수동 점검 | 수동 점검 | 인증 시도 제한은 보통 다른 계층(필터·라이브러리·게이트웨이)에 있어 판단할 수 없음 |
| | **시간 및 상태** | | | | |
| 3-1 | 경쟁조건: 검사 시점과 사용 시점(TOCTOU) | 위치 표시 | 위치 표시 | 위치 표시 |  |
| 3-2 | 종료되지 않는 반복문 또는 재귀 함수 | 탐지 | 탐지 | 탐지 |  |
| | **에러처리** | | | | |
| 4-1 | 오류 메시지 정보노출 | 위치 표시 | 위치 표시 | 위치 표시 |  |
| 4-2 | 오류상황 대응 부재 | 탐지 | 탐지 | 탐지 |  |
| 4-3 | 부적절한 예외 처리 | 탐지 | 탐지 | 탐지 |  |
| | **코드오류** | | | | |
| 5-1 | Null Pointer 역참조 | 탐지 | 탐지 | 탐지 |  |
| 5-2 | 부적절한 자원 해제 | 탐지 | 탐지 | 탐지 |  |
| 5-3 | 해제된 자원 사용 | 해당 없음 | 해당 없음 | 해당 없음 | C 언어 전용 |
| 5-4 | 초기화되지 않은 변수 사용 | 해당 없음 | 해당 없음 | 해당 없음 | C 언어 전용 |
| 5-5 | 신뢰할 수 없는 데이터의 역직렬화 | 탐지 | 탐지 | 탐지 |  |
| | **캡슐화** | | | | |
| 6-1 | 잘못된 세션에 의한 데이터 정보 노출 | 탐지 | 탐지 | 탐지 |  |
| 6-2 | 제거되지 않고 남은 디버그 코드 | 위치 표시 | 위치 표시 | 위치 표시 |  |
| 6-3 | Public 메소드부터 반환된 Private 배열 | 탐지 | 탐지 | 탐지 |  |
| 6-4 | Private 배열에 Public 데이터 할당 | 탐지 | 탐지 | 탐지 |  |
| | **API 오용** | | | | |
| 7-1 | DNS lookup에 의존한 보안결정 | 탐지 | 탐지 | 탐지 |  |
| 7-2 | 취약한 API 사용 | 탐지 | 탐지 | 탐지 |  |

현황표(규칙 id, 잡는 형태, 놓치는 형태): Java [`coverage/mois-coverage.csv`](coverage/mois-coverage.csv), Python [`coverage/mois-coverage-python.csv`](coverage/mois-coverage-python.csv), JS·TS [`coverage/mois-coverage-js.csv`](coverage/mois-coverage-js.csv)

**`v0.6.1` 에서 뺀 규칙.** 위 표의 "수동 점검" 9개 항목은 `v0.6.0` 까지 함수·변수 이름이나 "검사 흔적이 없다"는 추정으로 탐지했습니다.
실제 프로젝트에서 대부분 오탐이었고(검사가 필터·미들웨어·설정에 있음), 이름이 다르면 놓쳐서 결과를 믿을 수 없었습니다.
2-5 는 평문 **전송**(`http://` 상수 URL, TLS 없는 SMTP·FTP·Telnet)만 남기고, 값이 중요정보인지 이름으로 추정하던 평문 **저장**은 뺐습니다.
Python 의 "대상이 DB 인지 알 수 없는 `execute()`", "알 수 없는 호출의 `verify=False`" 규칙도 같은 이유로 뺐습니다.

### 규칙이 막는 것과 알리기만 하는 것

| gate | 기준 | 규칙 수 |
|---|---|---|
| `block` | 외부 입력이 위험한 곳까지 흘러가는 경우, 또는 확실히 안전하지 않은 설정 | Java 14 · Python 13 · CVE 1 |
| `warn` | 입력의 흐름을 끝까지 확인하지 못하는 경우, 코드 모양은 확실하지만 문제인지는 사람이 판단해야 하는 경우 | Java 29 · Python 27 |

`v0.6.0` 에서 아래 규칙을 `block` 에서 `warn` 으로 내렸습니다. 입력의 흐름을 끝까지 확인하지 못하거나, 최신 실행 환경이 스스로 막는 항목입니다.
MyBatis `${}`(2개), 포맷 스트링(Java · Python), HTTP 응답분할(Java), XXE(Java · Python).

### 외부 입력으로 보는 것

흐름을 추적하는 규칙은 아래 값을 외부 입력으로 봅니다.

**Java**

- Servlet 요청 값: 파라미터, 파라미터 이름, 헤더, 헤더 이름, 쿠키, 본문
- Spring 핸들러 매개변수: `@RequestParam` · `@PathVariable` · `@RequestHeader` · `@CookieValue` · `@RequestBody` · `@ModelAttribute` · `@MatrixVariable`
- 애너테이션이 없거나 검증 애너테이션(`@Valid` · `@NotBlank` 등)만 붙은 Spring 핸들러 매개변수 (`public String list(String keyword)` 같은 형태).
  직접 만든 애너테이션(`@CurrentUser` 등)이 붙은 매개변수는 입력으로 보지 않습니다
- Spring 멀티파트 · `WebRequest`, cos `MultipartRequest`, 업로드 파일의 원본 이름

숫자 · 날짜형 매개변수와, 프레임워크가 넣어 주는 객체(요청 · 응답 · 세션 · 모델)는 제외합니다.

**Python**

- 요청 객체의 값: Django `GET` · `POST` · `COOKIES` · `FILES` · `body` · `META`, DRF `data` · `query_params`, Flask `args` · `form` · `json` · `referrer` · `environ`,
  FastAPI·Starlette `query_params` · `path_params` · `headers`, WebSocket 수신 값. 객체 이름이 `request` · `req` · `self.request` 이거나,
  `flask.request`(별칭 import 포함)이거나, 타입이 `Request` · `WebSocket` 으로 적힌 매개변수
- 라우트 함수 매개변수: `@app.get(...)`, `@app.route(...)` 아래 함수의 인자. Django 뷰의 URL 인자(`def view(request, slug)`, `self.kwargs`)
- `Query()` · `Header()` · `Form()` · `Body()` 등으로 요청 값이라고 선언한 매개변수 (의존성 함수 포함)

제외하는 것: 문자열을 실을 수 없는 숫자 · 날짜형(`int | str` 처럼 문자열이 섞이면 입력), 프레임워크 객체, `Depends(...)` 로 주입받는 객체
(단 `str` 토큰과 OAuth2 폼 · 자격증명은 입력), Django ORM 조회 결과(`Model.objects.get(pk=입력)` — DB 에 저장된 값).
타입 이름이 `…Config` · `…Client` 라는 것만으로는 제외하지 않습니다 (요청 본문 모델일 수 있습니다).

**JavaScript · TypeScript**

- 서버 요청 값: Express · Fastify · Next.js API 의 `req` · `request`(`query` · `body` · `params` · `cookies` · `headers` · `get()` …),
  구조분해한 핸들러 매개변수(`({ query, body }, res) => …`), Koa `ctx`(`ctx.query` · `ctx.request.body` …), NestJS `@Query` · `@Body` · `@Param` · `@Headers` 매개변수
  (`ParseIntPipe` 등 숫자 변환 파이프는 제외)
- 브라우저 입력: `location` · `document.URL` · `document.referrer` · `window.name`, `postMessage` 의 `event.data`,
  React Router `useParams()` · `useSearchParams()` · `useLocation()`, Next.js `useRouter().query`, Angular `route.snapshot.queryParams` 등
- 공통 블록: [`docs/js-source-block.yaml`](docs/js-source-block.yaml)

### 검증으로 인정하는 것

"검증 함수를 불렀다"는 것만으로는 안전하다고 보지 않습니다. 아래처럼 **결과를 실제로 쓰는 형태**만 인정합니다.

```python
if host not in ALLOWED_HOSTS:      # 실패하면 빠져나간다 → 이 뒤의 host 는 검증된 값
    return HttpResponseBadRequest()
if host in ALLOWED_HOSTS:          # 통과한 if 안에서만 쓴다
    ping(host)
```

결과를 버리는 검사, 실패해도 계속 진행하는 검사, 검사 뒤에 다시 대입하거나 덧붙인 값(한 단계 안쪽 블록까지), `and` · `&` 로 다른 조건에 묶인 검사,
`not (…)` · `== False` 로 뒤집은 검사, `else` 가 붙은 검사는 탐지됩니다. 빠져나가는 호출은 `return` · `raise` · `flask.abort` · `sys.exit` 만 인정합니다.
허용 목록은 모듈 수준에 문자열 · 숫자 리터럴로 적혀 있고 그 함수에서 바뀌지 않는 것만 인정합니다. 자세한 기준은 [`docs/rule-conventions.md`](docs/rule-conventions.md) 에 있습니다.

---

## 얼마나 믿을 수 있나

### 검증 결과

**Java — OWASP Benchmark v1.2** (정답이 정해진 테스트 중 대응 규칙이 있는 8개 범주, 2,054건)

| 범주 | 탐지율 | 오탐률 |
|---|---|---|
| SQL 삽입 | 93.8% | 69.0% |
| 명령어 삽입 | 91.3% | 68.0% |
| 경로 조작 | 88.7% | 72.6% |
| XSS | 89.4% | 58.9% |
| LDAP 삽입 | 88.9% | 56.2% |
| XPath 삽입 | 93.3% | 75.0% |
| 취약한 암호 알고리즘 | 100% | 23.3% |
| 취약한 해시 | 69.0% | 0% |
| **합계** | **89.5%** | **53.9%** |

`v0.6.0` 까지는 "적절하지 않은 난수"(탐지율 100%, 오탐률 0%)를 더해 9개 범주 91.3% / 42.0% 였습니다. 난수 규칙은 용도를 판단할 수 없어 뺐고, 나머지 범주의 수치는 그대로입니다.
Benchmark 전용 클래스 이름에 맞춘 규칙은 두지 않았습니다. 이 수치는 **규칙을 고치면서 계속 본 자료**의 수치라, 처음 보는 코드에서의 성능은 아래 독립 프로젝트 결과가 더 정확합니다.

**독립 프로젝트 — 규칙 개발에 쓰지 않은 8개** (`block` 탐지를 전부 코드와 대조해 판정)

| 프로젝트 | 성격 | 처음 측정 (`v0.5.0`) 정탐 / 오탐 | `v0.6.1` 정탐 / 오탐 |
|---|---|---|---|
| WebGoat | Java 취약 앱 | 9 / 1 | 10 / 0 |
| 전자정부 표준프레임워크 공통컴포넌트 | Java 공공 SI 형태, 2,469개 파일 | 0 / 13 | 0 / 7 |
| spring-boot-realworld (MyBatis) | Java 깨끗한 코드 | - | - |
| Vulnerable-Flask-App | Python 취약 앱 | 4 / 0 | 4 / 0 |
| django.nV | Python 취약 앱 | 2 / 0 | 2 / 0 |
| microblog (Flask) | Python 깨끗한 코드 | 0 / 1 | 1 / 0 |
| djangoproject.com | Python 깨끗한 코드 | 0 / 4 | 0 / 3 |
| fastapi-realworld | Python 깨끗한 코드 | - | - |
| **합계** | | **15 / 19** | **17 / 10** |

- 처음 측정만 독립 수치입니다. `v0.6.1` 은 같은 프로젝트를 보며 일반적인 수정(전자정부 보안 유틸 인정, 직접 만든 애너테이션 제외, Django ORM 조회 결과 제외 등)을 한 결과입니다.
- microblog 1건은 처음에 오탐으로 봤던 `urlsplit(next).netloc != ''` 검사입니다. `///evil.com` · `\\evil.com` 이 통과하는 우회가 있어 정탐으로 바꿨습니다.
- 남은 오탐 10건은 모두 아래 "알려진 한계"의 첫 세 항목에 해당합니다 (서비스·DAO 호출 결과, 자기 호스트 리다이렉트, URL 조립).
- 스캔 오류 · 시간 초과: 11개 프로젝트에서 0건입니다 (전자정부의 MyBatis XML 파싱 오류 50건 제외 — 아래 한계 참고). 전자정부 2,469개 파일 스캔은 65초(병렬 4)입니다.

**예제(fixture)로 확인하는 것**

- 예제 파일 555개에 "이 줄이 탐지되어야 한다"는 표시가 3,000곳 넘게 있고, 회귀시험은 표시한 줄과 실제 탐지 위치가 **정확히 같은지** 봅니다.
- `patched` 예제는 자기 규칙뿐 아니라 **모든 규칙**에서 0건이어야 합니다.
- 규칙의 가지 · 제외 조건 · 정규식의 낱말을 하나씩 지워 보고 예제 결과가 달라지는지 확인합니다(`scripts/mutate.py`). 84개 규칙 모두 "지워도 결과가 그대로인 조각"이 0개입니다.
- 검증 조건(sanitizer)은 "통과시키지만 여전히 위험한 코드"를 일부러 만들어 보는 적대적 감사를 Java · Python · 입력 지점별로 따로 거쳤습니다.
  찾은 우회는 고치고 예제로 남겼습니다.

**JavaScript · TypeScript — 실제 프로젝트 6개** (`block` 탐지를 전부 코드와 대조해 판정, 규칙 개발과 같은 시기에 본 자료라 독립 수치는 아님)

| 프로젝트 | 성격 | block 정탐 / 오탐 |
|---|---|---|
| OWASP Juice Shop | TS · Express · Angular 취약 앱 | 19 / 4 |
| OWASP NodeGoat | Express 취약 앱 | 5 / 0 |
| DVNA | Express 취약 앱 | 4 / 0 |
| node-express-realworld | Express 깨끗한 코드 | 0 / 0 |
| react-redux-realworld | React 깨끗한 코드 | 0 / 0 |
| react-template (사내 Spring + React 템플릿) | React 깨끗한 코드 | 0 / 0 |

Juice Shop 오탐 4건은 모두 다른 함수에서 검증하거나(파일 이름 대조) 서버 데이터로 만든 경로입니다. 정탐에는 `file.includes('/')` 처럼 약한 검사만 거친 경로 4건이 들어 있습니다.
스캔 오류는 일부러 잘라 둔 코드 조각 파일의 구문 오류와, 저장소에 함께 들어 있는 큰 외부 라이브러리 파일(`three.js`, 850KB)에서 난 규칙 3개의 시간 초과뿐입니다.
시간 초과는 그 파일의 그 규칙 결과만 빠지고 빌드에는 영향이 없습니다.

**그 밖의 샘플**

| 샘플 | 결과 |
|---|---|
| java-sec-code (Spring 취약 예제) | 취약 컨트롤러 13개 중 12개에서 해당 항목 탐지. MyBatis `${}` 3건 모두 탐지(warn) |
| PyGoat (Django 취약 앱) | SQL 삽입 · 명령어 삽입 · 코드 삽입 · 역직렬화 · SSRF · 경로 조작 · 리다이렉트 탐지 |
| vulpy (Flask), dvpwa (aiohttp) | 막는 규칙 탐지 0건. SQL 실행이 다른 함수 · 다른 계층에 있습니다 |
| FastAPI 공식 템플릿 (깨끗한 코드) | 막는 규칙 1건 (오탐) |

### 알려진 한계

- **함수를 넘는 흐름은 추적하지 못합니다.** 입력을 받은 함수 안에서 위험한 호출까지 이어져야 잡습니다.
  컨트롤러에서 받은 값을 서비스 · DAO 로 넘겨 거기서 SQL 을 만드는 코드는 놓칩니다. Semgrep 무료판의 한계입니다.
- **서비스 · DAO 호출 결과도 입력으로 봅니다.** 입력을 인자로 받은 호출의 결과는 그대로 외부 입력으로 취급합니다(Django ORM 조회는 제외).
  DB 에서 읽은 저장 경로로 파일을 여는 코드, 인증 서비스가 만든 주소로 보내는 리다이렉트가 오탐으로 나옵니다.
  이 근사를 끄면 헬퍼 함수를 거치는 실제 취약점을 놓치므로 유지합니다.
- **자기 호스트로의 리다이렉트, 고정 경로를 조립한 URL 을 구분하지 못합니다.** 요청의 서버 이름으로 http ↔ https 를 바꾸는 필터,
  `reverse()` 결과에 `url += "?q=" + q` 를 덧붙인 코드가 오탐으로 나옵니다.
- **문자열 자르기에서 흐름이 끊깁니다(Python).** `name[1:]` 처럼 슬라이스를 거친 값은 Semgrep 엔진이 추적하지 못해 놓칩니다 (`name[0]` 은 추적).
- **검사 뒤 두 단계 이상 안쪽 블록에서 다시 대입한 값은 놓칩니다.** 한 단계 안쪽(if · for · try 등)까지는 탐지합니다.
- **화면 템플릿은 보지 않습니다.** JSP, Django · Jinja 템플릿 파일 안의 출력(XSS)은 대상이 아닙니다.
- **JavaScript · TypeScript 규칙은 없습니다.**
- **`warn` 탐지는 전수 판정하지 않았습니다.** 독립 프로젝트 8개에서 293건(전자정부 2,469개 파일에서 97건)이 나왔고, 건수가 많은 것은 광범위한 예외 처리, 하드코딩된 비밀번호, 디버그 출력입니다.
- **XML 의 `<![CDATA[ … ]]>` 가 든 MyBatis 매퍼는 Semgrep 이 파싱 오류로 보고합니다.** 그 파일의 `${}` 탐지 자체는 되고, 파이프라인은 오류가 있어도 결과를 SonarQube 로 보냅니다.
- **JS · TS: 화면 템플릿 파일(EJS `<%-`, Pug `!{}`, Vue `v-html`, Angular 템플릿)과 `node:fs` 처럼 `node:` 접두로 가져온 모듈은 보지 못합니다.**
  React 는 기본으로 출력을 이스케이프하므로 화면 쪽은 `dangerouslySetInnerHTML` · `innerHTML` · URL 속성 같은 명시적인 위험 지점만 봅니다.
- **설정 파일에서만 정하는 값은 모릅니다.** 암호 · 해시 알고리즘을 properties 에서 읽으면, 소스에 적힌 기본값만 봅니다.

---

## 직접 돌려 보기

Docker 만 있으면 됩니다. 네트워크는 쓰지 않습니다.

**내 소스 점검**

```bash
docker run --rm --network none \
  -v "$PWD":/semgrep-rules:ro -v /path/to/source:/src:ro -w /src \
  semgrep/semgrep:1.180.0 \
  semgrep scan --config /semgrep-rules/rules --metrics=off --disable-version-check .
```

**회귀시험** (규칙을 고쳤으면 반드시)

```bash
docker run --rm --network none -v "$PWD":/src:ro -w /src \
  semgrep/semgrep:1.180.0 bash scripts/test.sh
```

끝에 `전체 통과` 가 나와야 합니다. 20분 안팎 걸립니다. 확인하는 것은 네 가지입니다.

1. 모든 규칙에 필수 메타데이터가 있는지
2. 규칙마다 예제에 표시한 줄과 탐지 위치가 정확히 같은지, `patched` 예제는 0건인지
3. 모든 `patched` 예제가 모든 규칙에서 0건인지
4. 파이프라인 흐름(사전 검사 → 스캔 → 보고서)과 판정 시나리오

**가지별 변이 시험** (규칙의 가지 · 제외 조건 · 정규식을 고쳤으면)

```bash
docker run --rm --network none -v "$PWD":/src:ro -w /src \
  semgrep/semgrep:1.180.0 python3 scripts/mutate.py <규칙 id>
```

`기준 일치, 살아남은 변이 0개` 가 나와야 합니다. 규칙의 조각을 하나씩 지운 규칙으로 예제를 다시 돌려, 결과가 그대로인 조각(예제가 없거나 중복이거나 죽은 조각)을 찾습니다.
인자 없이 돌리면 전체 규칙을 보며 1시간 넘게 걸립니다.

폐쇄망에서는 `semgrep/semgrep:1.180.0` 대신 내부 레지스트리에 올린 같은 이미지를 씁니다
(`sha256:dffc9caeecc924370d30f9187b6edf10949600d3ef5f69ef5c359074d8fc7d2d`).

---

## 규칙을 추가하거나 고칠 때

### 순서

1. `rules/mois/<분류>/` 에 규칙 파일을 만들거나 고칩니다.
2. `fixtures/<규칙 id>/vulnerable/` 과 `patched/` 에 예제를 둡니다. 탐지되어야 하는 줄 바로 위에 `ruleid: <규칙 id>` 주석을 답니다.
3. 회귀시험과 그 규칙의 가지별 변이 시험을 통과시킵니다.
4. 현황표(`coverage/*.csv`)의 `rule_ids` 와 `note` 를 맞춥니다.
5. 커밋하고 **새 태그**를 붙여 올립니다. 태그는 회귀시험을 통과한 커밋에만 붙입니다.
6. 새 태그로 Semgrep 이미지를 다시 만들어 올리고(`Dockerfile`), Tekton Task `sonarqube-scanner` 의 `SEMGREP_IMAGE` 를 바꿉니다.

### 메타데이터 (필수)

```yaml
metadata:
  rule-type: mois
  mois-guide: "2021 소프트웨어 보안약점 진단가이드"
  mois-category: "입력데이터 검증 및 표현"
  mois-item-no: "1-1"
  mois-item: "SQL 삽입"
  cwe: "CWE-89"
  gate: block          # block 이면 severity: ERROR, warn 이면 severity: WARNING
```

메시지는 `"[행안부 <분류>] <항목>: <무엇이 문제인지> — <어떻게 고칠지>"` 형식으로 씁니다.
SonarQube 에는 메시지만 보이므로 조치 방법까지 적습니다.

### 지킬 것

자세한 기준과 틀은 [`docs/rule-conventions.md`](docs/rule-conventions.md) 에 있습니다. 규칙을 고치기 전에 먼저 읽습니다.

- **검증은 guard 형태로만 인정합니다.** "검증 함수가 불렸다"로 안전 처리하지 않습니다. 규약 문서의 틀을 그대로 씁니다.
- **가지마다 예제를 둡니다.** `pattern-either` 의 가지, 제외 조건, 정규식의 낱말 하나하나에 그것만이 결정하는 예제 줄이 있어야 합니다.
- **본문의 글자로 제외하지 않습니다.** `pattern-not-regex` 로 낱말을 찾으면 주석 · 메시지 문자열에도 반응해 탐지가 사라집니다. 코드 구조로 찾습니다.
- **예제는 규칙마다 반드시 둡니다.** 패키지 이름을 잘못 적은 규칙은 오류 없이 0건이 됩니다. `vulnerable` 예제가 그걸 잡아 줍니다.
- **`patched` 예제는 다른 규칙에도 걸리지 않게 씁니다.**
- **위험한 인자만 봅니다.** `focus-metavariable` 로 좁혀서, 바인딩 변수로 안전하게 넘긴 값은 탐지하지 않게 합니다.
- **입력 지점은 공통 블록을 그대로 씁니다.** Java 는 기존 흐름 추적 규칙의 `pattern-sources` 를,
  Python 은 [`docs/python-source-block.yaml`](docs/python-source-block.yaml) 을 복사합니다. 고칠 때는 모든 규칙에 같이 반영합니다.
- **Python 1-14(정수형 오버플로우)는 입력 지점이 다릅니다.** 정수형 매개변수를 더 봅니다.
- **Semgrep 이 판단할 수 없는 것은 규칙으로 만들지 않습니다.** 함수 · 변수 이름이나 "검사 흔적이 없다"로 추정하는 규칙은 두지 않습니다.

### Semgrep 에서 자주 틀리는 것

- **`metavariable-regex` 는 문자열 맨 앞부터 맞춥니다.** 이름 중간을 찾으려면 `.*` 로 시작하고, 전체 일치는 `^…$` 로 씁니다.
- **한 `patterns` 블록에서 일부 가지에만 있는 메타변수에 정규식을 걸면 나머지 가지가 조용히 무효가 됩니다.** 가지별로 항목을 나눕니다.
- **`java.lang` 클래스는 짧은 이름과 전체 이름을 모두 적습니다.** `(java.lang.Runtime $R)` 은 `Runtime r = …` 선언에 맞지 않습니다.
- **수신 객체의 타입을 모를 수 있습니다.** `getJdbcTemplate().query(sql)` 같은 호출을 위해,
  그 API 에만 있는 메서드 이름(`prepareStatement`)이나 이름 규칙(`…jdbcTemplate…`)으로 잡는 항목을 함께 둡니다.
- **컬렉션은 통째로 오염됩니다.** `add` · `put` 한 값은 컬렉션 전체를 외부 입력으로 만들고, 요소 단위로는 구분하지 못합니다.
- 그 밖에 실제로 걸렸던 함정 20여 가지를 [`docs/rule-conventions.md`](docs/rule-conventions.md) 4절에 모아 두었습니다.

---

## CVE 규칙

`rules/cve/` 의 규칙은 소스가 아니라 **의존성 목록 파일**을 읽습니다. 파일이 없으면 경고 없이 0건이 됩니다.

| 생태계 | 읽는 파일 | 비고 |
|---|---|---|
| Maven | `maven_dep_tree.txt`, `gradle.lockfile` | `pom.xml` 은 읽지 않습니다. 빌드에서 `mvn dependency:tree -DoutputFile=maven_dep_tree.txt` 로 만듭니다 |
| npm | `package-lock.json`, `yarn.lock`, `pnpm-lock.yaml` | 미확인 |
| PyPI | `*requirement*.txt`, `poetry.lock`, `Pipfile.lock`, `uv.lock` | 미확인 |
| Go | `go.mod` | 미확인 |

CVE 규칙의 필수 메타데이터는 `cve`, `cvss`, `severity-label`, `fixed-version`, `references`, `gate` 입니다.
영향 버전과 조치 버전은 NVD · GHSA 원문을 근거로 적고 `references` 에 남깁니다.

의존성 취약점 전반은 파이프라인의 Trivy 가 봅니다. 여기 CVE 규칙은 "취약한 버전을 쓰면서 실제로 그 기능을 호출하는지"까지 보려는 경우에만 추가합니다.

---

## 버전 이력

| 태그 | 내용 |
|---|---|
| `v0.7.0` | JavaScript · TypeScript 규칙 38개 추가 (Node.js 서버 · React · Angular · 브라우저), 행안부 49개 항목 표에 JS·TS 열 |
| `v0.6.2` | Codex 4차 검토 반영: Java 허용 목록 Map 을 메서드 참조·다른 호출 인자로 채우면 불인정, Python 이스케이프 결과를 변수에 담아 href·script 등에 넣으면 탐지 |
| `v0.6.1` | Semgrep 이 판단할 수 없는 추정 규칙 22개 삭제(9개 항목 → 수동 점검). 적대적 감사로 찾은 검증 조건 우회 수정(Java · Python), 입력 지점 확대(Django URL 인자, FastAPI 의존성 토큰 · 폼, WebSocket 등), Django ORM 조회 결과 제외. 규칙을 넣은 이미지용 `Dockerfile` |
| `v0.6.0` | 검증을 guard 형태로만 인정, 규칙 7개를 warn 으로 조정, 가지별 예제와 변이 시험, 독립 프로젝트 8개 검증, 전자정부 보안 유틸 인정, Python 규칙 2개 추가. 일부 규칙은 탐지 줄 위치가 바뀜 |
| `v0.5.0` | Java 탐지 범위 확대. OWASP Benchmark 탐지율 39% → 91% |
| `v0.4.0` | Python 규칙 49개, MyBatis 규칙 2개 추가 |
| `v0.3.0` | Java 규칙을 49개 항목 전체로 확대 |
| `v0.2.0` | Java 규칙 7개 추가, 항목 현황표 |
| `v0.1.0` | 저장소 골격, 보고서 스크립트 |

## 참고

- 항목 번호 · 분류 · 항목명: KISA 「소프트웨어 보안약점 진단가이드(2021)」 제4장 구현단계 목차.
  원문 5-5(역직렬화)의 CWE-918 은 오기로 보여 CWE-502 로 적었습니다.
- Semgrep 이 파일을 고르고 패턴 · 흐름을 맞추는 방식: [`docs/how-semgrep-works.md`](docs/how-semgrep-works.md)
