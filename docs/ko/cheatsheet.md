# agy-cli 치트시트

> 이 워크숍에서 다루는 모든 내용에 대한 빠른 참조입니다.
> 모든 명령어는 [antigravity.google/docs](https://antigravity.google/docs/cli-overview)를 기준으로 검증되었습니다.

---

## 설치 및 버전

```bash
curl -fsSL https://antigravity.google/cli/install.sh | bash
agy --help         # Show all flags and subcommands
agy changelog      # Show release notes
agy update         # Self-update
agy install        # Configure PATH and shell aliases
```

---

## 실행 모드

| 모드 | 명령어 | 사용 시기 |
| :-- | :-- | :-- |
| **대화형** | `agy` | 기본값 — 전체 대화형 세션 |
| **시드 대화형** | `agy -i "<프롬프트>"` | 지시사항으로 시작하여 대화형으로 계속 진행 |
| **출력 (헤드리스 모드)** | `agy -p "<프롬프트>"` | 단일 실행, stdout으로 파이프 |
| **마지막 세션 계속하기** | `agy -c` | 가장 최근 세션 재개 |
| **ID로 재개** | `agy --conversation <id>` | 특정 과거 세션 재개 |
| **세션 내 재개** | `/resume` 또는 `/switch` | agy를 종료하지 않고 대화 전환 |

---

## 주요 플래그

> 출처: [`agy --help`](https://antigravity.google/docs/cli-getting-started) · [cli-using](https://antigravity.google/docs/cli-using)

| 플래그 | 단축 | 설명 |
| :-- | :-- | :-- |
| `--print "<prompt>"` | `-p` | 비대화형 단일 프롬프트 |
| `--prompt-interactive "<prompt>"` | `-i` | 시드된 대화형 세션 |
| `--continue` | `-c` | 가장 최근 대화 재개 |
| `--conversation <id>` | — | 대화 ID로 재개 |
| `--add-dir <path>` | — | 작업 공간에 디렉터리 추가 (반복 가능) |
| `--sandbox` | — | 터미널 샌드박스 제한 활성화 |
| `--dangerously-skip-permissions` | — | 모든 도구 요청 자동 승인 (CI 전용) |
| `--print-timeout <duration>` | — | print 모드 시간 초과 (기본값: 5분) |
| `--log-file <path>` | — | 로그 출력 경로 재정의 |

> **참고:** 모델 선택 및 엄격 모드는 CLI 플래그가 아닌 `/model` 및 `/permissions` 슬래시 명령을 통해 설정됩니다. [기능 문서](https://antigravity.google/docs/cli-features)를 참조하세요.

---

## 슬래시 명령 (대화형 모드)

> 출처: [CLI 기능 — 핵심 슬래시 명령](https://antigravity.google/docs/cli-features) · [Antigravity CLI 사용하기](https://antigravity.google/docs/cli-using)

| 명령 | 카테고리 | 목적 |
| :-- | :-- | :-- |
| `/resume` (`/switch`) | 대화 | 대화 선택기를 열어 세션을 재개하거나 전환 |
| `/rewind` (`/undo`) | 대화 | 대화 기록을 이전 체크포인트로 롤백 |
| `/fork` | 대화 | 현재 대화를 병렬로 격리된 작업 공간으로 분기 — 원본에 영향을 주지 않고 위험한 단계를 시험 |
| `/rename <name>` | 대화 | 활성 대화 스레드의 이름 변경 |
| `/permissions` | 구성 | 자율성 수준 설정: `request-review`, `always-proceed`, `strict` |
| `/model` | 구성 | 기본 추론 모델 선택 (세션 간 유지됨) |
| `/config` (`/settings`) | 구성 | 전체 화면 설정 오버레이 열기 |
| `/keybindings` | 구성 | 대화형 키보드 단축키 편집기 열기 |
| `/statusline` | 구성 | 실시간 CLI 상태 표시줄 표시기 사용자 정의 |
| `/tasks` | 모니터링 | 백그라운드 작업 모니터링, 로그 보기 또는 종료 |
| `/skills` | 모니터링 | 로컬 및 글로벌 에이전트 스킬 탐색 |
| `/mcp` | 모니터링 | MCP 서버 구성 및 관리 |
| `/agents` | 모니터링 | 서브에이전트 작업 보기, 관리 및 승인 |
| `/open <path>` | 유틸리티 | 선호하는 외부 편집기에서 파일 열기 |
| `/usage` | 유틸리티 | 인라인 대화형 도움말 매뉴얼 열기 |
| `/logout` | 계정 | 로그아웃 및 캐시된 자격 증명 지우기 |

---

## 빠른 팁

> 출처: [Antigravity CLI 사용 — 빠른 팁 및 키 바인딩](https://antigravity.google/docs/cli-using)

| 단축키 / 팁 | 동작 |
| :-- | :-- |
| `@` | 파일 경로 자동 완성 (`@`를 입력하여 경로 제안 트리거) |
| `!` | 프롬프트에서 직접 터미널 명령어 실행 |
| `esc esc` | 프롬프트 상자 지우기 (스트리밍이 활성화되지 않은 경우) |
| `?` | 도움말 확인 및 모든 슬래시 명령어 목록 표시 |
| `alt+enter` / `shift+enter` | 제출하지 않고 줄 바꿈 삽입 |
| `ctrl+g` | 기본 셸 편집기에서 프롬프트 편집 |
| `ctrl+l` | TUI 화면 지우기 |
| `ctrl+d` | CLI 세션 종료 |
| `ctrl+z` | CLI를 터미널 백그라운드로 일시 중단 |
| `ctrl+j` (`/agents`에서) | 다음 대기 중인 서브에이전트 승인으로 이동 |
| `ctrl+k` | 메인 대화에서 대기 중인 서브에이전트 권한 빠른 승인 |

---

## 플러그인 명령어

```bash
# List all active plugins (JSON)
agy plugin list

# Import from Gemini CLI
agy plugin import gemini

# Import from Claude Code
agy plugin import claude

# Force re-import (after plugin updates)
agy plugin import gemini --force

# Install a plugin
agy plugin install <name>
agy plugin install <name>@<version>

# Enable / disable
agy plugin enable <name>
agy plugin disable <name>

# Validate a plugin directory
agy plugin validate ./my-plugin

# Generate marketplace link
agy plugin link <marketplace> <target>
```

---

## 사이드카

> AGY가 사용자를 위해 관리하는 백그라운드 프로세스입니다 — 대화와 독립적으로 실행, 재시작 및 작동합니다. 출처: [antigravity.google/docs/sidecars](https://antigravity.google/docs/sidecars)

```bash
# Config locations:
~/.gemini/config/sidecars/<name>/sidecar.json                         # global
~/.gemini/config/plugins/<plugin>/sidecars/<name>/sidecar.json        # plugin-scoped

# Enable (disabled by default) — edit ~/.gemini/config/config.json:
#   { "sidecars": { "<name>": { "enabled": true } } }

# Check logs:
ls ~/.gemini/antigravity-cli/sidecar_data/<name>/logs/

# agentapi (auto-available inside sidecars):
agentapi new-conversation "<prompt>"
agentapi send-message <conversation_id> "<prompt>"
```

최소한의 `sidecar.json` — 백그라운드 스크립트:

```json
{ "command": "python3", "args": ["worker.py"], "restart_policy": "on-failure" }
```

최소한의 `sidecar.json` — 예약된 반복 작업:

```json
{
  "builtin": "schedule",
  "args": ["0 9 * * 1-5", "agentapi", "new-conversation", "Summarise open PRs."]
}
```

---

## 작업 공간 및 컨텍스트

```bash
# Project config directory:
.agents/                    # settings.json, mcp.json, hooks.json, rules.md, skills/, plugins/

# Global config directory:
~/.gemini/config/           # settings.json, mcp.json, hooks.json, rules.md, skills/, plugins/

# User settings:
~/.gemini/antigravity-cli/settings.json

# Context file (hierarchical: cwd → parent → home):
AGENTS.md

# agy also reads:
.gemini/                    # Gemini CLI config (compatible)
```

### AGENTS.md 패턴

```markdown
# Project Context

Brief description of what this project is.

## Conventions
- Language: TypeScript, Node 20
- Testing: Jest + Supertest
- DO NOT run database migrations without explicit approval
```

---

## 유용한 패턴

```bash
# Review staged changes before commit
git diff --cached | agy -p "Review for bugs, security issues, missing tests."

# Generate docs for a file
cat src/api.ts | agy -p "Generate OpenAPI documentation for all exported functions."

# Analyze logs
tail -n 500 app.log | agy -p "Group these errors by root cause. Output as JSON."

# Multi-dir cross-repo analysis
agy --add-dir ../api --add-dir ../frontend \
    -p "Map data flow from frontend form submission to database write."

# Full headless CI audit (safe)
agy --sandbox --dangerously-skip-permissions \
    -p "Audit for hardcoded secrets and insecure patterns." \
    --print-timeout 5m > audit.md

# Schedule a recurring task (in interactive mode)
# > Schedule a daily code quality report at 9am weekdays.
```

---

## 멀티 에이전트 패턴

```text
# Spawn parallel subagents (in interactive mode)
> Spawn a security auditor and a performance auditor in parallel (branch mode).

# Adversarial review
> Spawn an adversarial reviewer subagent — its job is to find reasons to NOT merge this PR.

# Steer mid-task
/btw Focus only on the authentication module, skip the frontend.

# Background task
> In the background, audit all dependencies for known CVEs. Notify me when done.
```

---

## 인쇄 모드 파이프라인 예시

```bash
# Step 1: plan
agy -p "Create a refactoring plan for moving from callbacks to async/await. JSON output." \
  > plan.json

# Step 2: execute
cat plan.json | agy -p "Execute step 1 of this plan."

# Batch: process multiple files
for f in src/*.ts; do
  agy --add-dir "$(dirname $f)" \
      -p "Add JSDoc to all exported functions in $(basename $f)."
done
```

---

## 공식 문서

| 주제 | 링크 |
| :-- | :-- |
| CLI 개요 | [antigravity.google/docs/cli-overview](https://antigravity.google/docs/cli-overview) |
| 시작하기 | [antigravity.google/docs/cli-getting-started](https://antigravity.google/docs/cli-getting-started) |
| Antigravity CLI 사용 (설정, 팁, 키 바인딩) | [antigravity.google/docs/cli-using](https://antigravity.google/docs/cli-using) |
| 기능 (플러그인, 샌드박스, 슬래시 명령어, 서브에이전트) | [antigravity.google/docs/cli-features](https://antigravity.google/docs/cli-features) |
| Gemini CLI에서 마이그레이션 | [antigravity.google/docs/gcli-migration](https://antigravity.google/docs/gcli-migration) |
| 권한 | [antigravity.google/docs/permissions](https://antigravity.google/docs/permissions) |
| 엄격 모드 | [antigravity.google/docs/strict-mode](https://antigravity.google/docs/strict-mode) |
| 플러그인 | [antigravity.google/docs/plugins](https://antigravity.google/docs/plugins) |
| MCP | [antigravity.google/docs/mcp](https://antigravity.google/docs/mcp) |
| 스킬 | [antigravity.google/docs/skills](https://antigravity.google/docs/skills) |
| 규칙 | [antigravity.google/docs/rules-workflows](https://antigravity.google/docs/rules-workflows) |
| 훅 | [antigravity.google/docs/hooks](https://antigravity.google/docs/hooks) |
| 사이드카 | [antigravity.google/docs/sidecars](https://antigravity.google/docs/sidecars) |
| 서브에이전트 | [antigravity.google/docs/subagents](https://antigravity.google/docs/subagents) |
| 엔터프라이즈 | [antigravity.google/docs/enterprise](https://antigravity.google/docs/enterprise) |
