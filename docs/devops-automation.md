# Reference: DevOps & Automation Patterns

> **agy without a human in the loop.** Deep reference for non-interactive `--print` pipelines, CI/CD integration, multi-repository workspaces, and sandboxed execution. Essential commands are linked from the [Cheatsheet](cheatsheet.md).

---

## DevOps 1 — Print Mode: The Non-Interactive Core <span class="duration-badge">5 min</span>

`--print` (short: `-p`) is agy's headless mode. It runs a single prompt, prints the response, and exits. No interactive session, no prompts.

```bash
# Basic usage
agy --print "Summarize the top-level README of this project."

# Set a timeout (default: 5 minutes)
agy --print "Generate a full test suite for auth.js" --print-timeout 10m

# Short form
agy -p "What does this project do?"
```

Output goes to stdout — pipe it, redirect it, store it.

```bash
# Pipe into a file
agy -p "Generate API documentation for all endpoints" > docs/api.md

# Pipe into another command
agy -p "List all TODO comments in this codebase as JSON" | jq '.[] | .file'
```

---

## DevOps 2 — Shell Pipelines <span class="duration-badge">10 min</span>

> **Pattern: agy as a Unix command** — compose it with standard shell tools.

### Pattern: Pipe Code into agy

```bash
# Review a specific file
cat src/auth.js | agy -p "Review this file for security vulnerabilities."

# Review staged changes before commit
git diff --cached | agy -p "Review these changes. Flag bugs, security issues, or missing tests."

# Analyze a log file
tail -n 200 app.log | agy -p "Identify patterns in these errors. Group by root cause."
```

### Pattern: Chain agy Calls

```bash
# Step 1: Generate a plan
agy -p "Create a migration plan for moving this project from CommonJS to ESM. Output as JSON with steps array." > migration-plan.json

# Step 2: Execute step by step
cat migration-plan.json | agy -p "Execute step 1 of this migration plan."
```

### Pattern: Batch Processing

```bash
# Process multiple files
for f in src/**/*.js; do
  out="/tmp/review_$(basename $f .js).md"
  agy -p "Review $(basename $f) for issues" \
      --add-dir "$(dirname "$f")" \
      --print-timeout 2m > "$out"
  echo "=== $f ==="
  cat "$out"
done
```

---

## DevOps 3 — Multi-Directory Workspaces with --add-dir <span class="duration-badge">10 min</span>

> **Pattern: Cross-Repo Context** — give agy visibility into multiple codebases simultaneously.

By default, agy indexes the git repo containing your current directory. `--add-dir` extends that to additional directories.

```bash
# Give agy access to both your app and its shared library
agy --add-dir ../shared-lib "How does the app use shared-lib? Identify any API mismatches."

# Add multiple directories
agy --add-dir ../api --add-dir ../frontend "Generate an integration test that covers the API-to-frontend data flow."

# Use in print mode
agy -p "Compare the error handling patterns in app/ vs api/" --add-dir ../api
```

### Real-World Use Case: Monorepo Review

```bash
# From the root of a monorepo, review cross-package dependencies
agy --add-dir packages/core --add-dir packages/api --add-dir packages/ui \
    -p "Map the dependency graph between these three packages and flag any circular dependencies."
```

!!! tip "Repeatable flag"
    `--add-dir` is repeatable — add as many directories as you need. agy indexes all of them alongside the primary git repo.

---

## DevOps 4 — CI/CD Integration <span class="duration-badge">10 min</span>

> **Pattern: agy in the Pipeline** — automated code review and analysis on every PR.

### GitHub Actions Example

```yaml
# .github/workflows/agy-review.yml
name: agy Code Review
on: [pull_request]

jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Install agy-cli
        run: |
          curl -fsSL https://antigravity.google/cli/install.sh | bash

      - name: Review PR changes
        run: |
          git diff origin/main...HEAD | \
          agy --dangerously-skip-permissions \
              --print "Review these changes for: (1) correctness, (2) security, (3) missing tests. Output as markdown." \
              --print-timeout 5m > review.md

      - name: Post review as comment
        uses: actions/github-script@v7
        with:
          script: |
            const fs = require('fs');
            const review = fs.readFileSync('review.md', 'utf8');
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: review
            });
```

!!! warning "--dangerously-skip-permissions in CI"
    Always use `--dangerously-skip-permissions` in CI — there's no human to click "approve". Pair it with sandbox mode to restrict what agy can access.

### Pre-Commit Hook

```bash
#!/bin/bash
# .git/hooks/pre-commit
echo "🤖 Running agy pre-commit review..."
git diff --cached | agy --dangerously-skip-permissions \
    -p "Flag any obvious bugs or security issues in these staged changes. If none, output 'LGTM'." \
    --print-timeout 60s

# Optionally block commit if issues found
# (parse output for keywords)
```

---

## DevOps 5 — Sandbox Mode <span class="duration-badge">5 min</span>

> **Pattern: Restricted Execution** — run agy with OS-level terminal isolation.

### Enabling the Sandbox

The sandbox is configured via `settings.json` (either project `.agents/settings.json` or user `~/.gemini/antigravity-cli/settings.json`):

```json
{
  "enableTerminalSandbox": true
}
```

When enabled, agy uses **native OS isolation** to restrict terminal command execution:

| OS | Isolation Technology |
| :-- | :-- |
| **Linux** | nsjail |
| **macOS** | sandbox-exec |
| **Windows** | AppContainer |

### Per-Command Bypass

