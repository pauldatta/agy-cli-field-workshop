# 실습 10: 첫 번째 AGY 에이전트

> **소요 시간:** 45분 | **모듈:** 3 — AGY 에이전트 구축

---

## 목표

`google-antigravity` Python SDK를 사용하여 **코드 리뷰 에이전트**를 구축합니다. 이 에이전트는 파일을 읽고, 문제를 식별하며, 구조화된 리뷰 보고서를 생성합니다. 이 모든 과정은 쓰기를 차단하는 보안 가드 훅과 함께 자율적으로 실행됩니다.

---

## 설정

```bash
# Create project directory
mkdir -p ~/agy-review-agent/tools ~/agy-review-agent/hooks ~/agy-review-agent/skills/python-review

# Set up Python environment
cd ~/agy-review-agent
python3 -m venv .venv
source .venv/bin/activate
pip install google-antigravity pydantic
```

API 키를 설정하세요:

```bash
export GEMINI_API_KEY="your-api-key-here"
```

---

## 파트 1: 도구 정의 (10분)

두 개의 읽기 전용 도구를 포함하여 `tools/file_tools.py`를 생성합니다:

```python
import os


def read_file(file_path: str) -> str:
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
    except PermissionError:
        return f"Error: Permission denied reading {file_path}"


def list_directory(directory_path: str) -> str:
    """List files and subdirectories at the given path.

    Args:
        directory_path: Path to the directory to list.

    Returns:
        A formatted string listing all entries, or an error message.
    """
    try:
        entries = sorted(os.listdir(directory_path))
        result_lines = []
        for entry in entries:
            full_path = os.path.join(directory_path, entry)
            kind = "dir" if os.path.isdir(full_path) else "file"
            size = os.path.getsize(full_path) if kind == "file" else ""
            result_lines.append(f"  [{kind}] {entry}" + (f"  ({size} bytes)" if size else ""))
        return f"Contents of {directory_path}:\n" + "\n".join(result_lines)
    except FileNotFoundError:
        return f"Error: Directory not found at {directory_path}"
```

`ToolContext`를 사용하는 상태 저장(stateful) 도구를 포함하여 `tools/state_tools.py`를 생성합니다:

```python
from google.antigravity.tools.tool_context import ToolContext


def record_finding(
    severity: str,
    message: str,
    file_path: str,
    line_number: int = None,
    ctx: ToolContext = None,
) -> dict:
    """Records a code review finding into session state.

    Args:
        severity: One of 'critical', 'warning', 'info'.
        message: Description of the finding.
        file_path: The file where the issue was found.
        line_number: Optional line number of the finding.

    Returns:
        Confirmation dict with the finding index.
    """
    finding = {
        "severity": severity,
        "message": message,
        "file_path": file_path,
        "line_number": line_number,
    }
    findings = ctx.get_state("findings", [])
    findings.append(finding)
    ctx.set_state("findings", findings)
    return {"status": "recorded", "index": len(findings) - 1, "total": len(findings)}
```

> **핵심 개념:** `ctx: ToolContext` 매개변수는 호출 시 SDK에 의해 자동으로 주입되며 모델에 표시되는 스키마에서는 제거됩니다. 모델은 이를 전혀 볼 수 없으며, 단지 `record_finding(severity, message, file_path)`를 호출할 뿐입니다.

---

## 파트 2: 리뷰 스킬 작성 (5분)

`skills/python-review/SKILL.md` 파일을 생성합니다:

```text
---
name: python-review
description: Code review rubric for Python projects
---

## Python Code Review Rubric

When reviewing Python code, evaluate against these criteria:

### Correctness
- Are there logic errors or off-by-one bugs?
- Are edge cases handled (empty inputs, None values, large datasets)?
- Are exceptions caught and handled appropriately?

### Security
- Are there hardcoded secrets, API keys, or credentials?
- Is user input sanitised before use in SQL, shell commands, or file paths?
- Are there unsafe uses of `eval()`, `exec()`, or `pickle.loads()`?

### Code Quality
- Does the code follow PEP 8 style conventions?
- Are functions focused (single responsibility)?
- Are variable names descriptive and consistent?
- Are there unnecessary comments or dead code?

### Performance
- Are there N+1 query patterns or repeated expensive operations?
- Are large files read entirely into memory when streaming would suffice?
- Are there blocking calls in async code?

### Severity Classification
- **critical**: Security vulnerabilities, data loss risks, crashes
- **warning**: Logic bugs, performance issues, missing error handling
- **info**: Style issues, minor improvements, documentation gaps
```

---

## 파트 3: 에이전트 구성 (10분)

`config.py`를 생성합니다:

```python
from pathlib import Path
import re

from google.antigravity import LocalAgentConfig
from google.antigravity.hooks import policy
from google.antigravity.types import CapabilitiesConfig

from tools.file_tools import read_file, list_directory
from tools.state_tools import record_finding


def load_skill(skill_name: str) -> str:
    """Load a SKILL.md and strip YAML frontmatter."""
    skill_path = Path("skills") / skill_name / "SKILL.md"
    if skill_path.exists():
        content = skill_path.read_text(encoding="utf-8")
        return re.sub(r"^---\n.*?---\n", "", content, flags=re.DOTALL).strip()
    return ""


review_rubric = load_skill("python-review")

agent_config = LocalAgentConfig(
    model="gemini-3.5-flash",
    system_instructions=f"""You are a senior Python code reviewer.

Your job:
1. Use `list_directory` to understand the project structure
2. Use `read_file` to read each relevant source file
3. For every issue found, call `record_finding` with severity, message, file path, and line number
4. After reviewing all files, provide a final summary

Always read files before commenting. Be specific — cite line numbers.
Never guess at code contents. If you can't read a file, say so.

## Review Rubric
{review_rubric}
""",
    tools=[read_file, list_directory, record_finding],
    capabilities=CapabilitiesConfig(
        enable_subagents=False,
    ),
    policies=[policy.allow_all()],
)
```

