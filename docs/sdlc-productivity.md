# Module 1: SDLC Productivity <span class="duration-badge">75 min</span>

> **Your first real Antigravity CLI session.** This module covers the core daily-driver workflows — understanding code, refactoring, generating tests, and reviewing changes — plus how to extend the CLI with plugins for your team's toolchain.

---

## 1.0 — First Interactive Session <span class="duration-badge">5 min</span>

Launch Antigravity CLI in your workshop project directory:

```bash
cd agy-cli-field-workshop
agy
```

You'll land in the interactive prompt. Try:

```text
> What files are in this project and what does each one do?
```

Observe how agy reads your workspace — it indexes the git repo, reads file contents, and responds with context. This is **automatic**: no config, no prompts to write first.

!!! tip "The .agents/ folder"
    After your first session, check `.agents/` — agy created project config files tracking your workspace. This is how it knows what to index on future runs.

---

## 1.1 — Code Understanding <span class="duration-badge">10 min</span>

> **Pattern: Explain Before You Touch** — understand the code before changing it.

### Exercise: Map an Unfamiliar Codebase

```bash
# -i seeds the session with an initial prompt and stays interactive
agy -i "Give me a high-level architecture overview of this project. What are the main components and how do they connect?"
```

Then follow up interactively:

```text
> Which file handles the entry point?
> What external dependencies does this project have?
> Are there any obvious code smells or tech debt?
```

!!! tip "Use -i for seeded sessions"
    `agy -i "<task>"` (short for `--prompt-interactive`) starts with a prompt but stays interactive. Great for oriented exploration — you set the direction, then steer with follow-ups.

---

## 1.2 — Refactoring <span class="duration-badge">10 min</span>

> **Pattern: Propose, Review, Apply** — never apply changes you haven't read.

### Exercise: Targeted Refactor

```bash
agy
```

```text
> I want to refactor the error handling in this project. First, show me all the places where errors are currently caught or returned — don't change anything yet.
```

Review the findings. Then:

```text
> Now propose a refactored version of [specific function] using a consistent error handling pattern. Show me the diff before applying.
```

Only apply after you've read the proposed change.

### Permissions Model

agy has a **4-level permissions model** (`toolPermission` in `settings.json`) that controls how it handles tool approvals:

| Level | Behavior |
| :-- | :-- |
| `request-review` | **Default.** agy asks for approval before writing files or running commands |
| `proceed-in-sandbox` | Auto-approve within sandbox restrictions, prompt for elevated actions |
| `always-proceed` | Auto-approve all tool calls — useful for trusted scripts and CI |
| `strict` | Deny all tool use unless explicitly allowed — maximum control |

Use the `/permissions` slash command to view or change the current level. You can also configure fine-grained settings in `~/.gemini/antigravity-cli/settings.json` or `.agents/settings.json`:

```json
{
  "toolPermission": "request-review",
  "artifactReviewPolicy": "asks-for-review",
  "altScreenMode": "default",
  "editorMode": "default",
  "allowNonWorkspaceAccess": false,
  "enableTerminalSandbox": true,
  "permissions": {
    "allow": ["command(git)", "read_file"],
    "deny": ["command(rm -rf)"]
  }
}
```

