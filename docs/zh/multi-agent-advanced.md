# 模块 4：多代理与高级功能 <span class="duration-badge">45 分钟</span>

> **agy 超越聊天助手之处。** 本模块涵盖了使 agy-cli 区别于所有其他 AI 编码工具的功能：并行子代理、使用 `/btw` 进行任务中途的模型引导、后台调度以及会话恢复。

---

## 4.0 — agy 代理模型 <span class="duration-badge">5 分钟</span>

agy-cli 可以生成**子代理**——并行运行的隔离任务运行器，每个都有自己的工作区上下文。与运行带有独立 agy 会话的多个终端选项卡不同，子代理是协调的：它们可以共享工作区、在隔离的分支上工作，或者在克隆的副本上操作。

三种工作区模式：

| 模式 | 含义 | 适用场景 |
| :-- | :-- | :-- |
| `inherit` | 子代理共享同一个工作区 | 附加任务——预期不会发生冲突 |
| `branch` | 子代理获取一个隔离的克隆 | 对相同文件的并行更改 |
| `share` | git 工作树——隔离的分支，共享的仓库 | 真正的并行开发 |

### 切换模型

使用 `/model` 在会话中途切换活动模型——当您需要对特定任务进行更深度的推理时非常有用：

```bash
/model
```

这将打开一个模型选择器，显示可用选项（Gemini 3.5 Flash、Gemini 3.1 Pro、Claude Sonnet 4.6 等）。

