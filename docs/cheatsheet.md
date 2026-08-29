# agy-cli Cheatsheet

> Quick reference for everything covered in this workshop.
> All commands verified against [antigravity.google/docs](https://antigravity.google/docs/cli-overview).

---

## Installation & Version

```bash
curl -fsSL https://antigravity.google/cli/install.sh | bash
agy --help         # Show all flags and subcommands
agy changelog      # Show release notes
agy update         # Self-update
agy install        # Configure PATH and shell aliases
```

---

## Launch Modes

| Mode | Command | When to use |
| :-- | :-- | :-- |
| **Interactive** | `agy` | Default — full conversational session |
| **Seeded interactive** | `agy -i "<prompt>"` | Start with direction, continue conversationally |
| **Print (headless)** | `agy -p "<prompt>"` | Single shot, pipe to stdout |
| **Continue last** | `agy -c` | Resume most recent session |
| **Resume by ID** | `agy --conversation <id>` | Resume a specific past session |
| **Resume in-session** | `/resume` or `/switch` | Switch conversations without leaving agy |

---

## Key Flags

> Source: [`agy --help`](https://antigravity.google/docs/cli-getting-started) · [cli-using](https://antigravity.google/docs/cli-using)

| Flag | Short | Description |
| :-- | :-- | :-- |
| `--print "<prompt>"` | `-p` | Non-interactive single prompt |
| `--prompt-interactive "<prompt>"` | `-i` | Seeded interactive session |
| `--continue` | `-c` | Resume most recent conversation |
| `--conversation <id>` | — | Resume by conversation ID |
| `--add-dir <path>` | — | Add directory to workspace (repeatable) |
| `--sandbox` | — | Enable terminal sandbox restrictions |
| `--dangerously-skip-permissions` | — | Auto-approve all tool requests (CI only) |
| `--print-timeout <duration>` | — | Timeout for print mode (default: 5m) |
| `--log-file <path>` | — | Override log output path |

> **Note:** Model selection and strict mode are set via `/model` and `/permissions` slash commands, not CLI flags. See [Features docs](https://antigravity.google/docs/cli-features).

---

## Slash Commands (Interactive Mode)

> Source: [CLI Features — Core Slash Commands](https://antigravity.google/docs/cli-features) · [Using Antigravity CLI](https://antigravity.google/docs/cli-using)

| Command | Category | Purpose |
| :-- | :-- | :-- |
| `/resume` (`/switch`, `/conversation`) | Conversation | Open conversation picker to resume or switch sessions |
| `/rewind` (`/undo`) | Conversation | Roll back conversation history to a previous checkpoint |
| `/fork` (`/branch`) | Conversation | Branch current conversation into an isolated workspace |
| `/rename <name>` | Conversation | Rename the active conversation thread |
| `/clear` (`/new`) | Conversation | Clear active context and start a new conversation |
| `/permissions` | Config | Set autonomy level: `request-review`, `proceed-in-sandbox`, `always-proceed`, `strict` |
| `/model` | Config | Select default reasoning model (persists across sessions) |
| `/config` (`/settings`) | Config | Open full-screen settings overlay |
| `/keybindings` | Config | Open the interactive keyboard shortcut editor |
| `/statusline` | Config | Customize real-time CLI status bar indicators |
| `/fast` | Config | Toggle low-latency fast reasoning mode |
| `/planning` | Config | Toggle multi-turn plan generation mode |
| `/teamwork-preview` (`/teamwork`) | Reasoning | Launch collaborative multi-agent teams |
| `/goal` | Reasoning | Run autonomous goal-directed loop |
| `/grill-me` | Reasoning | Interactive requirements interview |
| `/diff` | Utility | Open interactive git diff viewer |
| `/btw <query>` | Utility | Send background note to steer active agent |
| `/schedule` | Automation | Schedule background cron or timer tasks |
| `/browser` | Tools | Launch Chrome DevTools browser automation |
| `/voice` (`/record`) | Input | Toggle voice prompt dictation |
| `/context` | Monitoring | View active token usage and context files |
| `/credits` (`/quota`) | Account | View G1 credit balance and quota status |
| `/tasks` | Monitoring | Monitor, view logs for, or terminate background tasks |
| `/skills` | Monitoring | Browse local and global agent skills |
| `/mcp` | Monitoring | Configure and manage MCP servers |
| `/agents` | Monitoring | View, manage, and approve subagent actions |
| `/hooks` | Monitoring | Browse active script and JSON hooks |
| `/open <path>` | Utility | Open a file in your preferred external editor |
| `/copy` | Utility | Copy last agent response to system clipboard |
| `/usage` | Utility | Open the inline interactive help manual |
| `/help` | Utility | Show all available slash commands and shortcuts |
| `/logout` | Account | Log out and clear cached credentials |
| `/exit` (`/quit`) | Account | Exit the CLI session |

---

## Quick Tips

> Source: [Using Antigravity CLI — Quick Tips & Keybindings](https://antigravity.google/docs/cli-using)

| Shortcut / Tip | Action |
| :-- | :-- |
| `@` | File path autocomplete (type `@` to trigger path suggestions) |
| `!` | Run terminal commands directly from the prompt |
| `esc esc` | Clear prompt box (when no streaming is active) |
| `?` | Get help and list all slash commands |
| `alt+enter` / `shift+enter` / `ctrl+j` | Insert newline without submitting (`prompt.newline`) |
| `ctrl+g` | Edit prompt inside your default shell editor (`$EDITOR`) |
| `ctrl+l` | Clear TUI screen |
| `ctrl+d` | Exit the CLI session (or forward delete character) |
| `ctrl+z` | Suspend CLI to terminal background |
| `alt+j` | Teleport to next pending subagent approval (`prompt.teleport_agent`) |
| `ctrl+k` | Fast-approve pending subagent permission from main conversation |
| `ctrl+o` | Toggle reasoning trajectory and thought expansion (`prompt.toggle_trajectory`) |
| `ctrl+r` | Open Artifact Review Panel (`prompt.open_review`) |
| `ctrl+v` | Paste clipboard block or graphic media file into prompt |
| `f5` | Toggle voice dictation (`voice.start_dictation`) |

---

## Plugin Commands

```bash
# List all active plugins (JSON)
agy plugin list

# Import from Gemini CLI
agy plugin import gemini

# Import from Claude Code
agy plugin import claude

# Force re-import (after plugin updates)
agy plugin import gemini --force

# Install a plugin
agy plugin install <name>
agy plugin install <name>@<version>

# Enable / disable
agy plugin enable <name>
agy plugin disable <name>

# Validate a plugin directory
agy plugin validate ./my-plugin

# Generate marketplace link
agy plugin link <marketplace> <target>
```

---

## Sidecars

> Background processes AGY manages for you — launches, restarts, and runs independently of any conversation. Source: [antigravity.google/docs/sidecars](https://antigravity.google/docs/sidecars)

```bash
# Config locations:
~/.gemini/config/sidecars/<name>/sidecar.json                         # global
~/.gemini/config/plugins/<plugin>/sidecars/<name>/sidecar.json        # plugin-scoped

# Enable (disabled by default) — edit ~/.gemini/config/config.json:
#   { "sidecars": { "<name>": { "enabled": true } } }

# Check logs:
ls ~/.gemini/antigravity-cli/sidecar_data/<name>/logs/

# agentapi (auto-available inside sidecars):
agentapi new-conversation "<prompt>"
agentapi send-message <conversation_id> "<prompt>"
```

Minimal `sidecar.json` — background script:

```json
{ "command": "python3", "args": ["worker.py"], "restart_policy": "on-failure" }
```

Minimal `sidecar.json` — scheduled recurring task:

```json
{
  "builtin": "schedule",
  "args": ["0 9 * * 1-5", "agentapi", "new-conversation", "Summarise open PRs."]
}
```

---

## Workspace & Context

```bash
# Project config directory:
.agents/                    # settings.json, mcp_config.json, hooks.json, rules.md, skills/, plugins/

# Global config directory:
~/.gemini/config/           # settings.json, mcp_config.json, hooks.json, rules.md, skills/, plugins/

# User settings:
~/.gemini/antigravity-cli/settings.json

# Context file (hierarchical: cwd → parent → home):
AGENTS.md

# agy also reads:
.gemini/                    # Gemini CLI config (compatible)
```

### AGENTS.md Pattern

```markdown
# Project Context

Brief description of what this project is.

## Conventions
- Language: TypeScript, Node 20
- Testing: Jest + Supertest
- DO NOT run database migrations without explicit approval
```

---

## Useful Patterns

```bash
# Review staged changes before commit
git diff --cached | agy -p "Review for bugs, security issues, missing tests."

# Generate docs for a file
cat src/api.ts | agy -p "Generate OpenAPI documentation for all exported functions."

# Analyze logs
tail -n 500 app.log | agy -p "Group these errors by root cause. Output as JSON."

# Multi-dir cross-repo analysis
agy --add-dir ../api --add-dir ../frontend \
    -p "Map data flow from frontend form submission to database write."

# Full headless CI audit (safe)
agy --sandbox --dangerously-skip-permissions \
    -p "Audit for hardcoded secrets and insecure patterns." \
    --print-timeout 5m > audit.md

# Schedule a recurring task (in interactive mode)
# > Schedule a daily code quality report at 9am weekdays.
```

---

## Multi-Agent Patterns

```text
# Spawn parallel subagents (in interactive mode)
> Spawn a security auditor and a performance auditor in parallel (branch mode).

# Adversarial review
> Spawn an adversarial reviewer subagent — its job is to find reasons to NOT merge this PR.

# Steer mid-task
/btw Focus only on the authentication module, skip the frontend.

# Background task
> In the background, audit all dependencies for known CVEs. Notify me when done.
```

---

## Print Mode Pipeline Examples

```bash
# Step 1: plan
agy -p "Create a refactoring plan for moving from callbacks to async/await. JSON output." \
  > plan.json

# Step 2: execute
cat plan.json | agy -p "Execute step 1 of this plan."

# Batch: process multiple files
for f in src/*.ts; do
  agy --add-dir "$(dirname $f)" \
      -p "Add JSDoc to all exported functions in $(basename $f)."
done
```

---

## Official Docs

| Topic | Link |
| :-- | :-- |
| CLI Overview | [antigravity.google/docs/cli-overview](https://antigravity.google/docs/cli-overview) |
| Getting Started | [antigravity.google/docs/cli-getting-started](https://antigravity.google/docs/cli-getting-started) |
| Using Antigravity CLI (settings, tips, keybindings) | [antigravity.google/docs/cli-using](https://antigravity.google/docs/cli-using) |
| Features (plugins, sandbox, slash commands, subagents) | [antigravity.google/docs/cli-features](https://antigravity.google/docs/cli-features) |
| Migration from Gemini CLI | [antigravity.google/docs/gcli-migration](https://antigravity.google/docs/gcli-migration) |
| Permissions | [antigravity.google/docs/permissions](https://antigravity.google/docs/permissions) |
| Strict Mode | [antigravity.google/docs/strict-mode](https://antigravity.google/docs/strict-mode) |
| Plugins | [antigravity.google/docs/plugins](https://antigravity.google/docs/plugins) |
| MCP | [antigravity.google/docs/mcp](https://antigravity.google/docs/mcp) |
| Skills | [antigravity.google/docs/skills](https://antigravity.google/docs/skills) |
| Rules | [antigravity.google/docs/rules-workflows](https://antigravity.google/docs/rules-workflows) |
| Hooks | [antigravity.google/docs/hooks](https://antigravity.google/docs/hooks) |
| Sidecars | [antigravity.google/docs/sidecars](https://antigravity.google/docs/sidecars) |
| Subagents | [antigravity.google/docs/subagents](https://antigravity.google/docs/subagents) |
| Enterprise | [antigravity.google/docs/enterprise](https://antigravity.google/docs/enterprise) |
