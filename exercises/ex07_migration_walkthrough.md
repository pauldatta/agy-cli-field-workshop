# Exercise 7 — Migration Walkthrough

> **Module:** Appendix — Migration Guide
> **Time:** 20 min
> **Format:** Individual or pair

---

## Objective

Walk through a real Gemini CLI project directory and migrate it to AGY CLI. You'll update config file locations, MCP server definitions, hook event names, and AGENTS.md content — then validate using the `migration-validator` subagent.

---

## Background

When teams migrate from Gemini CLI to AGY CLI, there are four common breakage points:

| What breaks | Why |
| :-- | :-- |
| Hook events `SessionStart`, `BeforeTool`, `AfterTool` | Renamed to `PreInvocation`, `PreToolUse`, `PostToolUse` |
| MCP `url` key in `settings.json` | AGY uses `serverUrl` in a separate `mcp_config.json` |
| `.gemini/` project config dir | AGY uses `.agents/` |
| `gemini` binary in scripts | Must be updated to `agy` |

---

## Setup

You need a sample Gemini CLI project to migrate. Create the starter:

```bash
mkdir ~/gemini-migration-lab && cd ~/gemini-migration-lab

# Create a legacy Gemini CLI settings.json
mkdir -p .gemini/hooks
cat > .gemini/settings.json << 'EOF'
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "github-mcp-server"],
      "env": { "GITHUB_PERSONAL_ACCESS_TOKEN": "$GITHUB_TOKEN" }
    }
  },
  "hooks": {
    "SessionStart": [
      {
        "hooks": [{
          "name": "session-context",
          "type": "command",
          "command": "$GEMINI_PROJECT_DIR/.gemini/hooks/session-context.sh",
          "timeout": 3000
        }]
      }
    ],
    "BeforeTool": [
      {
        "matcher": "write_file|replace_in_file",
        "hooks": [{
          "name": "secret-scanner",
          "type": "command",
          "command": "$GEMINI_PROJECT_DIR/.gemini/hooks/secret-scanner.sh",
          "timeout": 2000
        }]
      }
    ]
  }
}
EOF

# Create a legacy GEMINI.md
cat > .gemini/GEMINI.md << 'EOF'
# Project Context

This is a Node.js API service. Always run `npm test` after changes.
Use gemini for code reviews before merging PRs.
EOF

# Create a CI script that calls the old binary
mkdir -p .github/workflows
cat > scripts/review.sh << 'EOF'
#!/usr/bin/env bash
gemini -p "Review the diff: $(git diff HEAD~1)" > review.md
EOF
```

---

## Part 1 — Manual Migration (10 min)

Migrate the project yourself:

### Step 1: Move config to AGY directories

```bash
mkdir -p .agents/hooks
# AGY reads .agents/ instead of .gemini/ for project config
cp .gemini/GEMINI.md .agents/AGENTS.md
cp .gemini/settings.json .agents/settings.json
```

### Step 2: Separate MCP config

```bash
# AGY uses mcp_config.json, not mcpServers in settings.json
cat > .agents/mcp_config.json << 'EOF'
{
  "mcpServers": {
    "github": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "github-mcp-server"],
      "env": { "GITHUB_PERSONAL_ACCESS_TOKEN": "$GITHUB_TOKEN" }
    }
  }
}
EOF
```

### Step 3: Rewrite hook event names in settings.json

```json
{
  "hooks": {
    "PreInvocation": [
      {
        "hooks": [{
          "name": "session-context",
          "type": "command",
          "command": "$AGY_PROJECT_DIR/.agents/hooks/session-context.sh",
          "timeout": 3000
        }]
      }
    ],
    "PreToolUse": [
      {
        "matcher": "write_file|edit",
        "hooks": [{
          "name": "secret-scanner",
          "type": "command",
          "command": "$AGY_PROJECT_DIR/.agents/hooks/secret-scanner.sh",
          "timeout": 2000
        }]
      }
    ]
  }
}
```

### Step 4: Update binary references

```bash
sed -i 's/\bgemini\b/agy/g' scripts/review.sh
```

---

## Part 2 — Validate with the Migration Validator Agent (5 min)

Start AGY CLI and launch the migration validator:

```bash
cd ~/gemini-migration-lab
agy
```

Inside the AGY REPL:

```text
Use the migration-validator agent to check this project directory for any remaining Gemini CLI configuration.
```

The `migration-validator` subagent will check:

- [ ] Hook event names (no `SessionStart`, `BeforeTool`, `AfterTool`)
- [ ] MCP format (`serverUrl` for SSE, `type` field present)
- [ ] Binary references (`agy` not `gemini` in scripts)
- [ ] Config paths (`.agents/` not `.gemini/`)

---

## Part 3 — Discussion (5 min)

**Reflection questions:**

1. What would break first in CI if you forgot to update the hook event names?
2. Why does AGY separate MCP config into `mcp_config.json` instead of bundling it in `settings.json`?
3. If you have a monorepo with 10 projects, what would your migration script look like?

---

## Bonus Challenge

Add a `PreToolUse` hook to the migrated project that blocks the agent from calling `git push` without a confirmation. Use the hook `decision: deny` pattern.

Refer to [`samples/hooks/secret-scanner.sh`](https://github.com/pauldatta/agy-cli-field-workshop/blob/main/samples/hooks/secret-scanner.sh) as a template for the decision pattern.

---

## Key Takeaways

| Gemini CLI | AGY CLI |
| :-- | :-- |
| `SessionStart` | `PreInvocation` |
| `BeforeTool` | `PreToolUse` |
| `AfterTool` | `PostToolUse` |
| `replace_in_file` tool | `edit` tool |
| `.gemini/` project dir | `.agents/` project dir |
| `GEMINI.md` | `AGENTS.md` |
| `settings.json` MCP block | `mcp_config.json` with `serverUrl` |
| `url:` for SSE | `serverUrl:` for SSE |
| `gemini` binary | `agy` binary |
