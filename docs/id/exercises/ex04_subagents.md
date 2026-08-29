# Exercise 4: Built-In & Custom Subagents

> **Duration:** 25 min (Fast: 15 min · Average: 25 min · Thorough: 35 min) | **Module:** 4 — Multi-Agent & Advanced

---

## Objective

Master parallel subagent execution in Antigravity CLI:
1. Dispatch parallel built-in subagents using `branch` and `inherit` workspace modes.
2. Define a **Custom Subagent** in `.agents/agents/` using the YAML frontmatter schema.
3. Manage and inspect active subagents using the interactive **`/agents`** panel and keyboard shortcuts (**`Alt+J`** / **`Ctrl+K`**).
4. Coordinate collaborative multi-agent workflows with **`/teamwork-preview`**.

---

## Part 1: Dispatch Parallel Built-In Subagents (8 min)

Launch agy interactively:

```bash
agy
```

Dispatch a parallel audit team on your codebase:

```text
> Spawn two subagents in parallel using branch workspace mode:
> 1. A security auditor — scan for: hardcoded credentials, injection vulnerabilities, exposed sensitive data, and insecure dependencies
> 2. A test coverage auditor — identify: untested public functions, missing edge cases, and integration test gaps
>
> Report back when both complete with a combined findings summary.
```

While they execute in the background:

* Type **`/agents`** to open the Agent Manager Panel. Observe the live checklist showing subagent IDs, roles, lifecycle states (`running` / `done`), and active tool steps.
* Highlight an active subagent with `↑/↓` and press **`Enter`** to inspect its private reasoning trajectory and tool outputs. Press **`Esc`** to return.
* When subagents request tool approvals, press **`Alt+J`** to teleport focus directly to the pending approval, or press **`Ctrl+K`** to fast-path approve from the main conversation.

---

## Part 2: Define a Custom Subagent (`.agents/agents/`) (7 min)

Create the project workspace agents directory:

```bash
mkdir -p .agents/agents
```

Create a custom security auditor definition in `.agents/agents/security-auditor.md`:

```markdown
---
name: security-auditor
description: Specialized subagent for security audits, OWASP Top 10 scanning, and vulnerability reviews.
tools:
  - view_file
  - grep_search
  - find_by_name
  - run_command
mainAgent: false
subagent: true
model: pro
commandExecutionPolicy: sandbox
---

# System Prompt
You are a principal security engineer conducting a deep source code audit.

# Review Guidelines
1. Systematically check for SQL injection, unescaped user input (XSS), missing authorization middleware, hardcoded secrets, and path traversal flaws.
2. For every finding, provide: Severity, File path, Line number, Problem explanation, and concrete remediation code.
3. Perform read-only static analysis unless explicitly instructed to apply fixes.
```

---

## Part 3: Delegate to Your Custom Subagent (5 min)

Start a new agy session:

```bash
agy
```

Verify that your custom agent is discovered:

```text
> /agents
```

Notice that `security-auditor` is listed in the custom subagents registry.

Now trigger delegation naturally in chat:

```text
> Delegate a security review of our source code to the security-auditor subagent.
```

Observe how `agy`:
1. Identifies the `security-auditor` specialist from its YAML description.
2. Invokes it via `invoke_subagent` with the `pro` reasoning tier.
3. Constrains its toolset strictly to `[view_file, grep_search, find_by_name, run_command]` in sandbox mode.
4. Synthesizes the subagent's structured report back into your primary thread upon completion.

---

## Part 4: Multi-Agent Teamwork Preview (5 min)

For complex multi-file refactoring or large milestone decomposition, preview Antigravity's collaborative agent teams:

```text
> /teamwork-preview Refactor our database query layer to use prepared statements across all controllers. Coordinate a team to implement changes and verify with unit tests.
```

Observe how teamwork orchestrates multiple coordinated roles (planner, implementer, verifier) working in parallel git worktrees.

---

## Pro Tips & Key Watchouts

!!! tip "Key Things to Watch For"
    1. **Tool Name Validation:** When configuring `tools` in YAML frontmatter, ensure exact tool names are used (`view_file`, `grep_search`, `find_by_name`, `replace_file_content`, `run_command`). Misspelled or unmapped tool names may cause subagent processes to hang.
    2. **Nesting Depth Limits:** Subagents can spawn their own subagents up to a hard ceiling of **10 nesting levels** to prevent infinite recursion.
    3. **Idle State & Auto-Wake:** Subagents transition from `Running` to `Idle` upon completing a task. If you send a follow-up message to a subagent ID, it automatically re-awakens with full context retention.
    4. **Automatic Worktree Cleanup:** Subagents spawned in `branch` workspace mode create temporary git worktrees that are automatically cleaned up when the subagent finishes or is killed.

---

## Completion Criteria

- [ ] Spawned parallel built-in subagents and inspected active states via `/agents`
- [ ] Navigated approvals using `Alt+J` (teleport) and `Ctrl+K` (fast-path approve)
- [ ] Created a Custom Subagent `.md` file with valid YAML frontmatter in `.agents/agents/`
- [ ] Successfully delegated a task to the custom subagent via natural language
- [ ] Tested `/teamwork-preview` collaborative agent team orchestration


