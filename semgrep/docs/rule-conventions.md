# 규칙 작성 규약 (v0.6.1)

Semgrep CE 1.180.0 에서 실제로 돌려 확인한 형태만 적는다. 새 형태를 쓰려면 먼저 작은 예제로 확인하고 여기에 추가한다.


## 0. 무엇을 규칙으로 만드나 (v0.6.1)

**Semgrep 이 코드만 보고 판단할 수 있는 것만 규칙으로 만든다.** 함수 · 변수 이름이나 "검사 흔적이 없다"로 추정하는 규칙은 두지 않는다
(인증 · 권한 · 업로드 제한 · 로그인 시도 제한 · 비밀번호 정책처럼 다른 계층에 있을 수 있는 것). 그런 항목은 현황표에 `제외`(수동 점검)로 적는다.
규칙의 탐지는 "그 코드 자체가 약점"이어야 하고, 검증 인정(sanitizer)은 "그 코드가 안전함을 증명"해야 한다 — 증명하지 못하면 인정하지 않는다
(오탐은 SonarQube 에서 처리할 수 있지만, 미탐은 이슈가 생기지 않아 아무도 볼 수 없다).

## 1-a. v0.6.1 에서 바뀐 guard 틀 (아래 1절의 틀보다 우선)

- **빠져나가는 호출**: Python 은 `return` · `raise` · `continue` · import 로 확인되는 `flask.abort(...)` · `sys.exit(...)` 만. 이름만 `abort` 인 함수, 내장 `exit()` · `quit()` 은 불인정.
- **검사식 판정은 조건 원문 정규식으로**: `if $COND:` 의 `$COND` 원문이 "검사" 또는 "… or 검사 or …"(빠져나가는 형태) / "… and 검사 and …"(조건 안 사용) 일 때만.
  `not (…)` · `== False` · `and` · `&` · 괄호로 감싸면 불인정. Java 는 "검사식을 감싸는 식이 `||`(또는 `&&`)뿐" 인 `$WRAP` 허용 목록으로 같은 일을 한다.
- **재대입 제외**: 검사 뒤 같은 블록의 `=` · `+=`(튜플 풀기 포함 — `$X = $V` 가 맞는다) + 한 단계 안쪽 블록(if · else · for · while · with · try · except)의 `=` · `+=`.
  두 단계 이상 안쪽은 못 본다 (한계로 문서화).
- **else 가 붙은 검사는 인정하지 않는다.** 식 안의 조건부 종료(`strict and flask.abort(400)`)도 종료가 아니다.
- **허용 목록**: 모듈 수준 리터럴이고 그 함수에서 바뀌지 않을 때만 (`=` · `+=` · `|=` · `[k] =` · `append` · `add` · `update` …).
- **값 변환형 sanitizer 는 `exact: true`**: `Integer.parseInt(...)`, Django ORM 조회처럼 "결과만 안전"한 것은 exact 로 써서 인자 안의 sink · 대입을 지우지 않게 한다.
  exact 식 패턴은 대입한 변수를 깨끗하게 하지 못하므로 `$V = 변환(...)` 문장 형태를 따로 적고, 그 문장 안에 sink 가 들 수 있으면(raw · extra · RawSQL) `pattern-not` 으로 뺀다.

## 1. "검증됨"(sanitizer) 은 guard 일 때만 인정한다

검사 코드가 **있다는 것만으로** 값을 안전하다고 보면 실제 취약점을 조용히 놓친다.
아래 두 형태만 인정한다. 검사 결과를 버리거나, 실패해도 계속 진행하거나, 반대 분기에서 쓰면 **탐지되어야 한다**.

| 형태 | 예 | 인정 |
|---|---|---|
| 실패 시 중단 | `if x not in ALLOWED: return` 뒤의 `x` | O |
| 조건 안에서만 사용 | `if x in ALLOWED: use(x)` (else 없는 if) | O |
| 결과를 쓰지 않음 | `x in ALLOWED` 한 줄, `x.matches("...");` | X |
| 실패해도 계속 진행 | `if x not in ALLOWED: log(...)` 뒤의 `x` | X |
| 반대 분기 | `if x in ALLOWED: ... else: use(x)` | X |

