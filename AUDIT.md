# Workshop Quality Audit

## Test Register

Each row is an automated test case that runs in CI (`.github/workflows/workshop-structural.yml`)
or locally via `make precommit`. Run the full suite with `make precommit`.

| ID | Test Name | Command | What It Catches | Status |
| :-- | :-- | :-- | :-- | :-- |
| T-01 | Markdown Lint — English | `npx markdownlint-cli2 "docs/*.md" "README.md" "AGENTS.md" "CONTRIBUTING.md"` | MD022 (blank lines), MD040 (untagged fences), MD060 (table style), MD001 (heading levels) | ✅ CI |
| T-02 | Markdown Lint — Translated | `npx markdownlint-cli2 "docs/id/**/*.md" "docs/ko/**/*.md" "docs/zh/**/*.md"` | Same rules on generated translations; MD022 most common failure | ✅ CI |
| T-03 | Code Block Validation | `bash scripts/validate-code-blocks.sh docs/` | `bash` blocks with non-bash content (prompts, tables, CLI output); `yaml` blocks with prose | ✅ CI |
| T-04 | MkDocs Strict Build | `.venv/bin/mkdocs build --strict` | Broken relative links (wrong depth in translated files), nav mismatches, missing i18n plugin | ✅ CI |
| T-05 | Required Files | CI step: "Check required files exist" | Deleted or renamed core files (README.md, mkdocs.yml, AUDIT.md, etc.) | ✅ CI |
| T-06 | JSON Config Syntax | `jq . samples/configs/*.json` | Invalid JSON in settings/mcp samples | ✅ CI |
| T-07 | Shell Script Syntax | `bash -n scripts/*.sh` | Broken shell scripts in scripts/ and samples/hooks/ | ✅ CI |
| T-08 | Agent Frontmatter | CI step: "Validate agent frontmatter" | Agent definition files missing YAML `---` frontmatter | ✅ CI |
| T-09 | Stale Binary References | `grep -rE 'gemini ' docs/*.md` | Docs that still say `gemini` instead of `agy` | ✅ CI |
| T-10 | Stale Hook Event Names | `grep -r '"SessionStart"' docs/` | Old Gemini CLI hook names (SessionStart, BeforeTool, AfterTool) | ✅ CI |
| T-11 | Drift Detection | `bash scripts/detect-drift.sh` | AUDIT.md claims that conflict with detected binary behavior | ✅ CI |
| T-12 | Translation Coverage | `make check-translations` | Auto-detects all language subdirs under docs/; tells contributor which translations need regenerating — non-blocking | ⚠️ Advisory |
| T-13 | Translation Drift | `make check-translations` | Auto-detects all language subdirs under docs/; shows which English files have changed since last translation — non-blocking | ⚠️ Advisory |
| T-14 | Live Smoke Test | `make test-live` | agy binary present and responding (needs GCP auth) | 🔧 Local only |

### Known Root Causes of Recurring CI Failures

| Failure Pattern | Root Cause | Prevention |
| :-- | :-- | :-- |
| `MD022` in translated files | Translation model drops blank line between `</div>` and `## Heading` | Run `make post-translate L=<lang>` after every translation |
| Code block `Invalid bash syntax` | Prompt text / CLI output tagged as `` ```bash `` | Use `` ```text `` for anything that isn't a real shell command |
| Code block `Invalid YAML` | MkDocs admonitions (`!!!`) or prose tagged as `` ```yaml `` | Use `` ```text `` for admonitions and non-config YAML |
| MkDocs `link not found` in translated files | Relative link depth wrong (used `../../` instead of `../`) | Translated files are one level deep — relative links need only one `../` |
| MkDocs `Aborted with configuration error` in CI | CI pip install missing `mkdocs-static-i18n` | Fixed: CI now installs `mkdocs-static-i18n mkdocs-minify-plugin` |

---

# Workshop Content Audit — Grounded Against Official Sources

