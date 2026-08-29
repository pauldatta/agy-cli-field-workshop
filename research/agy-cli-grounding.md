# AGY CLI — Verified Grounding Reference

> **Purpose:** Single source of truth for all verified Antigravity CLI facts.
> Use this before writing, editing, or reviewing any workshop content.
> Do NOT invent commands or flags — if it's not in this doc, fetch the source first.
>
> **Last verified:** 2026-08-29 via Chrome DevTools MCP (rendered SPA) + `agy --help` live binary
> **Maintainer:** Update this doc whenever you verify a new claim against official sources.
> Add the source URL + uid node reference with every new entry.

---

## Official Documentation URLs

| Page | URL | How to read |
|:--|:--|:--|
| CLI Overview | https://antigravity.google/docs/cli-overview | Chrome DevTools MCP |
| Getting Started | https://antigravity.google/docs/cli-getting-started | Chrome DevTools MCP |
| Using Antigravity CLI | https://antigravity.google/docs/cli-using | Chrome DevTools MCP |
| Features | https://antigravity.google/docs/cli-features | Chrome DevTools MCP |
| Migration from Gemini CLI | https://antigravity.google/docs/gcli-migration | Chrome DevTools MCP |
| Permissions | https://antigravity.google/docs/permissions | Chrome DevTools MCP |
| Strict Mode | https://antigravity.google/docs/strict-mode | Chrome DevTools MCP |
| Plugins | https://antigravity.google/docs/plugins | Chrome DevTools MCP |
| MCP | https://antigravity.google/docs/mcp | Chrome DevTools MCP |
| Skills | https://antigravity.google/docs/skills | Chrome DevTools MCP |
| Rules & Workflows | https://antigravity.google/docs/rules-workflows | Chrome DevTools MCP |
| Hooks | https://antigravity.google/docs/hooks | Chrome DevTools MCP |
| Subagents | https://antigravity.google/docs/subagents | Chrome DevTools MCP |
| Enterprise | https://antigravity.google/docs/enterprise | Chrome DevTools MCP |

> **Note:** antigravity.google is an Angular SPA. Raw `curl` returns an empty shell.
> Always use Chrome DevTools MCP (`navigate_page` → `take_snapshot`) to capture the rendered accessibility tree.
> Every source reference below cites a `uid=N_M StaticText` node from those snapshots.

---

## 1. Installation

### macOS / Linux

```bash
curl -fsSL https://antigravity.google/cli/install.sh | bash
```