> **v2 (2026-11-17 변경)** — 처음 틀은 `by-side-effect` 로 "검사 식 이후의 값"을 안전 처리했는데 구멍이 셋 있었다.
> ① 실패 분기 **안**에서 쓰는 것까지 안전 처리(`if (!ok(x)) { return use(x); }` 미탐)
> ② null 검사와 묶이면 인정 못 함(`if (x == null || !ok(x)) throw …` 뒤가 오탐)
> ③ 분기 안쪽의 조건부 `return` 도 "중단"으로 봄.
> 그래서 **if 문 "뒤"에 나오는 `$X` 만** 안전 처리하는 아래 형태를 쓴다. 규칙에는 `options: {go_deeper_stmt: false}` 를 준다
> (마지막 문장이 return/raise/throw 일 때만 "중단"으로 맞게 된다). `by-side-effect` guard 는 쓰지 않는다.

### Python — 실패 시 중단 (if 문 뒤의 `$X`)

`NEGCHECK` 자리에 "실패" 를 뜻하는 식을 넣는다 (`$X not in $ALLOW`, `not re.fullmatch($PAT, $X)` 등). 여러 형태면 `pattern-either` 로 나열한다.

```yaml
options:
  go_deeper_stmt: false
...
- patterns:
    - pattern-either:
        - pattern-inside: |
            if $COND:
                ...
                return ...
            ...
        - pattern-inside: |
            if $COND:
                ...
                raise ...
            ...
        - pattern-inside: |
            if $COND:
                ...
                continue
            ...
        - patterns:
            - pattern-inside: |
                if $COND:
                    ...
                    $EXIT(...)
                ...
            - metavariable-regex:
                metavariable: $EXIT
                regex: ^(abort|flask\.abort|sys\.exit|exit|quit)$
    - metavariable-pattern:
        metavariable: $COND
        patterns:
          - pattern: NEGCHECK                 # 조건식 안 어디에 있어도 된다 (x is None or NEGCHECK)
          - pattern-not-inside: $P and $Q     # 다른 조건이 참일 때만 검사하는 형태는 인정하지 않는다
    - pattern-not-inside: |                   # if 문 자체(실패 분기 안)는 제외
        if $COND:
            ...
    - pattern-not-inside: |                   # 검사 뒤에 다시 대입하면 제외
        if $COND:
            ...
        ...
        $X = $V
        ...
    - pattern-not-inside: |                   # 검사 뒤에 덧붙여도 제외 (x += 입력)
        if $COND:
            ...
        ...
        $X += $V
        ...
    - pattern: $X
```

### Python — 조건 안에서만 사용

```yaml
- patterns:
    - pattern-inside: |
        if <... CHECK ...>:
            ...
    - pattern-not-inside: |
        if <... not $NEG ...>:
            ...
    - pattern-not-inside: |
        if <... $P or $Q ...>:
            ...
    - pattern-not-inside: |
        if $C:
            ...
        else:
            ...
    - pattern: $X
```

### Java — 실패 시 중단 (if 문 뒤의 `$X`)

