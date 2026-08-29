# Module 4: Multi-Agent & Advanced <span class="duration-badge">45 min</span>

> **Where agy goes beyond a chat assistant.** This module covers the features that separate agy-cli from every other AI coding tool: parallel subagents, mid-task steering with `/btw`, background scheduling, and session resumption.

---

## 4.0 — The agy Agent Model <span class="duration-badge">5 min</span>

agy-cli can spawn **subagents** — isolated task runners that operate in parallel, each with their own workspace context. Instead of executing every step serially, the primary agent delegates tasks (running tests, performing deep codebase searches, or refactoring modules) to dedicated subagents. This preserves the parent agent's context window while parallelizing execution.

### Workspace Modes

| Mode | What it means | Use when |
| :-- | :-- | :-- |
| `inherit` | Subagent shares the parent's working directory | Additive tasks where no concurrent file conflicts are expected |
| `branch` | Subagent gets an isolated Git clone / branch | Parallel changes to the same files or destructive refactoring |
| `share` | Git worktree — isolated branch sharing directory storage | True parallel development with minimal disk overhead |

### Model Selection (`/model`)

Use `/model` to inspect and switch the active model tier:

```bash
/model
```

Available model options include **Gemini 3.7 Flash** (default speed & reasoning), **Gemini 3.6 Flash**, **Gemini 3.5 Flash**, **Gemini 3.1 Pro** (complex orchestration), **Claude Sonnet / Opus 4.6**, and **GPT-OSS-120b**.

