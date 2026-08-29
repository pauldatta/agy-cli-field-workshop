# 모듈 2: 레거시 코드베이스 현대화

<div class="module-header" markdown>
**소요 시간:** 약 75분  
**목표:** Antigravity CLI 기본 요소를 사용하여 레거시 애플리케이션을 안전하게 마이그레이션합니다 — 엄격한 권한 제어, 에이전트 자체 온보딩, 병렬 서브에이전트 분석, 가드레일로서의 훅, 그리고 안전망으로서의 `/rewind`를 활용합니다.  
**실습 PRD:** [.NET 현대화](exercises/ex08_dotnet_modernization.md) · [Java 업그레이드](exercises/ex09_java_upgrade.md)
</div>

> 📖 출처: [권한](https://antigravity.google/docs/permissions) · [엄격 모드](https://antigravity.google/docs/strict-mode) · [서브에이전트](https://antigravity.google/docs/subagents) · [스킬](https://antigravity.google/docs/skills) · [훅](https://antigravity.google/docs/hooks) · [CLI 기능](https://antigravity.google/docs/cli-features) · [CLI 사용](https://antigravity.google/docs/cli-using)

---

## 레거시 현대화가 어려운 이유

대규모 마이그레이션의 위험은 코드 변경이 아니라 **미지의 요소**에 있습니다. 무언가 망가지기 전까지는 무엇이 망가질지 알 수 없습니다. 세 가지 실패 유형은 다음과 같습니다.

1. **범위 확장(Scope creep)** — 에이전트가 건드리라고 요청하지 않은 부분까지 리팩터링합니다.
2. **컨텍스트 붕괴(Context collapse)** — 긴 세션 후 에이전트가 마이그레이션 제약 조건을 잃어버립니다.
3. **롤백 불가(No rollback)** — 잘못된 변경 사항이 중단하기도 전에 연쇄적으로 퍼집니다.

AGY의 기본 요소는 이 세 가지 문제를 모두 직접적으로 해결합니다.

---

## 2.1 — 엄격한 권한: 쓰기 전에 읽기 <span class="duration-badge">15분</span>

AGY에서 "플랜 모드"에 해당하는 것은 **엄격한 권한(strict permissions)**입니다. 이는 명시적으로 허용할 때까지 모든 파일 쓰기 및 셸 명령을 거부하는 강력한 관문입니다.

### 탐색하기 전에 잠그기

```bash
/permissions
```

수준을 `strict`로 설정합니다:

```bash
# In the permissions dialog, select: strict
# Or set directly in settings.json:
```

```json
{
  "permissions": {
    "mode": "strict"
  }
}
```

`strict` 모드에서 에이전트는 파일을 읽고, 웹을 검색하고, 추론할 수 있지만 **어떤 것도 쓰거나, 삭제하거나, 실행할 수 없습니다**. 이는 부드러운 프롬프트가 아니라 단단한 벽입니다.

> 📖 출처: [엄격한 모드](https://antigravity.google/docs/strict-mode) · [권한](https://antigravity.google/docs/permissions)

### 이제 자유롭게 조사하기

쓰기가 잠긴 상태에서 에이전트에게 제약 없는 읽기 권한을 부여합니다:

```text
Analyze this entire codebase for a migration. Map:
1. Framework versions and dependency tree (check package.json / pom.xml / .csproj)
2. Architectural patterns in use (MVC, layered, hexagonal)
3. All deprecated API usage (javax.* imports, legacy auth patterns, XML config)
4. Configuration files and external property sources
5. Test frameworks and coverage gaps
6. Migration risks ordered by severity
```

> **진행 상황:** 에이전트는 필요한 모든 파일을 읽고, 가져오기(import) 및 호출 체인을 추적하며, 멘탈 모델을 구축합니다. 이 모든 과정에서 수정될 위험은 전혀 없습니다. 이것이 바로 정찰 단계입니다.

### 편집기에서 계획 검토하기

에이전트가 마이그레이션 계획을 생성하면, 편집기에서 열어 이를 다듬습니다:

```text
ctrl+g
```

이렇게 하면 현재 에이전트 출력과 함께 `$EDITOR`로 진입합니다. 제약 조건을 편집하고, 팀별 요구 사항을 추가하며, 원하지 않는 범위를 삭제하세요. 저장하고 종료하면 에이전트가 편집 내용을 반영합니다.

> 📖 출처: [cli-using — 키 바인딩](https://antigravity.google/docs/cli-using) — uid 3_276–3_280: "기본 셸 편집기 내에서 프롬프트 편집"

### 쓰기 잠금 해제 — 단, 승인한 항목에 대해서만

계획이 승인되면 선택적으로 쓰기 권한을 복원합니다:

```bash
/permissions
# Select: request-review
```

`request-review` 모드에서 에이전트는 모든 쓰기 또는 셸 명령을 실행하기 전에 승인을 요청합니다. 에이전트가 무엇을 하려는지 실행 전에 정확히 확인할 수 있습니다.

> **흐름:** `strict` (조사) → 계획 승인 → `request-review` (감독 하에 실행) → 신뢰할 수 있고 충분히 테스트된 최종 단계에만 `always-proceed` 사용.

---

## 2.2 — AGENTS.md: 마이그레이션 표준 인코딩 <span class="duration-badge">10 min</span>

긴 세션에서는 컨텍스트가 무너집니다. AGENTS.md는 이를 방지하는 방법입니다. 대화가 아무리 길어지더라도 모든 세션에 자동으로 주입됩니다.

### 에이전트 셀프 온보딩

가장 강력한 패턴은 에이전트가 조사 중에 발견한 내용을 바탕으로 **자신의 AGENTS.md를 직접 작성**하도록 하는 것입니다. 에이전트는 자신이 학습한 내용을 이후 작업의 가드레일로 인코딩합니다.

```text
Based on your codebase analysis, write an AGENTS.md that:
1. Documents current state (Spring Boot 2.6, Java 8, javax.* namespaces)
2. Defines target state (Spring Boot 3.3, Java 21, jakarta.* namespaces)
3. Sets migration rules:
   - Migrate one module at a time — never touch more than one bounded context per session
   - Every migrated class must have a passing test before moving on
   - Preserve all existing API contracts — no breaking changes to callers
   - Commit after each completed phase with a structured message
4. Flags the specific risks you identified in your analysis
5. Lists files that are off-limits in this phase

Write this to AGENTS.md in the project root.
```

> **셀프 온보딩이 효과적인 이유:** 에이전트는 자신을 위한 지침을 작성합니다. 이 시점부터 내리는 모든 마이그레이션 결정은 자신이 작성한 제약 조건에 대해 검사됩니다. 이는 자기 강화 루프입니다. 더 나은 컨텍스트는 더 나은 변경을 생성하고, 이는 더 많은 패턴을 드러내며, 다시 컨텍스트를 개선합니다.

### @file 가져오기를 사용한 모듈식 컨텍스트

대규모 프로젝트의 경우 AGENTS.md를 가볍게 유지하고 상세한 사양을 가져옵니다:

```markdown
# AGENTS.md

@./docs/migration/architecture-target.md
@./docs/migration/api-contracts.md
@./docs/migration/phase-1-checklist.md
```

> 📖 출처: [cli-using](https://antigravity.google/docs/cli-using) — AGENTS.md 가져오기 구문

### 엄격한 제약 조건을 위한 규칙 파일

타협할 수 없는 요구 사항의 경우 `.agents/rules.md`를 사용하세요. 이는 단순한 컨텍스트가 아니라 시스템 프롬프트 지시문으로 주입됩니다:

```markdown
# .agents/rules.md

- NEVER delete migration files (MIGRATION.md, phase-*.md)
- NEVER modify files outside the current migration module's directory
- ALWAYS run the test suite before declaring a phase complete
- ALWAYS commit with message format: "migrate(phase-N): <description>"
```

> 📖 출처: [cli-using](https://antigravity.google/docs/cli-using) — `.agents/rules.md` 시스템 프롬프트 지시문

---

## 2.3 — 서브에이전트: 병렬 분석 팀 <span class="duration-badge">15 min</span>

대규모 마이그레이션에는 보안, 성능, API 계약, 테스트 커버리지 등 여러 독립적인 고려 사항이 있습니다. 이를 순차적으로 실행하면 속도가 느려지고 에이전트의 컨텍스트 윈도우가 낭비됩니다. 서브에이전트를 사용하여 병렬화하세요.

### 병렬 분석 팀 생성하기

```text
I need three parallel analyses before we start migrating. Please spawn:

1. A security-analysis subagent: scan every auth and session-handling class
   for OWASP Top 10 issues. Read-only. Report back with file paths and line numbers.

2. A dependency-map subagent: trace all inter-module dependencies and identify
   which modules can be migrated independently vs which have shared state.
   Produce a migration-order recommendation.

3. A test-coverage subagent: list every public method in the auth module with
   no test coverage. Produce a test-gap report.

Run all three concurrently. I'll review the reports before we start Phase 1.
```

### 서브에이전트 패널에서 모니터링하기

```bash
/agents
```

패널에는 실행 중인 모든 서브에이전트가 `running`, `done`, `killed` 상태와 함께 표시됩니다. 세 개가 모두 동시에 완료되는 것을 지켜보세요.

```text
ctrl+j
```

승인을 기다리고 있는 다음 서브에이전트로 이동합니다. 권한 경계에 도달하여 승인이 필요한 경우에 유용합니다.

```text
ctrl+k
```

현재 컨텍스트를 벗어나지 않고 메인 대화에서 서브에이전트 권한 요청을 빠르게 승인합니다.

> 📖 출처: [cli-features — 서브에이전트](https://antigravity.google/docs/cli-features) — uid 5_278–5_316

### 사용자 지정 서브에이전트 정의

`.agents/agents/security-scanner.md`에 읽기 전용 보안 스캐너를 생성합니다:

```markdown
---
model: gemini-3.7-flash
tools:
  allow:
    - read_file
    - list_directory
    - grep_search
# No write_file, no run_command — this agent is read-only
---

You are a security analyst specializing in migration risk assessment.
Your job is to identify vulnerabilities in legacy code that could be
amplified during a modernization effort.

Focus on:
- Authentication and session management anti-patterns
- SQL injection vectors in legacy data access layers
- Hardcoded credentials or secrets in configuration files
- Deprecated cryptographic primitives (MD5, SHA-1, DES)
- Unvalidated redirects or file path traversal risks

Always report: file path, line number, severity (HIGH/MEDIUM/LOW), and remediation.
Never modify any file. Never execute any command.
```

> 📖 출처: [서브에이전트](https://antigravity.google/docs/subagents) · [cli-features](https://antigravity.google/docs/cli-features) — uid 5_274: 세분화된 권한 JSON 형식

---

## 2.4 — 스킬: 재사용 가능한 마이그레이션 전문 지식 <span class="duration-badge">10 min</span>

스킬은 에이전트가 관련 상황에서 읽고 활성화하는 지침 세트입니다. 반복 가능한 마이그레이션(Java 8→21, .NET Framework→.NET 8, Express→Fastify)의 경우, 해당 패턴을 스킬로 한 번만 인코딩하세요.

### 사용 가능한 스킬 찾아보기

```bash
/skills
```

### 마이그레이션 스킬 생성

```bash
mkdir -p ~/.gemini/antigravity-cli/skills/java-migration
```

`~/.gemini/antigravity-cli/skills/java-migration/SKILL.md` 생성:

```markdown
---
name: java-migration
description: >
  Guides Java 8 to Java 21 + Spring Boot 3.x migration. Activates when
  the user mentions javax.*, Spring Boot 2.x, or Java upgrade. Provides
  phase-by-phase migration steps, jakarta.* namespace rules, and
  mandatory test-gate requirements between phases.
---

## Java 8 → 21 Migration Protocol

### Phase 0 — Inventory (always first)
- Run: grep -r "javax\." src/ | grep -v test | sort | uniq -c | sort -rn
- Identify all Spring Boot starter versions in pom.xml
- Check for removed APIs: sun.misc.*, com.sun.*, internal packages

### Phase 1 — Dependency Upgrade
- Update Spring Boot parent to 3.3.x
- Replace javax.* with jakarta.* (use: sed -i 's/javax\./jakarta\./g')
- Update Hibernate to 6.x — @Entity annotation semantics changed
- Gate: mvn clean verify must pass before Phase 2

### Phase 2 — Configuration Migration

**Goal:** Migrate XML/property-file config to type-safe structured config.

**Steps:**
1. Identify all config sources (XML, .properties, environment variables)
2. Map to typed configuration classes
3. Replace with framework-native config (Spring Boot `@ConfigurationProperties`, .NET `IOptions<T>`)
4. Add validation annotations
5. Remove legacy config loading code

**Validation:** All tests pass with new config loading path.
```

> 📖 출처: [스킬](https://antigravity.google/docs/skills) · [cli-features — /skills](https://antigravity.google/docs/cli-features) — uid 5_251–5_253

---

## 2.5 — 훅: 자동화된 가드레일 <span class="duration-badge">10분</span>

엔터프라이즈 마이그레이션의 경우 단순한 수동 검토가 아닌 자동화된 게이트가 필요합니다. 훅은 CLI 이벤트에서 실행되며 도구 사용이 발생하기 전에 이를 차단, 경고 또는 기록할 수 있습니다.

### 도구 실행 전 훅: 마이그레이션 범위 밖의 쓰기 차단

`.agents/hooks/scope-guard.sh` 파일을 생성합니다:

```bash
#!/bin/bash
# AGY CLI hook event: PreToolUse
# Blocks writes to files outside the current migration module

TOOL_NAME="$1"
FILE_PATH="$2"
MIGRATION_MODULE="${MIGRATION_MODULE:-src/auth}"  # Set before starting each phase

if [[ "$TOOL_NAME" == "write_file" || "$TOOL_NAME" == "edit" ]]; then
  if [[ "$FILE_PATH" != *"$MIGRATION_MODULE"* ]]; then
    echo "BLOCK: Write to $FILE_PATH is outside migration scope ($MIGRATION_MODULE)" >&2
    exit 1  # Non-zero exit blocks the tool call
  fi
fi
```

`settings.json`에 등록합니다:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "write_file|edit",
        "command": ".agents/hooks/scope-guard.sh"
      }
    ]
  }
}
```

### 도구 실행 후 훅: 모든 파일 쓰기 후 테스트 자동 실행

```bash
#!/bin/bash
# AGY CLI hook event: PostToolUse
# Runs tests automatically after every source file write

TOOL_NAME="$1"
FILE_PATH="$2"

if [[ "$TOOL_NAME" == "write_file" && "$FILE_PATH" == *".java" ]]; then
  echo "Running test gate after $FILE_PATH was modified..."
  mvn test -pl "$(dirname $FILE_PATH | sed 's|src/main/java||')" -q 2>&1
  if [[ $? -ne 0 ]]; then
    echo "⚠️  Tests failed after writing $FILE_PATH — consider /rewind"
  fi
fi
```

> 📖 출처: [훅](https://antigravity.google/docs/hooks)

---

## 2.6 — /rewind 및 /fork: 안전망 <span class="duration-badge">5 min</span>

### /rewind — 대화 롤백하기

에이전트가 궤도를 벗어나더라도 처음부터 다시 시작할 필요가 없습니다. `/rewind`는 대화 기록을 롤백합니다:

```bash
/rewind
```

그러면 기록 선택기가 열립니다. 되돌릴 턴을 선택하세요. 코드베이스에 대한 에이전트의 이해도가 해당 시점으로 초기화되므로, 긴 세션 동안 잘못된 가정이 누적된 경우에 유용합니다.

> 📖 출처: [cli-features](https://antigravity.google/docs/cli-features) — uid 5_220–5_226: "`/rewind` (별칭 `/undo`) — 대화 기록 롤백"

### /fork — 위험 없이 탐색하기

위험한 마이그레이션 단계를 시도하기 전에 대화를 포크(fork)하세요:

```bash
/fork
```

그러면 병렬 작업 공간이 생성됩니다. 포크된 공간에서 위험한 접근 방식을 시도해 볼 수 있습니다. 성공하면 좋고, 실패하더라도 포크를 닫고 메인 대화에서 계속 진행하면 됩니다. 메인 대화는 전혀 변경되지 않습니다.

> 📖 출처: [cli-using](https://antigravity.google/docs/cli-using) — uid 3_219–3_224: "`/fork`를 사용하여 별도의 작업 공간 생성"

### /resume — 긴 마이그레이션 이어가기

대규모 마이그레이션은 며칠에 걸쳐 진행됩니다. 다시 돌아왔을 때:

```bash
/resume
```

그러면 타임스탬프와 대화 이름이 포함된 이전 마이그레이션 세션들을 보여주는 세션 선택기가 열립니다. 중단했던 부분부터 정확히 계속하려면 올바른 세션을 선택하세요.

> 📖 출처: [cli-features](https://antigravity.google/docs/cli-features) — uid 5_213–5_219

마이그레이션을 체계적으로 관리하려면 세션 이름을 변경하세요:

```bash
/rename "Java 21 Migration — Phase 2: Jakarta namespace"
```

---

## 2.7 — Print 모드: 비대화형 마이그레이션 파이프라인 <span class="duration-badge">5 min</span>

CI/CD 게이트나 야간 마이그레이션 실행의 경우, 상호 작용 없이 마이그레이션 작업을 파이프라인으로 연결하려면 Print 모드를 사용하세요:

```bash
# Dry-run: analyze and report issues — no writes
agy -p "Review the migration changes in the last commit. \
  Check for: javax.* references that weren't updated, \
  missing jakarta.* imports, and test files that weren't \
  updated to match renamed packages. \
  Output a structured report with file paths and line numbers."
```

```bash
# Chain: analyze → generate migration report → save
agy -p "Scan src/auth/ for javax.persistence.* usage" | \
  agy -p "Convert this javax.persistence usage report into \
  a step-by-step migration plan with exact sed commands" > migration-plan.md
```

> 📖 출처: [cli-getting-started](https://antigravity.google/docs/cli-getting-started) — `agy --help`: "-p: --print의 짧은 별칭"

---

## 실습 예제

<div class="exercise-card" markdown>

### :material-file-document: 실습 8: 레거시 현대화

**파일:** [`ex08_dotnet_modernization.md`](exercises/ex08_dotnet_modernization.md) · [`ex09_java_upgrade.md`](exercises/ex09_java_upgrade.md)  
**소요 시간:** 45분  
**목표:** 이 모듈의 AGY 기본 요소를 사용하여 전체 마이그레이션을 진행합니다.

**트랙 선택:**

#### 트랙 A: 계획 우선 (엄격 → 조사 → 실행)

1. `/permissions`를 `strict`로 설정합니다 — 모든 쓰기를 잠급니다.
2. 에이전트에게 전체 조사 권한을 부여합니다 (섹션 2.1).
3. `ctrl+g`를 사용하여 편집기에서 계획을 열고 팀 제약 조건을 추가합니다.
4. 마이그레이션 규칙을 인코딩하는 AGENTS.md를 작성합니다 (또는 에이전트가 작성하도록 합니다).
5. 절대 타협할 수 없는 조건을 포함하여 `.agents/rules.md`를 추가합니다.
6. `request-review`로 전환합니다 — 감독 하에 1단계를 시작합니다.
7. 에이전트가 범위를 벗어나면 `/rewind`를 사용합니다.
8. 세션 이름 변경: `/rename "마이그레이션 — 1단계 완료"`

#### 트랙 B: 서브에이전트 우선 (병렬 분석 → 컨텍스트 → 실행)

1. 세 개의 병렬 서브에이전트를 생성합니다: 보안 스캔, 종속성 맵, 테스트 커버리지.
2. `/agents`를 통해 모니터링합니다 — 승인을 위해 `ctrl+j` 및 `ctrl+k`를 사용합니다.
3. 보고서를 AGENTS.md로 통합합니다 (에이전트가 종합하도록 합니다).
4. `java-migration` 스킬을 설치합니다 (섹션 2.4).
5. 가장 위험한 단계 전에 `/fork`를 사용합니다 — 그곳에서 먼저 시도해 봅니다.
6. 인쇄 모드를 사용하여 단계 완료 후 보고서를 생성합니다.

</div>

---

## 요약: 레거시 현대화를 위한 AGY 프리미티브

| 프리미티브 | 기능 | 사용 시기 |
| :-- | :-- | :-- |
| `/permissions strict` | 강력한 읽기 전용 게이트 — 쓰기 또는 명령어 실행 불가 | 조사 단계 |
| `/permissions request-review` | 모든 쓰기 작업 전에 에이전트가 승인을 요청함 | 통제된 실행 |
| `ctrl+g` | 협업 편집을 위해 `$EDITOR`에서 계획 열기 | 계획 세분화 |
| **AGENTS.md** | 세션 간 영구적인 마이그레이션 표준 | 항상 — 제약 조건 인코딩 |
| `.agents/rules.md` | 강력한 시스템 프롬프트 지시문 | 타협할 수 없는 가드레일 |
| **서브에이전트** | 병렬 분석 팀 | 다중 관심사 조사 |
| `/agents` + `ctrl+j` + `ctrl+k` | 서브에이전트 작업 모니터링 및 승인 | 병렬 실행 중 |
| **훅** (PreToolUse) | 마이그레이션 범위 밖의 쓰기 차단 | 자동화된 가드레일 |
| **훅** (PostToolUse) | 모든 변경 후 테스트 자동 실행 | 테스트 게이트 자동화 |
| `/rewind` | 에이전트가 벗어날 경우 대화 롤백 | 세션 중간 경로 수정 |
| `/fork` | 격리된 브랜치에서 위험한 단계 시도 | 위험도가 높은 변경 전 |
| `/resume` | 며칠에 걸친 마이그레이션 재개 | 세션으로 돌아갈 때 |
| `/rename` | 단계별로 세션 레이블 지정 | 세션 관리 |
| `agy -p` | 비대화형 마이그레이션 파이프라인 | CI 게이트, 야간 실행 |
| **스킬** | 재사용 가능한 마이그레이션 플레이북 | 반복 가능한 마이그레이션 패턴 |

---

## 다음 단계

→ **[모듈 3: SDK로 AGY 에이전트 빌드하기](agy-sdk.md)**로 계속 진행하세요

→ **[치트시트](cheatsheet.md)** — 모든 명령어를 한곳에서 확인하세요
