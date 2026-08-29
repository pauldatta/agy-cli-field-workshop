# 练习 10：你的第一个 AGY 代理

> **时长：** 45 分钟 | **模块：** 3 — 构建 AGY 代理

---

## 目标

使用 `google-antigravity` Python SDK 构建一个**代码审查代理**。该代理读取文件、识别问题并生成结构化的审查报告 —— 所有操作均自主运行，并配有一个阻止写入操作的安全守卫钩子。

---

## 环境设置

```bash
# Create project directory
mkdir -p ~/agy-review-agent/tools ~/agy-review-agent/hooks ~/agy-review-agent/skills/python-review

# Set up Python environment
cd ~/agy-review-agent
python3 -m venv .venv
source .venv/bin/activate
pip install google-antigravity pydantic
```

设置您的 API 密钥：

```bash
export GEMINI_API_KEY="your-api-key-here"
```

---

## 第 1 部分：定义工具 (10 分钟)

创建包含两个只读工具的 `tools/file_tools.py`：

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

使用 `ToolContext` 创建包含有状态工具的 `tools/state_tools.py`：

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

> **核心概念：** `ctx: ToolContext` 参数在调用时由 SDK 自动注入，并从向模型展示的 schema 中剥离。模型永远不会看到它——模型只需调用 `record_finding(severity, message, file_path)`。

---

## 第 2 部分：编写审查技能 (5 分钟)

创建 `skills/python-review/SKILL.md`：

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

## 第 3 部分：配置代理 (10 分钟)

创建 `config.py`：

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

## 第 4 部分：添加安全守卫钩子 (5 分钟)

创建 `hooks/security_guard.py`：

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

> **为什么这很重要：** 即使使用了 `policy.allow_all()`，钩子也会在每次工具调用之前触发，并且可以拒绝该调用。深度防御——策略设定基线，钩子强制执行护栏。

---

## 第 5 部分：结合流式传输与结构化输出进行整合 (15 分钟)

创建 `main.py`：

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

### 运行

```bash
# Review the agent's own code (meta!)
python main.py .

# Review a specific project directory
python main.py /path/to/your/project/src
```

---

## 完成标准

- [ ] 定义了三个工具：`read_file`、`list_directory`、`record_finding`（带有 `ToolContext`）
- [ ] 创建了包含 Python 审查标准的 `SKILL.md`
- [ ] 使用 `policy.allow_all()` 和工具列表构建了 `LocalAgentConfig`
- [ ] `@hooks.pre_tool_call_decide` 安全守卫阻止了写入操作
- [ ] 代理运行并将输出流式传输到控制台
- [ ] 返回结构化的 `ReviewResult`，包含发现的问题、严重级别和整体健康状况
- [ ] 代理成功审查了至少一个 Python 文件并记录了发现的问题