```yaml
options:
  go_deeper_stmt: false
...
- patterns:
    - pattern-either:
        - pattern-inside: |
            if ($COND) { ... return ...; }
            ...
        - pattern-inside: |
            if ($COND) { ... throw $E; }
            ...
        - pattern-inside: |
            if ($COND) return ...;
            ...
        - pattern-inside: |
            if ($COND) throw $E;
            ...
    - metavariable-pattern:
        metavariable: $COND
        patterns:
          - pattern: NEGCHECK                 # 예: '!$X.matches(...)'  (x == null || !x.matches(..) 에도 맞는다)
          # 검사식을 감싸는 식은 || 뿐이어야 한다. $WRAP 은 검사식을 품은 모든 식(검사식 자신 포함)에 맞으므로,
          # "|| 도 아니고 검사식 자체도 아닌 식" 안에 있으면 인정하지 않는다 → &&·&·^·?:·!(…)·== false·호출 인자가 한 번에 걸린다.
          # (연산자를 하나씩 `$P && $Q` 로 빼던 예전 형태는 & 와 ?: 를 놓쳤다. `|` 로 묶은 것도 인정하지 않는다 — 오탐 쪽)
          - pattern-not-inside:
              patterns:
                - pattern: $WRAP
                - pattern-not: $OR1 || $OR2
                - pattern-not: NEGCHECK       # 검사식 자체. NEGCHECK 에 이름 정규식이 걸려 있으면 그 조건까지 그대로 다시 적는다
    - pattern-not-inside: |
        if ($COND) $S;
    - pattern-not-inside: |
        if ($COND) $S;
        ...
        $X = $V;
        ...
    - pattern-not-inside: |
        if ($COND) $S;
        ...
        $X += $V;
        ...
    - pattern: $X
```

### Java — 조건 안에서만 사용

```yaml
- patterns:
    - pattern-inside: |
        if ($COND) $S;
    - metavariable-pattern:
        metavariable: $COND
        patterns:
          - pattern: CHECK                    # 예: '$X.matches(...)'  (x != null && x.matches(..) 에도 맞는다)
          # 검사식을 감싸는 식은 && 뿐이어야 한다 (||·|·^·?:·!(…)·== false·호출 인자는 검사가 거짓이어도 본문에 들어온다)
          - pattern-not-inside:
              patterns:
                - pattern: $WRAP
                - pattern-not: $AND1 && $AND2
                - pattern-not: CHECK          # 검사식 자체. CHECK 가 호출이면(이름 정규식) 그 조건까지 다시 적는다 —
                                              # 아무 호출이나 허용하면 isDisabled(check(x)) 가 통과한다
    - pattern-not-inside: $COND               # 조건식 안에서 쓰는 것은 검사보다 먼저 실행될 수 있다: if (use(x) && check(x))
    - pattern-not-inside: |
        if ($C) $S1; else $S2;
    - pattern-not-inside: |                   # 본문에서 다시 대입 (안쪽 블록의 대입에도 맞는다)
        if ($COND) { ... $X = $V; ... }
    - pattern-not-inside: |
        if ($COND) { ... $X += $V; ... }
    - pattern: $X
```

두 언어 모두 속이는 예제로 확인한 것: 결과 버림, 실패해도 진행, 반대 분기, 조건 밖 사용, **실패 분기 안 사용**,
**안쪽 조건부 return**, **검사 뒤 재대입**, **다른 조건과 `and`/`&&` 로 묶임**, **다른 변수만 검사** → 모두 탐지.
null 검사와 `or`/`||` 로 묶인 guard 는 인정.
구현 예: `rules/mois/01-input-validation/integer-overflow.yaml`, `code-injection.yaml`.

## 2. 검사 식(CHECK) 자체도 가려 쓴다

