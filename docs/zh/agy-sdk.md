# 模块 3：使用 SDK 构建 AGY 代理

<div class="module-header" markdown>
**时长：** 约 90 分钟  
**目标：** 使用 `google-antigravity` Python 库从头开始构建一个生产就绪的 AGY 代理 —— 包括工具、钩子、策略、会话状态、多代理编排和结构化输出。  
**练习：** [练习 10：你的第一个代理](exercises/ex10_first_agent.md) · [练习 11：多代理流水线](exercises/ex11_multi_agent_pipeline.md)
</div>

> 📖 参考资料：[SDK 概述](https://antigravity.google/docs/sdk-overview) · [google-antigravity PyPI](https://pypi.org/project/google-antigravity/) · [技能](https://antigravity.google/docs/skills)

---

## 为什么构建代理而不是仅仅使用 CLI？

CLI 是一个**通用助手**。您使用 SDK 构建的代理是一个**专家**——它有明确的工作范围、特定领域的工具、精心设计的系统提示词，并且可以作为服务部署供整个团队调用。

| | Antigravity CLI | AGY SDK 代理 |
| :-- | :-- | :-- |
| **使用者** | 个人开发者 | 团队 / API 消费者 |
| **自定义** | AGENTS.md + 插件 | 完全的代码控制 |
| **工具** | 内置 CLI 工具 | 您编写的任何 Python 函数 |
| **策略** | 交互式审批提示词 | 编程式 `policy.*` 规则 |
| **部署** | 本地交互式会话 | Cloud Run 服务，可通过 API 调用 |
| **多代理** | CLI 会话中的子代理 | `asyncio.gather` + `START_SUBAGENT` |

---

## 3.1 — SDK 环境设置 <span class="duration-badge">10 分钟</span>

### 前置条件

- Python 3.11+
- 一个 Gemini API 密钥 — 设置为 `GEMINI_API_KEY` 或通过配置中的 `api_key=` 传递

### 安装

```bash
python -m venv .venv
source .venv/bin/activate
pip install google-antigravity
```

### 验证

```python
from google.antigravity import Agent, LocalAgentConfig
from google.antigravity.hooks import policy
print("google-antigravity installed ✅")
```

> **API 密钥与 Vertex AI：** 对于快速的本地开发，请在 `LocalAgentConfig` 中使用 `api_key="AIza..."`。对于 GCP 上的生产环境，请使用 `gcloud auth application-default login` 进行身份验证 — 库会自动获取 ADC（应用程序默认凭据）。

---

## 3.2 — 核心原语：代理、配置、工具 <span class="duration-badge">20 分钟</span>

`google-antigravity` SDK 有三个构建块：`Agent`、`LocalAgentConfig` 和工具（纯 Python 函数）。掌握这些，你就可以构建任何东西。

### 工具

工具是一个**纯 Python 函数**。没有包装类，没有装饰器。代理根据文档字符串（docstring）决定何时调用它——这就是完整的接口契约。

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

> **工具的关键规则：**
>
> - 使用显式的类型注解 —— `str`、`int`、`bool`、`list[str]`。不要使用 `typing.Optional`。
> - 对于可选参数，使用 `None` 作为默认值：`param: str = None`
> - 文档字符串就是工具的 schema —— 模型通过读取它来决定何时以及如何调用该工具。它是写给模型看的，而不是写给人类看的。
> - 保持工具的狭窄和专注。每个工具只做一件事。

### 带有会话状态的工具

要在工具内部读写**会话状态**，请声明一个类型为 `ToolContext` 的参数。
SDK 会自动检测它，在调用时将其注入，并**从展示给模型的 schema 中将其剥离**：

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

### 代理 + 配置

`Agent` 是唯一的入口点。所有的配置都在 `LocalAgentConfig` 中进行：

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

> **`async with Agent(config) as agent:`** —— 始终使用上下文管理器。它会启动 Go 运行时桥接器（`bin/localharness`）并在退出时干净地将其卸载。

### 模型选择

根据任务匹配合适的模型。注重成本的策略：

| 角色 | 模型 | 理由 |
| :-- | :-- | :-- |
| 常规任务、代码审查 | `gemini-3.5-flash` | SDK 默认 —— 成本效益高、速度快 |
| 编排、路由、规划 | `gemini-3.1-pro-preview` | 复杂推理、多步决策 |
| 图像生成任务 | `gemini-3.1-flash-image-preview` | SDK 默认的图像生成模型 |
| 高风险分析 | 带有 `ThinkingLevel.HIGH` 的 `gemini-3.1-pro-preview` | 用于合规/安全的深度推理 |

> **切勿使用** `gemini-1.5-flash`、`gemini-1.5-pro`。已弃用。

### 技能

技能是在运行时加载的 `SKILL.md` 文件，用于注入领域知识。保持你的系统提示词精简 —— 从文件中加载专业知识：

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

技能也可以通过 `LocalAgentConfig(skills_paths=["/path/to/skills/"])` 原生加载 —— SDK 会自动发现 `SKILL.md` 文件。

---

## 3.3 — 策略与安全 <span class="duration-badge">10 分钟</span>

**策略是您首先要配置的内容** ——它控制代理在未经人类批准的情况下被允许执行的操作。每个 `LocalAgentConfig` 都需要一个 `policies=` 列表：

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

> **优先级顺序：** `specific_deny` > `specific_ask` > `specific_allow` > `wildcard_deny` > `wildcard_ask` > `wildcard_allow`

---

## 3.4 — 钩子：可观测性与控制 <span class="duration-badge">10 分钟</span>

钩子允许您拦截并响应代理生命周期中的每个事件——用于日志记录、审计、护栏或自定义审批流程：

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

**钩子类型：**

| 钩子 | 阻塞执行 | 修改数据 | 用途 |
| :-- | :-- | :-- | :-- |
| `@hooks.pre_tool_call_decide` | 是 | 否 | 批准/拒绝工具调用 |
| `@hooks.post_tool_call` | 否 | 否 | 日志记录、指标 |
| `@hooks.pre_turn` | 否 | 否 | 轮次级别日志记录 |
| `@hooks.post_turn` | 否 | 否 | 响应日志记录 |
| `@hooks.on_session_start/end` | 否 | 否 | 环境设置/清理 |
| `@hooks.on_tool_error` | 是 | 是 | 错误恢复 |

---

## 3.5 — 多代理编排 <span class="duration-badge">15 分钟</span>

`google-antigravity` 没有 `SequentialAgent` 或 `ParallelAgent` 类。多代理通过两种方式实现：**模型驱动**（让代理生成子代理）或 **Python 驱动**（直接由你编排 `Agent` 实例）。

### 模式 A — 模型驱动的子代理

在 capabilities 中启用 `START_SUBAGENT`。当模型决定委派任务时，它会调用此功能：

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

### 模式 B — 顺序流水线（Python 驱动）

将一个代理的输出作为下一个代理的输入：

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

### 模式 C — 并行分析

使用 `asyncio.gather` 同时运行独立的代理：

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

> **何时使用并行：** 任何时候当你需要进行 N 个独立的分析时。与顺序运行相比，这可以将实际耗时减少 60–80%。

---

## 3.6 — 流式与结构化输出 <span class="duration-badge">5 min</span>

### 流式响应

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

### 结构化输出

将代理的输出绑定到 Pydantic 模式：

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

## 3.7 — 会话恢复与持久化 <span class="duration-badge">5 min</span>

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

## 3.8 — 触发器：自主后台代理 <span class="duration-badge">5 分钟</span>

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

## 3.9 — 项目结构约定 <span class="duration-badge">5 min</span>

构建您的代理项目以提高可维护性：

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

### 部署到 Cloud Run

作为标准的 Python 异步应用程序进行部署：

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

> **提示：** 在运行之前设置 `GOOGLE_CLOUD_PROJECT` 和 `GOOGLE_CLOUD_REGION`（例如 `us-central1`）。

---

## 动手实践练习

<div class="exercise-card" markdown>

### :material-code-braces: 练习 10：你的第一个 AGY 代理

**文件：** [`ex10_first_agent.md`](exercises/ex10_first_agent.md)  
**时长：** 45 分钟  
**构建：** 一个**代码审查代理**，它能够读取文件、识别问题并生成结构化的审查报告。

**你将实现的内容：**

1. 定义 3 个工具：`read_file`、`list_directory`、`record_finding`（使用 `ToolContext`）
2. 编写带有审查标准的系统提示词（从 `SKILL.md` 加载）
3. 使用 `policy.allow_all()` 和 `CapabilitiesConfig` 配置 `LocalAgentConfig`
4. 添加一个 `@hooks.pre_tool_call_decide` 安全护栏
5. 使用流式输出和结构化的 `ReviewResult` Pydantic 模式运行

</div>

<div class="exercise-card" markdown>

### :material-graph: 练习 11：多代理流水线

**文件：** [`ex11_multi_agent_pipeline.md`](exercises/ex11_multi_agent_pipeline.md)  
**时长：** 45 分钟  
**构建：** 一个**先写后审流水线** —— 技术作家代理生成文档，然后合规分析师审查其中的 GDPR 漏洞。

**你将实现的内容：**

1. 构建一个 `technical_writer` 代理，通过 `skills_paths` 加载 GDPR SKILL.md
2. 构建一个带有 `response_schema=ComplianceReport` 的 `compliance_analyst` 代理
3. 将它们按顺序连接：作家的输出作为输入传递给分析师
4. 添加一个使用 `asyncio.gather` 的并行变体，用于同时进行草稿编写和法律检查
5. 添加会话恢复：分析师读取作家的 `conversation_id` 以加载上下文
6. 使用 `gcloud run deploy` 将其作为 `my-pipeline` 部署到 Cloud Run

</div>

---

## 总结：SDK 构建块

| 原语 | 作用 | 何时使用 |
| :-- | :-- | :-- |
| `Agent` | 带有工具、钩子和策略的单一 LLM 代理 | 核心 — 每个代理都从这里开始 |
| `LocalAgentConfig` | 所有配置集中在一处（模型、工具、策略、钩子） | 总是 |
| `tools=[fn]` | 普通的 Python 可调用对象，文档字符串即为模式（schema） | 任何外部操作 |
| `ToolContext` | 注入到工具中的状态读/写 | 管道中的有状态工具 |
| `policy.allow_all()` | 自主批准所有工具调用 | 受信任的沙盒代理 |
| `policy.deny("run_command")` | 阻止特定的工具类型 | 安全护栏 |
| `@hooks.pre_tool_call_decide` | 在执行前阻止/批准工具调用 | 安全守卫 |
| `@hooks.post_tool_call` | 观察已完成的工具调用 | 审计日志 |
| `response_schema=` | 将输出绑定到 Pydantic 模式 | 结构化数据提取 |
| `async for delta in response:` | 在文本到达时进行流式传输 | 长文本生成 |
| `asyncio.gather(...)` | 并行运行代理 | 独立分析 |
| `every(60, handler)` | 按时间间隔触发代理 | 后台监视器 |
| `on_file_change(path, fn)` | 在文件系统事件上触发代理 | 实时代码监视器 |
| `skills_paths=[...]` | 在运行时加载 SKILL.md 文件 | 可移植的领域专业知识 |
| `conversation_id=` | 恢复之前的会话 | 多会话工作流 |

---

## 下一步

→ 继续前往 **[模块 4：多代理与高级模式](multi-agent-advanced.md)**

→ 参考：**[速查表](cheatsheet.md)** — 所有命令一览
