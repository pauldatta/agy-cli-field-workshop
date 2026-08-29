# 실습 7 — 마이그레이션 워크스루

> **모듈:** 부록 — 마이그레이션 가이드
> **소요 시간:** 20분
> **진행 방식:** 개인 또는 2인 1조

---

## 목표

실제 Gemini CLI 프로젝트 디렉터리를 살펴보고 AGY CLI로 마이그레이션합니다. 설정 파일 위치, MCP 서버 정의, 훅 이벤트 이름 및 AGENTS.md 콘텐츠를 업데이트한 다음, `migration-validator` 서브에이전트를 사용하여 유효성을 검사합니다.

---

## 배경

팀이 Gemini CLI에서 AGY CLI로 마이그레이션할 때, 네 가지 일반적인 오류 발생 지점이 있습니다:

| 오류 발생 항목 | 이유 |
| :-- | :-- |
| 훅 이벤트 `SessionStart`, `BeforeTool`, `AfterTool` | `PreInvocation`, `PreToolUse`, `PostToolUse`로 이름이 변경됨 |
| `settings.json`의 MCP `url` 키 | AGY는 별도의 `mcp.json`에서 `serverUrl`을 사용함 |
| `.gemini/` 프로젝트 설정 디렉터리 | AGY는 `.agents/`를 사용함 |
| 스크립트의 `gemini` 바이너리 | `agy`로 업데이트해야 함 |

---

## 설정

마이그레이션할 샘플 Gemini CLI 프로젝트가 필요합니다. 스타터를 생성합니다:

```bash
mkdir ~/gemini-migration-lab && cd ~/gemini-migration-lab

# Create a legacy Gemini CLI settings.json
mkdir -p .gemini/hooks
cat > .gemini/settings.json << 'EOF'
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "github-mcp-server"],
      "env": { "GITHUB_PERSONAL_ACCESS_TOKEN": "$GITHUB_TOKEN" }
    }
  },
  "hooks": {
    "SessionStart": [
      {
        "hooks": [{
          "name": "session-context",
          "type": "command",
          "command": "$GEMINI_PROJECT_DIR/.gemini/hooks/session-context.sh",
          "timeout": 3000
        }]
      }
    ],
    "BeforeTool": [
      {
        "matcher": "write_file|replace_in_file",
        "hooks": [{
          "name": "secret-scanner",
          "type": "command",
          "command": "$GEMINI_PROJECT_DIR/.gemini/hooks/secret-scanner.sh",
          "timeout": 2000
        }]
      }
    ]
  }
}
EOF

# Create a legacy GEMINI.md
cat > .gemini/GEMINI.md << 'EOF'
# Project Context

This is a Node.js API service. Always run `npm test` after changes.
Use gemini for code reviews before merging PRs.
EOF

# Create a CI script that calls the old binary
mkdir -p .github/workflows
cat > scripts/review.sh << 'EOF'
#!/usr/bin/env bash
gemini -p "Review the diff: $(git diff HEAD~1)" > review.md
EOF
```

---

## 파트 1 — 수동 마이그레이션 (10분)

프로젝트를 직접 마이그레이션하세요:

### 1단계: 설정을 AGY 디렉토리로 이동

```bash
mkdir -p .agents/hooks
# AGY reads .agents/ instead of .gemini/ for project config
cp .gemini/GEMINI.md .agents/AGENTS.md
cp .gemini/settings.json .agents/settings.json
```

### 2단계: MCP 설정 분리

```bash
# AGY uses mcp.json, not mcpServers in settings.json
cat > .agents/mcp_config.json << 'EOF'
{
  "mcpServers": {
    "github": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "github-mcp-server"],
      "env": { "GITHUB_PERSONAL_ACCESS_TOKEN": "$GITHUB_TOKEN" }
    }
  }
}
EOF
```

### 3단계: settings.json의 훅 이벤트 이름 재작성

```json
{
  "hooks": {
    "PreInvocation": [
      {
        "hooks": [{
          "name": "session-context",
          "type": "command",
          "command": "$AGY_PROJECT_DIR/.agents/hooks/session-context.sh",
          "timeout": 3000
        }]
      }
    ],
    "PreToolUse": [
      {
        "matcher": "write_file|edit",
        "hooks": [{
          "name": "secret-scanner",
          "type": "command",
          "command": "$AGY_PROJECT_DIR/.agents/hooks/secret-scanner.sh",
          "timeout": 2000
        }]
      }
    ]
  }
}
```

### 4단계: 바이너리 참조 업데이트

```bash
sed -i 's/\bgemini\b/agy/g' scripts/review.sh
```

---

## 파트 2 — 마이그레이션 검증 에이전트로 검증하기 (5분)

AGY CLI를 시작하고 마이그레이션 검증기를 실행합니다:

```bash
cd ~/gemini-migration-lab
agy
```

AGY REPL 내부에서:

```text
Use the migration-validator agent to check this project directory for any remaining Gemini CLI configuration.
```

`migration-validator` 서브에이전트가 다음을 확인합니다:

- [ ] 훅 이벤트 이름 (`SessionStart`, `BeforeTool`, `AfterTool` 없음)
- [ ] MCP 형식 (SSE용 `serverUrl`, `type` 필드 존재 여부)
- [ ] 바이너리 참조 (스크립트 내에 `gemini`가 아닌 `agy` 사용)
- [ ] 설정 경로 (`.gemini/`가 아닌 `.agents/` 사용)

---

## 파트 3 — 토론 (5분)

**생각해 볼 질문:**

1. 훅 이벤트 이름을 업데이트하는 것을 잊었다면 CI에서 가장 먼저 중단되는 것은 무엇일까요?
2. AGY는 왜 MCP 구성을 `settings.json`에 번들로 묶지 않고 `mcp.json`으로 분리할까요?
3. 10개의 프로젝트가 있는 모노레포가 있다면 마이그레이션 스크립트는 어떤 모습일까요?

---

## 보너스 챌린지

마이그레이션된 프로젝트에 에이전트가 확인 없이 `git push`를 호출하는 것을 차단하는 `PreToolUse` 훅을 추가하세요. 훅의 `decision: deny` 패턴을 사용하세요.

결정(decision) 패턴의 템플릿으로 [`samples/hooks/secret-scanner.sh`](https://github.com/pauldatta/agy-cli-field-workshop/blob/main/samples/hooks/secret-scanner.sh)를 참조하세요.

---

## 핵심 요약

| Gemini CLI | AGY CLI |
| :-- | :-- |
| `SessionStart` | `PreInvocation` |
| `BeforeTool` | `PreToolUse` |
| `AfterTool` | `PostToolUse` |
| `replace_in_file` 도구 | `edit` 도구 |
| `.gemini/` 프로젝트 디렉터리 | `.agents/` 프로젝트 디렉터리 |
| `GEMINI.md` | `AGENTS.md` |
| `settings.json` MCP 블록 | `serverUrl`이 포함된 `mcp.json` |
| SSE용 `url:` | SSE용 `serverUrl:` |
| `gemini` 바이너리 | `agy` 바이너리 |
