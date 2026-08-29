# google-antigravity SDK Grounding Data

_Generated: 2026-08-29 — source: google-antigravity v0.1.15 package_
_plus official docs at `https://antigravity.google/docs/sdk-overview`_

---

## 1. Package Structure

```
google/antigravity/
├── __init__.py           → Agent, AgentConfig, LocalAgentConfig, ToolContext,
│                           CapabilitiesConfig, GeminiConfig, GenerationConfig,
│                           ModelConfig, ModelEntry, ThinkingLevel, UsageMetadata
├── agent.py              → class Agent  (the single high-level entry point)
├── types.py              → all core types (1104 lines)
├── connections/
│   ├── connection.py     → abstract AgentConfig, Connection, ConnectionStrategy
│   └── local/
│       ├── local_connection_config.py  → class LocalAgentConfig(AgentConfig)
│       ├── local_connection.py         → LocalConnectionStrategy, LocalConnection
│       └── types.py                    → ToolOutput, RunCommandResult, EditFileResult, etc.
├── conversation/
│   └── conversation.py   → class Conversation (Layer 2 session API)
├── hooks/
│   ├── hooks.py          → Hook base classes + decorators
│   ├── policy.py         → policy.allow(), deny(), ask_user(), enforce()
│   └── __init__.py       → exports all hook types + decorators
├── tools/
│   ├── tool_runner.py    → class ToolRunner, class ToolWithSchema
│   └── tool_context.py   → class ToolContext (injected into tools)
├── triggers/
│   ├── triggers.py       → Trigger type, @trigger decorator, TriggerContext
│   ├── helpers.py        → every(), on_file_change() factories
│   └── __init__.py       → exports
├── mcp/
│   └── bridge.py         → class McpBridge (MCP server integration)
├── utils/
│   └── interactive.py    → AskQuestionHook, async_input helpers
└── bin/
    └── localharness      → Go binary (~100MB) — the actual agent runtime
```

> **Critical:** There is NO `SequentialAgent`, `ParallelAgent`, `LlmAgent`, or `BaseAgent`
> in this package. Those are `google.adk` concepts. Multi-agent in `google.antigravity`
> is done via `BuiltinTools.START_SUBAGENT` or by orchestrating multiple `Agent` instances
> in Python with `asyncio.gather`.

---

## 2. Exact Import Patterns (Verified from `__init__.py`)

```python
# Top-level exports
from google.antigravity import Agent
from google.antigravity import AgentConfig, LocalAgentConfig
from google.antigravity import ToolContext
from google.antigravity import CapabilitiesConfig, GeminiConfig, GenerationConfig
from google.antigravity import ModelConfig, ModelEntry, ThinkingLevel, UsageMetadata

# Types module
from google.antigravity.types import (
    BuiltinTools,
    McpStdioServer, McpSseServer, McpStreamableHttpServer,
    TemplatedSystemInstructions, CustomSystemInstructions, SystemInstructionSection,
    Step, StepType, StepSource, StepTarget, StepStatus,
    ToolCall, ToolResult, HookResult,
    ChatResponse, StreamChunk, Text, Thought,
    Image, Document, Audio, Video, Content, ContentPrimitive,
    FileChange, FileChangeKind, TriggerDelivery,
    AntigravityConnectionError, AntigravityValidationError,
)
from google.antigravity.types import from_file  # auto-detects media type

# Hooks
from google.antigravity.hooks import (
    pre_turn, post_turn, pre_tool_call_decide, post_tool_call,
    on_session_start, on_session_end, on_interaction, on_compaction, on_tool_error,
    PreTurnHook, PostTurnHook, PreToolCallDecideHook, PostToolCallHook,
    OnSessionStartHook, OnSessionEndHook, OnInteractionHook, OnCompactionHook,
    OnToolErrorHook, HookContext,
)

# Policy
from google.antigravity.hooks import policy
# policy.allow(), deny(), ask_user(), allow_all(), deny_all(),
# confirm_run_command(), workspace_only(), safe_defaults(), enforce()

# Triggers
from google.antigravity.triggers import trigger, TriggerContext, Trigger
from google.antigravity.triggers import every, on_file_change

# ToolContext (also re-exported at top level)
from google.antigravity.tools.tool_context import ToolContext

# Conversation (Layer 2 — advanced)
from google.antigravity.conversation.conversation import Conversation

# MCP types
from google.antigravity.types import McpStdioServer, McpSseServer, McpStreamableHttpServer
```

---

## 3. Agent & Config Constructor Signatures (verbatim)