---

## 파트 4: 보안 가드 훅 추가 (5분)

`hooks/security_guard.py`를 생성합니다:

```python
from google.antigravity.hooks import hooks
from google.antigravity.types import ToolCall, HookResult

# Tools that could modify the filesystem
WRITE_TOOLS = {BuiltinTools.CREATE_FILE, BuiltinTools.EDIT_FILE, BuiltinTools.RUN_COMMAND}


@hooks.pre_tool_call_decide
async def block_writes(tool_call: ToolCall) -> HookResult:
    """Block any tool call that could modify files.

    This agent is read-only — it reviews code but never changes it.
    """
    if tool_call.name in WRITE_TOOLS:
        return HookResult(
            allow=False,
            message=f"Blocked: {tool_call.name} is not allowed. This agent is read-only.",
        )

    if tool_call.name == "run_command":
        cmd = tool_call.args.get("CommandLine", "")
        if any(danger in cmd for danger in ["rm ", "mv ", "chmod", "chown", "dd "]):
            return HookResult(
                allow=False,
                message=f"Blocked dangerous command: {cmd}",
            )

    return HookResult(allow=True)
```

> **이것이 중요한 이유:** `policy.allow_all()`을 사용하더라도, 모든 도구 호출 전에 훅이 실행되어 이를 거부할 수 있습니다. 심층 방어(Defense in depth) — 정책은 기준선을 설정하고, 훅은 가드레일을 적용합니다.

---

## 파트 5: 스트리밍 + 구조화된 출력으로 모두 연결하기 (15분)

`main.py`를 생성합니다:

```python
import asyncio
import pydantic
from google.antigravity import Agent

from config import agent_config
from hooks.security_guard import block_writes


class ReviewFinding(pydantic.BaseModel):
    severity: str
    message: str
    file_path: str
    line_number: int = None


class ReviewResult(pydantic.BaseModel):
    summary: str
    findings: list[ReviewFinding]
    files_reviewed: list[str]
    overall_health: str  # 'healthy', 'needs-attention', 'critical'


async def run_review(target_path: str):
    """Run a code review with streaming output, then extract structured result."""

    # Add the hook to the config
    config = agent_config.model_copy(
        update={
            "hooks": [block_writes],
        }
    )

    print(f"=== Code Review: {target_path} ===\n")

    # Phase 1: Streaming review (human-readable output)
    async with Agent(config) as agent:
        response = await agent.chat(
            f"Review all Python files in {target_path}. "
            f"Use record_finding for each issue. Then provide a summary."
        )

        # Stream the response as it arrives
        async for delta in response:
            print(delta, end="", flush=True)

        print("\n\n=== Structured Report ===\n")

    # Phase 2: Structured extraction
    structured_config = agent_config.model_copy(
        update={
            "response_schema": ReviewResult,
            "hooks": [block_writes],
        }
    )

    async with Agent(structured_config) as agent:
        response = await agent.chat(
            f"Review all Python files in {target_path}. "
            f"Return your findings as structured output."
        )
        result = await response.structured_output()

        print(f"Overall Health: {result['overall_health']}")
        print(f"Files Reviewed: {len(result['files_reviewed'])}")
        print(f"Findings: {len(result['findings'])}")
        for finding in result["findings"]:
            icon = {"critical": "🔴", "warning": "🟡", "info": "🔵"}.get(
                finding["severity"], "⚪"
            )
            loc = f":{finding['line_number']}" if finding.get("line_number") else ""
            print(f"  {icon} [{finding['severity']}] {finding['file_path']}{loc}")
            print(f"     {finding['message']}")


if __name__ == "__main__":
    import sys

    target = sys.argv[1] if len(sys.argv) > 1 else "."
    asyncio.run(run_review(target))
```

### 실행하기

```bash
# Review the agent's own code (meta!)
python main.py .

# Review a specific project directory
python main.py /path/to/your/project/src
```

---

## 완료 기준

- [ ] 3개의 도구 정의됨: `read_file`, `list_directory`, `record_finding` (`ToolContext` 포함)
- [ ] 파이썬 리뷰 루브릭이 포함된 `SKILL.md` 생성됨
- [ ] `policy.allow_all()` 및 도구 목록을 사용하여 `LocalAgentConfig` 구성됨
- [ ] `@hooks.pre_tool_call_decide` 보안 가드가 쓰기 작업을 차단함
- [ ] 에이전트가 실행되고 콘솔로 출력을 스트리밍함
- [ ] 발견된 문제, 심각도 수준 및 전반적인 상태가 포함된 구조화된 `ReviewResult`가 반환됨
- [ ] 에이전트가 하나 이상의 파이썬 파일을 성공적으로 리뷰하고 발견된 문제를 기록함
