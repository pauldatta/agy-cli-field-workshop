# Exercise 10: Your First AGY Agent

> **Duration:** 45 min | **Module:** 3 — Building AGY Agents

---

## Objective

Build a **Code Review Agent** using the `google-antigravity` Python SDK. The agent reads files, identifies issues, and produces a structured review report — all running autonomously with a security guard hook that blocks writes.

---

## Setup

```bash
# Create project directory
mkdir -p ~/agy-review-agent/tools ~/agy-review-agent/hooks ~/agy-review-agent/skills/python-review

# Set up Python environment
cd ~/agy-review-agent
python3 -m venv .venv
source .venv/bin/activate
pip install google-antigravity pydantic
```

Set your API key:

```bash
export GEMINI_API_KEY="your-api-key-here"
```

---

## Part 1: Define the Tools (10 min)

Create `tools/file_tools.py` with two read-only tools:

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

Create `tools/state_tools.py` with a stateful tool using `ToolContext`:

```python
from google.antigravity import ToolContext


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

> **Key concept:** The `ctx: ToolContext` parameter is auto-injected by the SDK at call time and stripped from the schema shown to the model. The model never sees it — it just calls `record_finding(severity, message, file_path)`.

---

## Part 2: Write the Review Skill (5 min)

Create `skills/python-review/SKILL.md`:

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

## Part 3: Configure the Agent (10 min)

Create `config.py`:

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
    model="gemini-3.7-flash",
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

## Part 4: Add a Security Guard Hook (5 min)

Create `hooks/security_guard.py`:

```python
from google.antigravity.hooks import hooks
from google.antigravity.types import BuiltinTools, ToolCall, HookResult

# Tools that could modify the filesystem
WRITE_TOOLS = {
    BuiltinTools.CREATE_FILE,
    BuiltinTools.EDIT_FILE,
    BuiltinTools.RUN_COMMAND,
    "create_file",
    "edit_file",
    "run_command",
}


@hooks.pre_tool_call_decide
async def block_writes(tool_call: ToolCall) -> HookResult:
    """Block any tool call that could modify files.

    This agent is read-only — it reviews code but never changes it.
    """
    if tool_call.name in WRITE_TOOLS:
        return HookResult(allow=False)

    if tool_call.name in (BuiltinTools.RUN_COMMAND, "run_command"):
        cmd = tool_call.args.get("CommandLine", "")
        if any(danger in cmd for danger in ["rm ", "mv ", "chmod", "chown", "dd "]):
            return HookResult(allow=False)

    return HookResult(allow=True)
```

> **Why this matters:** Even with `policy.allow_all()`, the hook fires before every tool call and can deny it. Defense in depth — policy sets the baseline, hooks enforce guardrails.

---

## Part 5: Wire It Together with Streaming + Structured Output (15 min)

Create `main.py`:

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

### Run It

```bash
# Review the agent's own code (meta!)
python main.py .

# Review a specific project directory
python main.py /path/to/your/project/src
```

---

## Pro Tips & Key Watchouts

!!! tip "Key Things to Watch For"
    1. **`ToolContext` Schema Stripping:** Never pass `ctx` from prompts. The SDK auto-injects `ctx: ToolContext` at runtime. If your prompt mentions `ctx`, the model may attempt to hallucinate an argument.
    2. **API Key & Project Auth:** Ensure `export GEMINI_API_KEY="..."` is set in your active shell or `gcloud auth application-default login` has been executed for Vertex AI project access.
    3. **Hook Return Signatures:** `HookResult` only accepts `allow: bool`. Do not pass deprecated `message="..."` or `reason="..."` arguments.

---

## Completion Criteria

- [ ] Three tools defined: `read_file`, `list_directory`, `record_finding` (with `ToolContext`)
- [ ] `SKILL.md` created with a Python review rubric
- [ ] `LocalAgentConfig` constructed with `policy.allow_all()` and tools list
- [ ] `@hooks.pre_tool_call_decide` security guard blocks write operations
- [ ] Agent runs and streams output to the console
- [ ] Structured `ReviewResult` returned with findings, severity levels, and overall health
- [ ] Agent successfully reviews at least one Python file and records findings
