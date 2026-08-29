# 모듈 1: SDLC 생산성 향상 <span class="duration-badge">75분</span>

> **첫 번째 실제 Antigravity CLI 세션입니다.** 이 모듈에서는 코드 이해, 리팩토링, 테스트 생성 및 변경 사항 검토와 같은 핵심적인 일상 워크플로우를 다루며, 팀의 툴체인을 위한 플러그인으로 CLI를 확장하는 방법도 알아봅니다.

---

## 1.0 — 첫 번째 대화형 세션 <span class="duration-badge">5분</span>

워크숍 프로젝트 디렉터리에서 Antigravity CLI를 실행합니다:

```bash
cd agy-cli-field-workshop
agy
```

대화형 프롬프트로 진입하게 됩니다. 다음을 시도해 보세요:

```text
> What files are in this project and what does each one do?
```

agy가 작업 공간을 어떻게 읽는지 관찰해 보세요. git 저장소를 인덱싱하고, 파일 내용을 읽으며, 컨텍스트를 바탕으로 응답합니다. 이는 **자동**으로 이루어집니다. 별도의 설정이나 사전에 작성해야 할 프롬프트가 없습니다.

!!! tip ".agents/ 폴더"
    첫 번째 세션 이후 `.agents/`를 확인해 보세요. agy가 작업 공간을 추적하는 프로젝트 설정 파일을 생성했습니다. 이를 통해 향후 실행 시 무엇을 인덱싱할지 알 수 있습니다.

---

## 1.1 — 코드 이해 <span class="duration-badge">10분</span>

> **패턴: 수정 전 설명** — 코드를 변경하기 전에 먼저 이해하세요.

### 실습: 낯선 코드베이스 파악하기

```bash
# -i seeds the session with an initial prompt and stays interactive
agy -i "Give me a high-level architecture overview of this project. What are the main components and how do they connect?"
```

그런 다음 대화형으로 후속 질문을 이어나갑니다:

```text
> Which file handles the entry point?
> What external dependencies does this project have?
> Are there any obvious code smells or tech debt?
```

!!! tip "시드 세션에 -i 사용하기"
    `agy -i "<task>"`(`--prompt-interactive`의 약어)는 프롬프트로 시작하지만 대화형 상태를 유지합니다. 방향성 있는 탐색에 매우 유용합니다. 방향을 설정한 다음 후속 질문으로 이끌어갈 수 있습니다.

---

## 1.2 — 리팩토링 <span class="duration-badge">10분</span>

> **패턴: 제안, 검토, 적용** — 읽지 않은 변경 사항은 절대 적용하지 마세요.

### 실습: 타겟 리팩토링

```bash
agy
```

```text
> I want to refactor the error handling in this project. First, show me all the places where errors are currently caught or returned — don't change anything yet.
```

결과를 검토하세요. 그런 다음:

```text
> Now propose a refactored version of [specific function] using a consistent error handling pattern. Show me the diff before applying.
```

제안된 변경 사항을 읽은 후에만 적용하세요.

### 권한 모델

agy는 도구 승인 처리 방식을 제어하는 **3단계 권한 모델**을 가지고 있습니다:

| 레벨 | 동작 |
| :-- | :-- |
| `request-review` | **기본값.** agy는 파일을 작성하거나 명령을 실행하기 전에 승인을 요청합니다 |
| `always-proceed` | 모든 도구 호출을 자동 승인합니다 — 신뢰할 수 있는 스크립트 및 CI에 유용합니다 |
| `strict` | 명시적으로 허용되지 않는 한 모든 도구 사용을 거부합니다 — 최대 제어 |

`/permissions` 슬래시 명령을 사용하여 현재 레벨을 보거나 변경하세요. `settings.json`에서 세분화된 규칙을 설정할 수도 있습니다:

```json
{
  "permissions": {
    "allow": ["command(git)", "read_file"],
    "deny": ["command(rm -rf)"]
  }
}
```