### `Agent`
```python
class Agent:
    def __init__(self, config: AgentConfig): ...
    async def chat(self, prompt: types.Content) -> types.ChatResponse: ...
    async def __aenter__(self) -> "Agent": ...
    async def __aexit__(self, exc_type, exc_val, exc_tb): ...
    def register_hook(self, hook: hooks.Hook): ...
    def register_trigger(self, trigger: triggers_lib.Trigger): ...
    @property
    def conversation(self) -> Conversation: ...
    @property
    def conversation_id(self) -> str | None: ...
    @property
    def is_started(self) -> bool: ...
```

### `LocalAgentConfig` (the concrete config used in all applications)
```python
class LocalAgentConfig(AgentConfig):  # pydantic.BaseModel subclass
    # From AgentConfig base:
    system_instructions: str | types.SystemInstructions | None = None
    capabilities: types.CapabilitiesConfig = CapabilitiesConfig(enabled_tools=BuiltinTools.read_only())
    tools: list[Callable[..., Any]] = []
    policies: list[Any] = []     # default: [confirm_run_command()]
    hooks: list[Any] = []
    triggers: list[Any] = []
    mcp_servers: list[types.McpServerConfig] = []
    workspaces: list[str] = [os.getcwd()]
    conversation_id: str | None = None
    save_dir: str | None = None
    app_data_dir: str | None = None
    response_schema: dict | type[pydantic.BaseModel] | str | None = None
    skills_paths: list[str] = []

    # LocalAgentConfig-specific:
    gemini_config: types.GeminiConfig = GeminiConfig()
    model: str | None = None        # shorthand → gemini_config.models.default
    api_key: str | None = None      # shorthand → gemini_config.api_key
```

---

## 4. Tool Definition Pattern

**No `@tool` decorator. No `FunctionTool` class.** Tools are plain Python callables:

```python
def my_tool(query: str, count: int = 5) -> str:
    """Searches for query and returns count results.

    Args:
        query: The search term.
        count: Number of results to return.

    Returns:
        Search results as a formatted string.
    """
    return f"Results for {query}: ..."

config = LocalAgentConfig(
    tools=[my_tool],
    policies=[policy.allow_all()],
)
```

**To inject `ToolContext`** — declare a parameter typed as `ToolContext`. The ToolRunner
auto-detects it, injects it at call time, and strips it from the schema shown to the model:

```python
from google.antigravity.tools.tool_context import ToolContext

def stateful_tool(query: str, ctx: ToolContext) -> str:
    """Searches and stores query in session state.

    Args:
        query: The search term.
    """
    ctx.set_state("last_query", query)
    last = ctx.get_state("prev_query", "none")
    return f"Querying: {query} (prev: {last})"
```

**`ToolWithSchema`** — for tools with explicit JSON Schema:
```python
from google.antigravity.tools.tool_runner import ToolWithSchema

wrapped = ToolWithSchema(fn=my_callable, input_schema={"type": "object", ...})
config = LocalAgentConfig(tools=[wrapped])
```

---

## 5. ToolContext API (State Management)

```python
class ToolContext:
    @property
    def conversation_id(self) -> str: ...

    @property
    def is_idle(self) -> bool: ...

    async def send(self, message: str) -> None:
        """Inject a message into the conversation mid-tool."""

    def get_state(self, key: str, default=None) -> Any: ...
    def set_state(self, key: str, value: Any) -> None: ...
```

> **No `output_key`. No `{placeholder}` substitution. No `state["key"]` dict access.**
> State is always via `ctx.get_state()` / `ctx.set_state()`.

---

## 6. Agent Execution (ChatResponse API)

```python
import asyncio
from google.antigravity import Agent, LocalAgentConfig
from google.antigravity.hooks import policy

async def main():
    config = LocalAgentConfig(
        model="gemini-3.7-flash",
        system_instructions="You are a helpful assistant.",
        tools=[my_tool],
        policies=[policy.allow_all()],
        workspaces=["/path/to/workspace"],
    )
    async with Agent(config) as agent:
        # Await full text
        response = await agent.chat("Hello!")
        text = await response.text()

        # Streaming text deltas
        response = await agent.chat("Write a long report...")
        async for delta in response:
            print(delta, end="", flush=True)

        # Stream reasoning/thoughts
        async for thought in response.thoughts:
            print(f"[thinking] {thought}")

        # Structured output
        result = await response.structured_output()

        # Multi-turn (stateful — context preserved)
        r2 = await agent.chat("Follow up question...")

asyncio.run(main())
```