> 📖 Full details: [Permissions docs](https://antigravity.google/docs/permissions)

---

## 1.3 — Test Generation <span class="duration-badge">10 min</span>

> **Pattern: Test What Exists** — generate tests for real code, not hypotheticals.

### Exercise: Generate Unit Tests

```bash
agy
```

```text
> Look at [specific function or file]. Generate a comprehensive unit test suite for it. Include happy path, edge cases, and error conditions. Use the testing framework already in this project.
```

Then:

```text
> Run the tests and fix any that fail.
```

!!! tip "Let agy run the tests"
    agy can execute shell commands. It will run your test suite and iterate on failures without you having to copy-paste error messages. Watch it self-correct.

---

## 1.4 — Code Review <span class="duration-badge">10 min</span>

> **Pattern: Pre-Commit Review** — use agy as a senior reviewer before every push.

### Exercise: Review Your Changes

```bash
# Stage some changes (or use an existing branch)
git add -p

# Start agy and review what's staged
agy
```

```text
> Review my staged changes for: (1) correctness, (2) security issues, (3) missing test coverage, (4) anything that would block a PR. Be direct — don't soften findings.
```

### Headless Variant (for scripting)

```bash
# Review changes non-interactively — useful in pre-commit hooks or CI
git diff --cached | agy --print "Review these changes. Flag any bugs, security issues, or missing tests. Output as markdown."
```

---

## 1.5 — Project Context with AGENTS.md <span class="duration-badge">5 min</span>

> **Pattern: Persistent Context** — tell agy once, it remembers every session.

agy reads context files at session start. Create one at the project root:

```bash
cat > AGENTS.md << 'EOF'
# Project Context

This is a Node.js REST API built with Express and TypeScript.

## Key Conventions
- Language: TypeScript (strict mode, no `any`)
- Testing: Jest with 80% coverage minimum; run `npm test` to validate
- Style: ESLint + Prettier; run `npm run lint` before committing
- DO NOT modify `src/db/migrations/` — those are append-only
- DO NOT use `console.log` in production code; use the `logger` utility

## Architecture
Three-layer: `routes/` → `services/` → `repositories/`. All DB access goes through the repository layer. External HTTP calls go through `src/clients/`.

## Common Commands
- `npm run dev` — start local dev server on :3000
- `npm test` — run full test suite
- `npm run db:migrate` — apply pending DB migrations
EOF
```

Now start a new session:

```bash
agy --print "What do you know about this project?"
```

agy will incorporate your AGENTS.md into every subsequent session automatically.

!!! info "Context hierarchy"
    agy reads AGENTS.md from: current directory → parent directories → home directory. More specific context overrides broader context.

### Additional Context Sources

Beyond AGENTS.md, agy also loads:

- **`.agents/rules.md`** (or `.agents/rules/*.md`) — project-level rules injected as system prompt directives. Use these for hard requirements like "never delete migration files" or "always use TypeScript strict mode."
- **`.gemini/`** — for Gemini CLI compatibility, agy reads `.gemini/` directories alongside `.agents/`.
- **`~/.gemini/config/rules.md`** — global rules applied to all sessions.

> 📖 Full details: [Rules & Workflows docs](https://www.antigravity.google/docs/rules-workflows)

### Sample Agent Definitions (in `samples/agents/`)

| Agent | Model | Purpose |
| :-- | :-- | :-- |
| `doc-writer.md` | `gemini-3.7-flash` | Generates API docs, README sections, and inline comments from source |
| `pr-reviewer.md` | `gemini-3.7-flash` | Reviews code changes for quality, bugs, and style violations |
| `migration-validator.md` | `gemini-3.7-flash` | Validates Gemini CLI → Antigravity CLI migration completeness |

---

## 1.6 — Interactive Navigation <span class="duration-badge">5 min</span>

> **Pattern: Terminal Fluency** — know the shortcuts that make agy sessions fast.
> 📖 Full reference: [Using Antigravity CLI](https://www.antigravity.google/docs/cli-using)

### Key Slash Commands

| Command | What it does |
| :-- | :-- |
| `/resume` (or `/switch`) | Open conversation picker to resume or switch sessions |
| `/rewind` (or `/undo`) | Roll back conversation history to a previous checkpoint |
| `/fork` (or `/branch`) | Branch the active conversation into an isolated workspace |
| `/rename <name>` | Rename the active conversation thread |
| `/clear` (or `/new`) | Clear active context and start a new conversation |
| `/config` (or `/settings`) | Open full-screen settings overlay |
| `/permissions` | Set agent autonomy level (`request-review`, `proceed-in-sandbox`, `always-proceed`, `strict`) |
| `/model` | Select reasoning model (persists across sessions) |
| `/teamwork-preview` | Launch collaborative multi-agent teams |
| `/diff` | Open interactive git diff viewer |
| `/btw <query>` | Inject a guidance note into an active agent task |
| `/tasks` | Monitor, view logs for, or terminate background tasks |
| `/agents` | View, manage, and approve subagent actions |
| `/skills` | Browse local and global agent skills |
| `/mcp` | Configure and manage MCP servers |
| `/context` | View active context token usage |
| `/credits` | View remaining G1 credit balances |
| `/open <path>` | Open a file in your preferred external editor |
| `/usage` | Open the inline interactive help manual |

> 📖 Full slash command reference: [CLI Features](https://antigravity.google/docs/cli-features)

### Quick Tips

| Shortcut | What it does |
| :-- | :-- |
| `@` | File path autocomplete — type `@` to trigger path suggestions |
| `!` | Run terminal commands directly without leaving agy |
| `esc esc` | Clear the current prompt input (when no streaming is active) |
| `?` | Get help and list all slash commands |
| `alt+enter` / `shift+enter` / `ctrl+j` | Insert a newline in your prompt (`prompt.newline`) |
| `ctrl+g` | Edit prompt inside your default shell editor (`$EDITOR`) |
| `ctrl+l` | Clear TUI screen |
| `ctrl+d` | Exit the CLI (or forward delete character) |
| `alt+j` | Teleport to next pending subagent approval (`prompt.teleport_agent`) |
| `ctrl+k` | Fast-approve pending subagent permission from main conversation |
| `ctrl+o` | Toggle reasoning trajectory expansion (`prompt.toggle_trajectory`) |
| `ctrl+r` | Open Artifact Review Panel (`prompt.open_review`) |
| `ctrl+v` | Paste graphic media or clipboard block into prompt |
| `f5` | Toggle voice dictation (`voice.start_dictation`) |

> 📖 Full keybindings reference: [Using Antigravity CLI](https://antigravity.google/docs/cli-using)

---

## 1.7 — Extend with Plugins <span class="duration-badge">15 min</span>

> **Pattern: Bring Your Toolchain** — plugins add skills, MCP servers, agents, and rules to agy. Install once, available in every session.

Antigravity CLI's plugin system does something unique: it can **import plugins you've already installed in Gemini CLI** — without reinstalling or reconfiguring. Your existing investment carries over.

### See What's Active

```bash
agy plugin list
```

Shows each plugin's name, source, import date, and components (skills, commands, mcpServers, agents).

### Import from Gemini CLI

```bash
agy plugin import gemini
```

agy scans your local Gemini CLI installation, discovers all installed plugins, and stages their components into `~/.gemini/antigravity-cli/`. Output:

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

!!! warning "Custom themes are silently dropped"
    Custom theme components cannot be migrated 1:1 to agy's model and are skipped without error during import. Check your active plugins after import if themes are important to your workflow.

!!! tip "Re-import after plugin updates"
    Already-imported plugins are skipped by default. Force a re-import:
    ```bash
    agy plugin import gemini --force
    ```

### What Gets Imported

| Component | What it means |
| :-- | :-- |
| `skills` | SKILL.md files — injected as domain expertise into agy sessions |
| `commands` | Slash commands available inside agy sessions |
| `mcpServers` | MCP tool servers (GitHub, gcloud, Workspace, etc.) |
| `agents` | Custom subagent definitions |
| `rules` | Rules files injected as system prompt directives |
| `hooks` | Staged but not auto-executed — agy handles lifecycle differently |

### Enable / Disable Per-Project

Not every plugin is appropriate for every codebase:

```bash
# Disable for this project
agy plugin disable gemini-deep-research

# Re-enable
agy plugin enable gemini-deep-research
```

### Plugin Locations

| Scope | Path |
| :-- | :-- |
| **Global** | `~/.gemini/antigravity-cli/plugins/` |
| **Project** | `.agents/plugins/` |

### Building a Custom Plugin

A valid agy plugin needs a `plugin.json` manifest:

```text
my-plugin/
├── plugin.json          ← required
├── mcp_config.json      ← MCP server definitions (optional)
├── hooks.json           ← hook event handlers (optional)
├── skills/              ← SKILL.md files (optional)
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

Validate it before shipping:

```bash
agy plugin validate ./my-plugin
# ✔ Plugin manifest is valid
```

> 📖 Full reference: [Plugins](https://www.antigravity.google/docs/plugins) · [Migration guide](https://www.antigravity.google/docs/gcli-migration)

---

## Module 1 Exercises

<div class="exercise-card" markdown>

### :material-file-document: Exercise 1: First Session

**File:** [`ex01_first_session.md`](exercises/ex01_first_session.md)  
**Duration:** 15 min  
**Objective:** Launch agy, explore a codebase, generate an AGENTS.md.

</div>

<div class="exercise-card" markdown>

### :material-puzzle: Exercise 2: Plugin Bridge

**File:** [`ex02_plugin_bridge.md`](exercises/ex02_plugin_bridge.md)  
**Duration:** 20 min  
**Objective:** Import plugins from Gemini CLI, enable/disable selectively, validate a custom plugin.

</div>

---

## Next Module

→ **[Module 2: Legacy Codebase Modernization](legacy-modernization.md)** — strict mode, agent self-onboarding, subagents, and `/rewind` as your safety net.