> 📖 전체 세부 정보: [권한 문서](https://www.antigravity.google/docs/permissions) · [엄격 모드 문서](https://www.antigravity.google/docs/strict-mode)

---

## 1.3 — 테스트 생성 <span class="duration-badge">10분</span>

> **패턴: 존재하는 것 테스트하기** — 가상의 코드가 아닌 실제 코드에 대한 테스트를 생성합니다.

### 실습: 단위 테스트 생성

```bash
agy
```

```text
> Look at [specific function or file]. Generate a comprehensive unit test suite for it. Include happy path, edge cases, and error conditions. Use the testing framework already in this project.
```

그런 다음:

```text
> Run the tests and fix any that fail.
```

!!! tip "agy가 테스트를 실행하도록 하기"
    agy는 셸 명령을 실행할 수 있습니다. 오류 메시지를 복사하여 붙여넣을 필요 없이 테스트 도구 모음을 실행하고 실패 시 반복 작업을 수행합니다. 스스로 수정하는 과정을 지켜보세요.

---

## 1.4 — 코드 리뷰 <span class="duration-badge">10분</span>

> **패턴: 커밋 전 리뷰(Pre-Commit Review)** — 모든 푸시 전에 agy를 시니어 리뷰어로 사용하세요.

### 실습: 변경 사항 리뷰하기

```bash
# Stage some changes (or use an existing branch)
git add -p

# Start agy and review what's staged
agy
```

```text
> Review my staged changes for: (1) correctness, (2) security issues, (3) missing test coverage, (4) anything that would block a PR. Be direct — don't soften findings.
```

### 헤드리스 변형 (스크립팅용)

```bash
# Review changes non-interactively — useful in pre-commit hooks or CI
git diff --cached | agy --print "Review these changes. Flag any bugs, security issues, or missing tests. Output as markdown."
```

---

## 1.5 — AGENTS.md를 사용한 프로젝트 컨텍스트 <span class="duration-badge">5 min</span>

> **패턴: 영구 컨텍스트(Persistent Context)** — agy에게 한 번 알려주면 모든 세션에서 기억합니다.

agy는 세션 시작 시 컨텍스트 파일을 읽습니다. 프로젝트 루트에 하나를 생성하세요:

```bash
cat > AGENTS.md << 'EOF'
# Project Context

This is a Node.js REST API built with Express and TypeScript.

## Key Conventions
- Language: TypeScript (strict mode, no `any`)
- Testing: Jest with 80% coverage minimum; run `npm test` to validate
- Style: ESLint + Prettier; run `npm run lint` before committing
- DO NOT modify `src/db/migrations/` — those are append-only
- DO NOT use `console.log` in production code; use the `logger` utility

## Architecture
Three-layer: `routes/` → `services/` → `repositories/`. All DB access goes through the repository layer. External HTTP calls go through `src/clients/`.

## Common Commands
- `npm run dev` — start local dev server on :3000
- `npm test` — run full test suite
- `npm run db:migrate` — apply pending DB migrations
EOF
```

이제 새 세션을 시작하세요:

```bash
agy --print "What do you know about this project?"
```

agy는 이후의 모든 세션에 AGENTS.md를 자동으로 포함합니다.

!!! info "컨텍스트 계층 구조"
    agy는 현재 디렉토리 → 상위 디렉토리 → 홈 디렉토리 순으로 AGENTS.md를 읽습니다. 더 구체적인 컨텍스트가 광범위한 컨텍스트를 재정의합니다.

### 추가 컨텍스트 소스

AGENTS.md 외에도 agy는 다음을 로드합니다:

- **`.agents/rules.md`** (또는 `.agents/rules/*.md`) — 시스템 프롬프트 지시문으로 주입되는 프로젝트 수준 규칙입니다. "마이그레이션 파일을 절대 삭제하지 마세요" 또는 "항상 TypeScript 엄격 모드를 사용하세요"와 같은 필수 요구 사항에 이를 사용하세요.
- **`.gemini/`** — Gemini CLI 호환성을 위해 agy는 `.agents/`와 함께 `.gemini/` 디렉토리를 읽습니다.
- **`~/.gemini/config/rules.md`** — 모든 세션에 적용되는 전역 규칙입니다.

> 📖 전체 세부 정보: [규칙 및 워크플로우 문서](https://www.antigravity.google/docs/rules-workflows)

### 샘플 에이전트 정의 (`samples/agents/` 내)

| 에이전트 | 모델 | 목적 |
| :-- | :-- | :-- |
| `doc-writer.md` | `gemini-3.5-flash` | 소스에서 API 문서, README 섹션 및 인라인 주석을 생성합니다 |
| `pr-reviewer.md` | `gemini-3.5-flash` | 품질, 버그 및 스타일 위반에 대한 코드 변경 사항을 검토합니다 |
| `migration-validator.md` | `gemini-3.5-flash` | Gemini CLI → Antigravity CLI 마이그레이션 완료 여부를 검증합니다 |

---

## 1.6 — 대화형 탐색 <span class="duration-badge">5 min</span>

> **패턴: 터미널 숙련도** — agy 세션을 빠르게 만드는 단축키를 알아두세요.
> 📖 전체 참조: [Antigravity CLI 사용하기](https://www.antigravity.google/docs/cli-using)

### 주요 슬래시 명령어

| 명령어 | 기능 |
| :-- | :-- |
| `/rewind` (또는 `/undo`) | 대화 기록을 이전 체크포인트로 롤백합니다 |
| `/resume` (또는 `/switch`) | 대화 선택기를 열어 세션을 재개하거나 전환합니다 |
| `/rename <name>` | 활성 대화 스레드의 이름을 변경합니다 |
| `/config` (또는 `/settings`) | 전체 화면 설정 오버레이를 엽니다 |
| `/permissions` | 에이전트 자율성 수준을 설정합니다 (`request-review`, `always-proceed`, `strict`) |
| `/model` | 추론 모델을 선택합니다 (세션 간 유지됨) |
| `/tasks` | 백그라운드 작업을 모니터링하거나, 로그를 보거나, 종료합니다 |
| `/agents` | 서브에이전트 작업을 보고, 관리하고, 승인합니다 |
| `/open <path>` | 선호하는 외부 편집기에서 파일을 엽니다 |
| `/usage` | 인라인 대화형 도움말 매뉴얼을 엽니다 |
| `/skills` | 로컬 및 글로벌 에이전트 스킬을 찾아봅니다 |
| `/mcp` | MCP 서버를 구성하고 관리합니다 |

> 📖 전체 슬래시 명령어 참조: [CLI 기능](https://antigravity.google/docs/cli-features)

### 빠른 팁

| 단축키 | 기능 |
| :-- | :-- |
| `@` | 파일 경로 자동 완성 — `@`를 입력하여 경로 제안을 트리거합니다 |
| `!` | agy를 종료하지 않고 터미널 명령어를 직접 실행합니다 |
| `esc esc` | 현재 프롬프트 입력을 지웁니다 (스트리밍이 활성화되지 않은 경우) |
| `?` | 도움말을 확인하고 모든 슬래시 명령어를 나열합니다 |
| `alt+enter` / `ctrl+j` / `shift+enter` | 프롬프트에 줄바꿈을 삽입합니다 (여러 줄 입력) |
| `ctrl+g` | 기본 셸 편집기에서 프롬프트를 편집합니다 |
| `ctrl+l` | TUI 화면을 지웁니다 |
| `ctrl+d` | CLI를 종료합니다 |

> 📖 전체 키 바인딩 참조: [Antigravity CLI 사용하기](https://antigravity.google/docs/cli-using)

---

## 1.7 — 플러그인으로 확장하기 <span class="duration-badge">15분</span> {: #17-extend-with-plugins-15-min }

> **패턴: 자체 툴체인 가져오기** — 플러그인은 agy에 스킬, MCP 서버, 에이전트 및 규칙을 추가합니다. 한 번 설치하면 모든 세션에서 사용할 수 있습니다.

Antigravity CLI의 플러그인 시스템은 특별한 기능을 수행합니다. 재설치나 재구성 없이 **Gemini CLI에 이미 설치한 플러그인을 가져올 수 있습니다**. 기존의 투자가 그대로 이어집니다.

### 활성화된 항목 확인하기

```bash
agy plugin list
```

각 플러그인의 이름, 소스, 가져오기 날짜 및 구성 요소(스킬, 명령어, mcpServers, 에이전트)를 보여줍니다.

### Gemini CLI에서 가져오기

```bash
agy plugin import gemini
```

agy는 로컬 Gemini CLI 설치를 스캔하고, 설치된 모든 플러그인을 발견하여 해당 구성 요소를 `~/.gemini/antigravity-cli/`에 스테이징합니다. 출력:

```text
  [ok]    code-review
          ✔ skills      : 3 processed
          ✔ commands    : 2 processed
          - mcpServers  : skipped (not found)
  [ok]    gemini-deep-research
          ✔ commands    : 1 processed
          ✔ mcpServers  : 1 processed
  [skip]  superpowers (already imported)
```

!!! warning "사용자 지정 테마는 조용히 무시됩니다"
    사용자 지정 테마 구성 요소는 agy의 모델로 1:1 마이그레이션할 수 없으며 가져오는 동안 오류 없이 건너뜁니다. 테마가 워크플로우에 중요한 경우 가져오기 후 활성화된 플러그인을 확인하세요.

!!! tip "플러그인 업데이트 후 다시 가져오기"
    이미 가져온 플러그인은 기본적으로 건너뜁니다. 강제로 다시 가져오기:
    ```bash
    agy plugin import gemini --force
    ```

### What Gets Imported

| Component | What it means |
| :-- | :-- |
| `skills` | SKILL.md files — injected as domain expertise into agy sessions |
| `commands` | Slash commands available inside agy sessions |
| `mcpServers` | MCP tool servers (GitHub, gcloud, Workspace, etc.) |
| `agents` | Custom subagent definitions |
| `rules` | Rules files injected as system prompt directives |
| `hooks` | Staged but not auto-executed — agy handles lifecycle differently |

### Enable / Disable Per-Project

Not every plugin is appropriate for every codebase:

```bash
# 이 프로젝트에 대해 비활성화
agy plugin disable gemini-deep-research

# 다시 활성화
agy plugin enable gemini-deep-research
```

### Plugin Locations

| Scope | Path |
| :-- | :-- |
| **Global** | `~/.gemini/antigravity-cli/plugins/` |
| **Project** | `.agents/plugins/` |

### Building a Custom Plugin

A valid agy plugin needs a `plugin.json` manifest:

```text
my-plugin/
├── plugin.json          ← 필수
├── mcp_config.json      ← MCP 서버 정의 (선택 사항)
├── hooks.json           ← 훅 이벤트 핸들러 (선택 사항)
├── skills/              ← SKILL.md 파일 (선택 사항)
│   └── my-skill/
│       └── SKILL.md
├── agents/              ← 서브에이전트 정의 (선택 사항)
└── rules/               ← 규칙 파일 (선택 사항)
    └── my-rules.md
```

```json
{
  "name": "my-plugin",
  "version": "1.0.0",
  "description": "내 사용자 지정 agy 플러그인",
  "components": ["skills"]
}
```

Validate it before shipping:

```bash
agy plugin validate ./my-plugin
# ✔ 플러그인 매니페스트가 유효합니다
```

> 📖 전체 참조: [플러그인](https://www.antigravity.google/docs/plugins) · [마이그레이션 가이드](https://www.antigravity.google/docs/gcli-migration)

---

## 모듈 1 실습

<div class="exercise-card" markdown>

### :material-file-document: 실습 1: 첫 번째 세션

**파일:** [`ex01_first_session.md`](exercises/ex01_first_session.md)  
**소요 시간:** 15분  
**목표:** agy를 실행하고, 코드베이스를 탐색하며, AGENTS.md를 생성합니다.

</div>

<div class="exercise-card" markdown>

### :material-puzzle: 실습 2: 플러그인 브리지

**파일:** [`ex02_plugin_bridge.md`](exercises/ex02_plugin_bridge.md)  
**소요 시간:** 20분  
**목표:** Gemini CLI에서 플러그인을 가져오고, 선택적으로 활성화/비활성화하며, 사용자 지정 플러그인을 검증합니다.

</div>

---

## 다음 모듈

→ **[모듈 2: 레거시 코드베이스 현대화](legacy-modernization.md)** — 엄격 모드, 에이전트 셀프 온보딩, 서브에이전트, 그리고 안전망 역할을 하는 `/rewind`.
