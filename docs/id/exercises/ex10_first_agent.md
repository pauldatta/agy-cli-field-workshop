# Latihan 10: Agen AGY Pertama Anda

> **Durasi:** 45 menit | **Modul:** 3 — Membangun Agen AGY

---

## Tujuan

Bangun sebuah **Agen Tinjauan Kode** menggunakan SDK Python `google-antigravity`. Agen tersebut membaca file, mengidentifikasi masalah, dan menghasilkan laporan tinjauan terstruktur — semuanya berjalan secara otonom dengan hook penjaga keamanan yang memblokir penulisan.

---

## Pengaturan

```bash
# Create project directory
mkdir -p ~/agy-review-agent/tools ~/agy-review-agent/hooks ~/agy-review-agent/skills/python-review

# Set up Python environment
cd ~/agy-review-agent
python3 -m venv .venv
source .venv/bin/activate
pip install google-antigravity pydantic
```

Atur kunci API Anda:

```bash
export GEMINI_API_KEY="your-api-key-here"
```

---

## Bagian 1: Mendefinisikan Alat (10 menit)

Buat `tools/file_tools.py` dengan dua alat hanya-baca:

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

Buat `tools/state_tools.py` dengan alat stateful menggunakan `ToolContext`:

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

> **Konsep utama:** Parameter `ctx: ToolContext` disuntikkan secara otomatis oleh SDK saat pemanggilan dan dihapus dari skema yang ditampilkan kepada model. Model tidak pernah melihatnya — model hanya memanggil `record_finding(severity, message, file_path)`.

---

## Bagian 2: Menulis Skill Peninjauan (5 menit)

Buat `skills/python-review/SKILL.md`:

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

## Bagian 3: Konfigurasi Agen (10 menit)

Buat `config.py`:

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

## Bagian 4: Menambahkan Hook Security Guard (5 menit)

Buat `hooks/security_guard.py`:

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

> **Mengapa ini penting:** Bahkan dengan `policy.allow_all()`, hook dipicu sebelum setiap pemanggilan alat dan dapat menolaknya. Pertahanan mendalam — kebijakan menetapkan dasar, hook menegakkan pagar pengaman.

---

## Bagian 5: Rangkai Semuanya dengan Streaming + Output Terstruktur (15 menit)

Buat `main.py`:

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

### Jalankan

```bash
# Review the agent's own code (meta!)
python main.py .

# Review a specific project directory
python main.py /path/to/your/project/src
```

---

## Kriteria Penyelesaian

- [ ] Tiga alat didefinisikan: `read_file`, `list_directory`, `record_finding` (dengan `ToolContext`)
- [ ] `SKILL.md` dibuat dengan rubrik ulasan Python
- [ ] `LocalAgentConfig` dibangun dengan `policy.allow_all()` dan daftar alat
- [ ] Penjaga keamanan `@hooks.pre_tool_call_decide` memblokir operasi penulisan
- [ ] Agen berjalan dan mengalirkan output ke konsol
- [ ] `ReviewResult` terstruktur dikembalikan dengan temuan, tingkat keparahan, dan kesehatan keseluruhan
- [ ] Agen berhasil meninjau setidaknya satu file Python dan mencatat temuan
