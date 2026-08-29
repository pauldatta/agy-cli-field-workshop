# Exercise 16: Lifecycle Hooks & Enterprise Safety Gates

> **Duration:** 25 min (Fast: 15 min · Average: 25 min · Thorough: 35 min) | **Module:** 1 — SDLC Productivity & Automation

---

## Objective

Master Antigravity lifecycle hooks for automated policy enforcement:
1. Implement a **`PreToolUse`** security gate that hard-blocks destructive shell commands (`rm -rf`, `DROP TABLE`, `git push --force`) using the `{"decision": "deny"}` JSON contract.
2. Implement a **`PreInvocation`** context injector that dynamically passes uncommitted git state before model turns via `injectSteps`.
3. Implement a **`PostToolUse`** telemetry hook that records tool execution failures to an audit log.
4. Configure and validate `.agents/hooks.json` in a live repository session.

---

## Background: The Antigravity Hooks Contract

Unlike legacy tools that rely on exit codes or environment variables, Antigravity CLI lifecycle hooks adhere to a strict **JSON-over-stdin** and **JSON-over-stdout** protocol:

* **stdin:** JSON payload containing system metadata (`workspacePaths`, `conversationId`, `transcriptPath`, `modelName`) and event data (`toolCall`, `stepIdx`, `error`, `invocationNum`).
* **stdout:** Structured JSON response controlling execution flow (`decision: allow`, `decision: deny`, `injectSteps`).

---

## Part 1: Create a PreToolUse Destructive Command Guard (8 min)

Create the project hooks directory:

```bash
mkdir -p .agents/hooks
```

Create `.agents/hooks/destructive-guard.sh`:

```bash
cat > .agents/hooks/destructive-guard.sh << 'EOF'
#!/usr/bin/env bash
# PreToolUse Hook: Destructive Command Safety Gate
# Matcher: run_command
# Gating: Blocks dangerous commands with decision: deny

input=$(cat)

# Extract command line from toolCall arguments
cmd=$(echo "$input" | jq -r '.toolCall.args.CommandLine // ""' 2>/dev/null)

# Check for high-risk commands
if echo "$cmd" | grep -qEi '(rm\s+-rf\s+[/~]|DROP\s+DATABASE|DROP\s+TABLE|git\s+push\s+.*--force|mkfs|dd\s+if=)'; then
    echo "{\"decision\":\"deny\",\"reason\":\"Command blocked by policy: detected high-risk destructive operation ($cmd).\"} "
else
    echo '{"decision":"allow"}'
fi
EOF
chmod +x .agents/hooks/destructive-guard.sh
```

Test the script standalone using mock JSON input:

```bash
# Test 1: Dangerous command (should deny)
echo '{"toolCall":{"name":"run_command","args":{"CommandLine":"rm -rf /"}}}' | bash .agents/hooks/destructive-guard.sh

# Test 2: Safe command (should allow)
echo '{"toolCall":{"name":"run_command","args":{"CommandLine":"npm test"}}}' | bash .agents/hooks/destructive-guard.sh
```

---

## Part 2: Create a PreInvocation Ephemeral Context Injector (7 min)

Create `.agents/hooks/git-context-injector.sh` to provide branch awareness before each prompt:

```bash
cat > .agents/hooks/git-context-injector.sh << 'EOF'
#!/usr/bin/env bash
# PreInvocation Hook: Ephemeral Git Context Injector
# Injects current branch and uncommitted file count before model invocation

input=$(cat)

# Extract workspace root
workspace=$(echo "$input" | jq -r '.workspacePaths[0] // "."' 2>/dev/null)

branch=$(git -C "$workspace" branch --show-current 2>/dev/null || echo "main")
dirty_count=$(git -C "$workspace" status --porcelain 2>/dev/null | wc -l | tr -d ' ')

context="[Active Environment] Branch: $branch | Modified Files: $dirty_count"

# Inject as an ephemeral system message
echo "{\"injectSteps\":[{\"ephemeralMessage\":\"$context\"}]}"
EOF
chmod +x .agents/hooks/git-context-injector.sh
```

Test standalone:

```bash
echo '{"workspacePaths":["."]}' | bash .agents/hooks/git-context-injector.sh
```

---

## Part 3: Configure `.agents/hooks.json` (5 min)

Create `.agents/hooks.json` mapping your custom hooks to lifecycle events:

```bash
cat > .agents/hooks.json << 'EOF'
{
  "destructive-command-guard": {
    "enabled": true,
    "PreToolUse": [
      {
        "matcher": "run_command",
        "hooks": [
          {
            "type": "command",
            "command": "./.agents/hooks/destructive-guard.sh",
            "timeout": 5
          }
        ]
      }
    ]
  },
  "git-context-injector": {
    "enabled": true,
    "PreInvocation": [
      {
        "type": "command",
        "command": "./.agents/hooks/git-context-injector.sh",
        "timeout": 5
      }
    ]
  }
}
EOF
```

---

## Part 4: Test in Live Session (5 min)

Launch agy:

```bash
agy
```

1. **Verify Context Awareness:**
   Prompt agy:

    ```text
    > What branch am I currently on and do I have modified files?
    ```

    Notice that agy knows your branch and dirty file count immediately from the `PreInvocation` hook injection without running `git status`.

2. **Trigger the Safety Gate:**
   Prompt agy:

    ```text
    > Clean up temp directories by running: rm -rf /tmp/test-project/
    ```

    Observe how the `PreToolUse` hook intercepts the proposed `run_command` and returns a hard block message with your custom reason.

---

## Pro Tips & Key Watchouts

!!! tip "Key Things to Watch For"
    1. **Strict JSON Schema:** Hooks must always return valid JSON on stdout. Printing debugging logs to stdout corrupts the payload. Route debug output to `stderr` (`>&2`) or log files.
    2. **Timeout in Seconds:** The `timeout` field in `hooks.json` accepts integer seconds (e.g. `timeout: 5`), not milliseconds.
    3. **PreToolUse Decision Field:** For `PreToolUse`, `decision` is mandatory (`allow`, `deny`, `ask`, `force_ask`). Returning `{}` causes a schema validation failure.
    4. **Performance Budgets:** `PreToolUse` and `PreInvocation` hooks run in the critical path of every tool call and turn. Keep execution times below **100ms** to preserve CLI responsiveness.

---

## Completion Criteria

- [ ] Created executable `destructive-guard.sh` and verified both deny and allow JSON outputs
- [ ] Created executable `git-context-injector.sh` returning valid `injectSteps`
- [ ] Created valid `.agents/hooks.json` registering both hooks
- [ ] Verified live interception and ephemeral context injection in an interactive `agy` session
