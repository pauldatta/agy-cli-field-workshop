# 모듈 3: SDK를 사용하여 AGY 에이전트 구축하기

<div class="module-header" markdown>
**소요 시간:** 약 90분  
**목표:** `google-antigravity` 파이썬 라이브러리를 사용하여 도구, 훅, 정책, 세션 상태, 멀티 에이전트 오케스트레이션 및 구조화된 출력을 갖춘 프로덕션 수준의 AGY 에이전트를 처음부터 구축합니다.  
**실습:** [실습 10: 첫 번째 에이전트](exercises/ex10_first_agent.md) · [실습 11: 멀티 에이전트 파이프라인](exercises/ex11_multi_agent_pipeline.md)
</div>

> 📖 출처: [SDK 개요](https://antigravity.google/docs/sdk-overview) · [google-antigravity PyPI](https://pypi.org/project/google-antigravity/) · [스킬](https://antigravity.google/docs/skills)

---

## 단순히 CLI를 사용하는 대신 에이전트를 구축하는 이유는 무엇인가요?

CLI는 **범용 어시스턴트**입니다. SDK로 구축한 에이전트는 **전문가**입니다. 좁은 범위의 작업, 도메인 특화 도구, 세심하게 엔지니어링된 시스템 프롬프트를 갖추고 있으며, 팀 전체가 호출할 수 있는 서비스로 배포될 수 있습니다.

| | Antigravity CLI | AGY SDK 에이전트 |
| :-- | :-- | :-- |
| **사용자** | 개인 개발자 | 팀 / API 소비자 |
| **커스터마이징** | AGENTS.md + 플러그인 | 전체 코드 제어 |
| **도구** | 내장 CLI 도구 | 작성한 모든 Python 함수 |
| **정책** | 대화형 승인 프롬프트 | 프로그래밍 방식의 `policy.*` 규칙 |
| **배포** | 로컬 대화형 세션 | API를 통해 호출 가능한 Cloud Run 서비스 |
| **멀티 에이전트** | CLI 세션의 서브에이전트 | `asyncio.gather` + `START_SUBAGENT` |

---

## 3.1 — SDK 설정 <span class="duration-badge">10분</span>

### 사전 요구 사항

- Python 3.11+
- Gemini API 키 — `GEMINI_API_KEY`로 설정하거나 구성에서 `api_key=`를 통해 전달합니다.

### 설치

```bash
python -m venv .venv
source .venv/bin/activate
pip install google-antigravity
```

### 확인

```python
from google.antigravity import Agent, LocalAgentConfig
from google.antigravity.hooks import policy
print("google-antigravity installed ✅")
```

> **API 키 vs Vertex AI:** 빠른 로컬 개발을 위해서는 `LocalAgentConfig`에서
> `api_key="AIza..."`를 사용하세요. GCP 프로덕션 환경의 경우,
> `gcloud auth application-default login`으로 인증하세요. 라이브러리가 ADC를 자동으로 인식합니다.

---

## 3.2 — 핵심 기본 요소: 에이전트, Config, 도구 <span class="duration-badge">20분</span>

`google-antigravity` SDK에는 `Agent`, `LocalAgentConfig`, 그리고 도구(일반 Python 함수)라는 세 가지 구성 요소가 있습니다. 이를 익히면 무엇이든 빌드할 수 있습니다.

### 도구

도구는 **일반 Python 함수**입니다. 래퍼 클래스나 데코레이터가 없습니다. 에이전트는 독스트링(docstring)을 기반으로 언제 호출할지 결정하며, 이것이 인터페이스 계약의 전부입니다.

```python
def get_file_contents(file_path: str) -> str:
    """Read and return the contents of a file at the given path.

    Args:
        file_path: Absolute or relative path to the file.

    Returns:
        The file contents as a string, or an error message if not found.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return f"Error: File not found at {file_path}"
```

> **도구에 대한 중요 규칙:**
>
> - 명시적인 타입 어노테이션(`str`, `int`, `bool`, `list[str]`)을 사용하세요. `typing.Optional`은 사용하지 마세요.
> - 선택적 매개변수에는 기본값으로 `None`을 사용하세요: `param: str = None`
> - 독스트링은 도구의 스키마입니다. 모델은 이를 읽고 도구를 언제 어떻게 호출할지 결정합니다. 사람이 아닌 모델을 위해 작성하세요.
> - 도구는 좁고 집중된 범위를 유지하세요. 도구당 하나의 작업만 수행해야 합니다.

### 세션 상태를 가진 도구

도구 내부에서 **세션 상태**를 읽거나 쓰려면 `ToolContext` 타입의 매개변수를 선언하세요.
SDK는 이를 자동 감지하여 호출 시 주입하며, **모델에 표시되는 스키마에서는 이를 제거합니다**:

```python
from google.antigravity.tools.tool_context import ToolContext

def record_finding(
    severity: str,
    message: str,
    ctx: ToolContext,
) -> dict:
    """Records a review finding into session state.

    Args:
        severity: One of 'critical', 'warning', 'info'.
        message: Description of the finding.

    Returns:
        Confirmation dict with the finding index.
    """
    findings = ctx.get_state("findings", [])
    findings.append({"severity": severity, "message": message})
    ctx.set_state("findings", findings)
    return {"status": "recorded", "index": len(findings) - 1}
```

### 에이전트 + Config

`Agent`는 단일 진입점입니다. 모든 구성은 `LocalAgentConfig`에 들어갑니다:

```python
import asyncio
from google.antigravity import Agent, LocalAgentConfig
from google.antigravity.hooks import policy

config = LocalAgentConfig(
    model="gemini-3.5-flash",
    system_instructions="""You are a code reviewer specialising in Python.
When given a file path, read the file and provide a structured review covering:
- Correctness and edge cases
- Code style and readability
- Security concerns
- Suggested improvements

Always read the file first before commenting. Be specific — cite line numbers.
""",
    tools=[get_file_contents, record_finding],
    policies=[policy.allow_all()],          # autonomous — no interactive prompts
    workspaces=["/path/to/project"],        # file ops scoped to this directory
)

async def main():
    async with Agent(config) as agent:
        response = await agent.chat("Review src/auth/login.py")
        print(await response.text())

asyncio.run(main())
```

> **`async with Agent(config) as agent:`** — 항상 컨텍스트 관리자를 사용하세요. 이는
> Go 런타임 브리지(`bin/localharness`)를 시작하고 종료 시 깔끔하게 해제합니다.

### 모델 선택

작업에 맞는 모델을 선택하세요. 비용을 고려한 정책은 다음과 같습니다:

| 역할 | 모델 | 이유 |
| :-- | :-- | :-- |
| 일반 작업, 코드 리뷰 | `gemini-3.5-flash` | SDK 기본값 — 비용 효율적, 빠름 |
| 오케스트레이션, 라우팅, 계획 수립 | `gemini-3.1-pro-preview` | 복잡한 추론, 다단계 의사 결정 |
| 이미지 생성 작업 | `gemini-3.1-flash-image-preview` | 이미지 생성을 위한 SDK 기본값 |
| 중요도가 높은 분석 | `ThinkingLevel.HIGH`가 설정된 `gemini-3.1-pro-preview` | 규정 준수/보안을 위한 심층 추론 |

> `gemini-1.5-flash`, `gemini-1.5-pro`는 **절대 사용하지 마세요**. 더 이상 사용되지 않습니다.

### 스킬

스킬은 런타임에 로드되어 도메인 지식을 주입하는 `SKILL.md` 파일입니다. 시스템 프롬프트를 간결하게 유지하고, 파일에서 전문 지식을 로드하세요:

```python
from pathlib import Path
import re

def load_skill(skill_name: str) -> str:
    """Load a SKILL.md and strip YAML frontmatter."""
    skill_path = Path("skills") / skill_name / "SKILL.md"
    if skill_path.exists():
        content = skill_path.read_text(encoding="utf-8")
        return re.sub(r'^---\n.*?---\n', '', content, flags=re.DOTALL).strip()
    return ""

review_guidelines = load_skill("python-review")

config = LocalAgentConfig(
    model="gemini-3.5-flash",
    system_instructions=f"""You are a code reviewer.

## Review Guidelines
{review_guidelines}
""",
    tools=[get_file_contents],
    policies=[policy.allow_all()],
)
```

스킬은 `LocalAgentConfig(skills_paths=["/path/to/skills/"])`를 통해 기본적으로 로드할 수도 있습니다. SDK가 `SKILL.md` 파일을 자동으로 검색합니다.

---

## 3.3 — 정책 및 안전 <span class="duration-badge">10분</span>

**정책은 가장 먼저 설정해야 하는 항목입니다.** — 이는 에이전트가 사람의 승인 없이 수행할 수 있는 작업을 제어합니다. 모든 `LocalAgentConfig`에는 `policies=` 목록이 필요합니다:

```python
from google.antigravity.hooks import policy

# Fully autonomous — approve all tool calls (use for trusted, sandboxed agents)
policies=[policy.allow_all()]

# Default behaviour — ask user before running shell commands, allow everything else
policies=[policy.confirm_run_command()]

# Fine-grained rules (evaluated in order, first match wins)
async def approval_handler(tool_call) -> bool:
    answer = input(f"Allow {tool_call.name}? [y/N]: ")
    return answer.lower() == "y"

policies=[
    policy.deny("run_command"),                 # never run shell commands
    policy.allow("view_file"),                  # always allow reading
    policy.ask_user("edit_file", handler=approval_handler),  # ask before every write
    policy.allow("*"),                          # allow everything else
]

# Conditional deny — block dangerous patterns
policy.deny("run_command", when=lambda args: "rm -rf" in args.get("CommandLine", ""))

# Scope file operations to a specific directory
policy.workspace_only(["/path/to/project"])
```

> **우선순위:** `specific_deny` > `specific_ask` > `specific_allow` > `wildcard_deny` > `wildcard_ask` > `wildcard_allow`

---

## 3.4 — 훅: 관찰 가능성 및 제어 <span class="duration-badge">10분</span>

훅을 사용하면 로깅, 감사, 가드레일 또는 사용자 지정 승인 흐름을 위해 에이전트 수명 주기의 모든 이벤트를 가로채고 반응할 수 있습니다:

```python
from google.antigravity.hooks import hooks
from google.antigravity.types import ToolCall, ToolResult, HookResult

# Block dangerous tool calls BEFORE they execute
@hooks.pre_tool_call_decide
async def security_guard(tool_call: ToolCall) -> HookResult:
    if tool_call.name == "run_command":
        cmd = tool_call.args.get("CommandLine", "")
        if any(danger in cmd for danger in ["rm -rf", "drop table", "DELETE FROM"]):
            return HookResult(allow=False)
    return HookResult(allow=True)

# Log all tool completions (non-blocking, read-only)
@hooks.post_tool_call
async def audit_logger(tool_result: ToolResult) -> None:
    print(f"[AUDIT] tool={tool_result.name} ok={tool_result.error is None}")

# Initialise state when a session begins
@hooks.on_session_start
async def initialise_state() -> None:
    print("[AGENT] Session started — ready.")

config = LocalAgentConfig(
    hooks=[security_guard, audit_logger, initialise_state],
    policies=[policy.allow_all()],
    model="gemini-3.5-flash",
    system_instructions="You are a code reviewer.",
    tools=[get_file_contents],
)
```

**훅 유형:**

| 훅 | 실행 차단 | 데이터 수정 | 용도 |
| :-- | :-- | :-- | :-- |
| `@hooks.pre_tool_call_decide` | 예 | 아니요 | 도구 호출 승인/거부 |
| `@hooks.post_tool_call` | 아니요 | 아니요 | 로깅, 지표 |
| `@hooks.pre_turn` | 아니요 | 아니요 | 턴(Turn) 수준 로깅 |
| `@hooks.post_turn` | 아니요 | 아니요 | 응답 로깅 |
| `@hooks.on_session_start/end` | 아니요 | 아니요 | 설정/정리 |
| `@hooks.on_tool_error` | 예 | 예 | 오류 복구 |

---

## 3.5 — 다중 에이전트 오케스트레이션 <span class="duration-badge">15분</span>

`google-antigravity`에는 `SequentialAgent` 또는 `ParallelAgent` 클래스가 없습니다. 다중 에이전트는 두 가지 방식으로 수행됩니다. **모델 기반(model-driven)**(에이전트가 서브에이전트를 생성하도록 함) 또는 **Python 기반(Python-driven)**(`Agent` 인스턴스를 직접 오케스트레이션함)입니다.

### 패턴 A — 모델 기반 서브에이전트

기능(capabilities)에서 `START_SUBAGENT`를 활성화합니다. 모델이 위임하기로 결정할 때 이를 호출합니다:

```python
from google.antigravity.types import BuiltinTools, CapabilitiesConfig

config = LocalAgentConfig(
    capabilities=CapabilitiesConfig(
        enable_subagents=True,
        enabled_tools=BuiltinTools.all_tools(),
    ),
    policies=[policy.allow_all()],
    model="gemini-3.1-pro-preview",
    system_instructions="""You are an engineering lead.
For complex tasks, spawn focused subagents to handle each part in parallel.
Synthesise their outputs into a final summary.""",
)
```

### 패턴 B — 순차적 파이프라인 (Python 기반)

한 에이전트의 출력을 다음 에이전트의 입력으로 전달합니다:

```python
async def sequential_review(file_path: str):
    # Step 1 — read and summarise the file
    async with Agent(reader_config) as reader:
        r1 = await reader.chat(f"Read and summarise {file_path}")
        summary = await r1.text()

    # Step 2 — security audit using the summary
    async with Agent(security_config) as auditor:
        r2 = await auditor.chat(f"Security audit this code summary:\n\n{summary}")
        report = await r2.text()

    return report
```

### 패턴 C — 병렬 분석

`asyncio.gather`를 사용하여 독립적인 에이전트들을 동시에 실행합니다:

```python
async def parallel_analysis(file_path: str):
    async with (
        Agent(security_config) as security_agent,
        Agent(style_config)    as style_agent,
        Agent(perf_config)     as perf_agent,
    ):
        results = await asyncio.gather(
            security_agent.chat(f"Security review: {file_path}"),
            style_agent.chat(f"Style review: {file_path}"),
            perf_agent.chat(f"Performance review: {file_path}"),
        )
        texts = await asyncio.gather(*[r.text() for r in results])

    return {
        "security": texts[0],
        "style":    texts[1],
        "perf":     texts[2],
    }
```

> **병렬 처리를 사용해야 할 때:** N개의 독립적인 분석이 있을 때마다 사용합니다. 이는 순차적으로 실행할 때와 비교하여 실제 소요 시간(wall-clock time)을 60~80% 단축합니다.

---

## 3.6 — 스트리밍 및 구조화된 출력 <span class="duration-badge">5분</span>

### 스트리밍 응답

```python
async with Agent(config) as agent:
    response = await agent.chat("Write a detailed security report...")

    # Stream text deltas as they arrive
    async for delta in response:
        print(delta, end="", flush=True)

    # Stream reasoning/thinking (if thinking enabled)
    async for thought in response.thoughts:
        print(f"[thinking] {thought}")
```

### 구조화된 출력

에이전트의 출력을 Pydantic 스키마에 바인딩합니다:

```python
import asyncio
import pydantic
from google.antigravity import Agent, LocalAgentConfig
from google.antigravity.hooks import policy

class ReviewResult(pydantic.BaseModel):
    issues: list[str]
    severity: str          # 'critical' | 'warning' | 'info'
    recommendation: str

config = LocalAgentConfig(
    response_schema=ReviewResult,
    system_instructions="Analyse the code and return structured output via the finish tool.",
    policies=[policy.allow_all()],
    model="gemini-3.5-flash",
    tools=[get_file_contents],
)

async def main():
    async with Agent(config) as agent:
        response = await agent.chat("Review src/auth/login.py")
        result = await response.structured_output()   # dict matching ReviewResult schema
        print(result["severity"], result["issues"])

asyncio.run(main())
```

---

## 3.7 — 세션 재개 및 지속성 <span class="duration-badge">5분</span>

```python
# First session — save the conversation ID
async with Agent(config) as agent:
    await agent.chat("Analyse this codebase and build a mental model.")
    conv_id = agent.conversation_id   # persist this

# Later session — resume exactly where you left off
resume_config = LocalAgentConfig(
    conversation_id=conv_id,
    save_dir="/path/where/first/session/was/saved",
    model="gemini-3.5-flash",
    policies=[policy.allow_all()],
)
async with Agent(resume_config) as agent:
    await agent.chat("Now suggest the top 3 refactoring priorities.")
```

---

## 3.8 — 트리거: 자율 백그라운드 에이전트 <span class="duration-badge">5분</span>

```python
import asyncio
from google.antigravity import Agent, LocalAgentConfig
from google.antigravity.hooks import policy
from google.antigravity.triggers import every, on_file_change, TriggerContext

# Poll every 60 seconds
async def check_for_new_issues(ctx: TriggerContext) -> None:
    await ctx.send("Scan the repo for any new TODO comments added since last run.")

# React to file changes
async def on_code_change(ctx: TriggerContext, changes) -> None:
    paths = [c.path for c in changes]
    await ctx.send(f"Files changed: {paths}. Run quick security check.")

config = LocalAgentConfig(
    triggers=[
        every(60.0, check_for_new_issues),
        on_file_change("/path/to/src", on_code_change),
    ],
    policies=[policy.allow_all()],
    model="gemini-3.5-flash",
    system_instructions="You are a background code monitor.",
)

async def main():
    # The agent runs indefinitely, responding to triggers
    async with Agent(config) as agent:
        await asyncio.Event().wait()  # keep alive

asyncio.run(main())
```

---

## 3.9 — 프로젝트 구조 컨벤션 <span class="duration-badge">5분</span>

유지보수성을 위해 에이전트 프로젝트를 다음과 같이 구조화하세요:

```text
my_agent/
├── main.py                   # entry point — asyncio.run(main())
├── config.py                 # LocalAgentConfig construction
├── tools/
│   ├── __init__.py
│   ├── file_reader.py        # one tool per file
│   └── search_tool.py
├── hooks/
│   ├── __init__.py
│   └── security_guard.py     # pre_tool_call_decide hooks
├── skills/
│   └── domain-expertise/
│       └── SKILL.md          # portable skill packs
├── tests/
│   ├── test_file_reader.py
│   └── test_search_tool.py
├── requirements.txt          # google-antigravity + deps
└── README.md
```

### Cloud Run에 배포

표준 Python 비동기 애플리케이션으로 배포합니다:

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "main.py"]
```

```bash
gcloud run deploy my-code-reviewer \
  --source . \
  --project $GOOGLE_CLOUD_PROJECT \
  --region $GOOGLE_CLOUD_REGION \
  --allow-unauthenticated
