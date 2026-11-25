# Semgrep 동작 원리

Tekton Task `semgrep-security-scan` 이 소스코드를 점검하는 방식을 정리한다.
예시 수치는 2026-10-15 spring-petclinic 실행(`spring-petclinic-dev-semgrep-build-pr-c5zvt`) 결과다.

## 한눈에 보기

```
규칙(YAML) ──┐
             ├─▶ ① 대상 고르기 ─▶ ② 코드를 구문 트리로 ─▶ ③ 패턴·taint 매칭 ─┐
소스 코드 ───┘                                                              ├─▶ JSON ─▶ ⑤ report.py 판정
의존성 파일 ───────────────▶ ④ 버전 비교 + 도달성 확인 ─────────────────────┘
```

Task step 과의 관계:

| step | 하는 일 |
|---|---|
| preflight | 규칙 저장소를 태그로 받아 임시 볼륨에 둔 뒤 입력값·규칙 메타데이터·의존성 파일을 검사 |
| scan | `semgrep scan` 실행 — 아래 ①~④ |
| report | 결과 JSON 을 판정 — 아래 ⑤ |

## ① 점검할 파일 고르기

- git 저장소면 git 이 추적하는 파일과, 무시되지 않은 새 파일만 본다. petclinic 은 101개.
- 저장소에 `.semgrepignore` 가 없으면 기본 제외 목록(`test/`, `tests/`, `build/`, `node_modules/` 등)을 쓴다.
  petclinic 은 테스트 코드 19개가 여기서 빠졌다.
- 규칙의 `languages` 에 맞는 파일만 남긴다. Java 규칙이므로 `.java` 30개 + 의존성 파일 1개 = 31개.

## ② 코드를 구문 트리로 바꾼다 (정규식이 아님)

- 언어별 파서로 코드를 구문 트리(AST)로 바꾸고, 여러 언어를 같은 형태(공통 AST)로 맞춘다.
  `semgrep` 명령은 Python 이고, 실제 파싱·매칭은 `semgrep-core`(OCaml) 엔진이 한다.
- 그래서 공백·줄바꿈·주석·괄호 모양이 달라도 같은 코드로 본다. grep 과 가장 큰 차이다.
- 파싱하지 못한 파일은 결과의 `errors` 에 남는다. report 는 이를 실패로 처리한다 (조용히 빠지는 것을 막기 위해).

## ③-a 패턴 매칭

규칙의 패턴도 같은 언어의 코드 조각으로 쓰고, 똑같이 트리로 바꿔 구조를 비교한다.

| 문법 | 뜻 |
|---|---|
| `$X` (메타변수) | 아무 식이나 받는다. 같은 이름은 같은 값이어야 한다 |
| `...` | 아무 인자·문장이 와도 된다 |
| `(java.sql.Statement $S).executeQuery($Q)` | 타입 지정. import 와 선언을 보고 `$S` 가 실제로 그 타입일 때만 맞는다 |
| `metavariable-regex` | 메타변수가 받은 값을 정규식으로 한 번 더 거른다 |

예: CVE 규칙의 도달성 패턴은 `(org.apache.logging.log4j.Logger $LOG).$METHOD(...)` 에
메서드 이름이 `trace|debug|info|warn|error|fatal|log|printf` 인 경우만 남긴다.

## ③-b taint 모드 (SQL 삽입 규칙)

"오염된 외부 입력이 위험한 함수까지 흘러가는가" 를 데이터 흐름으로 본다.

| 구분 | 규칙에서 |
|---|---|
| source (오염 시작) | Servlet 요청 값(`request.getParameter(...)`·헤더·쿠키·본문)과 Spring MVC 바인딩 파라미터(`@RequestParam`·`@PathVariable`·`@RequestBody` 등, 숫자형 제외). 모든 taint 규칙이 같은 블록을 쓴다 |
| sink (위험한 곳) | `Statement.executeQuery/executeUpdate/execute(쿼리)`, `Connection.prepareStatement(쿼리)` — 위험한 인자만 `focus-metavariable` 로 지정 |
| sanitizer (오염 해제) | `Integer.parseInt(...)` |

함수 안에서 변수 대입·문자열 결합을 따라 오염 표시를 옮긴다.

```java
String name = request.getParameter("name");                // 오염
stmt.executeQuery("... '" + name + "'");                    // 오염이 sink 인자까지 → 탐지
int id = Integer.parseInt(request.getParameter("id"));      // sanitizer 통과 → 깨끗
conn.prepareStatement("... = ?"); ps.setString(1, name);    // sink 인자는 상수 → 미탐지
```