**`ChatResponse` methods:**
```python
class ChatResponse:
    async def __aiter__(self) -> AsyncIterator[str]   # text deltas
    async def text(self) -> str                        # full text (drains stream)
    async def resolve(self) -> list[...]               # all chunks
    async def structured_output(self) -> Any | None
    @property chunks: AsyncIterator[StreamChunk | ToolCall | ToolResult]
    @property thoughts: AsyncIterator[str]
    @property tool_calls: AsyncIterator[ToolCall]
    @property usage_metadata: UsageMetadata | None
```

---

## 7. Conversation / Session State

```python
agent.conversation.history        # list[types.Step]
agent.conversation.last_response  # str
agent.conversation.turn_count     # int
agent.conversation.total_usage    # UsageMetadata
agent.conversation.last_turn_usage # UsageMetadata | None
agent.conversation_id             # str | None — save to resume later
```

**Resuming a session:**
```python
save_dir = "/path/to/session_storage"

# First run — specify save_dir to persist trajectory
init_config = LocalAgentConfig(
    save_dir=save_dir,
    model="gemini-3.7-flash",
    policies=[policy.allow_all()],
)
async with Agent(init_config) as agent:
    await agent.chat("Hello")
    conv_id = agent.conversation_id

# Resume using the same save_dir and conversation_id
resume_config = LocalAgentConfig(
    conversation_id=conv_id,
    save_dir=save_dir,
    model="gemini-3.7-flash",
    policies=[policy.allow_all()],
)
async with Agent(resume_config) as agent:
    await agent.chat("Continue from where we left off")
```

---

## 8. Multi-Agent Orchestration

**No `SequentialAgent` or `ParallelAgent`.** Two patterns:

### Pattern A — Built-in subagent tool (model-driven)
```python
from google.antigravity.types import BuiltinTools, CapabilitiesConfig

config = LocalAgentConfig(
    capabilities=CapabilitiesConfig(
        enable_subagents=True,
        enabled_tools=BuiltinTools.all_tools(),
    ),
    policies=[policy.allow_all()],
    system_instructions="Spawn subagents to handle parallel subtasks.",
)
# The model calls START_SUBAGENT when it decides to delegate
```

### Pattern B — Python-level parallelism (developer-driven)
```python
async def run_pipeline():
    async with Agent(config_a) as agent_a, Agent(config_b) as agent_b:
        resp_a, resp_b = await asyncio.gather(
            agent_a.chat("Analyze security vulnerabilities"),
            agent_b.chat("Analyze performance bottlenecks"),
        )
        analysis_a = await resp_a.text()
        analysis_b = await resp_b.text()

    # Sequential — pass output of A as input to B
    async with Agent(config_a) as agent_a:
        resp = await agent_a.chat("Extract key findings")
        findings = await resp.text()
    async with Agent(config_b) as agent_b:
        report = await agent_b.chat(f"Write a report from: {findings}")
```

---

## 9. Hooks System

```python
from google.antigravity.hooks import hooks
from google.antigravity.types import ToolCall, ToolResult, HookResult

# Decorator pattern (preferred)
@hooks.pre_tool_call_decide
async def my_guard(tool_call: ToolCall) -> HookResult:
    if tool_call.name == "run_command":
        return HookResult(allow=False, message="Shell execution disabled.")
    return HookResult(allow=True)

@hooks.post_tool_call
async def my_logger(tool_result: ToolResult) -> None:
    print(f"Tool {tool_result.name} completed")

@hooks.on_session_start
async def on_start() -> None:
    print("Session started!")

@hooks.pre_turn
async def pre(turn) -> None:
    print(f"User said: {turn}")

# Register via config
config = LocalAgentConfig(hooks=[my_guard, my_logger, on_start])
```

**Hook categories:**
| Category | Blocks execution | Modifies data |
| :-- | :-- | :-- |
| `InspectHook[T]` | No | No |
| `DecideHook[T]` | Yes — returns `HookResult(allow=bool)` | No |
| `TransformHook[T, R]` | Yes | Yes |

**Available hook decorators:**
- `@hooks.pre_turn` — before each user turn
- `@hooks.post_turn` — after each model response
- `@hooks.pre_tool_call_decide` — approve/deny tool calls (DecideHook)
- `@hooks.post_tool_call` — after tool execution (InspectHook)
- `@hooks.on_session_start` / `@hooks.on_session_end`
- `@hooks.on_interaction` — for ASK_USER dialogs
- `@hooks.on_compaction` — context compaction events
- `@hooks.on_tool_error` — transform/recover from tool failures (TransformHook)

---

## 10. Policy System