| 검사 | 인정하는 형태 | 인정하지 않는 형태 |
|---|---|---|
| 허용 목록 | **문자열·숫자만 든 리터럴**. 같은 파일에서 이름을 붙인 것(`ALLOWED = {"a", "b"}`)이나 조건에 바로 적은 것(`x not in ("a", "b")`) | 다른 모듈에서 가져온 목록, 실행 중에 만든 목록(`load()`, `request.GET.getlist(...)`), 변수가 섞인 목록 |
| dict / Map 조회 | 키·값이 문자열·숫자뿐인 리터럴 dict 의 `T[k]`·`T.get(k)`. Java 는 `final` 필드이고 클래스 안에서 리터럴 아닌 값을 넣지 않는 Map | `T.get(k, 입력)`, 요청 값으로 만든 dict(`{"host": request…}`), 일반 Map |
| 정규식 | 전체 일치: Python `re.fullmatch`, Java `String.matches` | `re.match`·`re.search` (앞부분만 맞아도 통과) |
| 문자 제거 | 위험 문자를 지우는 것이 리터럴로 보일 때 (`replaceAll("[\\r\\n]", "")`) | 임의의 `replace`·`replaceAll`·`re.sub` |
| 경로 | 정규화 후 **구분자를 붙인** 접두 비교(`startsWith(base + File.separator)`), `Path.startsWith(Path)`, `is_relative_to`, `commonpath([base, p]) == base` | `commonprefix`, 구분자 없는 문자열 `startswith` (`/safe-evil` 이 `/safe` 로 통과) |
| 설정에 의한 제외 | 탐지 대상과 **같은 객체**에, 사용 **이전**에 설정된 경우 | 같은 메서드의 다른 객체에 설정된 경우 |

## 3. sink 는 라이브러리를 확인할 수 있을 때만 block

- 타입(`(java.sql.Statement $S)`), import 로 풀리는 이름(`sqlalchemy.text`), 같은 함수 안의 생성(`$C = $CONN.cursor()`) 중 하나로 확인되는 것만 `block` 규칙에 둔다.
- 메서드 이름만으로 잡는 것은, 그 이름이 사실상 한 API 전용일 때(`prepareStatement`·`prepareCall`·`executeQuery`·`executeUpdate`·`addBatch`)만 허용한다.
- 그 밖의 "아무 객체의 `.execute(...)`", "아무 호출의 `verify=False`" 는 별도 `warn` 규칙으로 나눈다.
- `java.lang` 클래스는 짧은 이름과 전체 이름을 모두 적는다 (`(Runtime $R)` 과 `(java.lang.Runtime $R)`).

## 4. Semgrep 에서 자주 틀리는 것

- `metavariable-regex` 는 문자열 **맨 앞부터** 맞춘다. 이름 중간을 찾으려면 `.*` 로 시작하고, 전체 일치는 `^…$`.
- 한 `patterns` 블록에서 `pattern-either` 의 일부 가지에만 있는 메타변수에 `metavariable-regex` 를 걸면 나머지 가지가 **조용히 무효**가 된다. 가지별로 항목을 나눈다.
- `pattern-not-inside` 의 메타변수는 바깥 패턴과 같은 이름이면 같은 코드에 묶인다. "같은 객체" 조건은 이걸로 표현한다.
- 컬렉션에 넣은 값(`add`·`put`)은 컬렉션 전체를 오염시킨다. 요소 단위로는 구분하지 못한다.

아래는 규칙을 고치며 실제로 걸렸던 것들이다.

**패턴이 생각보다 넓게 맞는 경우**

- `$X = (...)` 는 튜플이 아니라 **모든 대입**에 맞는다 (괄호 친 식). 튜플은 `(..., )` 로 쓰거나 원문을 정규식으로 본다.
- `$S.$M(...)`·`@$APP.$M(...)` 는 import 한 맨이름 호출(`call_api(...)`, `@login_required`)에도 맞는다.
- `$F(...)` 는 `a.b(x)` 에도 맞고 `$F` 가 `a.b` 로 묶인다. 이름 정규식을 `.*(hash|…).*` 로 쓰면 수신 객체 이름(`hashService.log(pw)`)으로 통과한다. `$O.$F(...)` 를 따로 두고 `$F` 는 `^\w*(…)\w*$` 로 쓴다.
- `식;` 패턴(Java)은 대입·선언·return·호출 인자 안의 그 식에도 맞는다.
- `metavariable-pattern` 은 메타변수 **안 어딘가**에 맞으면 통과한다 (전체 일치가 아니다).
- `return ...` 는 값 없는 `return` 에도, `@X(...)` 는 인자 없는 `@X` 에도, `$P` 인자 패턴은 타입 표기·기본값이 있는 인자에도 맞는다.

**패턴이 생각보다 좁게 맞는 경우**