> 📖 Full model list: [Models docs](https://www.antigravity.google/docs/models)

---

## 4.1 — Built-In & Custom Subagents <span class="duration-badge">20 min</span>

> **Pattern: Parallel Specialization** — dispatch specialized agents configured for specific roles and toolsets.
> 📖 Full reference: [Subagents docs](https://antigravity.google/docs/subagents) · [CLI Subagents](https://antigravity.google/docs/cli/subagents)

### Built-In Subagents

Antigravity comes pre-packaged with several specialized subagents:

* **`research`**: Optimized for codebase exploration, symbol lookups, and structural navigation.
* **`browser`**: Operates sandboxed web browsers to perform UI testing and DOM analysis (invoked via `/browser`).
* **`self`**: A direct clone of the parent agent, inheriting identical system prompts and toolsets.

### Defining Custom Subagents (`.md`)

You can define reusable custom subagents in Markdown format (`.md`) with YAML frontmatter.

#### Agent Location and Discovery

Antigravity automatically discovers custom agent definitions across three hierarchical scopes:

| Scope | Discovery Path | Use Case |
| :-- | :-- | :-- |
| **Workspace** | `.agents/agents/<name>.md` or `.agents/agents/<name>/agent.md` | Team/project-specific specialists committed to git |
| **Global** | `~/.gemini/config/agents/<name>.md` or `.../agents/<name>/agent.md` | Personal agents available across all projects on your machine |
| **Plugins** | `plugins/<plugin_name>/agents/` | Bundled agents distributed with CLI plugins |

#### YAML Frontmatter Specification

```markdown
---
name: security-auditor
description: Specialized subagent for security audits, static analysis, and vulnerability reviews.
tools:
  - view_file
  - grep_search
  - find_by_name
  - run_command
mainAgent: false
subagent: true
model: pro
commandExecutionPolicy: sandbox
skills:
  - skills/security-checklist
---

# System Prompt
You are an expert security auditor and code reviewer. Inspect source code for vulnerabilities, injection flaws, and exposed credentials.

# Review Guidelines
1. Perform thorough static analysis without altering files unless explicitly instructed.
2. Provide concrete remediation snippets for each finding.
```

#### Frontmatter Configuration Parameters

| Property | Type | Default | Description |
| :-- | :-- | :-- | :-- |
| `name` | `string` | *(Required)* | Unique identifier for the custom agent. |
| `description` | `string` | *(Required)* | Purpose description used by the planner to determine when to delegate tasks. |
| `tools` | `string[]` | `[]` | Explicit list of permitted tools (`view_file`, `replace_file_content`, `grep_search`, `run_command`, etc.). |
| `mainAgent` | `boolean` | `true` | If `true`, allows selection as the primary session agent in `/agents`. |
| `subagent` | `boolean` | `true` | If `true`, allows invocation via the `invoke_subagent` tool. |
| `model` | `string` | `inherit` | Model tier used when invoked (`inherit`, `flash`, or `pro`). |
| `commandExecutionPolicy` | `string` | `sandbox` | Auto-execution policy for shell commands (`off`, `auto`, `eager`, `sandbox`). |
| `mcpServers` | `object[]` | `[]` | Custom MCP servers configured for this subagent. |
| `skills` / `plugins` | `string[]` | `[]` | List of skill paths or plugin dependencies. |

---

## 4.2 — Subagent Lifecycle & Inter-Agent Communication <span class="duration-badge">10 min</span>

### Subagent State Machine

Subagents execute asynchronously in the background across three lifecycle states:

```
┌─────────┐      task complete       ┌──────┐      kill / finish      ┌────────┐
│ Running │ ───────────────────────> │ Idle │ ──────────────────────> │ Killed │
└─────────┘                          └──────┘                         └────────┘
     ▲                                  │
     │        incoming message          │
     └──────────────────────────────────┘
```

1. **Running:** Actively calling tools, generating responses, and executing tasks. (Cancel at any time with `k` in the CLI).
2. **Idle:** Completed its current task, sent a result message to the parent agent, and paused. **Auto-reawakens to Running** upon receiving a message, retaining full context from prior turns.
3. **Killed:** Permanently terminated. Temporary Git worktrees are automatically cleaned up, while JSONL execution transcripts remain recorded in `~/.gemini/antigravity-cli/brain/<session-id>/`.

### Inter-Agent Messaging & Nesting Limits

* **Direct Routing:** Agents communicate by passing messages to unique conversation IDs (`send_message`).
* **Auto-Wake:** Sending a message to an idle subagent immediately wakes it up to process new instructions.
* **Nesting Depth Limit:** A maximum nesting depth of **10 levels** is enforced to prevent runaway recursive delegation.
* **Permission Bubbling:** If a subagent encounters an action requiring user authorization, the request bubbles up directly to your active CLI prompt.

---

## 4.3 — CLI Ergonomics & Agent Management <span class="duration-badge">10 min</span>

### Managing Agents with `/agents`

Open the interactive Agent Manager Panel:

```bash
/agents
```

The `/agents` panel displays:
* **Identifier & Role:** Unique subagent ID and specialized role.
* **State:** Live status indicators (`running`, `done`, `killed`, `error`).
* **Step Summary:** Real-time summary of the tool or reasoning step currently being executed.
* **Deep-Dive:** Highlight an agent with `↑/↓` and press `Enter` to inspect its private thoughts, reasoning logs, and tool outputs. Press `Esc` to return.

### Background Task Monitor (`/tasks`)

For non-agentic background shell operations (e.g. build jobs, background test suites):

```bash
/tasks
```

### High-Efficiency Keyboard Shortcuts

| Shortcut | Action | Description |
| :-- | :-- | :-- |
| **`Alt+J`** | Teleport to Subagent | Instantly jumps from your main conversation into the Detail View of the next subagent awaiting approval. |
| **`Ctrl+K`** | Fast-Approve Action | Instantly approves a pending subagent tool request from the main prompt bar without switching panels. |
| **`Ctrl+O`** | Toggle Trajectory | Expands/collapses the full reasoning trajectory in the active turn. |

### Multi-Agent Teamwork (`/teamwork-preview`)

For large software projects and multi-file refactoring campaigns, launch collaborative agent teams:

```bash
/teamwork-preview
```

Coordinated teams handle milestone decomposition, parallel implementation across worktrees, and independent verification checks.

---

## 4.4 — Parallel Execution Patterns <span class="duration-badge">10 min</span>

### Parallel Audit Pattern

```text
> Spawn three subagents in parallel using branch workspace mode:
> 1. Security auditor — scan for hardcoded credentials, injection risks, and insecure dependencies
> 2. Performance auditor — find N+1 queries, unindexed lookups, and memory leaks
> 3. Coverage auditor — identify untested functions and missing integration tests
>
> Report back when all three complete with a synthesized findings summary.
```

### Adversarial Review Pattern

```text
> Spawn a subagent to act as an adversarial reviewer for the changes in this branch.
> Its only job: find reasons why this code should NOT be merged.
> Challenge every assumption, probe concurrency edge cases, and be skeptical of everything.
```

---

## 4.2 — /btw: Mid-Task Steering <span class="duration-badge">10 min</span>

> **Pattern: Steer Without Interrupting** — inject context into a running task without stopping it.

`/btw` is one of agy's most distinctive features. When agy is mid-task, you can send it a message without cancelling the current operation.

### How It Works

```text
> Refactor the entire authentication module to use JWT instead of sessions. This will touch multiple files. Start with the backend.
```

*agy starts working... while it's running:*

```bash
/btw Actually, keep backward compatibility with sessions for 30 days — implement a dual-mode auth.
```

agy incorporates your note into the ongoing task without stopping. It's like leaving a sticky note for a developer in the middle of a sprint — they see it and adjust.

### Use Cases for /btw

```bash
/btw The API rate limit is 100 req/min, factor that into any retry logic you add.
```

```bash
/btw The team uses conventional commits — make sure any commit messages follow that format.
```

```bash
/btw Skip the frontend changes for now, just focus on the backend API.
```

!!! info "Contrast with interrupting"
    Without `/btw`, steering a long-running task means cancelling it, adjusting your prompt, and restarting — losing all progress. `/btw` lets you course-correct without that cost.

---

## 4.3 — Background Execution & Scheduling <span class="duration-badge">10 min</span>

> **Pattern: Async Agy** — kick off long-running tasks and get notified when they finish.

### Background Tasks

agy supports asynchronous execution — you can kick off a task and continue working. agy notifies you when it completes.

```text
> In the background, do a comprehensive security audit of this entire codebase. Take as long as you need. Notify me when done.
```

agy runs the audit without blocking your terminal. When it finishes, you receive a notification with the results.

### Scheduled Tasks

agy supports cron-style scheduling for recurring analysis:

```text
> Schedule a nightly code quality report every day at 2am. It should check for new TODOs, failing tests, and dependency updates. Save the report to reports/nightly-YYYY-MM-DD.md.
```

Cron expressions (up to 5 fields) are supported:

```bash
# Run at 2am daily
0 2 * * *

# Run every Monday at 9am
0 9 * * 1

# Run every 15 minutes
*/15 * * * *
```

!!! warning "Scheduling is session-persistent"
    Scheduled tasks persist across sessions as long as agy is running. Check `/tasks` to view and manage scheduled tasks.

---

## 4.4 — Session Resumption <span class="duration-badge">5 min</span>

> **Pattern: Long-Running Work** — pick up exactly where you left off.
> 📖 Full reference: [Using Antigravity CLI](https://www.antigravity.google/docs/cli-using)

### Resume the Most Recent Session

From inside agy, use the `/resume` slash command:

```bash
/resume
```

This opens a session picker showing your recent conversations. Select one to resume.

### Browse and Switch Sessions

```bash
/switch
```

Same as `/resume` — both commands open the session picker.

### Auto-Resume on Exit

When you exit an agy session, agy prints the exact command to resume it:

```bash
Session saved. Resume with: agy --conversation <conversation-id>
```

You can use this command directly from the terminal to jump back in.

### Use Case: Multi-Day Feature Work

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

agy will have the full context, including code written, decisions made, and open questions.

---

## 4.5 — Advanced: Combining Patterns <span class="duration-badge">Optional</span>

> **The full power stack:** subagents + /btw + background + scheduling + conversation resumption.

### Enterprise Incident Response

```text
> I'm starting an incident response for a production issue. Spawn:
> 1. A log-analyzer subagent (branch mode) — read the last 1000 lines of app.log and identify the root cause
> 2. A config-checker subagent (branch mode) — review all environment configs and recent deploys for anomalies
>
> Report back when both complete. I'll be monitoring in the meantime.
```

While they run:

```bash
/btw The incident started at 14:32 UTC. Focus analysis on that window.
```

This is multi-agent incident triage — two parallel investigations, steerable mid-flight.

---

## Module 4 Exercises

<div class="exercise-card" markdown>

### :material-file-document: Exercise 4: Subagents

**File:** [`ex04_subagents.md`](exercises/ex04_subagents.md)
**Duration:** 20 min
**Objective:** Spawn a parallel audit team. Practice the adversarial reviewer pattern.

</div>

<div class="exercise-card" markdown>

### :material-file-document: Exercise 5: /btw & Scheduling

**File:** [`ex05_btw_scheduling.md`](exercises/ex05_btw_scheduling.md)
**Duration:** 20 min
**Objective:** Use /btw to steer a long-running task. Schedule a recurring code quality report.

</div>

<div class="exercise-card" markdown>

### :material-file-document: Exercise 6: Sandbox Governance

**File:** [`ex06_sandbox_governance.md`](exercises/ex06_sandbox_governance.md)  
**Duration:** 15 min  
**Objective:** Configure sandbox mode in settings.json and test with the permissions model.

</div>

---

## Next Steps

→ **[Module 5: Building ADK Agents with agents-cli](agents-cli.md)** — build, evaluate, and deploy ADK agents on Google Cloud

→ **[Cheatsheet](cheatsheet.md)** — every command and shortcut across the workshop

→ **[Reference: DevOps Patterns](devops-automation.md)** — `--print` pipelines, CI/CD, sandbox deep dive

→ **[Reference: Plugin Ecosystem](plugin-ecosystem.md)** — full plugin lifecycle reference