> 📖 完整模型列表：[模型文档](https://www.antigravity.google/docs/models)

---

## 4.1 — 派生子代理 <span class="duration-badge">15 min</span>

> **模式：并行执行** — 调度多个代理同时工作。
> 📖 完整参考：[子代理文档](https://www.antigravity.google/docs/subagents)

### 来自交互式会话

```text
> Spawn a subagent to write unit tests for the auth module while I work on the API refactor.
```

agy 将派生一个子代理，报告其 ID，并继续您的主会话。该子代理独立工作。

```text
> What's the status of the test-writing subagent?
```

```text
> Show me what the test subagent produced.
```

### 使用 /agents 管理子代理

使用 `/agents` 面板查看所有活动的子代理、它们的状态和输出：

```bash
/agents
```

主对话中的关键快捷键：

| 快捷键 | 操作 |
| :-- | :-- |
| `Ctrl+J` | 传送到等待批准的子代理 — 直接跳转以审查其请求 |
| `Ctrl+K` | 从主对话中快速批准 — 无需切换即可批准子代理的待处理操作 |

子代理生命周期：**运行中 → 空闲 → 已终止**

### 限制与内置类型

- **最大深度：** 10（子代理可以派生自己的子代理，最多 10 层）
- **内置类型：** `research`（网络研究）、`browser`（浏览器自动化）、`self`（通用）

### 并行审计模式

```text
> Spawn three subagents in parallel:
> 1. Security audit — scan for hardcoded credentials, injection risks, and insecure dependencies
> 2. Performance audit — find N+1 queries, unindexed lookups, and memory leaks
> 3. Coverage audit — identify untested functions and missing integration tests
>
> Use branch workspace mode for each. Report back when all three complete.
```

观察三个独立的分析同时运行。当它们完成时，agy 会综合这些结果。

!!! tip "惊艳时刻"
    三个专门的代理在您的代码库上并行运行，每个代理都拥有完整的上下文，每个代理都产生独立的发现。正是这种模式使 agy 与基于聊天的助手产生了质的区别。

### 对抗性审查模式

```text
> Spawn a subagent to act as an adversarial reviewer for the changes in this branch.
> Its only job: find reasons why this code should NOT be merged.
> It should challenge every assumption and look for edge cases the implementer missed.
```

对抗性审查模式对于安全敏感的更改、基础设施修改或任何仅仅一句“看起来不错 (looks good to me)”还不够的 PR 来说，特别强大。

---

## 4.2 — /btw: 任务中途引导 <span class="duration-badge">10 分钟</span>

> **模式：无中断引导** — 在不停止任务的情况下，将上下文注入到正在运行的任务中。

`/btw` 是 agy 最具特色的功能之一。当 agy 处于任务中途时，您可以向它发送消息而无需取消当前操作。

### 工作原理

```text
> Refactor the entire authentication module to use JWT instead of sessions. This will touch multiple files. Start with the backend.
```

*agy 开始工作……在它运行期间：*

```bash
/btw Actually, keep backward compatibility with sessions for 30 days — implement a dual-mode auth.
```

agy 会在不停止的情况下将您的备注整合到正在进行的任务中。这就像在冲刺（sprint）中途给开发人员留下一张便利贴——他们看到后就会做出调整。

### /btw 的使用场景

```bash
/btw The API rate limit is 100 req/min, factor that into any retry logic you add.
```

```bash
/btw The team uses conventional commits — make sure any commit messages follow that format.
```

```bash
/btw Skip the frontend changes for now, just focus on the backend API.
```

!!! info "与中断的对比"
    如果没有 `/btw`，引导一个长时间运行的任务意味着取消它、调整您的提示词并重新启动——从而丢失所有进度。`/btw` 让您无需付出这种代价即可纠正路线。

---

## 4.3 — 后台执行与调度 <span class="duration-badge">10 分钟</span>

> **模式：异步 agy** — 启动长时间运行的任务，并在其完成时收到通知。

### 后台任务

agy 支持异步执行 — 您可以启动任务并继续工作。agy 会在任务完成时通知您。

```text
> In the background, do a comprehensive security audit of this entire codebase. Take as long as you need. Notify me when done.
```

agy 会在不阻塞终端的情况下运行审计。完成时，您将收到包含结果的通知。

### 调度任务

agy 支持用于定期分析的 cron 风格调度：

```text
> Schedule a nightly code quality report every day at 2am. It should check for new TODOs, failing tests, and dependency updates. Save the report to reports/nightly-YYYY-MM-DD.md.
```

支持 Cron 表达式（最多 5 个字段）：

```bash
# Run at 2am daily
0 2 * * *

# Run every Monday at 9am
0 9 * * 1

# Run every 15 minutes
*/15 * * * *
```

!!! warning "调度具有会话持久性"
    只要 agy 正在运行，调度任务就会跨会话持久存在。检查 `/tasks` 以查看和管理调度任务。

---

## 4.4 — 会话恢复 <span class="duration-badge">5 min</span>

> **模式：长时间运行的工作** — 准确地从上次中断的地方继续。
> 📖 完整参考：[使用 Antigravity CLI](https://www.antigravity.google/docs/cli-using)

### 恢复最近的会话

在 agy 内部，使用 `/resume` 斜杠命令：

```bash
/resume
```

这将打开一个会话选择器，显示你最近的对话。选择一个进行恢复。

### 浏览和切换会话

```bash
/switch
```

与 `/resume` 相同 — 这两个命令都会打开会话选择器。

### 退出时自动恢复

当你退出 agy 会话时，agy 会打印出恢复该会话的确切命令：

```bash
Session saved. Resume with: agy --conversation <conversation-id>
```

你可以直接从终端使用此命令来重新进入。

### 使用场景：多日功能开发工作

```bash
# Day 1: Start a feature
agy -i "I'm building a payment integration feature. Let's start with the backend API design."

# Day 2: Resume from terminal
agy --conversation <conversation-id>

# Or from inside agy:
# /resume
```

```text
> What was the last thing we decided about the payment API schema?
```

agy 将拥有完整的上下文，包括已编写的代码、已做出的决策以及未解决的问题。

---

## 4.5 — 高级：组合模式 <span class="duration-badge">可选</span>

> **完整能力栈：** 子代理 + /btw + 后台运行 + 调度 + 会话恢复。

### 企业级事件响应

```text
> I'm starting an incident response for a production issue. Spawn:
> 1. A log-analyzer subagent (branch mode) — read the last 1000 lines of app.log and identify the root cause
> 2. A config-checker subagent (branch mode) — review all environment configs and recent deploys for anomalies
>
> Report back when both complete. I'll be monitoring in the meantime.
```

在它们运行时：

```bash
/btw The incident started at 14:32 UTC. Focus analysis on that window.
```

这是多代理事件分类——两个并行的调查，且可在运行中途进行引导。

---

## 模块 4 练习

<div class="exercise-card" markdown>

### :material-file-document: 练习 4：子代理

**文件：** [`ex04_subagents.md`](exercises/ex04_subagents.md)
**时长：** 20 分钟
**目标：** 生成一个并行的审计团队。练习对抗性审查者模式。

</div>

<div class="exercise-card" markdown>

### :material-file-document: 练习 5：/btw 与调度

**文件：** [`ex05_btw_scheduling.md`](exercises/ex05_btw_scheduling.md)
**时长：** 20 分钟
**目标：** 使用 /btw 引导长时间运行的任务。安排定期的代码质量报告。

</div>

<div class="exercise-card" markdown>

### :material-file-document: 练习 6：沙盒治理

**文件：** [`ex06_sandbox_governance.md`](exercises/ex06_sandbox_governance.md)  
**时长：** 15 分钟  
**目标：** 在 settings.json 中配置沙盒模式，并使用权限模型进行测试。

</div>

---

## 您已完成

→ **[速查表](cheatsheet.md)** — 所有四个模块的每个命令集中于一处

→ **[参考：DevOps 模式](devops-automation.md)** — `--print` 流水线、CI/CD、沙盒深度解析

→ **[参考：插件生态系统](plugin-ecosystem.md)** — 完整的插件生命周期参考