Source: [cli-getting-started](https://antigravity.google/docs/cli-getting-started) — uid 1_160

### Windows (PowerShell)

```powershell
irm https://antigravity.google/cli/install.ps1 | iex
```

Source: [cli-getting-started](https://antigravity.google/docs/cli-getting-started) — uid 1_164–1_168

### Windows (CMD)

```cmd
curl -fsSL https://antigravity.google/cli/install.cmd -o install.cmd && install.cmd && del install.cmd
```

Source: [cli-getting-started](https://antigravity.google/docs/cli-getting-started) — uid 1_172–1_176

---

## 2. Authentication

| Scenario | Behaviour |
|:--|:--|
| Local machine | CLI opens default browser to Google Sign-In automatically |
| SSH session | CLI detects SSH and prints a secure authorization URL instead |
| Sign out | Run `/logout` in the CLI |
| Enterprise | Auth via GCP project — see [Enterprise docs](https://antigravity.google/docs/enterprise) |

Source: [cli-getting-started](https://antigravity.google/docs/cli-getting-started) — uid 1_179, 1_182, 1_185–1_189

---

## 3. CLI Flags

All flags verified against `agy --help` live binary output.

| Flag | Description |
|:--|:--|
| `-p` / `--print` | Non-interactive: runs a single prompt and exits |
| `-i` / `--prompt-interactive` | Seeded interactive: starts CLI with initial prompt pre-filled |
| `-c` / `--continue` | Resume most recent session |
| `--conversation <id>` | Resume a specific previous conversation by ID |
| `--add-dir <path>` | Add a directory to the workspace context (repeatable) |
| `--sandbox` | Enable terminal sandbox restrictions |
| `--dangerously-skip-permissions` | Auto-approve all tool permission requests without prompting |
| `--print-timeout <duration>` | Timeout for print mode (default: `5m0s`) |
| `--log-file <path>` | Override CLI log file path |

### ❌ Flags that do NOT exist

These were in older drafts and have been removed. Do not reference them:

| Flag | Why absent |
|:--|:--|
| `--strict` | Not a flag. Strict mode is set via `/permissions` slash command |
| `--model <model>` | Not a flag. Model is set via `/model` slash command |
| `--workspace <path>` | Not in `agy --help` or any official doc |

---

## 4. Top-Level Commands

All verified against `agy --help`.

```
agy update      # Update the CLI to the latest version
agy changelog   # Show release notes and changelog
agy install     # Configure environment paths and shell settings
agy plugin      # Manage plugins (install, uninstall, list, enable, disable)
```

---

## 5. Slash Commands (Interactive Mode)

Official source: [cli-features — Core Slash Commands](https://antigravity.google/docs/cli-features) (uid 5_209–5_265) and [cli-using](https://antigravity.google/docs/cli-using)

| Command | Description | Source |
|:--|:--|:--|
| `/resume` (aliases `/switch`, `/conversation`) | Open session picker — list and resume previous conversations | cli-features uid 5_213–5_219 |
| `/rewind` (alias `/undo`) | Roll back conversation history to a previous turn | cli-features uid 5_220–5_226 |
| `/rename <name>` | Rename the active conversation thread | cli-features uid 5_227–5_229 |
| `/permissions` | View/set autonomy level: `request-review`, `proceed-in-sandbox`, `always-proceed`, `strict` | cli-features uid 5_230–5_238 |
| `/model` | Select default reasoning model — persists across sessions | cli-features uid 5_239–5_241 |
| `/keybindings` | Open keyboard shortcut editor | cli-features uid 5_242–5_244 |
| `/statusline` | Customize the CLI status bar | cli-features uid 5_245–5_247 |
| `/fast` | Toggle fast reasoning mode | cli-features reference |
| `/planning` | Toggle multi-turn plan generation mode | cli-features reference |
| `/teamwork-preview` (alias `/teamwork`) | Launch collaborative multi-agent teams | cli-features reference |
| `/goal` | Autonomous goal-directed loop | cli-features reference |
| `/grill-me` | Interactive requirements interview | cli-features reference |
| `/diff` | Open interactive git diff viewer | cli-features reference |
| `/btw <query>` | Send background note to steer active agent | cli-features reference |
| `/schedule` | Schedule background cron or timer tasks | cli-features reference |
| `/browser` | Launch Chrome DevTools browser automation | cli-features reference |
| `/voice` (alias `/record`) | Toggle voice prompt dictation | cli-features reference |
| `/context` | View active context token usage and files | cli-features reference |
| `/credits` (alias `/quota`) | View G1 credit balance and quota status | cli-features reference |
| `/tasks` | Monitor and terminate background tasks | cli-features uid 5_248–5_250 |
| `/skills` | Browse available agent skills | cli-features uid 5_251–5_253 |
| `/mcp` | Manage MCP servers | cli-features uid 5_254–5_256 |
| `/hooks` | Browse active script and JSON hooks | cli-features reference |
| `/open <path>` | Open a file in the external editor | cli-features uid 5_257–5_259 |
| `/copy` | Copy last agent response to clipboard | cli-features reference |
| `/usage` | Inline interactive help manual | cli-features uid 5_260–5_262 |
| `/help` | Show all available slash commands and shortcuts | cli-features reference |
| `/logout` | Log out and clear cached credentials | cli-features uid 5_263–5_265 |
| `/exit` (alias `/quit`) | Exit the CLI session | cli-features reference |
| `/agents` | Open the subagents panel | cli-features uid 5_289–5_295 |
| `/config` or `/settings` | Open full-screen settings overlay | cli-using uid 3_166–3_169 |
| `/clear` (alias `/new`) | Clear prompt and start new session | cli-using uid 3_225 |
| `/fork` (alias `/branch`) | Spin up a separate parallel workspace | cli-using uid 3_221 |

---

## 6. Quick Tips

Source: [cli-using — Quick Tips](https://antigravity.google/docs/cli-using) uid 3_185–3_232

| Input | Effect |
|:--|:--|
| `@` | Triggers file path autocomplete suggestions |
| `!` at start of prompt | Runs as a terminal command directly |
| `?` | Shows help and lists all slash commands |
| `esc esc` | Clears the prompt box (when no streaming is active) |
| `/rewind` or `/undo` | Go back in conversation history |
| `/fork` | Spin up a separate workspace from current state |
| `/clear` | Clear prompt and start a new session |
| `/resume` | List and resume previous conversation logs |

> When you close the CLI, it automatically prints the exact command to resume that specific session.
> Source: cli-using uid 3_231–3_234

---

## 7. Keyboard Shortcuts

Source: [cli-using — Keybindings](https://antigravity.google/docs/cli-using) uid 3_233–3_335

| Shortcut | Action |
|:--|:--|
| `alt+enter` / `shift+enter` / `ctrl+j` | Insert newline without submitting (`prompt.newline`) |
| `ctrl+g` | Open current prompt in `$EDITOR` (external editor) |
| `ctrl+l` | Clear TUI screen |
| `ctrl+d` | Exit the CLI (or forward delete character) |
| `ctrl+z` | Suspend CLI to background |
| `alt+j` | Teleport to next pending subagent approval (`prompt.teleport_agent`) |
| `ctrl+k` | Fast-approve a pending subagent permission from main conversation |
| `ctrl+o` | Toggle reasoning trajectory expansion (`prompt.toggle_trajectory`) |
| `ctrl+r` | Open Artifact Review Panel (`prompt.open_review`) |
| `ctrl+v` | Paste graphic media or clipboard block into prompt |
| `f5` | Toggle voice dictation (`voice.start_dictation`) |

> **Casing:** Official docs use lowercase consistently (`alt+enter`, not `Alt+Enter`).
> Source: cli-using uid 3_324–3_332 (all three insert-newline combos)
> Source: cli-features uid 5_307–5_309 (ctrl+j), uid 5_314–5_316 (ctrl+k)

---

## 8. Permissions Model

Source: [Permissions](https://antigravity.google/docs/permissions) · [Strict Mode](https://antigravity.google/docs/strict-mode)

Three autonomy levels set via `/permissions` or `settings.json`:

| Level | Behaviour |
|:--|:--|
| `request-review` | **Default.** CLI asks for approval before writing files or running commands |
| `always-proceed` | Auto-approve all tool calls — useful for trusted scripts and CI pipelines |
| `strict` | Deny all tool use unless explicitly allowed — maximum control, read-only equivalent |

### Fine-Grained Allow Rules (settings.json)

```json
{
  "permissions": {
    "mode": "request-review",
    "allow": [
      "command(git)",
      "command(npm test)",
      "write_file(./src/)"
    ]
  }
}
```

Source: [cli-features](https://antigravity.google/docs/cli-features) — uid 5_274

---

## 9. Settings File

Location: `~/.gemini/antigravity-cli/settings.json`

Source: [cli-using](https://antigravity.google/docs/cli-using) — uid 3_161

Open from inside the CLI: `/config` or `/settings`

Source: cli-using uid 3_166–3_169: "Type `/config` or `/settings` to open a full-screen overlay menu"

### Enable Terminal Sandbox

```json
{
  "enableTerminalSandbox": true
}
```

Source: [cli-features](https://antigravity.google/docs/cli-features) — uid 5_185–5_207 (exact JSON key, boolean, default false)

### Hook Registration

```json
{
  "hooks": {
    "PreInvocation": [
      { "command": ".agents/hooks/session-context.sh" }
    ],
    "PreToolUse": [
      { "matcher": "write_file|edit", "command": ".agents/hooks/scope-guard.sh" }
    ],
    "PostToolUse": [
      { "matcher": "write_file", "command": ".agents/hooks/test-nudge.sh" }
    ]
  }
}
```

Source: [Hooks](https://antigravity.google/docs/hooks)

> Hook event names: `PreInvocation`, `PreToolUse`, `PostToolUse`
> Tool names used by AGY: `write_file`, `edit` (not `replace_in_file`)

---

## 10. Terminal Sandbox

Source: [cli-features — Terminal Sandbox](https://antigravity.google/docs/cli-features) uid 5_166–5_219

| Platform | Sandbox mechanism |
|:--|:--|
| Linux | nsjail |
| macOS | sandbox-exec |
| Windows | AppContainer |

**Runtime behaviour:**
- When sandbox **enabled**: prompt offers "Yes, and run without sandbox restrictions" (uid 5_199–5_201)
- When sandbox **disabled**: prompt offers "Yes, and run in sandbox" (uid 5_202–5_206)

---

## 11. Plugins

Source: [cli-features — Plugins](https://antigravity.google/docs/cli-features) uid 5_156–5_174 · [Plugins](https://antigravity.google/docs/plugins)

### Plugin Directory Structure

```
~/.gemini/antigravity-cli/plugins/<plugin_name>/
  plugin.json          # Required marker file
  mcp_config.json      # Optional: MCP server definitions
  hooks.json           # Optional: event hooks
  skills/              # Optional: skill instruction sets
  agents/              # Optional: subagent definitions
  rules/               # Optional: rule files
  import_manifest.json # Tracking manifest (auto-generated on import)
```

Source: cli-features uid 5_159–5_163

### Plugin Commands

```bash
agy plugin install <name>
agy plugin uninstall <name>
agy plugin list
agy plugin enable <name>
agy plugin disable <name>
agy plugin import gemini    # Migrate Gemini CLI extensions
```

Source: `agy --help` + [gcli-migration](https://antigravity.google/docs/gcli-migration) uid 7_187

### Migration Behaviour

- On **first launch**, AGY prompts to migrate extensions automatically (uid 7_170–7_176)
- **Custom themes** cannot be migrated 1:1 — not currently supported (uid 7_177–7_179)

---

## 12. Subagents

Source: [cli-features — Subagents](https://antigravity.google/docs/cli-features) uid 5_278–5_316 · [Subagents](https://antigravity.google/docs/subagents)

- Subagents run **concurrently** with the main conversation without blocking it (uid 5_279)
- `/agents` opens the subagents panel (uid 5_289–5_295)
- Panel shows status: `running`, `done`, `killed` (uid 5_296–5_300)
- `ctrl+j` — teleport to next subagent waiting for approval (uid 5_307–5_309)
- `ctrl+k` — fast-approve a pending subagent permission (uid 5_314–5_316)
- Main agent controls what tools and permissions subagents receive (uid 5_288)

### Fine-Grained Subagent Permissions

```json
{
  "permissions": {
    "allow": ["command(git)", "command(npm test)"]
  }
}
```

Source: cli-features uid 5_274

### Custom Subagent Definition (`.agents/agents/<name>.md`)

```markdown
---
model: gemini-3.1-flash-lite-preview
tools:
  allow:
    - read_file
    - list_directory
    - grep_search
# Omit write_file, run_command to create a read-only agent
---

System prompt for the subagent goes here.
```

Source: [Subagents](https://antigravity.google/docs/subagents)

---

## 13. Skills

Source: [Skills](https://antigravity.google/docs/skills) · [cli-features /skills](https://antigravity.google/docs/cli-features) uid 5_251–5_253

### Global Skills Path

```
~/.gemini/skills/                              # Shared with Gemini CLI (no action needed)
~/.gemini/antigravity-cli/skills/              # AGY-specific global skills
```

Source: [gcli-migration](https://antigravity.google/docs/gcli-migration) uid 7_248–7_263, 7_270

### Workspace Skills Path

```
.agents/skills/     # Workspace-level skills (was .gemini/skills/ in Gemini CLI)
```

Source: gcli-migration uid 7_265–7_270

### Skill File Structure

```
<skills-dir>/<skill-name>/
  SKILL.md    # Required: frontmatter (name, description) + instructions
```

### Browse Skills in CLI

```bash
/skills
```

---

## 14. Context Files

### AGENTS.md

- Read from: current directory → parent directories → home directory
- More specific context overrides broader context
- AGY reads **both** `GEMINI.md` and `AGENTS.md` from the workspace directory

Source: [gcli-migration](https://antigravity.google/docs/gcli-migration) uid 7_234–7_238

Global context file: `~/.gemini/GEMINI.md` (uid 7_241–7_243)

### .agents/ Directory Structure

```
.agents/
  rules.md         # (or rules/*.md) — injected as system prompt directives
  skills/          # Workspace skills
  agents/          # Custom subagent definitions
  mcp_config.json  # Workspace MCP server config
```

Source: [cli-using](https://antigravity.google/docs/cli-using)

---

## 15. MCP Configuration

Source: [MCP](https://antigravity.google/docs/mcp) · [gcli-migration](https://antigravity.google/docs/gcli-migration) uid 7_293–7_320

MCP configs are stored in a **separate `mcp_config.json`** file, not inside `settings.json`.

| Scope | Path |
|:--|:--|
| Global | `~/.gemini/antigravity-cli/mcp_config.json` |
| Workspace | `.agents/mcp_config.json` |

**Key field rename from Gemini CLI:**

```json
{
  "mcpServers": {
    "my-server": {
      "serverUrl": "https://..."
    }
  }
}
```

> `url` and `httpUrl` are deprecated. Use `serverUrl`.
> Source: gcli-migration uid 7_299–7_306

---

## 16. Migration from Gemini CLI

Source: [gcli-migration](https://antigravity.google/docs/gcli-migration) · [Google Developers Blog](https://developers.googleblog.com/an-important-update-transitioning-gemini-cli-to-antigravity-cli/)

| What changed | Gemini CLI | Antigravity CLI |
|:--|:--|:--|
| Binary | `gemini` | `agy` |
| Workspace config dir | `.gemini/` | `.agents/` |
| Workspace skills | `.gemini/skills/` | `.agents/skills/` |
| Workspace MCP config | `settings.json` (mcpServers key) | `.agents/mcp_config.json` |
| Global settings | `~/.gemini/settings.json` | `~/.gemini/antigravity-cli/settings.json` |
| Global MCP config | inside settings.json | `~/.gemini/antigravity-cli/mcp_config.json` |
| Global skills | `~/.gemini/skills/` | Shared — no action needed |
| Context file | `GEMINI.md` | `AGENTS.md` (both are read) |
| MCP `url` field | `url` / `httpUrl` | `serverUrl` |
| Extensions | `.gemini/extensions/` | Plugins: `~/.gemini/antigravity-cli/plugins/` |
| `gemini skills` command | existed | **No equivalent** — use `npx skills install` or create manually |

Source: gcli-migration uid 7_282–7_286: "Antigravity CLI does not currently have an equivalent to the `gemini skills` command"

**Sunset date:** Gemini CLI stops serving requests **June 18, 2026**
Source: Google Developers Blog: "stop serving requests … on June 18, 2026"

---

## 17. Verified Model Names

> **DEPRECATED** — never use in workshop content:
> - `gemini-1.5-flash`
> - `gemini-1.5-pro`

**Current recommended models (per user rules):**

| Use case | Model |
|:--|:--|
| Cost-efficient, everyday tasks | `gemini-3.1-flash-lite-preview` or `gemini-3-flash-preview` |
| Orchestration, complex routing | `gemini-3.1-pro-preview` or `gemini-3-pro-preview` |

Set via `/model` slash command inside the CLI.

---

## 18. What Has No Official Documentation

Treat the following as **unverified** until sourced. Do not include in workshop content without a doc reference:

| Claim | Status |
|:--|:--|
| Auto Memory (`experimental.autoMemory`) | Referenced in Gemini CLI docs — not yet verified against AGY docs |
| `/memory show` / `/memory add` commands | Not found in AGY cli-features slash command table |
| `@codebase_investigator` built-in subagent | Was a Gemini CLI built-in — not verified in AGY docs |
| `Conductor` orchestrator | Was a Gemini CLI feature — not verified in AGY docs |
| Automatic model routing (Pro for planning, Flash for coding) | Was heuristic in Gemini CLI — not documented in AGY |
| `/stats` command | Not in AGY cli-features slash command table |

---

## Update Protocol

When you verify a new claim against official AGY docs:

1. Add it to the relevant section above with exact syntax
2. Include the source URL + uid node reference
3. If it contradicts something already here, update the existing entry and note the change
4. If it invalidates a workshop doc, update that doc and the AUDIT.md claim count

When AGY releases a new version, re-run the Chrome DevTools MCP verification sweep against each section header URL and update uid references where the page structure has changed.