- fixture 실측: 취약 3건 탐지, 안전 2건 미탐지.
- 한계: CE 는 함수 안의 흐름만 따라간다. Controller → Service → DAO 처럼 함수·파일을 넘나드는 흐름은
  Pro 기능이라 놓칠 수 있다 (작업 지시서 R4). coverage 표에 "부분" 으로 적는 이유다.

## ④ CVE(공급망) 규칙 — `r2c-internal-project-depends-on`

1. **의존성 파일 해석**: 빌드에서 만든 `maven_dep_tree.txt` 를 읽어 패키지·버전 171개를 얻었다.
   `pom.xml`·`build.gradle` 은 빌드 도구로 의존성을 계산해야 해서 읽지 않는다.
   scan 로그의 `build.gradle  Disabled (use --allow-local-builds)` 가 그 뜻이다 (폐쇄망 Task 에서는 쓰지 않음).
2. **버전 비교**: 규칙의 범위(예: `>= 2.13.0, < 2.15.0`)와 생태계별 버전 규칙(Maven 은 Maven 규칙)으로 비교한다.
   범위가 여러 개면 `depends-on-either` 로 나열한다.
3. **도달성 확인**: 취약 버전이면 규칙의 코드 패턴을 찾는다.
   - 호출이 있으면 그 호출 위치에 `reachable=Y`
   - 없으면 의존성 파일 위치에 `reachable=N`

의존성 파일이 없으면 규칙이 점검할 대상 자체가 없어 **경고 없이 0건**이 된다.
그래서 report 가 `[3] 경고` 에 "의존성 파일 미발견" 을 따로 출력한다.
패키지 이름을 잘못 써도 오류 없이 0건이 되므로, 규칙마다 반드시 탐지되는 `vulnerable` fixture 가 필요하다.

## ⑤ 결과와 판정

- semgrep 은 JSON 만 낸다: 탐지 목록(규칙 id, 위치, metadata, 도달 여부), `errors`, 스캔한 파일 목록.
  통과·실패 판단은 하지 않게 했다 (`--error` 미사용) — 그래야 report 가 항상 실행된다.
- 판정은 `scripts/report.py`:
  1. 규칙 metadata(`rule-type`, `gate`, `severity-label`)로 행안부/CVE 를 나눈다.
  2. 기준치(`MAX_*`)와 비교한다. `-1` 은 무제한(보고만).
  3. 로그 보고서, Task results 5개(`mois-findings`, `cve-findings`, `cve-reachable`, `gate`, `ruleset-version`),
     종료코드(기준치 초과 또는 semgrep 오류면 1)를 낸다.

## 꼭 기억할 점

semgrep 은 **규칙에 적힌 것만** 찾는다. 폐쇄망이라 공개 규칙(Registry)을 쓰지 않으므로,
점검 범위는 이 저장소에 있는 규칙이 전부다. 탐지 0건은 "안전하다" 가 아니라
"현재 규칙 기준으로 0건" 이라는 뜻이다. 보고서의 "규칙 N개 적용" 을 함께 볼 것.

## 실행 로그 예 (scan step)

```
+ timeout 900 semgrep scan --config /semgrep-rules/rules --metrics=off --disable-version-check --json -o /semgrep-out/semgrep.json .
  Scanning 101 files tracked by git with 1 Code rule, 1 Supply Chain rule:
  Scanning 30 files.
  maven_dep_tree.txt   Lockfile                              Maven       171                1
  build.gradle         Disabled (use --allow-local-builds)   Unknown     -                  -
 • Findings: 0 (0 blocking)
 • Rules run: 2
 • Targets scanned: 31
   ◦ Files matching .semgrepignore patterns: 19
Ran 2 rules on 31 files: 0 findings.
```

## 관련 파일

- 규칙: `rules/mois/01-input-validation/sql-injection-jdbc.yaml`, `rules/cve/CVE-2021-44228.yaml`
- 판정: `scripts/report.py`, 회귀시험: `scripts/test.sh`
- Task: tekton_pipeline_manager `01.init/tekton-catalog/tasks/build-4-analyze-semgrep.yaml`
- Semgrep 문서: [taint mode](https://semgrep.dev/docs/writing-rules/data-flow/taint-mode),
  [r2c-internal-project-depends-on](https://docs.semgrep.dev/writing-rules/experiments/r2c-internal-project-depends-on)