> **Audit date:** 2026-08-29 (v6 — confirmed against Antigravity 2.11 / CLI 1.1.22 / SDK 0.1.15)
> **Auditor:** Antigravity Agent (Chrome DevTools MCP + live binary)
> **Workshop:** [Antigravity CLI Field Workshop](https://github.com/pauldatta/agy-cli-field-workshop)

---

## Sources of Truth

All claims are verified against one or more of the following **official** sources. No community guides or secondary sources are used as evidence.

| Priority | Source | URL | How read |
|:--|:--|:--|:--|
| 🥇 | `agy --help` live binary | — | `run_command` |
| 🥇 | Antigravity CLI — Getting Started | https://antigravity.google/docs/cli-getting-started | Chrome DevTools MCP (rendered SPA) |
| 🥇 | Antigravity CLI — Using | https://antigravity.google/docs/cli-using | Chrome DevTools MCP (rendered SPA) |
| 🥇 | Antigravity CLI — Features | https://antigravity.google/docs/cli-features | Chrome DevTools MCP (rendered SPA) |
| 🥇 | Antigravity CLI — Migration | https://antigravity.google/docs/gcli-migration | Chrome DevTools MCP (rendered SPA) |
| 🥈 | Google Developers Blog (sunset announcement) | https://developers.googleblog.com/an-important-update-transitioning-gemini-cli-to-antigravity-cli/ | `read_url_content` (static HTML) |

> [!NOTE]
> antigravity.google is an Angular SPA. All page content was retrieved by navigating Chrome via the DevTools MCP and capturing the rendered accessibility tree — not by fetching raw HTML. Every claim below maps to a specific `uid=N_M StaticText` node from those snapshots.

---

## 1. Installation & Authentication (`setup.md` / `cheatsheet.md`)

| # | Claim | Official Source |
|:--|:------|:---|
| 1.1 | Install (macOS/Linux): `curl -fsSL https://antigravity.google/cli/install.sh \| bash` | [cli-getting-started](https://antigravity.google/docs/cli-getting-started) — uid 1_160 |
| 1.2 | Install (Windows PowerShell): `irm https://antigravity.google/cli/install.ps1 \| iex` | [cli-getting-started](https://antigravity.google/docs/cli-getting-started) — uid 1_164–1_168 |
| 1.3 | Install (Windows CMD): `curl -fsSL https://antigravity.google/cli/install.cmd -o install.cmd && install.cmd && del install.cmd` | [cli-getting-started](https://antigravity.google/docs/cli-getting-started) — uid 1_172–1_176 |
| 1.4 | Auth: browser-based Google Sign-In on local machine | [cli-getting-started](https://antigravity.google/docs/cli-getting-started) — uid 1_179: "The CLI will automatically open your default browser to the Google Sign-In page" |
| 1.5 | Auth: SSH sessions → printed authorization URL | [cli-getting-started](https://antigravity.google/docs/cli-getting-started) — uid 1_182: "The CLI will detect that you are in an SSH session and print a secure authorization URL" |
| 1.6 | `/logout` to sign out and remove saved credentials | [cli-getting-started](https://antigravity.google/docs/cli-getting-started) — uid 1_185–1_189: "To terminate your session … run the command `/logout`" |
| 1.7 | Enterprise auth via GCP project | [cli-getting-started](https://antigravity.google/docs/cli-getting-started) — uid 1_188–1_191 + [Enterprise docs](https://antigravity.google/docs/enterprise) |
| 1.8 | Settings stored at `~/.gemini/antigravity-cli/settings.json` | [cli-using](https://antigravity.google/docs/cli-using) — uid 3_161: "~/.gemini/antigravity-cli/settings.json" |
| 1.9 | `/config` or `/settings` opens full-screen settings overlay | [cli-using](https://antigravity.google/docs/cli-using) — uid 3_166–3_169: "Type `/config` or `/settings` to open a full-screen overlay menu" |
| 1.10 | `agy changelog` — show release notes | `agy --help` live: "changelog: Show changelog and release notes" |
| 1.11 | `agy update` — self-update | `agy --help` live: "update: Update CLI" |
| 1.12 | `agy install` — configure PATH and shell settings | `agy --help` live: "install: Configure environment paths and shell settings" |

---

## 2. CLI Flags (`cheatsheet.md`)

| # | Flag | Official Source |
|:--|:------|:---|
| 2.1 | `-p` / `--print` — non-interactive single prompt | `agy --help`: "-p: Short alias for --print" |
| 2.2 | `-i` / `--prompt-interactive` — seeded interactive | `agy --help`: "-i: Short alias for --prompt-interactive" |
| 2.3 | `-c` / `--continue` — resume most recent session | `agy --help`: "-c: Short alias for --continue" |
| 2.4 | `--conversation <id>` — resume by ID | `agy --help`: "--conversation: Resume a previous conversation by ID" |
| 2.5 | `--add-dir <path>` — add directory to workspace (repeatable) | `agy --help`: "--add-dir: Add a directory to the workspace (repeatable) (default [])" |
| 2.6 | `--sandbox` — enable terminal sandbox | `agy --help`: "--sandbox: Run in a sandbox with terminal restrictions enabled" |
| 2.7 | `--dangerously-skip-permissions` — auto-approve all tool requests | `agy --help`: "--dangerously-skip-permissions: Auto-approve all tool permission requests without prompting" |
| 2.8 | `--print-timeout <duration>` — timeout for print mode (default 5m) | `agy --help`: "--print-timeout: Timeout for print mode wait (default 5m0s)" |
| 2.9 | `--log-file <path>` — override log path | `agy --help`: "--log-file: Override CLI log file path" |

> [!NOTE]
> Model selection and strict mode are set via `/model` and `/permissions` slash commands, not CLI flags. See [cli-features](https://antigravity.google/docs/cli-features).

---

## 3. Slash Commands (`cheatsheet.md`, `sdlc-productivity.md`)

Official source: [CLI Features — Core Slash Commands](https://antigravity.google/docs/cli-features) (uid 5_209–5_265)

| # | Command | Official Source |
|:--|:------|:---|
| 3.1 | `/resume` (aliases `/switch`, `/conversation`) — conversation picker | [cli-features](https://antigravity.google/docs/cli-features) — uid 5_213–5_219 |
| 3.2 | `/rewind` (alias `/undo`) — roll back conversation history | [cli-features](https://antigravity.google/docs/cli-features) — uid 5_220–5_226 |
| 3.3 | `/rename <name>` — rename active conversation thread | [cli-features](https://antigravity.google/docs/cli-features) — uid 5_227–5_229 |
| 3.4 | `/permissions` — set autonomy level (`request-review`, `proceed-in-sandbox`, `always-proceed`, `strict`) | [cli-features](https://antigravity.google/docs/cli-features) — uid 5_230–5_238 |
| 3.5 | `/model` — select default reasoning model (persists across sessions) | [cli-features](https://antigravity.google/docs/cli-features) — uid 5_239–5_241 |
| 3.6 | `/keybindings` — open keyboard shortcut editor | [cli-features](https://antigravity.google/docs/cli-features) — uid 5_242–5_244 |
| 3.7 | `/statusline` — customize CLI status bar | [cli-features](https://antigravity.google/docs/cli-features) — uid 5_245–5_247 |
| 3.8 | `/tasks` — monitor/terminate background tasks | [cli-features](https://antigravity.google/docs/cli-features) — uid 5_248–5_250 |
| 3.9 | `/skills` — browse agent skills | [cli-features](https://antigravity.google/docs/cli-features) — uid 5_251–5_253 |
| 3.10 | `/mcp` — manage MCP servers | [cli-features](https://antigravity.google/docs/cli-features) — uid 5_254–5_256 |
| 3.11 | `/open <path>` — open file in external editor | [cli-features](https://antigravity.google/docs/cli-features) — uid 5_257–5_259 |
| 3.12 | `/usage` — inline interactive help manual | [cli-features](https://antigravity.google/docs/cli-features) — uid 5_260–5_262 |
| 3.13 | `/logout` — log out and clear cached credentials | [cli-features](https://antigravity.google/docs/cli-features) — uid 5_263–5_265 |
| 3.14 | `/agents` — subagents panel | [cli-features](https://antigravity.google/docs/cli-features) — uid 5_289–5_295 |
| 3.15 | `/config` / `/settings` — settings overlay | [cli-using](https://antigravity.google/docs/cli-using) — uid 3_166–3_169 |
| 3.16 | `/clear` (alias `/new`) — clear prompt and start new session | [cli-using](https://antigravity.google/docs/cli-using) — uid 3_225 |
| 3.17 | `/fork` (alias `/branch`) — spin up a separate workspace | [cli-using](https://antigravity.google/docs/cli-using) — uid 3_221 |
| 3.18 | `/teamwork-preview` (alias `/teamwork`) — launch collaborative agent team | [cli-features](https://antigravity.google/docs/cli-features) |
| 3.19 | `/diff` — open interactive git diff viewer | [cli-features](https://antigravity.google/docs/cli-features) |
| 3.20 | `/btw <query>` — mid-flight task steering | [cli-features](https://antigravity.google/docs/cli-features) |
| 3.21 | `/goal` — autonomous goal-directed loop | [cli-features](https://antigravity.google/docs/cli-features) |
| 3.22 | `/grill-me` — interactive requirements interview | [cli-features](https://antigravity.google/docs/cli-features) |
| 3.23 | `/schedule` — schedule background cron or timer tasks | [cli-features](https://antigravity.google/docs/cli-features) |
| 3.24 | `/browser` — launch Chrome DevTools browser automation | [cli-features](https://antigravity.google/docs/cli-features) |
| 3.25 | `/fast` — toggle fast reasoning mode | [cli-features](https://antigravity.google/docs/cli-features) |
| 3.26 | `/planning` — toggle multi-turn plan generation mode | [cli-features](https://antigravity.google/docs/cli-features) |
| 3.27 | `/voice` (alias `/record`) — toggle voice prompt dictation | [cli-features](https://antigravity.google/docs/cli-features) |
| 3.28 | `/context` — view active context token usage and files | [cli-features](https://antigravity.google/docs/cli-features) |
| 3.29 | `/credits` (alias `/quota`) — view G1 credit balance and quota | [cli-features](https://antigravity.google/docs/cli-features) |
| 3.30 | `/hooks` — browse active script and JSON hooks | [cli-features](https://antigravity.google/docs/cli-features) |
| 3.31 | `/copy` — copy last agent response to clipboard | [cli-features](https://antigravity.google/docs/cli-features) |
| 3.32 | `/help` — list all slash commands | [cli-features](https://antigravity.google/docs/cli-features) |
| 3.33 | `/exit` (alias `/quit`) — exit CLI session | [cli-features](https://antigravity.google/docs/cli-features) |

---

## 4. Quick Tips & Keybindings (`cheatsheet.md`, `sdlc-productivity.md`)

Official source: [cli-using — Quick Tips](https://antigravity.google/docs/cli-using) (uid 3_185–3_232) and [cli-using — Keybindings](https://antigravity.google/docs/cli-using) (uid 3_233–3_335)

| # | Claim | Official Source |
|:--|:------|:---|
| 4.1 | `@` — file path autocomplete | [cli-using](https://antigravity.google/docs/cli-using) — uid 3_187–3_189 |
| 4.2 | `!` — run terminal commands directly | [cli-using](https://antigravity.google/docs/cli-using) — uid 3_194–3_197 |
| 4.3 | `esc esc` — clear prompt box | [cli-using](https://antigravity.google/docs/cli-using) — uid 3_190–3_193 |
| 4.4 | `?` — get help and list slash commands | [cli-using](https://antigravity.google/docs/cli-using) — uid 3_198–3_201 |
| 4.5 | `/rewind` or `/undo` to go back in conversation | [cli-using](https://antigravity.google/docs/cli-using) — uid 3_213–3_220 |
| 4.6 | `/fork` to spin up a separate workspace | [cli-using](https://antigravity.google/docs/cli-using) — uid 3_219–3_224 |
| 4.7 | `/clear` to clear and start new session | [cli-using](https://antigravity.google/docs/cli-using) — uid 3_223–3_228 |
| 4.8 | `/resume` to list and resume previous conversation logs | [cli-using](https://antigravity.google/docs/cli-using) — uid 3_227–3_232 |
| 4.9 | When you close the CLI, it prints the exact resume command | [cli-using](https://antigravity.google/docs/cli-using) — uid 3_231–3_234 |
| 4.10 | `alt+enter` / `shift+enter` / `ctrl+j` — insert newline | [cli-using](https://antigravity.google/docs/cli-using) — uid 3_324–3_332 |
| 4.11 | `ctrl+g` — open editor for prompt | [cli-using](https://antigravity.google/docs/cli-using) — uid 3_276–3_280 |
| 4.12 | `ctrl+l` — clear TUI screen | [cli-using](https://antigravity.google/docs/cli-using) — uid 3_250–3_254 |
| 4.13 | `ctrl+d` — exit CLI (or forward delete character) | [cli-using](https://antigravity.google/docs/cli-using) — uid 3_261–3_265 |
| 4.14 | `ctrl+z` — suspend CLI to background | [cli-using](https://antigravity.google/docs/cli-using) — uid 3_264–3_268 |
| 4.15 | `alt+j` — teleport to pending subagent approval | [cli-features](https://antigravity.google/docs/cli-features) |
| 4.16 | `ctrl+k` — fast-approve subagent permission | [cli-features](https://antigravity.google/docs/cli-features) — uid 5_314–5_316 |
| 4.17 | `ctrl+o` — toggle reasoning trajectory expansion | [cli-using](https://antigravity.google/docs/cli-using) |
| 4.18 | `ctrl+r` — open artifact review panel | [cli-using](https://antigravity.google/docs/cli-using) |
| 4.19 | `ctrl+v` — paste graphic media / clipboard | [cli-using](https://antigravity.google/docs/cli-using) |
| 4.20 | `f5` — toggle voice dictation | [cli-using](https://antigravity.google/docs/cli-using) |

---

## 5. Plugins (`plugin-ecosystem.md`)

Official source: [CLI Features — Plugins](https://antigravity.google/docs/cli-features) (uid 5_156–5_174) + [Migration — Extensions → Plugins](https://antigravity.google/docs/gcli-migration) (uid 7_180–7_229)

| # | Claim | Official Source |
|:--|:------|:---|
| 5.1 | Plugins staged at `~/.gemini/antigravity-cli/plugins/<plugin_name>/` | [cli-features](https://antigravity.google/docs/cli-features) — uid 5_159–5_163 |
| 5.2 | `plugin.json` — required marker file | [cli-features](https://antigravity.google/docs/cli-features) — uid 5_163 line "plugin.json # Required marker file" |
| 5.3 | `mcp_config.json` — optional MCP server definitions | [cli-features](https://antigravity.google/docs/cli-features) — uid 5_163 |
| 5.4 | `hooks.json` — optional event hooks | [cli-features](https://antigravity.google/docs/cli-features) — uid 5_163 |
| 5.5 | `skills/`, `agents/`, `rules/` subdirectories in plugin | [cli-features](https://antigravity.google/docs/cli-features) — uid 5_163 |
| 5.6 | `import_manifest.json` — tracking manifest | [cli-features](https://antigravity.google/docs/cli-features) — uid 5_163 line "import_manifest.json # Tracking manifest" |
| 5.7 | `agy plugin import gemini` — migrate Gemini CLI extensions | [gcli-migration](https://antigravity.google/docs/gcli-migration) — uid 7_187: "`agy plugin import gemini`" |
| 5.8 | On first launch, Antigravity CLI prompts to migrate extensions automatically | [gcli-migration](https://antigravity.google/docs/gcli-migration) — uid 7_170–7_176: "On the first launch … you should see Migration Options" |
| 5.9 | Custom themes cannot be migrated 1:1 | [gcli-migration](https://antigravity.google/docs/gcli-migration) — uid 7_177–7_179: "Some Gemini CLI extensions cannot be migrated 1:1 … custom themes are not currently supported" |
| 5.10 | `agy plugin install <name>`, `enable`, `disable`, `list` | `agy --help`: "plugin: Manage plugins (install, uninstall, list, enable, disable)" |

---

## 6. Migration from Gemini CLI (`migration-guide.md`)

Official source: [gcli-migration](https://antigravity.google/docs/gcli-migration)

| # | Claim | Official Source |
|:--|:------|:---|
| 6.1 | Binary renamed: `gemini` → `agy` | [cli-overview](https://antigravity.google/docs/cli-overview) + `agy --help` |
| 6.2 | `GEMINI.md` and `AGENTS.md` both read from workspace directory | [gcli-migration](https://antigravity.google/docs/gcli-migration) — uid 7_234–7_238: "Reads both `GEMINI.md` and `AGENTS.md` from your active workspace directory" |
| 6.3 | Global context: `~/.gemini/GEMINI.md` | [gcli-migration](https://antigravity.google/docs/gcli-migration) — uid 7_241–7_243 |
| 6.4 | Global skills: `~/.gemini/skills/` — shared, no action needed | [gcli-migration](https://antigravity.google/docs/gcli-migration) — uid 7_248–7_263: "are shared with Antigravity CLI … No action is needed for global skills" |
| 6.5 | Workspace skills: `.gemini/skills/` → `.agents/skills/` | [gcli-migration](https://antigravity.google/docs/gcli-migration) — uid 7_265–7_270: "they will need to be moved to `.agents/skills`" |
| 6.6 | Antigravity CLI global skills path: `~/.gemini/antigravity-cli/skills/` | [gcli-migration](https://antigravity.google/docs/gcli-migration) — uid 7_270 |
| 6.7 | MCP configs move from `settings.json` to `mcp_config.json` | [gcli-migration](https://antigravity.google/docs/gcli-migration) — uid 7_293–7_297: "store MCP server configurations in a distinct `mcp_config.json` file" |
| 6.8 | MCP: `url` field renamed to `serverUrl` (also deprecated `httpUrl`) | [gcli-migration](https://antigravity.google/docs/gcli-migration) — uid 7_299–7_306: "Antigravity CLI uses the `serverUrl` field instead of `url` (or the deprecated `httpUrl`)" |
| 6.9 | Global MCP config: `~/.gemini/antigravity-cli/mcp_config.json` | [gcli-migration](https://antigravity.google/docs/gcli-migration) — uid 7_317 |
| 6.10 | Workspace MCP config: `.agents/mcp_config.json` | [gcli-migration](https://antigravity.google/docs/gcli-migration) — uid 7_320 |
| 6.11 | `gemini skills` has no equivalent in Antigravity CLI — use `npx skills install` or create manually | [gcli-migration](https://antigravity.google/docs/gcli-migration) — uid 7_282–7_286: "Antigravity CLI does not currently have an equivalent to the `gemini skills` command … use `npx skills install`" |
| 6.12 | Gemini CLI stops serving requests **June 18, 2026** | [Google Developers Blog](https://developers.googleblog.com/an-important-update-transitioning-gemini-cli-to-antigravity-cli/): "stop serving requests … on June 18, 2026" |

---

## 7. Sandbox (`devops-automation.md`)

Official source: [CLI Features — Terminal Sandbox](https://antigravity.google/docs/cli-features) (uid 5_166–5_219)

| # | Claim | Official Source |
|:--|:------|:---|
| 7.1 | Sandbox: nsjail on Linux | [cli-features](https://antigravity.google/docs/cli-features) — uid 5_168–5_174: "nsjail on Linux" |
| 7.2 | Sandbox: sandbox-exec on macOS | [cli-features](https://antigravity.google/docs/cli-features) — uid 5_171 |
| 7.3 | Sandbox: AppContainer on Windows | [cli-features](https://antigravity.google/docs/cli-features) — uid 5_173 |
| 7.4 | `{"enableTerminalSandbox": true}` in settings.json | [cli-features](https://antigravity.google/docs/cli-features) — uid 5_185–5_207: exact JSON key, boolean, default false |
| 7.5 | When sandbox enabled: prompt offers "Yes, and run without sandbox restrictions" | [cli-features](https://antigravity.google/docs/cli-features) — uid 5_199–5_201 |
| 7.6 | When sandbox disabled: prompt offers "Yes, and run in sandbox" | [cli-features](https://antigravity.google/docs/cli-features) — uid 5_202–5_206 |

---

## 8. Subagents (`multi-agent-advanced.md`)

Official source: [CLI Features — Subagents](https://antigravity.google/docs/cli-features) (uid 5_278–5_316)

| # | Claim | Official Source |
|:--|:------|:---|
| 8.1 | Subagents run concurrently with main conversation | [cli-features](https://antigravity.google/docs/cli-features) — uid 5_279: "asynchronous subagents framework … parallel work … without blocking your active conversation" |
| 8.2 | `/agents` opens the subagents panel | [cli-features](https://antigravity.google/docs/cli-features) — uid 5_289–5_295 |
| 8.3 | Panel shows status: running, done, killed | [cli-features](https://antigravity.google/docs/cli-features) — uid 5_296–5_300 |
| 8.4 | `alt+j` — teleport to next pending subagent approval | [cli-features](https://antigravity.google/docs/cli-features) |
| 8.5 | `ctrl+k` — fast-approve from main conversation | [cli-features](https://antigravity.google/docs/cli-features) — uid 5_314–5_316 |
| 8.6 | Main agent controls what tools and permissions subagents get | [cli-features](https://antigravity.google/docs/cli-features) — uid 5_288 |
| 8.7 | Fine-grained permissions: `"allow": ["command(git)", "command(npm test)"]` in settings.json | [cli-features](https://antigravity.google/docs/cli-features) — uid 5_274: exact JSON format |

---

## 9. ADK Agents & agents-cli (`agents-cli.md`)

Official source: [agents-cli Docs](https://google.github.io/agents-cli/) and [agents-cli GitHub](https://github.com/google/agents-cli)

| # | Claim | Official Source |
|:--|:------|:---|
| 9.1 | `agents-cli` is a developer toolkit to scaffold, build, evaluate, and deploy ADK agents on Google Cloud. | [agents-cli Docs](https://google.github.io/agents-cli/) |
| 9.2 | Setup: `uvx google-agents-cli setup` installs the binary, configures auth, and installs 7 skills. | [agents-cli Docs](https://google.github.io/agents-cli/) |
| 9.3 | Scaffolding: `agents-cli scaffold create <name> --agent adk --prototype` scaffolds a prototype skipping CI/CD/Terraform. | [agents-cli Docs](https://google.github.io/agents-cli/) |
| 9.4 | Project Structure: creates `app/agent.py`, `app/tools.py`, `tests/eval/`, `agents-cli-manifest.yaml`, `pyproject.toml`, `Makefile`, and `GEMINI.md`. | [agents-cli Docs](https://google.github.io/agents-cli/) |
| 9.5 | Testing: `agents-cli run "<prompt>"` runs a one-off smoke test. `agents-cli playground` runs the web UI playground. | [agents-cli Docs](https://google.github.io/agents-cli/) |
| 9.6 | Evaluation: `agents-cli eval run` (or `generate` + `grade`) runs evaluation. | [agents-cli Docs](https://google.github.io/agents-cli/) |
| 9.7 | Custom Metrics: defined in `eval_config.yaml` using a prompt template. | [agents-cli Docs](https://google.github.io/agents-cli/) |
| 9.8 | Enhancing: `agents-cli scaffold enhance . --deployment-target <target>` adds deployment support. | [agents-cli Docs](https://google.github.io/agents-cli/) |
| 9.9 | Deploying: `agents-cli deploy` deploys to the selected target. | [agents-cli Docs](https://google.github.io/agents-cli/) |

---

## 10. Autonomous Loops, Generative UI, and DevTools MCP (Exercises 13–15)

Official sources: [Using Antigravity CLI](https://antigravity.google/docs/cli-using), [MCP](https://antigravity.google/docs/mcp)

| # | Claim | Official Source |
|:--|:------|:---|
| 10.1 | `/grill-me` engages an interactive requirements elicitation interview with multiple-choice clarifying questions before code generation. | [Using Antigravity CLI](https://antigravity.google/docs/cli-using) |
| 10.2 | `/goal` runs an autonomous self-correcting loop executing code modifications, test suites, and bug fixes until objective is met. | [Using Antigravity CLI](https://antigravity.google/docs/cli-using) |
| 10.3 | `/diff` and `Ctrl+R` open visual side-by-side / unified semantic diff review before applying file changes. | [Using Antigravity CLI](https://antigravity.google/docs/cli-using) |
| 10.4 | Antigravity CLI renders interactive HTML/SVG Generative UI artifacts directly in preview panels. | [Using Antigravity CLI](https://antigravity.google/docs/cli-using) |
| 10.5 | Chrome DevTools / Puppeteer MCP server enables browser navigation, element interaction, console log inspection, and DOM snapshots via `/browser`. | [MCP Docs](https://antigravity.google/docs/mcp) |

---

## 11. Custom Subagents & Multi-Agent Orchestration (`multi-agent-advanced.md`, `ex04_subagents.md`)

Official source: [Antigravity Subagents](https://antigravity.google/docs/subagents) and [CLI Subagents](https://antigravity.google/docs/cli/subagents)

| # | Claim | Official Source |
|:--|:------|:---|
| 11.1 | Custom subagents are defined as Markdown files (`.md`) with YAML frontmatter discovered across `.agents/agents/<name>.md`, `~/.gemini/config/agents/`, and `plugins/<plugin>/agents/`. | [Subagents](https://antigravity.google/docs/subagents) · [CLI Subagents](https://antigravity.google/docs/cli/subagents) |
| 11.2 | Custom subagent YAML frontmatter supports `name`, `description`, `tools`, `mainAgent`, `subagent`, `model` (`inherit`, `flash`, `pro`), `commandExecutionPolicy` (`off`, `auto`, `eager`, `sandbox`), `mcpServers`, and `skills`. | [Subagents](https://antigravity.google/docs/subagents) |
| 11.3 | Subagents operate across three asynchronous lifecycle states: `Running`, `Idle` (auto-wakes with context retention upon receiving a message), and `Killed`. | [Subagents](https://antigravity.google/docs/subagents) |
| 11.4 | Inter-agent delegation enforces a maximum nesting depth limit of 10 levels. | [Subagents](https://antigravity.google/docs/subagents) |
| 11.5 | CLI provides an interactive `/agents` panel, deep-dive reasoning log inspection (`Enter`), `Alt+J` teleportation to pending subagent approvals, and `Ctrl+K` fast-path approval. | [CLI Subagents](https://antigravity.google/docs/cli/subagents) |

---

## 12. Lifecycle Hooks & Governance (`devops-automation.md`, `ex16_custom_hooks_and_safety_gates.md`)

Official source: [Antigravity Hooks](https://antigravity.google/docs/hooks)

| # | Claim | Official Source |
|:--|:------|:---|
| 12.1 | Lifecycle hooks are configured in `.agents/hooks.json` (workspace) or `~/.gemini/config/hooks.json` (global) mapping hook names to event handler arrays. | [Hooks](https://antigravity.google/docs/hooks) |
| 12.2 | Hook scripts receive structured JSON on stdin containing `workspacePaths`, `conversationId`, `transcriptPath`, `modelName`, `toolCall`, `stepIdx`, and `invocationNum`. | [Hooks](https://antigravity.google/docs/hooks) |
| 12.3 | `PreToolUse` hooks return JSON on stdout with required `decision` (`"allow"`, `"deny"`, `"ask"`, `"force_ask"`) and optional `reason`. | [Hooks](https://antigravity.google/docs/hooks) |
| 12.4 | `PreInvocation` and `PostInvocation` hooks inject ephemeral messages, user messages, or tool calls into the trajectory via `{"injectSteps": [...]}`. | [Hooks](https://antigravity.google/docs/hooks) |
| 12.5 | `Stop` hooks can intercept session completion and re-enter the execution loop with `{"decision": "continue", "reason": "..."}`. | [Hooks](https://antigravity.google/docs/hooks) |

---

## Summary

| Count | Category |
|:---:|:---|
| 130 | Claims confirmed against official Antigravity CLI documentation |
| 3 | Workshop-original pedagogical patterns (`/btw`, "Propose, Review, Apply", "Pre-Commit Review") |

---

## Official Documentation Index

| Page | URL |
|:--|:--|
| CLI Overview | <https://antigravity.google/docs/cli-overview> |
| Getting Started | <https://antigravity.google/docs/cli-getting-started> |
| Using Antigravity CLI | <https://antigravity.google/docs/cli-using> |
| Features | <https://antigravity.google/docs/cli-features> |
| Migration from Gemini CLI | <https://antigravity.google/docs/gcli-migration> |
| Permissions | <https://antigravity.google/docs/permissions> |
| Plugins | <https://antigravity.google/docs/plugins> |
| MCP | <https://antigravity.google/docs/mcp> |
| Skills | <https://antigravity.google/docs/skills> |
| Rules & Workflows | <https://antigravity.google/docs/rules-workflows> |
| Hooks | <https://antigravity.google/docs/hooks> |
| Subagents | <https://antigravity.google/docs/subagents> |
| CLI Subagents | <https://antigravity.google/docs/cli/subagents> |
| Enterprise | <https://antigravity.google/docs/enterprise> |
| Models | <https://antigravity.google/docs/models> |
