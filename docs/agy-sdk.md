# Module 3: Building AGY Agents with the SDK

<div class="module-header" markdown>
**Duration:** ~90 minutes  
**Goal:** Build a production-ready AGY agent from scratch using the `google-antigravity` Python library — tools, hooks, policy, session state, multi-agent orchestration, and structured output.  
**Exercises:** [Exercise 10: Your First Agent](exercises/ex10_first_agent.md) · [Exercise 11: Multi-Agent Pipeline](exercises/ex11_multi_agent_pipeline.md)
</div>

> 📖 Sources: [SDK Overview](https://antigravity.google/docs/sdk-overview) · [google-antigravity PyPI](https://pypi.org/project/google-antigravity/) · [Skills](https://antigravity.google/docs/skills)

---

## Why Build an Agent Instead of Just Using the CLI?

The CLI is a **general-purpose assistant**. An agent you build with the SDK is a **specialist** — it has a narrow job, domain-specific tools, a carefully engineered system prompt, and it can be deployed as a service that your whole team calls.

| | Antigravity CLI | AGY SDK Agent |
| :-- | :-- | :-- |
| **Who uses it** | Individual developer | Team / API consumers |
| **Customization** | AGENTS.md + plugins | Full code control |
| **Tools** | Built-in CLI tools | Any Python function you write |
| **Policy** | Interactive approval prompts | Programmatic `policy.*` rules |
| **Deployment** | Local interactive session | Cloud Run service, callable via API |
| **Multi-agent** | Subagents in CLI session | `asyncio.gather` + `START_SUBAGENT` |

---

## 3.1 — SDK Setup <span class="duration-badge">10 min</span>

### Prerequisites

- Python 3.11+
- A Gemini API key — set as `GEMINI_API_KEY` or pass via `api_key=` in config

### Install

```bash
python -m venv .venv
source .venv/bin/activate
pip install google-antigravity
```

### Verify

```python
from google.antigravity import Agent, LocalAgentConfig
from google.antigravity.hooks import policy
print("google-antigravity installed ✅")
```

> **API key vs Vertex AI:** For quick local development, use `api_key="AIza..."` in
> `LocalAgentConfig`. For production on GCP, authenticate with
> `gcloud auth application-default login` — the library picks up ADC automatically.

---

## 3.2 — Core Primitives: Agent, Config, Tool <span class="duration-badge">20 min</span>

The `google-antigravity` SDK has three building blocks: `Agent`, `LocalAgentConfig`, and tools (plain Python functions). Learn these and you can build anything.

### The Tool

A tool is a **plain Python function**. No wrapper class, no decorator. The agent decides when to call it based on the docstring — that's the entire interface contract.

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

> **Critical rules for tools:**
>
> - Use explicit type annotations — `str`, `int`, `bool`, `list[str]`. No `typing.Optional`.
> - Use a default of `None` for optional parameters: `param: str = None`
> - The docstring is the tool's schema — the model reads it to decide when and how to call the tool. Write it for the model, not a human.
> - Keep tools narrow and focused. One job per tool.

### Tools with Session State

To read/write **session state** inside a tool, declare a parameter typed as `ToolContext`.
The SDK auto-detects it, injects it at call time, and **strips it from the schema shown to the model**:

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

### The Agent + Config

`Agent` is the single entry point. All configuration goes in `LocalAgentConfig`:

```python
import asyncio
from google.antigravity import Agent, LocalAgentConfig
from google.antigravity.hooks import policy

config = LocalAgentConfig(
    model="gemini-3.7-flash",
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

> **`async with Agent(config) as agent:`** — always use the context manager. It starts
> the Go runtime bridge (`bin/localharness`) and tears it down cleanly on exit.

### Model Selection

Match the model to the job. Cost-conscious policy:

| Role | Model | Rationale |
| :-- | :-- | :-- |
| General tasks, code review | `gemini-3.7-flash` | SDK default — high efficiency and coding performance |
| High-throughput baseline | `gemini-3.5-flash` / `gemini-3.6-flash` | Fast, cost-efficient execution |
| Orchestration, routing, planning | `gemini-3.1-pro-preview` | Complex reasoning, multi-step decisions |
| Image generation tasks | `gemini-3.1-flash-lite-image` | SDK default for image generation (Nano Banana 2) |
| High-stakes analysis | `gemini-3.1-pro-preview` with `ThinkingLevel.HIGH` | Deep reasoning for compliance and security |
| Enterprise alternative models | `claude-sonnet-4-6`, `claude-opus-4-6`, `gpt-oss-120b` | Multi-provider support on Vertex AI / enterprise |

> **Never use** `gemini-1.5-flash`, `gemini-1.5-pro`. Deprecated.

### The Skill

Skills are `SKILL.md` files loaded at runtime to inject domain knowledge. Keep your system prompt lean — load expertise from files:

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

Skills can also be loaded natively via `LocalAgentConfig(skills_paths=["/path/to/skills/"])` — the SDK discovers `SKILL.md` files automatically.

---

## 3.3 — Policy and Safety <span class="duration-badge">10 min</span>

**Policy is the first thing you configure** — it controls what the agent is allowed to do without human approval. Every `LocalAgentConfig` needs a `policies=` list:

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

> **Priority order:** `specific_deny` > `specific_ask` > `specific_allow` > `wildcard_deny` > `wildcard_ask` > `wildcard_allow`

---

## 3.4 — Hooks: Observability and Control <span class="duration-badge">10 min</span>

Hooks let you intercept and react to every event in the agent lifecycle — for logging, auditing, guardrails, or custom approval flows:

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
    is_success = tool_result.error is None
    print(f"[AUDIT] tool={tool_result.name} success={is_success}")

# Initialise state when a session begins
@hooks.on_session_start
async def initialise_state() -> None:
    print("[AGENT] Session started — ready.")

config = LocalAgentConfig(
    hooks=[security_guard, audit_logger, initialise_state],
    policies=[policy.allow_all()],
    model="gemini-3.7-flash",
    system_instructions="You are a code reviewer.",
    tools=[get_file_contents],
)
```

**Hook types:**

| Hook | Blocks execution | Modifies data | Use for |
| :-- | :-- | :-- | :-- |
| `@hooks.pre_tool_call_decide` | Yes | No | Approve/deny tool calls |
| `@hooks.post_tool_call` | No | No | Logging, metrics |
| `@hooks.pre_turn` | No | No | Turn-level logging |
| `@hooks.post_turn` | No | No | Response logging |
| `@hooks.on_session_start/end` | No | No | Setup/teardown |
| `@hooks.on_tool_error` | Yes | Yes | Error recovery |

---

## 3.5 — Multi-Agent Orchestration <span class="duration-badge">15 min</span>

`google-antigravity` has no `SequentialAgent` or `ParallelAgent` classes. Multi-agent is done two ways: **model-driven** (let the agent spawn subagents) or **Python-driven** (you orchestrate `Agent` instances directly).

### Pattern A — Model-Driven Subagents

Enable `START_SUBAGENT` in capabilities. The model calls it when it decides to delegate:

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

### Pattern B — Sequential Pipeline (Python-Driven)

Pass the output of one agent as the input to the next:

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

### Pattern C — Parallel Analysis

Run independent agents simultaneously with `asyncio.gather`:

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

> **When to use parallel:** Any time you have N independent analyses. This cuts wall-clock
> time by 60–80% compared to running them sequentially.

---

## 3.6 — Streaming and Structured Output <span class="duration-badge">5 min</span>

### Streaming Responses

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

### Structured Output

Bind the agent's output to a Pydantic schema:

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
    model="gemini-3.7-flash",
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

## 3.7 — Session Resume and Persistence <span class="duration-badge">5 min</span>

```python
save_dir = "/path/to/session_storage"

# First session — specify save_dir to persist trajectory
init_config = LocalAgentConfig(
    save_dir=save_dir,
    model="gemini-3.7-flash",
    policies=[policy.allow_all()],
)
async with Agent(init_config) as agent:
    await agent.chat("Analyse this codebase and build a mental model.")
    conv_id = agent.conversation_id   # persist this ID

# Later session — resume using the same save_dir and conversation_id
resume_config = LocalAgentConfig(
    conversation_id=conv_id,
    save_dir=save_dir,
    model="gemini-3.7-flash",
    policies=[policy.allow_all()],
)
async with Agent(resume_config) as agent:
    await agent.chat("Now suggest the top 3 refactoring priorities.")
```

---

## 3.8 — Triggers: Autonomous Background Agents <span class="duration-badge">5 min</span>

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

## 3.9 — Project Structure Conventions <span class="duration-badge">5 min</span>

Structure your agent project for maintainability:

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

### Deployment to Cloud Run

Deploy as a standard Python async application:

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

> **Tip:** Set `GOOGLE_CLOUD_PROJECT` and `GOOGLE_CLOUD_REGION` (e.g. `us-central1`) before running.

---

## Hands-On Exercises

<div class="exercise-card" markdown>

### :material-code-braces: Exercise 10: Your First AGY Agent

**File:** [`ex10_first_agent.md`](exercises/ex10_first_agent.md)  
**Duration:** 45 min  
**Build:** A **Code Review Agent** that reads files, identifies issues, and produces a structured review report.

**What you'll implement:**

1. Define 3 tools: `read_file`, `list_directory`, `record_finding` (with `ToolContext`)
2. Write a system prompt with a review rubric (loaded from a `SKILL.md`)
3. Configure `LocalAgentConfig` with `policy.allow_all()` and `CapabilitiesConfig`
4. Add a `@hooks.pre_tool_call_decide` security guard
5. Run with streaming output and structured `ReviewResult` Pydantic schema

</div>

<div class="exercise-card" markdown>

### :material-graph: Exercise 11: Multi-Agent Pipeline

**File:** [`ex11_multi_agent_pipeline.md`](exercises/ex11_multi_agent_pipeline.md)  
**Duration:** 45 min  
**Build:** A **Write-then-Audit Pipeline** — a Technical Writer agent produces a document, then a Compliance Analyst audits it for GDPR gaps.

**What you'll implement:**

1. Build a `technical_writer` agent with a GDPR SKILL.md loaded via `skills_paths`
2. Build a `compliance_analyst` agent with `response_schema=ComplianceReport`
3. Wire them sequentially: output of writer passed as input to analyst
4. Add a parallel variant using `asyncio.gather` for simultaneous draft + legal check
5. Add session resume: analyst reads the writer's `conversation_id` to load context
6. Deploy to Cloud Run as `my-pipeline` using `gcloud run deploy`

</div>

---

## Summary: SDK Building Blocks

| Primitive | What It Does | When to Use |
| :-- | :-- | :-- |
| `Agent` | Single LLM agent with tools, hooks, policy | The core — every agent starts here |
| `LocalAgentConfig` | All config in one place (model, tools, policy, hooks) | Always |
| `tools=[fn]` | Plain Python callable, docstring is the schema | Any external operation |
| `ToolContext` | State read/write injected into tools | Stateful tools in pipelines |
| `policy.allow_all()` | Approve all tool calls autonomously | Trusted, sandboxed agents |
| `policy.deny("run_command")` | Block specific tool types | Safety guardrails |
| `@hooks.pre_tool_call_decide` | Block/approve tool calls before execution | Security guards |
| `@hooks.post_tool_call` | Observe completed tool calls | Audit logging |
| `response_schema=` | Bind output to Pydantic schema | Structured data extraction |
| `async for delta in response:` | Stream text as it arrives | Long-form generation |
| `asyncio.gather(...)` | Run agents in parallel | Independent analyses |
| `every(60, handler)` | Trigger agent on interval | Background monitors |
| `on_file_change(path, fn)` | Trigger agent on filesystem events | Live code watchers |
| `skills_paths=[...]` | Load SKILL.md files at runtime | Portable domain expertise |
| `conversation_id=` | Resume a previous session | Multi-session workflows |

---

## Next Step

→ Continue to **[Module 4: Multi-Agent & Advanced Patterns](multi-agent-advanced.md)**

→ Reference: **[Cheatsheet](cheatsheet.md)** — all commands in one place