```

> **팁:** 실행하기 전에 `GOOGLE_CLOUD_PROJECT` 및 `GOOGLE_CLOUD_REGION`(예: `us-central1`)을 설정하세요.

---

## 실습 과제

<div class="exercise-card" markdown>

### :material-code-braces: 연습문제 10: 첫 번째 AGY 에이전트

**파일:** [`ex10_first_agent.md`](exercises/ex10_first_agent.md)  
**소요 시간:** 45분  
**구축:** 파일을 읽고, 문제를 식별하며, 구조화된 리뷰 보고서를 생성하는 **코드 리뷰 에이전트(Code Review Agent)**.

**구현할 내용:**

1. 3개의 도구 정의: `read_file`, `list_directory`, `record_finding` (`ToolContext` 사용)
2. 리뷰 루브릭이 포함된 시스템 프롬프트 작성 (`SKILL.md`에서 로드됨)
3. `policy.allow_all()` 및 `CapabilitiesConfig`를 사용하여 `LocalAgentConfig` 구성
4. `@hooks.pre_tool_call_decide` 보안 가드 추가
5. 스트리밍 출력 및 구조화된 `ReviewResult` Pydantic 스키마로 실행

</div>

<div class="exercise-card" markdown>

### :material-graph: 연습문제 11: 멀티 에이전트 파이프라인

**파일:** [`ex11_multi_agent_pipeline.md`](exercises/ex11_multi_agent_pipeline.md)  
**소요 시간:** 45분  
**구축:** **작성 후 감사(Write-then-Audit) 파이프라인** — 테크니컬 라이터(Technical Writer) 에이전트가 문서를 생성한 다음, 컴플라이언스 분석가(Compliance Analyst)가 GDPR 위반 사항이 있는지 감사합니다.

**구현할 내용:**

1. `skills_paths`를 통해 로드된 GDPR `SKILL.md`를 사용하여 `technical_writer` 에이전트 구축
2. `response_schema=ComplianceReport`를 사용하여 `compliance_analyst` 에이전트 구축
3. 순차적으로 연결: 작성자의 출력이 분석가의 입력으로 전달됨
4. 동시 초안 작성 및 법률 검토를 위해 `asyncio.gather`를 사용하는 병렬 변형 추가
5. 세션 재개 추가: 분석가가 작성자의 `conversation_id`를 읽어 컨텍스트를 로드함
6. `gcloud run deploy`를 사용하여 `my-pipeline`으로 Cloud Run에 배포

</div>

---

## 요약: SDK 빌딩 블록

| 기본 요소 | 기능 | 사용 시기 |
| :-- | :-- | :-- |
| `Agent` | 도구, 훅, 정책을 갖춘 단일 LLM 에이전트 | 핵심 요소 — 모든 에이전트는 여기서 시작됨 |
| `LocalAgentConfig` | 한 곳에 모인 모든 설정 (모델, 도구, 정책, 훅) | 항상 |
| `tools=[fn]` | 일반 Python 콜러블, 독스트링(docstring)이 스키마가 됨 | 모든 외부 작업 |
| `ToolContext` | 도구에 주입되는 상태 읽기/쓰기 | 파이프라인 내의 상태 저장(Stateful) 도구 |
| `policy.allow_all()` | 모든 도구 호출을 자율적으로 승인 | 신뢰할 수 있는 샌드박스 처리된 에이전트 |
| `policy.deny("run_command")` | 특정 도구 유형 차단 | 안전 가드레일 |
| `@hooks.pre_tool_call_decide` | 실행 전 도구 호출 차단/승인 | 보안 가드 |
| `@hooks.post_tool_call` | 완료된 도구 호출 관찰 | 감사 로깅 |
| `response_schema=` | 출력을 Pydantic 스키마에 바인딩 | 구조화된 데이터 추출 |
| `async for delta in response:` | 텍스트가 도착하는 대로 스트리밍 | 장문 생성 |
| `asyncio.gather(...)` | 에이전트를 병렬로 실행 | 독립적인 분석 |
| `every(60, handler)` | 주기적으로 에이전트 트리거 | 백그라운드 모니터 |
| `on_file_change(path, fn)` | 파일 시스템 이벤트 발생 시 에이전트 트리거 | 실시간 코드 감시자 |
| `skills_paths=[...]` | 런타임에 SKILL.md 파일 로드 | 이식 가능한 도메인 전문 지식 |
| `conversation_id=` | 이전 세션 재개 | 다중 세션 워크플로우 |

---

## 다음 단계

→ **[모듈 4: 멀티 에이전트 및 고급 패턴](multi-agent-advanced.md)**으로 계속 진행합니다.

→ 참고: **[치트시트](cheatsheet.md)** — 모든 명령어를 한곳에서 확인하세요.
