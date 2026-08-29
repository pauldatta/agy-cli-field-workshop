# 모듈 4: 멀티 에이전트 & 고급 기능 <span class="duration-badge">45분</span>

> **agy가 단순한 채팅 어시스턴트를 뛰어넘는 부분입니다.** 이 모듈에서는 병렬 서브에이전트, `/btw`를 사용한 작업 중 스티어링, 백그라운드 스케줄링, 세션 재개 등 agy-cli를 다른 모든 AI 코딩 도구와 차별화하는 기능들을 다룹니다.

---

## 4.0 — agy 에이전트 모델 <span class="duration-badge">5분</span>

agy-cli는 **서브에이전트**를 생성할 수 있습니다. 이는 병렬로 작동하며 각각 고유한 작업 공간 컨텍스트를 갖는 격리된 작업 실행기입니다. 별도의 agy 세션으로 여러 터미널 탭을 실행하는 것과 달리, 서브에이전트는 조정됩니다. 작업 공간을 공유하거나, 격리된 브랜치에서 작업하거나, 복제된 사본에서 작동할 수 있습니다.

세 가지 작업 공간 모드:

| 모드 | 의미 | 사용 시기 |
| :-- | :-- | :-- |
| `inherit` | 서브에이전트가 동일한 작업 공간을 공유함 | 추가적인 작업 — 충돌이 예상되지 않을 때 |
| `branch` | 서브에이전트가 격리된 복제본을 가져옴 | 동일한 파일에 대한 병렬 변경 시 |
| `share` | git 워크트리 — 격리된 브랜치, 공유 저장소 | 진정한 병렬 개발 시 |

### 모델 전환

세션 도중에 활성 모델을 전환하려면 `/model`을 사용하세요. 특정 작업에 대해 더 심도 있는 추론이 필요할 때 유용합니다:

```bash
/model
```

그러면 사용 가능한 옵션(Gemini 3.5 Flash, Gemini 3.1 Pro, Claude Sonnet 4.6 등)을 보여주는 모델 선택기가 열립니다.