With the sandbox enabled, agy will **prompt for approval** when a command needs to break out of the sandbox. You'll see a per-command bypass prompt — allowing selective execution without disabling the entire sandbox.

### Use Cases

- Running agy on untrusted code
- Auditing for sensitive content without side effects
- Governance-sensitive environments where any execution requires approval

### Combining with Permissions

For maximum control, pair sandbox mode with the permissions model:

```json
{
  "enableTerminalSandbox": true,
  "permissions": {
    "allow": ["read_file", "command(git)"],
    "deny": ["command(rm)", "unsandboxed"]
  }
}
```

> 📖 Full details: [Permissions docs](https://www.antigravity.google/docs/permissions)

---

## DevOps 6 — Hooks & Rules <span class="duration-badge">10 min</span>

> **Pattern: Guardrails & Automation** — enforce standards and trigger actions at key lifecycle points.

### Antigravity Lifecycle Hooks

Hooks execute custom scripts or binaries at 5 lifecycle stages in Antigravity's execution loop. Configured in `.agents/hooks.json` (workspace) or `~/.gemini/config/hooks.json` (global).

#### Lifecycle Events & Contracts

| Event | Matcher Target | stdin Input Summary | stdout Response Contract |
| :-- | :-- | :-- | :-- |
| **`PreToolUse`** | Tool name regex (e.g. `run_command`, `write_to_file` or `replace_file_content`) | `.toolCall.name`, `.toolCall.args`, `.stepIdx`, `.workspacePaths` | `{"decision": "allow"}` or `{"decision": "deny", "reason": "..."}` |
| **`PostToolUse`** | Tool name regex | `.toolCall.name`, `.toolCall.args`, `.stepIdx`, `.error` | `{}` (Telemetry and observer contract) |
| **`PreInvocation`** | N/A (fires before model turn) | `.invocationNum`, `.initialNumSteps`, `.workspacePaths`, `.modelName` | `{"injectSteps": [{"ephemeralMessage": "..."}]}` |
| **`PostInvocation`** | N/A (fires after model turn) | `.invocationNum`, `.initialNumSteps`, `.workspacePaths` | `{"injectSteps": [...], "terminationBehavior": "force_continue"}` |
| **`Stop`** | N/A (fires upon completion) | `.executionNum`, `.terminationReason`, `.error`, `.fullyIdle` | `{"decision": "continue", "reason": "..."}` or `{"decision": "allow"}` |

#### Configuration File Format (`.agents/hooks.json`)

```json
{
  "security-gate": {
    "enabled": true,
    "PreToolUse": [
      {
        "matcher": "write_to_file|replace_file_content|multi_replace_file_content|run_command",
        "hooks": [
          {
            "type": "command",
            "command": "./.agents/hooks/secret-scanner.sh",
            "timeout": 5
          }
        ]
      }
    ]
  },
  "session-context-injector": {
    "enabled": true,
    "PreInvocation": [
      {
        "type": "command",
        "command": "./.agents/hooks/session-context.sh",
        "timeout": 5
      }
    ]
  },
  "tool-telemetry": {
    "enabled": true,
    "PostToolUse": [
      {
        "matcher": "write_to_file|replace_file_content|run_command",
        "hooks": [
          {
            "type": "command",
            "command": "./.agents/hooks/test-nudge.sh",
            "timeout": 5
          }
        ]
      }
    ]
  }
}
```

#### Sample Scripts (in `samples/hooks/`)

| Script | Event | Contract Output | Purpose |
| :-- | :-- | :-- | :-- |
| **`secret-scanner.sh`** | `PreToolUse` | `{"decision": "deny"}` or `{"decision": "allow"}` | Hard blocks credential leaks in file writes and shell commands |
| **`git-context-injector.sh`** | `PreToolUse` | `{"decision": "allow", "reason": "..."}` | Verifies recent git history before file modifications |
| **`session-context.sh`** | `PreInvocation` | `{"injectSteps": [{"ephemeralMessage": "..."}]}` | Injects branch, dirty files, and toolchain version as ephemeral context |
| **`test-nudge.sh`** | `PostToolUse` | `{}` | Logs failed tool executions to `.agents/logs/tool_audit.log` |

> 📖 Full reference: [Hooks docs](https://antigravity.google/docs/hooks)
### Rules

Rules are markdown files injected into agy's system prompt as `RULE` blocks — hard constraints that agy must follow.

| Scope | Location |
| :-- | :-- |
| **Project** | `.agents/rules.md` or `.agents/rules/*.md` |
| **Global** | `~/.gemini/config/rules.md` or `~/.gemini/config/rules/*.md` |

Example `.agents/rules.md`:

```markdown
- Never delete migration files
- Always use TypeScript strict mode
- Run `npm test` after any code change
- Do not modify files in the vendor/ directory
```

> 📖 Full details: [Rules & Workflows docs](https://www.antigravity.google/docs/rules-workflows)

---

## Exercises

<div class="exercise-card" markdown>

### :material-file-document: Exercise 3: --print Pipeline

**File:** [`ex03_print_mode_pipeline.md`](exercises/ex03_print_mode_pipeline.md)
**Duration:** 20 min
**Objective:** Build a multi-step shell pipeline using agy --print. Review staged changes, generate docs, and wire up a GitHub Actions workflow.

</div>

---

## Next Module

→ **[Module 4: Multi-Agent & Advanced](multi-agent-advanced.md)** — subagents, /btw mid-task steering, scheduling.