- 타입을 적은 메타변수(`(java.nio.file.Path $P)`)는 **호출 결과의 타입을 풀지 못한다**. `Paths.get(x).resolve(y)`, `f.toPath().resolve(y)` 는 따로 적는다.
- `$X == null` 은 `null == x` 에 맞지 않는다.
- try 패턴은 모양이 다르면 서로 맞지 않는다. Java `try{}catch{}` 는 finally 가 붙은 try 에 안 맞고, Python 은 except 만 / else / finally / else+finally 가 각각 다른 모양이다. Python `except $E:` 는 `except E as e:`·튜플에 안 맞는다 — `except ...:` 를 쓴다.
- Java `if (c) { ... return ...; }` 와 `if (c) return ...;` 는 다른 모양이다 (문장 하나짜리 중괄호 본문만 양쪽에 맞는다).

**조용히 틀어지는 경우**

- 한 `patterns` 안에 `metavariable-pattern` 이 둘이고 뒤쪽이 새 메타변수를 묶으면, 앞쪽에서 묶은 메타변수와 바깥 패턴의 연결이 풀린다.
- `metavariable-pattern` 안에서 묶인 메타변수는 바깥의 `metavariable-regex` 에서 보이지 않는다. 조건을 그 안에 함께 적는다.
- `pattern-not`·`pattern-not-inside` 아래 중첩 `patterns` 에 `pattern-inside` 만 있으면, 그 안의 제외는 탐지 대상이 아니라 바깥 범위에 적용된다. 중첩 블록에 탐지 대상 패턴을 다시 적는다.
- **본문 글자로 제외하는 규칙**(`pattern-not-regex`, `$...BODY` 정규식)은 주석·문자열에도 반응한다. `# TODO: login_required` 한 줄이 탐지를 지운다. 코드에서만 찾게 쓰고(`(?m)^[^#\n]*\K(…)`), 가능하면 구조 패턴으로 바꾼다. fixture 의 `ruleid:` 주석에 든 규칙 이름 낱말도 걸린다.
- `pattern-not-regex` 는 일치 범위가 탐지 범위 **안**에 있어야 제외한다.
- XML 의 `<![CDATA[ … ]]>` 는 파싱 오류로 보고된다 (탐지는 된다). fixture 에는 넣지 않는다.
- **`metavariable-pattern` 안에 `metavariable-regex` 를 두지 않는다.** 실제 코드의 특정 모양(괄호 친 수신 객체의 메서드 호출 등)에서 Semgrep 1.180 이
  내부 오류(`Invalid_argument: String.sub`)를 내고, **그 파일의 모든 규칙 결과가 사라진다.** 정규식은 바깥에서 조건 원문(`$COND`)에 건다.
- **Python 슬라이스(`x[1:]`)는 taint 를 끊는다** (`x[0]` 은 이어진다). propagator · focus 로도 잇지 못한다 — 한계로 문서화.
- **Python `list.append · extend · insert` 는 목록을 오염시키지 않는다** — 필요한 규칙은 `pattern-propagators` 를 넣는다.
- **한 fixture 파일에 같은 sink 줄이 수십 개를 넘으면** 변이 시험이 `Too many matches` 로 그 파일을 버린다 — 파일을 나눈다.
- **`$...BODY` 를 `metavariable-pattern` 으로 다시 파싱하지 않는다.** 본문에 `with (a / b).open() as f:` 가 있으면 Semgrep 1.180 이 내부 오류(`Invalid_argument: String.sub`)를 내고 그 파일의 탐지가 빠진다. 본문 안의 식은 `def $F(...): ... <... $V ...> ...` 로 찾는다. `$...BODY` 에 `metavariable-regex` 만 거는 것은 괜찮다.
- Python `class $C(...): $...BODY` 는 맞지 않는다 (def·while 은 된다). `@$D` 는 호출 형태 데코레이터(`@a.b(...)`)에 맞지 않고, `$V` 는 데코레이터 식과 키워드 인자 이름을 방문하지 않는다.
- `pattern-not` 은 범위가 정확히 같아야 제외한다. `focus-metavariable` 뒤에서는 `pattern-not-inside` 를 쓴다.
- Semgrep 은 문자열 리터럴의 이스케이프를 풀어서 묶는다. `"\r\n"` 은 CR·LF 두 글자, `r"\r\n"` 은 역슬래시가 든 네 글자다. 정규식으로 구분할 때 주의한다.

