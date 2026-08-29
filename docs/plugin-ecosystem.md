# Reference: Plugin Ecosystem

> **Deep reference for agy-cli's plugin system.** The essential commands are covered in [Module 1 — Section 1.7](sdlc-productivity.md#17-extend-with-plugins-15-min). This page has the full lifecycle detail for teams building and maintaining custom plugins.

---

## 2.0 — Why Plugins Matter <span class="duration-badge">5 min</span>

agy-cli's plugin system does something unique: it can **import plugins you've already installed in Gemini CLI or Claude Code** — without reinstalling or reconfiguring. Your existing investment in extensions carries over.

```bash
# See what plugins are currently active in agy
agy plugin list
```

The output is JSON showing each plugin's name, source, import date, and components (skills, commands, mcpServers, agents).

```bash
# More readable
agy plugin list | python3 -m json.tool
```

> 📖 Official docs: [Plugins](https://www.antigravity.google/docs/plugins) · [MCP](https://www.antigravity.google/docs/mcp) · [Skills](https://www.antigravity.google/docs/skills)

---

## 2.1 — Importing from Gemini CLI <span class="duration-badge">10 min</span>

> **Pattern: Cross-Tool Plugin Bridge** — pull your entire Gemini CLI plugin setup into agy.

### Import All Gemini CLI Plugins

```bash
agy plugin import gemini
```

agy scans your local Gemini CLI installation, discovers all installed plugins, and stages their components (skills, commands, MCP servers, agents) into agy's config at `~/.gemini/antigravity-cli/`.

Output looks like:

```text
  [ok]    code-review
          ✔ skills      : 3 processed
          ✔ commands    : 2 processed
          - mcpServers  : skipped (not found)
  [ok]    gemini-deep-research
          ✔ commands    : 1 processed
          ✔ mcpServers  : 1 processed
  [skip]  superpowers (already imported)
```

!!! tip "Re-import with --force"
    Already imported plugins are skipped by default. To force re-import after a plugin update:
    ```bash
    agy plugin import gemini --force
    ```

### What Gets Imported

| Component | What it means |
| :-- | :-- |
| `skills` | SKILL.md files with YAML frontmatter — injected into agy's context |
| `commands` | Slash commands available inside agy sessions |
| `mcpServers` | MCP tool servers (GitHub, gcloud, Workspace, etc.) — stdio or SSE |
| `agents` | Custom subagent definitions |
| `hooks` | Staged but not auto-executed (agy handles lifecycle differently) |
| `rules` | Rules files (`rules.md`, `rules/*.md`) injected as RULE blocks |

---

## 2.2 — Importing from Claude Code <span class="duration-badge">5 min</span>

> **Pattern: Unified Tool Surface** — if you use Claude Code alongside agy, import its plugins too.

```bash
agy plugin import claude
```

Same mechanic — agy discovers your Claude Code extension installations and bridges compatible components.

!!! info "Component compatibility"
    Not all Claude Code extension components map 1:1 to agy's model. agy imports what's compatible and silently skips what isn't.

---

## 2.3 — Managing Plugins Per-Project <span class="duration-badge">10 min</span>

> **Pattern: Project-Scoped Plugin Config** — not every plugin is appropriate for every codebase.

### Enable / Disable

```bash
# Disable a plugin for this session/project
agy plugin disable gemini-deep-research

# Re-enable it
agy plugin enable gemini-deep-research

# Check current state
agy plugin list
```

### Plugin Locations

Plugins can be installed at two levels:

| Scope | Path |
| :-- | :-- |
| **Global** | `~/.gemini/config/plugins/` |
| **Project** | `.agents/plugins/` |

### Install a Specific Plugin

```bash
# Install by name (from configured source)
agy plugin install <plugin-name>

# Install a specific version
agy plugin install <plugin-name>@<version>
```

---

## 2.4 — Validating a Plugin <span class="duration-badge">10 min</span>

> **Pattern: Plugin-as-Code** — treat plugin definitions like source code. Validate before shipping.

### Validate an Existing Plugin Directory

```bash
# Validate a plugin directory
agy plugin validate ./path/to/my-plugin

# Or validate the current directory
agy plugin validate .
```

This checks that the plugin's `plugin.json` manifest is well-formed and all referenced components exist.

### Build a Minimal Custom Plugin

A valid agy plugin needs a `plugin.json` manifest. Here's the official structure:

```text
my-plugin/
├── plugin.json          ← manifest (required)
├── mcp_config.json      ← MCP server definitions (optional)
├── hooks.json           ← hook event handlers (optional)
├── skills/              ← SKILL.md files with YAML frontmatter
│   └── my-skill/
│       └── SKILL.md
├── agents/              ← subagent definitions (optional)
└── rules/               ← rules files (optional)
    └── my-rules.md
```

```json
{
  "name": "my-plugin",
  "version": "1.0.0",
  "description": "My custom agy plugin",
  "components": ["skills"]
}
```

```bash
# Validate it
agy plugin validate ./my-plugin

# If valid, you'll see: ✔ Plugin manifest is valid
```

### Interacting with Plugin Components

Use slash commands to inspect active plugin components in a session:

| Command | What it shows |
| :-- | :-- |
| `/skills` | All loaded skills (from plugins, project, global) |
| `/mcp` | Active MCP servers and their status |

### Exercise: Validate the Workshop Plugin

The workshop repo includes a sample plugin at `samples/plugins/workshop-helpers/`. Validate it:

```bash
agy plugin validate samples/plugins/workshop-helpers/
```

---

## 2.5 — Plugin Architecture Overview

```mermaid
graph LR
    GC["Gemini CLI\nPlugins"] --> |agy plugin import gemini| S["Plugin Staging\n~/.gemini/antigravity-cli/plugins/"]
    CC["Claude Code\nExtensions"] --> |agy plugin import claude| S
    S --> |agy plugin enable/disable| A[agy session]
    A --> SK[Skills]
    A --> MCP[MCP Servers]
    A --> AG[Agents]
    A --> RU[Rules]
    A --> HK[Hooks]
    A --> SD[Sidecars]
```

Plugin staging directory structure:

```text
~/.gemini/antigravity-cli/plugins/<name>/
├── plugin.json
├── mcp_config.json
├── hooks.json
├── skills/
├── agents/
├── rules/
└── sidecars/          ← plugin-scoped background processes
```

---

## 2.6 — Sidecars: Persistent Background Processes <span class="duration-badge">15 min</span>

> **Pattern: Always-On Agent** — sidecars run alongside AGY CLI, independently of any conversation. Use them for scheduled tasks, event watchers, and persistent background workers.
>
> 📖 Source: [sidecars](https://antigravity.google/docs/sidecars)

### What Sidecars Are

A sidecar is a background process that AGY manages for you: it launches automatically when AGY starts, restarts on crash, and runs independently of your active conversation. Unlike hooks (which fire in response to conversation events), sidecars are **always running**.

**Three use cases:**

| Use case | Example |
| :-- | :-- |
| Persistent background worker | Python script that watches a queue |
| Scheduled recurring task | Hourly PR triage via `schedule` builtin |
| Event-reactive agent | `agentapi` call that spins up a new conversation |

### Configuration

Sidecars are discovered from two locations:

```bash
# Global sidecars (available in all projects)
~/.gemini/config/sidecars/<sidecar-name>/sidecar.json

# Plugin-scoped sidecars (shipped with a plugin)
~/.gemini/config/plugins/<plugin-name>/sidecars/<sidecar-name>/sidecar.json
```

The directory name becomes the sidecar's ID. Plugin sidecars get the ID `<pluginName>/<sidecarName>`.

**Sidecars are disabled by default.** Enable them explicitly in `~/.gemini/config/config.json`:

```json
{
  "sidecars": {
    "pr-triage": {
      "enabled": true
    },
    "my-plugin/log-watcher": {
      "enabled": true,
      "projectId": "<conversation-project-id>"
    }
  }
}
```

### sidecar.json Schema

| Field | Type | Description |
| :-- | :-- | :-- |
| `command` | string | Executable to run (e.g. `python3`). Mutually exclusive with `builtin`. |
| `builtin` | string | Built-in function. Currently only `schedule`. Mutually exclusive with `command`. |
| `args` | string[] | Arguments passed to the command or builtin. |
| `restart_policy` | string | `always` (default), `on-failure`, or `never`. |
| `description` | string | Human-readable label shown in AGY UI. |
| `env` | object | Environment variables for the sidecar process. |
| `display_name` | string | Display name in the UI. |

### Example 1: Background Worker Script

```json
{
  "description": "Watches the build queue and notifies on failures",
  "command": "python3",
  "args": ["watch_builds.py"],
  "restart_policy": "on-failure",
  "env": {
    "BUILD_QUEUE_URL": "https://ci.example.com/api/queue"
  }
}
```

### Example 2: Scheduled Recurring Task (the `schedule` builtin)

The `schedule` builtin takes a cron expression as its first arg, then the command + args to run:

```json
{
  "description": "Hourly PR triage — summarises incoming review requests",
  "builtin": "schedule",
  "args": [
    "0 * * * *",
    "agentapi",
    "new-conversation",
    "Summarise all open PRs waiting for my review. Group by urgency."
  ]
}
```

`agentapi` is automatically available to sidecars — it lets them **programmatically create or message conversations**:

```bash
# Start a new conversation from a sidecar
agentapi new-conversation "<prompt>"

# Send a message to an existing conversation
agentapi send-message <conversation_id> "<prompt>"
```

!!! warning "projectId required for agentapi"
    Sidecars that use `agentapi new-conversation` must have a `projectId` set in `config.json` — this scopes which conversation project the new session is created under.

### Runtime Data

Sidecar output is stored at:

```text
~/.gemini/antigravity-cli/sidecar_data/<sidecarId>/
├── data/     ← persistent storage (ANTIGRAVITY_EXECUTABLE_DATA_DIR env var)
├── logs/     ← timestamped stdout/stderr logs
└── events/   ← JSON records of agentapi calls
```

### Directory Structure for a Plugin Sidecar

```text
~/.gemini/config/plugins/my-plugin/
└── sidecars/
    └── pr-triage/
        ├── sidecar.json   ← config (required)
        └── triage.py      ← helper script (optional, runs in this dir)
```

---

## Module 2 Exercises

<div class="exercise-card" markdown>

### :material-file-document: Exercise 2: Plugin Bridge

**File:** [`ex02_plugin_bridge.md`](exercises/ex02_plugin_bridge.md)
**Duration:** 20 min
**Objective:** Import plugins from Gemini CLI, enable/disable selectively, validate a custom plugin.

</div>

<div class="exercise-card" markdown>

### :material-clock-outline: Exercise 2B: Your First Sidecar

**File:** [`ex02b_first_sidecar.md`](exercises/ex02b_first_sidecar.md)

> **Duration:** 20 min
> **Build:** A scheduled **daily standup sidecar** that fires at 9am, creates a new AGY conversation, and asks it to summarise yesterday's git commits across your repos.

**What you'll do:**

1. Create `~/.gemini/config/sidecars/standup/sidecar.json` using the `schedule` builtin
2. Set the cron to `0 9 * * 1-5` (9am Monday–Friday)
3. Use `agentapi new-conversation` to open a conversation with your standup prompt
4. Enable it in `~/.gemini/config/config.json`
5. Verify it appears in logs at `~/.gemini/antigravity-cli/sidecar_data/standup/logs/`

**Stretch goal:** Add a second sidecar using `command: python3` that watches a local file for changes and sends a message to an existing conversation when it detects a diff.

</div>

---

## Back to Workshop

→ **[Module 1: SDLC Productivity](sdlc-productivity.md)** — plugins are introduced in Section 1.7

→ **[Cheatsheet](cheatsheet.md)** — all plugin and sidecar commands in one place