> 📖 전체 모델 목록: [모델 문서](https://www.antigravity.google/docs/models)

---

## 4.1 — 서브에이전트 생성 <span class="duration-badge">15분</span>

> **패턴: 병렬 실행** — 여러 에이전트를 파견하여 동시에 작업하도록 합니다.
> 📖 전체 참조: [서브에이전트 문서](https://www.antigravity.google/docs/subagents)

### 대화형 세션에서

```text
> Spawn a subagent to write unit tests for the auth module while I work on the API refactor.
```

agy는 서브에이전트를 생성하고, 해당 ID를 보고한 뒤, 메인 세션을 계속 진행합니다. 서브에이전트는 독립적으로 작동합니다.

```text
> What's the status of the test-writing subagent?
```

```text
> Show me what the test subagent produced.
```

### /agents를 사용한 서브에이전트 관리

`/agents` 패널을 사용하여 활성화된 모든 서브에이전트, 상태 및 출력을 확인하세요:

```bash
/agents
```

메인 대화의 주요 단축키:

| 단축키 | 작업 |
| :-- | :-- |
| `Ctrl+J` | 승인 대기 중인 서브에이전트로 텔레포트 — 요청을 검토하기 위해 직접 이동합니다 |
| `Ctrl+K` | 메인 대화에서 빠른 승인 — 화면 전환 없이 서브에이전트의 대기 중인 작업을 승인합니다 |

서브에이전트 수명 주기: **실행 중(Running) → 대기 중(Idle) → 종료됨(Killed)**

### 제한 사항 및 내장 유형

- **최대 깊이:** 10 (서브에이전트는 자체 서브에이전트를 생성할 수 있으며, 최대 10단계까지 가능합니다)
- **내장 유형:** `research` (웹 검색), `browser` (브라우저 자동화), `self` (범용)

### 병렬 감사 패턴

```text
> Spawn three subagents in parallel:
> 1. Security audit — scan for hardcoded credentials, injection risks, and insecure dependencies
> 2. Performance audit — find N+1 queries, unindexed lookups, and memory leaks
> 3. Coverage audit — identify untested functions and missing integration tests
>
> Use branch workspace mode for each. Report back when all three complete.
```

세 개의 독립적인 분석이 동시에 실행되는 것을 지켜보세요. 분석이 완료되면 agy가 결과를 종합합니다.

!!! tip "놀라운 순간"
    코드베이스에서 세 개의 특화된 에이전트가 병렬로 실행되며, 각각 전체 컨텍스트를 가지고 독립적인 결과를 도출합니다. 이것이 바로 agy를 채팅 기반 어시스턴트와 질적으로 다르게 만드는 패턴입니다.

### 적대적 검토 패턴

```text
> Spawn a subagent to act as an adversarial reviewer for the changes in this branch.
> Its only job: find reasons why this code should NOT be merged.
> It should challenge every assumption and look for edge cases the implementer missed.
```

적대적 검토자 패턴은 보안에 민감한 변경 사항, 인프라 수정 또는 "좋아 보입니다(looks good to me)" 정도로는 충분하지 않은 모든 PR에 특히 강력합니다.

---

## 4.2 — /btw: 작업 중 스티어링 <span class="duration-badge">10 min</span>

> **패턴: 중단 없는 스티어링** — 실행 중인 작업을 멈추지 않고 컨텍스트를 주입합니다.

`/btw`는 agy의 가장 독특한 기능 중 하나입니다. agy가 작업 중일 때 현재 작업을 취소하지 않고 메시지를 보낼 수 있습니다.

### 작동 방식

```text
> Refactor the entire authentication module to use JWT instead of sessions. This will touch multiple files. Start with the backend.
```

*agy가 작업을 시작합니다... 실행되는 동안:*

```bash
/btw Actually, keep backward compatibility with sessions for 30 days — implement a dual-mode auth.
```

agy는 작업을 멈추지 않고 진행 중인 작업에 사용자의 메모를 반영합니다. 이는 스프린트 도중 개발자에게 포스트잇을 남기는 것과 같습니다. 개발자는 이를 보고 조정합니다.

### /btw 사용 사례

```bash
/btw The API rate limit is 100 req/min, factor that into any retry logic you add.
```

```bash
/btw The team uses conventional commits — make sure any commit messages follow that format.
```

```bash
/btw Skip the frontend changes for now, just focus on the backend API.
```

!!! info "중단과의 차이점"
    `/btw`가 없다면 장기 실행 작업을 스티어링하는 것은 작업을 취소하고 프롬프트를 조정한 후 다시 시작하는 것을 의미하며, 이로 인해 모든 진행 상황을 잃게 됩니다. `/btw`를 사용하면 이러한 비용 없이 경로를 수정할 수 있습니다.

---

## 4.3 — 백그라운드 실행 및 스케줄링 <span class="duration-badge">10분</span>

> **패턴: 비동기 agy** — 장기 실행 작업을 시작하고 완료 시 알림을 받습니다.

### 백그라운드 작업

agy는 비동기 실행을 지원합니다. 작업을 시작해 두고 계속해서 다른 작업을 할 수 있습니다. 작업이 완료되면 agy가 알림을 보냅니다.

```text
> In the background, do a comprehensive security audit of this entire codebase. Take as long as you need. Notify me when done.
```

agy는 터미널을 차단하지 않고 감사를 실행합니다. 완료되면 결과와 함께 알림을 받게 됩니다.

### 스케줄링된 작업

agy는 반복적인 분석을 위해 cron 스타일의 스케줄링을 지원합니다:

```text
> Schedule a nightly code quality report every day at 2am. It should check for new TODOs, failing tests, and dependency updates. Save the report to reports/nightly-YYYY-MM-DD.md.
```

Cron 표현식(최대 5개 필드)이 지원됩니다:

```bash
# Run at 2am daily
0 2 * * *

# Run every Monday at 9am
0 9 * * 1

# Run every 15 minutes
*/15 * * * *
```

!!! warning "스케줄링은 세션 간에 유지됩니다"
    스케줄링된 작업은 agy가 실행되는 동안 세션 간에 유지됩니다. 스케줄링된 작업을 확인하고 관리하려면 `/tasks`를 확인하세요.

---

## 4.4 — 세션 재개 <span class="duration-badge">5분</span>

> **패턴: 장기 실행 작업** — 중단한 부분부터 정확히 다시 시작합니다.
> 📖 전체 참조: [Antigravity CLI 사용하기](https://www.antigravity.google/docs/cli-using)

### 가장 최근 세션 재개

agy 내부에서 `/resume` 슬래시 명령어를 사용하세요:

```bash
/resume
```

그러면 최근 대화를 보여주는 세션 선택기가 열립니다. 재개할 세션을 선택하세요.

### 세션 찾아보기 및 전환

```bash
/switch
```

`/resume`와 동일합니다 — 두 명령어 모두 세션 선택기를 엽니다.

### 종료 시 자동 재개

agy 세션을 종료할 때, agy는 해당 세션을 재개할 수 있는 정확한 명령어를 출력합니다:

```bash
Session saved. Resume with: agy --conversation <conversation-id>
```

터미널에서 이 명령어를 직접 사용하여 다시 돌아갈 수 있습니다.

### 사용 사례: 며칠에 걸친 기능 작업

```bash
# Day 1: Start a feature
agy -i "I'm building a payment integration feature. Let's start with the backend API design."

# Day 2: Resume from terminal
agy --conversation <conversation-id>

# Or from inside agy:
# /resume
```

```text
> What was the last thing we decided about the payment API schema?
```

agy는 작성된 코드, 내려진 결정, 미해결 질문을 포함한 전체 컨텍스트를 갖게 됩니다.

---

## 4.5 — 고급: 패턴 결합 <span class="duration-badge">선택 사항</span>

> **전체 파워 스택:** 서브에이전트 + /btw + 백그라운드 + 스케줄링 + 대화 재개.

### 엔터프라이즈 사고 대응

```text
> I'm starting an incident response for a production issue. Spawn:
> 1. A log-analyzer subagent (branch mode) — read the last 1000 lines of app.log and identify the root cause
> 2. A config-checker subagent (branch mode) — review all environment configs and recent deploys for anomalies
>
> Report back when both complete. I'll be monitoring in the meantime.
```

실행되는 동안:

```bash
/btw The incident started at 14:32 UTC. Focus analysis on that window.
```

이것은 다중 에이전트 사고 트리아지입니다. 두 개의 병렬 조사가 진행되며, 실행 도중에도 방향을 조정할 수 있습니다.

---

## 모듈 4 실습

<div class="exercise-card" markdown>

### :material-file-document: 실습 4: 서브에이전트

**파일:** [`ex04_subagents.md`](exercises/ex04_subagents.md)
**소요 시간:** 20분
**목표:** 병렬 감사 팀을 생성합니다. 적대적 리뷰어 패턴을 연습합니다.

</div>

<div class="exercise-card" markdown>

### :material-file-document: 실습 5: /btw 및 스케줄링

**파일:** [`ex05_btw_scheduling.md`](exercises/ex05_btw_scheduling.md)
**소요 시간:** 20분
**목표:** /btw를 사용하여 장기 실행 작업을 스티어링합니다. 반복적인 코드 품질 보고서를 예약합니다.

</div>

<div class="exercise-card" markdown>

### :material-file-document: 실습 6: 샌드박스 거버넌스

**파일:** [`ex06_sandbox_governance.md`](exercises/ex06_sandbox_governance.md)  
**소요 시간:** 15분  
**목표:** settings.json에서 샌드박스 모드를 구성하고 권한 모델을 테스트합니다.

</div>

---

## 완료되었습니다

→ **[치트시트](cheatsheet.md)** — 4개의 모든 모듈의 모든 명령어를 한 곳에 모아두었습니다.

→ **[참조: DevOps 패턴](devops-automation.md)** — `--print` 파이프라인, CI/CD, 샌드박스 심층 분석

→ **[참조: 플러그인 생태계](plugin-ecosystem.md)** — 전체 플러그인 수명 주기 참조