## 5. fixture

- `fixtures/<규칙 id>/vulnerable/` 과 `patched/` 를 둔다.
- 탐지되어야 하는 줄 **바로 위**에 주석을 단다. 회귀시험은 표시한 줄과 탐지 위치가 **정확히 같은지** 본다.
  - Java `// ruleid: <규칙 id>` · Python `# ruleid: <규칙 id>` · XML `<!-- ruleid: <규칙 id> -->`
  - 주석을 넣을 수 없는 파일은 `fixtures/<규칙 id>/vulnerable/expected.txt` 에 `상대경로:줄`.
- 탐지되면 안 되는 줄에는 `// ok: <규칙 id>` 로 이유를 남긴다 (검사에는 쓰이지 않는다).
- **가지마다 예제를 둔다.** 규칙의 `pattern-either` 가지, source 형태, sink, sanitizer 각각에 대해
  탐지되는 줄이 하나 이상 있어야 한다. 예제로 살릴 수 없는 가지는 죽은 가지이므로 고치거나 지운다.
- **sanitizer 마다 "속이는" 예제를 둔다.** 결과를 버림 · 실패해도 진행 · 반대 분기 · 경계가 틀린 비교가
  `vulnerable/` 에서 탐지되어야 한다.
- `patched/` 예제는 **모든 규칙**에서 0건이어야 한다 (회귀시험 [2b]).

## 6. 가지별 변이 시험 (`scripts/mutate.py`)

"가지마다 예제"는 눈으로 확인하지 않는다. 규칙의 가지 · 제외 · sink · sanitizer · 정규식 대안을 하나씩 지워 보고,
fixture 결과가 그대로면 그 조각은 죽었거나 중복이거나 예제가 없는 것이다.

```bash
docker run --rm --network none -v "$PWD":/src:ro -w /src semgrep/semgrep:1.180.0 python3 scripts/mutate.py <규칙 id>
```

`기준 일치, 살아남은 변이 0개` 가 나와야 한다. 살아남은 변이는 이렇게 없앤다.

1. 그 조각만이 결정하는 예제 줄을 넣는다 (탐지 조각은 `vulnerable/`, 제외·sanitizer 는 `patched/` 또는 속이는 `vulnerable/`).
2. 다른 조각에 완전히 포함되면 지우거나 좁혀서 조각마다 맡은 일이 하나씩 있게 한다.
3. 실제 코드에 맞을 수 없는 조각은 지운다.

같은 정규식을 여러 가지에 복사해 두면 서로를 가려 변이가 살아남는다. 가지를 `pattern-either` 로 묶고 정규식은 한 번만 건다.
Python 공통 sanitizer 는 `mois-1-05-os-command-injection-py` 의 fixture 에서만 가지별로 증명한다.

도구가 지워 보지 않는 것은 직접 확인한다: `metavariable-comparison` 의 경계값, 문자 클래스(`[...]`) 안의 글자,
대안 묶음이 아닌 전방 탐색(`(?!.*\.objects$)`), 공통 source 블록과 propagator. 이런 조각을 넣을 때는 그것만이 결정하는 예제를 함께 넣는다.

fixture 만으로는 못 잡는 것도 있다. 규칙을 크게 고쳤으면 실제 프로젝트 몇 개를 스캔해 **Semgrep 오류(errors)가 0건인지**도 본다
(본문 재파싱이 특정 코드 모양에서 내부 오류를 내 그 파일의 탐지가 통째로 빠진 적이 있다 — 4절).
