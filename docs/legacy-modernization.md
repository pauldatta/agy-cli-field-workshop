# Module 2: Legacy Codebase Modernization

<div class="module-header" markdown>
**Duration:** ~75 minutes  
**Goal:** Migrate a legacy application safely using Antigravity CLI primitives — strict permissions gating, agent self-onboarding, parallel subagent analysis, hooks as guardrails, and `/rewind` as your safety net.  
**Exercise PRDs:** [.NET Modernization](exercises/ex08_dotnet_modernization.md) · [Java Upgrade](exercises/ex09_java_upgrade.md)
</div>

> 📖 Sources: [Permissions](https://antigravity.google/docs/permissions) · [Strict Mode](https://antigravity.google/docs/strict-mode) · [Subagents](https://antigravity.google/docs/subagents) · [Skills](https://antigravity.google/docs/skills) · [Hooks](https://antigravity.google/docs/hooks) · [cli-features](https://antigravity.google/docs/cli-features) · [cli-using](https://antigravity.google/docs/cli-using)

---

!!! example "Video Walkthrough: Legacy Modernization"
    <video controls width="100%" poster="assets/videos/module_02_poster.png">
      <source src="assets/videos/module_02_legacy_modernization.mp4" type="video/mp4">
      Download video: [module_02_legacy_modernization.mp4](assets/videos/module_02_legacy_modernization.mp4)
    </video>

---

## Why Legacy Modernization Is Hard

The risk in large migrations isn't the code changes — it's the **unknowns**. You don't know what you'll break until it's broken. The three failure modes are:

1. **Scope creep** — the agent refactors things you didn't ask it to touch
2. **Context collapse** — after a long session, the agent loses track of your migration constraints
3. **No rollback** — a wrong change cascades before you can stop it

AGY's primitives address all three directly.

---

## 2.1 — Strict Permissions: Read Before You Write <span class="duration-badge">15 min</span>

The AGY equivalent of "Plan Mode" is **strict permissions** — a hard gate that denies all file writes and shell commands until you explicitly permit them.

### Lock Down Before You Explore

```bash
/permissions
```

Set the level to `strict`:

```bash
# In the permissions dialog, select: strict
# Or set directly in settings.json:
```

```json
{
  "permissions": {
    "mode": "strict"
  }
}
```

In `strict` mode the agent can read files, search the web, and reason — but **cannot write, delete, or execute anything**. It's a hard wall, not a soft prompt.

> 📖 Source: [Strict Mode](https://antigravity.google/docs/strict-mode) · [Permissions](https://antigravity.google/docs/permissions)

### Now Investigate Freely

With writes locked, give the agent an unconstrained read mandate:

```text
Analyze this entire codebase for a migration. Map:
1. Framework versions and dependency tree (check package.json / pom.xml / .csproj)
2. Architectural patterns in use (MVC, layered, hexagonal)
3. All deprecated API usage (javax.* imports, legacy auth patterns, XML config)
4. Configuration files and external property sources
5. Test frameworks and coverage gaps
6. Migration risks ordered by severity
```

> **What's happening:** The agent reads every file it needs, traces imports and call chains, and builds a mental model — all with zero risk of modification. This is your reconnaissance phase.

### Review the Plan in Your Editor

Once the agent produces a migration plan, open it in your editor to refine it:

```text
ctrl+g
```

This drops you into `$EDITOR` with the current agent output. Edit constraints, add team-specific requirements, strike out scope you don't want. The agent incorporates your edits when you save and exit.

> 📖 Source: [cli-using — Keybindings](https://antigravity.google/docs/cli-using) — uid 3_276–3_280: "Edit prompt inside your default shell editor"

### Unlock Writes — But Only for What You Approved

Once the plan is signed off, restore write access selectively:

```bash
/permissions
# Select: request-review
```

In `request-review` mode, the agent asks for approval before every write or shell command. You see exactly what it wants to do before it does it.

> **The flow:** `strict` (investigate) → approve plan → `request-review` (execute with oversight) → `always-proceed` only for trusted, well-tested final steps.

---

## 2.2 — AGENTS.md: Encoding Migration Standards <span class="duration-badge">10 min</span>

Context collapses over long sessions. AGENTS.md is how you prevent it — it's injected into every session automatically, no matter how long the conversation runs.

### Agent Self-Onboarding

The most powerful pattern is having the agent **write its own AGENTS.md** from what it found during investigation. It encodes what it learned as guardrails for its own subsequent work.

```text
Based on your codebase analysis, write an AGENTS.md that:
1. Documents current state (Spring Boot 2.6, Java 8, javax.* namespaces)
2. Defines target state (Spring Boot 3.3, Java 21, jakarta.* namespaces)
3. Sets migration rules:
   - Migrate one module at a time — never touch more than one bounded context per session
   - Every migrated class must have a passing test before moving on
   - Preserve all existing API contracts — no breaking changes to callers
   - Commit after each completed phase with a structured message
4. Flags the specific risks you identified in your analysis
5. Lists files that are off-limits in this phase

Write this to AGENTS.md in the project root.
```

> **Why self-onboarding works:** The agent is writing instructions for itself. Every migration decision it makes from this point forward is checked against constraints it authored. This is a self-reinforcing loop — better context produces better changes, which surface more patterns, which improve context.

### Modular Context with @file Imports

For large projects, keep AGENTS.md lean and import detailed specs:

```markdown
# AGENTS.md

@./docs/migration/architecture-target.md
@./docs/migration/api-contracts.md
@./docs/migration/phase-1-checklist.md
```

> 📖 Source: [cli-using](https://antigravity.google/docs/cli-using) — AGENTS.md import syntax

### Rules Files for Hard Constraints

For non-negotiable requirements, use `.agents/rules.md` — these are injected as system prompt directives, not just context:

```markdown
# .agents/rules.md

- NEVER delete migration files (MIGRATION.md, phase-*.md)
- NEVER modify files outside the current migration module's directory
- ALWAYS run the test suite before declaring a phase complete
- ALWAYS commit with message format: "migrate(phase-N): <description>"
```

> 📖 Source: [cli-using](https://antigravity.google/docs/cli-using) — `.agents/rules.md` system prompt directives

---

## 2.3 — Subagents: Parallel Analysis Teams <span class="duration-badge">15 min</span>

Large migrations have multiple independent concerns — security, performance, API contracts, test coverage. Running them sequentially is slow and wastes the agent's context window. Use subagents to parallelize.

### Spawn a Parallel Analysis Team

```text
I need three parallel analyses before we start migrating. Please spawn:

1. A security-analysis subagent: scan every auth and session-handling class
   for OWASP Top 10 issues. Read-only. Report back with file paths and line numbers.

2. A dependency-map subagent: trace all inter-module dependencies and identify
   which modules can be migrated independently vs which have shared state.
   Produce a migration-order recommendation.

3. A test-coverage subagent: list every public method in the auth module with
   no test coverage. Produce a test-gap report.

Run all three concurrently. I'll review the reports before we start Phase 1.
```

### Monitor from the Subagents Panel

```bash
/agents
```

The panel shows all running subagents with status: `running`, `done`, `killed`. Watch all three finish simultaneously.

```text
alt+j
```

Teleports you to the next subagent waiting for your approval — useful if one hits a permission boundary and needs a go-ahead.

```text
ctrl+k
```

Fast-approve a subagent permission request from the main conversation without leaving your current context.

> 📖 Source: [cli-features — Subagents](https://antigravity.google/docs/cli-features) — uid 5_278–5_316

### Custom Subagent Definition

Create a read-only security scanner in `.agents/agents/security-scanner.md`:

```markdown
---
model: gemini-3.7-flash
tools:
  allow:
    - read_file
    - list_directory
    - grep_search
# No write_file, no run_command — this agent is read-only
---

You are a security analyst specializing in migration risk assessment.
Your job is to identify vulnerabilities in legacy code that could be
amplified during a modernization effort.

Focus on:
- Authentication and session management anti-patterns
- SQL injection vectors in legacy data access layers
- Hardcoded credentials or secrets in configuration files
- Deprecated cryptographic primitives (MD5, SHA-1, DES)
- Unvalidated redirects or file path traversal risks

Always report: file path, line number, severity (HIGH/MEDIUM/LOW), and remediation.
Never modify any file. Never execute any command.
```

> 📖 Source: [Subagents](https://antigravity.google/docs/subagents) · [cli-features](https://antigravity.google/docs/cli-features) — uid 5_274: fine-grained permissions JSON format

---

## 2.4 — Skills: Reusable Migration Expertise <span class="duration-badge">10 min</span>

Skills are instruction sets the agent reads and activates when relevant. For repeatable migrations (Java 8→21, .NET Framework→.NET 8, Express→Fastify), encode the pattern once as a skill.

### Browse Available Skills

```bash
/skills
```

### Create a Migration Skill

```bash
mkdir -p ~/.gemini/antigravity-cli/skills/java-migration
```

Create `~/.gemini/antigravity-cli/skills/java-migration/SKILL.md`:

```markdown
---
name: java-migration
description: >
  Guides Java 8 to Java 21 + Spring Boot 3.x migration. Activates when
  the user mentions javax.*, Spring Boot 2.x, or Java upgrade. Provides
  phase-by-phase migration steps, jakarta.* namespace rules, and
  mandatory test-gate requirements between phases.
---

## Java 8 → 21 Migration Protocol

### Phase 0 — Inventory (always first)
- Run: grep -r "javax\." src/ | grep -v test | sort | uniq -c | sort -rn
- Identify all Spring Boot starter versions in pom.xml
- Check for removed APIs: sun.misc.*, com.sun.*, internal packages

### Phase 1 — Dependency Upgrade
- Update Spring Boot parent to 3.3.x
- Replace javax.* with jakarta.* (use: sed -i 's/javax\./jakarta\./g')
- Update Hibernate to 6.x — @Entity annotation semantics changed
- Gate: mvn clean verify must pass before Phase 2

### Phase 2 — Configuration Migration

**Goal:** Migrate XML/property-file config to type-safe structured config.

**Steps:**
1. Identify all config sources (XML, .properties, environment variables)
2. Map to typed configuration classes
3. Replace with framework-native config (Spring Boot `@ConfigurationProperties`, .NET `IOptions<T>`)
4. Add validation annotations
5. Remove legacy config loading code

**Validation:** All tests pass with new config loading path.
```

> 📖 Source: [Skills](https://antigravity.google/docs/skills) · [cli-features — /skills](https://antigravity.google/docs/cli-features) — uid 5_251–5_253

---

## 2.5 — Hooks: Automated Guardrails <span class="duration-badge">10 min</span>

For enterprise migrations, you want automated gates — not just manual review. Hooks fire on CLI lifecycle events and can block, warn, or log tool calls before and after execution.

### Pre-Tool Hook: Block Writes Outside Migration Scope

Create `.agents/hooks/scope-guard.sh`:

```bash
#!/usr/bin/env bash
# AGY CLI hook event: PreToolUse
# Blocks file modifications outside migration module

input=$(cat)
filepath=$(echo "$input" | jq -r '.toolCall.args.TargetFile // ""')
migration_module="${MIGRATION_MODULE:-src/auth}"

if [ -n "$filepath" ] && [[ "$filepath" != *"$migration_module"* ]]; then
  echo "{\"decision\":\"deny\",\"reason\":\"File write to $filepath is outside active migration module ($migration_module)\"}"
else
  echo '{"decision":"allow"}'
fi
```

Make it executable:

```bash
chmod +x .agents/hooks/scope-guard.sh
```

Register in `.agents/hooks.json`:

```json
{
  "scope-guard": {
    "PreToolUse": [
      {
        "matcher": "write_to_file|replace_file_content|multi_replace_file_content",
        "hooks": [
          {
            "type": "command",
            "command": "./.agents/hooks/scope-guard.sh",
            "timeout": 5
          }
        ]
      }
    ]
  }
}
```

### Post-Tool Hook: Diagnostic Telemetry After File Writes

Create `.agents/hooks/test-logger.sh`:

```bash
#!/usr/bin/env bash
# AGY CLI hook event: PostToolUse
# Logs diagnostic telemetry if a tool execution encounters an error

input=$(cat)
tool_name=$(echo "$input" | jq -r '.toolCall.name // ""')
tool_error=$(echo "$input" | jq -r '.error // ""')

if [ -n "$tool_error" ]; then
  mkdir -p .agents/logs
  echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] Error in $tool_name: $tool_error" >> .agents/logs/migration_errors.log
fi

# PostToolUse output contract is strictly an empty JSON object
echo '{}'
```

> 📖 Source: [Hooks docs](https://antigravity.google/docs/hooks)

---

## 2.6 — /rewind and /fork: Your Safety Net <span class="duration-badge">5 min</span>

### /rewind — Roll Back the Conversation

If the agent goes off-track, you don't need to start over. `/rewind` rolls back conversation history:

```bash
/rewind
```

This opens a history picker. Select the turn to revert to. The agent's understanding of the codebase resets to that point — useful if it's accumulated incorrect assumptions during a long session.

> 📖 Source: [cli-features](https://antigravity.google/docs/cli-features) — uid 5_220–5_226: "`/rewind` (alias `/undo`) — roll back conversation history"

### /fork — Explore Without Risk

Before attempting a risky migration step, fork the conversation:

```bash
/fork
```

This creates a parallel workspace. You can try the risky approach in the fork. If it works, great. If it doesn't, close the fork and continue from the main conversation — which never changed.

> 📖 Source: [cli-using](https://antigravity.google/docs/cli-using) — uid 3_219–3_224: "`/fork` to spin up a separate workspace"

### /resume — Pick Up Long Migrations

Large migrations span multiple days. When you return:

```bash
/resume
```

This opens a session picker showing your previous migration sessions with timestamps and conversation names. Select the right one to continue exactly where you left off.

> 📖 Source: [cli-features](https://antigravity.google/docs/cli-features) — uid 5_213–5_219

Rename sessions to keep migrations organized:

```bash
/rename "Java 21 Migration — Phase 2: Jakarta namespace"
```

---

## 2.7 — Print Mode: Non-Interactive Migration Pipeline <span class="duration-badge">5 min</span>

For CI/CD gates or overnight migration runs, use print mode to pipe migration tasks without interaction:

```bash
# Dry-run: analyze and report issues — no writes
agy -p "Review the migration changes in the last commit. \
  Check for: javax.* references that weren't updated, \
  missing jakarta.* imports, and test files that weren't \
  updated to match renamed packages. \
  Output a structured report with file paths and line numbers."
```

```bash
# Chain: analyze → generate migration report → save
agy -p "Scan src/auth/ for javax.persistence.* usage" | \
  agy -p "Convert this javax.persistence usage report into \
  a step-by-step migration plan with exact sed commands" > migration-plan.md
```

> 📖 Source: [cli-getting-started](https://antigravity.google/docs/cli-getting-started) — `agy --help`: "-p: Short alias for --print"

---

## Hands-On Exercise

<div class="exercise-card" markdown>

### :material-file-document: Exercise 8: Legacy Modernization

**Files:** [`ex08_dotnet_modernization.md`](exercises/ex08_dotnet_modernization.md) · [`ex09_java_upgrade.md`](exercises/ex09_java_upgrade.md)  
**Duration:** 45 min  
**Objective:** Walk through a full migration using the AGY primitives from this module.

**Choose your track:**

#### Track A: Plan-First (Strict → Investigate → Execute)

1. Set `/permissions` to `strict` — lock all writes
2. Give the agent a full investigation mandate (Section 2.1)
3. Use `ctrl+g` to open the plan in your editor and add team constraints
4. Write an AGENTS.md encoding the migration rules (or have the agent write it)
5. Add a `.agents/rules.md` with hard non-negotiables
6. Switch to `request-review` — begin Phase 1 with oversight
7. Use `/rewind` if the agent drifts outside scope
8. Rename the session: `/rename "Migration — Phase 1 complete"`

#### Track B: Subagent-First (Parallel Analysis → Context → Execute)

1. Spawn three parallel subagents: security scan, dependency map, test coverage
2. Monitor via `/agents` — use `alt+j` and `ctrl+k` for approvals
3. Aggregate their reports into an AGENTS.md (have the agent synthesize)
4. Install the `java-migration` skill (Section 2.4)
5. Use `/fork` before the riskiest step — try it there first
6. Use print mode to generate a post-phase report

</div>

---

## Summary: AGY Primitives for Legacy Modernization

| Primitive | What It Does | When to Use |
| :-- | :-- | :-- |
| `/permissions strict` | Hard read-only gate — no writes or commands | Investigation phase |
| `/permissions request-review` | Agent asks before every write | Controlled execution |
| `ctrl+g` | Open plan in `$EDITOR` for collaborative editing | Plan refinement |
| **AGENTS.md** | Persistent migration standards across sessions | Always — encode constraints |
| `.agents/rules.md` | Hard system-prompt directives | Non-negotiable guardrails |
| **Subagents** | Parallel analysis teams | Multi-concern investigations |
| `/agents` + `alt+j` + `ctrl+k` | Monitor and approve subagent work | During parallel runs |
| **Hooks** (PreToolUse) | Block writes outside migration scope | Automated guardrails |
| **Hooks** (PostToolUse) | Auto-run tests after every change | Test gate automation |
| `/rewind` | Roll back conversation if agent drifts | Mid-session course correction |
| `/fork` | Try risky steps in an isolated branch | Before high-risk changes |
| `/resume` | Pick up multi-day migrations | Returning to a session |
| `/rename` | Label sessions by phase | Session management |
| `agy -p` | Non-interactive migration pipeline | CI gates, overnight runs |
| **Skills** | Reusable migration playbooks | Repeatable migration patterns |

---

## Next Step

→ Continue to **[Module 3: Building AGY Agents with the SDK](agy-sdk.md)**

→ **[Cheatsheet](cheatsheet.md)** — all commands in one place