```python
from google.antigravity.hooks import policy

# Built-in presets
policies=[policy.allow_all()]            # approve everything (autonomous)
policies=[policy.deny_all()]             # block everything
policies=[policy.confirm_run_command()]  # default: ask for shell, allow rest

# Composable fine-grained rules
policies=[
    policy.deny("run_command"),
    policy.allow("view_file"),
    policy.ask_user("edit_file", handler=my_approval_fn),
    policy.allow("*"),                   # fallback wildcard
]

# Conditional deny with predicate
policy.deny("run_command", when=lambda args: "rm -rf" in args.get("CommandLine", ""))

# Workspace scoping
policy.workspace_only(["/path/to/project"])

# Safe defaults (read-only allowed, everything else asks)
policy.safe_defaults(handler=my_approval_fn)

# Priority order: specific_deny > specific_ask > specific_allow > wildcard_deny > wildcard_ask > wildcard_allow
```

---

## 11. Triggers

```python
from google.antigravity.triggers import every, on_file_change, trigger, TriggerContext

# Poll every N seconds
async def poll_handler(ctx: TriggerContext) -> None:
    await ctx.send("Check for new tasks.")

config = LocalAgentConfig(
    triggers=[every(60.0, poll_handler)],
    policies=[policy.allow_all()],
)

# File-watch trigger
async def file_handler(ctx: TriggerContext, changes) -> None:
    paths = [c.path for c in changes]
    await ctx.send(f"Files changed: {paths}. Please review.")

config = LocalAgentConfig(
    triggers=[on_file_change("/path/to/watch", file_handler)],
    policies=[policy.allow_all()],
)

# Custom trigger with decorator
@trigger
async def my_trigger(ctx: TriggerContext) -> None:
    await asyncio.sleep(30)
    await ctx.send("30 seconds elapsed.")
```

---

## 12. MCP Integration

```python
from google.antigravity.types import McpStdioServer, McpSseServer, McpStreamableHttpServer

config = LocalAgentConfig(
    mcp_servers=[
        McpStdioServer(
            command="npx",
            args=["-y", "@modelcontextprotocol/server-filesystem", "."],
        ),
        McpSseServer(
            url="http://localhost:8080/sse",
            headers={"Authorization": "Bearer token"},
        ),
        McpStreamableHttpServer(
            url="http://localhost:8080/mcp",
            timeout=30.0,
            sse_read_timeout=300.0,
        ),
    ],
    policies=[policy.allow_all()],  # required when MCP servers present
)
```

---

## 13. Multimodal Input

```python
from google.antigravity.types import Image, Document, Audio, Video, from_file

# Auto-detect from extension
media = from_file("/path/to/image.png")
media = from_file("/path/to/report.pdf", description="Q4 report")

# Explicit types
img   = Image.from_file("/path/to/screenshot.png")
doc   = Document.from_file("/path/to/spec.pdf")
audio = Audio.from_file("/path/to/recording.wav")

# Pass as content (str | media | list)
response = await agent.chat(["Analyze this image:", img])
response = await agent.chat([doc, "What are the key findings?"])
```

---

## 14. Structured Output

```python
import pydantic
from google.antigravity import LocalAgentConfig

class ReviewResult(pydantic.BaseModel):
    issues: list[str]
    severity: str
    recommendation: str

config = LocalAgentConfig(
    response_schema=ReviewResult,  # Pydantic class, dict, or JSON string
    system_instructions="Return structured output via the finish tool.",
    policies=[policy.allow_all()],
)

async with Agent(config) as agent:
    response = await agent.chat("Review this code...")
    result = await response.structured_output()  # dict matching schema
```

---

## 15. Model Configuration

```python
from google.antigravity import LocalAgentConfig, GeminiConfig, ModelConfig, ModelEntry, ThinkingLevel

# Simple shorthand
config = LocalAgentConfig(model="gemini-3.5-flash")

# Full model config with per-task overrides
config = LocalAgentConfig(
    gemini_config=GeminiConfig(
        api_key="AIza...",
        models=ModelConfig(
            default=ModelEntry(
                name="gemini-3.1-pro-preview",
                generation=GenerationConfig(thinking_level=ThinkingLevel.HIGH),
            ),
            image_generation=ModelEntry(name="gemini-3.1-flash-image-preview"),
        )
    )
)
```

**Defaults (from source):**
- `DEFAULT_MODEL = "gemini-3.5-flash"`
- `DEFAULT_IMAGE_GENERATION_MODEL = "gemini-3.1-flash-image-preview"`
- `ThinkingLevel` values: `MINIMAL`, `LOW`, `MEDIUM`, `HIGH`

---

## 16. CapabilitiesConfig & BuiltinTools

```python
from google.antigravity.types import BuiltinTools, CapabilitiesConfig

CapabilitiesConfig()                                      # all tools enabled (LocalAgentConfig default)
CapabilitiesConfig(enabled_tools=BuiltinTools.read_only()) # LIST_DIR, SEARCH_DIR, FIND_FILE, VIEW_FILE, FINISH
CapabilitiesConfig(enabled_tools=BuiltinTools.none())     # no tools
CapabilitiesConfig(enabled_tools=BuiltinTools.all_tools()) # everything incl. RUN_COMMAND, START_SUBAGENT
CapabilitiesConfig(disabled_tools=[BuiltinTools.RUN_COMMAND]) # deny-list
CapabilitiesConfig(enable_subagents=False)                # no subagents
CapabilitiesConfig(compaction_threshold=50000)            # context compaction threshold
```

**`BuiltinTools` enum values:**
`LIST_DIR`, `SEARCH_DIR`, `FIND_FILE`, `VIEW_FILE`, `CREATE_FILE`, `EDIT_FILE`,
`RUN_COMMAND`, `ASK_QUESTION`, `START_SUBAGENT`, `GENERATE_IMAGE`, `FINISH`

---

## 17. System Instructions (3 Variants)

```python
from google.antigravity.types import (
    TemplatedSystemInstructions, CustomSystemInstructions, SystemInstructionSection
)

# 1. Plain string — appended to AGY defaults as a named section
LocalAgentConfig(system_instructions="You are a code reviewer.")

# 2. TemplatedSystemInstructions — override identity, add sections
LocalAgentConfig(system_instructions=TemplatedSystemInstructions(
    identity="You are an expert Python code reviewer.",
    sections=[
        SystemInstructionSection(title="review_rules", content="Always cite line numbers."),
    ]
))

# 3. CustomSystemInstructions — FULL replacement of ALL defaults (advanced)
LocalAgentConfig(system_instructions=CustomSystemInstructions(
    text="FULL system prompt. You are responsible for ALL instructions."
))
```

---

## 18. Skills

```python
config = LocalAgentConfig(
    skills_paths=["/path/to/skills/dir"],  # list[str] of skill root dirs
)
# Skills are SKILL.md files discovered under each path
```

---

## 19. Deployment

**There is no `agy deploy`, `adk deploy`, `adk web .`, or `adk run .` command in this package.**

The package ships a Go binary (`bin/localharness`) used internally. Deployment is as a
standard Python async application. For Cloud Run:

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install google-antigravity
COPY . .
CMD ["python", "main.py"]
```

For persistent sessions, configure `save_dir` and `app_data_dir` to a mounted volume.

---

## 20. Critical Errors in Current `agy-sdk.md`

| # | What it says | What's correct |
| :-- | :-- | :-- |
| 1 | `pip install google-adk` | `pip install google-antigravity` |
| 2 | `from google.adk.agents import LlmAgent, SequentialAgent` | `from google.antigravity import Agent, LocalAgentConfig` |
| 3 | `SequentialAgent`, `ParallelAgent`, `BaseAgent` | Don't exist — use `asyncio.gather` or `START_SUBAGENT` |
| 4 | `FunctionTool(my_fn)` | Plain callable: `tools=[my_fn]` |
| 5 | `tool_context.state["key"]` | `ctx.get_state("key")` / `ctx.set_state("key", val)` |
| 6 | `output_key=`, `{placeholder}` in instructions | Does not exist — no template substitution |
| 7 | `adk web .`, `adk run .`, `adk eval .` | No CLI — pure Python library |
| 8 | `InvocationContext` | Does not exist |
| 9 | `class X(BaseAgent): _run_async_impl(ctx)` | Does not exist |
| 10 | No mention of policy system | `policy.allow_all()`, `policy.deny()`, etc. — required for any non-trivial agent |
| 11 | No mention of hooks | `@hooks.pre_tool_call_decide`, `@hooks.post_tool_call`, etc. |
| 12 | No mention of triggers | `every()`, `on_file_change()`, `@trigger` |
| 13 | No mention of MCP integration | `McpStdioServer`, `McpSseServer`, `McpStreamableHttpServer` |
| 14 | No mention of structured output | `response_schema=ReviewResult`, `response.structured_output()` |
| 15 | No mention of multimodal | `Image.from_file()`, `Document.from_file()`, `from_file()` |
| 16 | No streaming API documented | `async for delta in response:`, `response.thoughts`, `response.text()` |
