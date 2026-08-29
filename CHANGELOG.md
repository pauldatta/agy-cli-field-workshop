# Changelog

Content-specific changes to workshop materials — CLI breakages, deprecated commands, and doc corrections. For general repo changes see the commit history.

---

## 2026-08-29

### ✅ Antigravity 2.11 / CLI v1.1.22 / SDK v0.1.15 Modernization Audit & Fixes

**Affects:** All documentation, exercises 02b, 07, 10, 11, AUDIT.md, research grounding data

- **SDK Runtime Fixes:**
  - Fixed `ToolResult.success` AttributeError in `docs/agy-sdk.md` (replaced with `tool_result.error is None`).
  - Fixed `HookResult` schema mismatch in `docs/agy-sdk.md` and `ex10_first_agent.md` (removed unsupported `message` parameter).
  - Fixed `WRITE_TOOLS` in `ex10_first_agent.md` to use SDK built-in constants `BuiltinTools.CREATE_FILE`, `BuiltinTools.EDIT_FILE`, `BuiltinTools.RUN_COMMAND`.
  - Fixed session persistence in `docs/agy-sdk.md` and `ex11_multi_agent_pipeline.md` by explicitly setting `save_dir` on initial `LocalAgentConfig`.
  - Updated SDK default model to `gemini-3.7-flash` (SDK v0.1.15 default) and image model to `gemini-3.1-flash-lite-image`.
- **CLI Keybinding & Command Alignments:**
  - Corrected subagent teleport shortcut from `ctrl+j` to `alt+j` across cheatsheet, Module 4, Module 1, and legacy modernization.
  - Added missing shortcuts: `ctrl+o` (trajectory toggle), `ctrl+r` (open review panel), `ctrl+v` (paste media), `f5` (voice dictation).
  - Added modern slash commands to Cheatsheet and Module 1: `/teamwork-preview`, `/diff`, `/btw`, `/goal`, `/grill-me`, `/schedule`, `/browser`, `/fast`, `/planning`, `/voice`, `/context`, `/credits`, `/hooks`, `/copy`, `/exit`.
- **Configuration & Path Normalizations:**
  - Normalized CLI state directories from `~/.gemini/antigravity/` to `~/.gemini/antigravity-cli/`.
  - Standardized `.agents/mcp.json` references to `.agents/mcp_config.json`.
  - Documented typed `settings.json` keys: `toolPermission`, `artifactReviewPolicy`, `altScreenMode`, `editorMode`, `vimInsertFirst`, `runningLightSpeed`, `allowNonWorkspaceAccess`, `enableTerminalSandbox`, `useG1Credits`.
- **Facilitator Guide Decoupling:**
  - Cleaned up crossover references in `docs/facilitator-guide.md` to cleanly separate Module 3 (`google-antigravity` SDK) from Module 5 (`google-adk` / `agents-cli`).
- **Ground Truth & Verification:**
  - Refreshed `AUDIT.md` (115 verified claims, 0 drift).
  - Validated all 93 code blocks and verified `scripts/precommit-checks.sh` and `scripts/detect-drift.sh --upstream`.

---

## 2026-06-09

### ✅ Exercise 12 — Eval Judge Model & Standalone Lab Guide

**Affects:** ex12, translations (ko, zh, id)

- Renamed "Vertex AI Eval Service" → "GenAI Evaluation Service" (Agent Platform branding)
- Clarified judge model config: built-in metrics use server-side autorater; custom metrics require fully-qualified resource paths
- Added standalone 90 min lab guide (`exercises/ex12_lab_guide_gdoc.md`, gitignored)
- Re-synced ko, zh, id translations

---

## 2026-06-07

### ✅ Module 5 Added — ADK Agents with agents-cli

**Affects:** All navigation (mkdocs.yml, README, facilitator guide, index), new module + exercise

The workshop is now a **5-module, ~7-hour curriculum**. Module 5 teaches the `agents-cli` lifecycle for building production ADK agents.

**New files:**

- `docs/agents-cli.md` — Module 5: Building ADK Agents with agents-cli (75 min)
- `exercises/ex12_agents_cli_lifecycle.md` — Exercise 12: Meeting Notes Summarizer agent (scaffold → build → eval → deploy)
- `docs/assets/agents-cli-hero.png` — Module 5 hero image (Nano Banana Pro 2)
- `docs/assets/banner.png` — Updated workshop banner with 5 modules (Nano Banana Pro 2)
- `docs/ko/agents-cli.md` — Korean translation
- `docs/zh/agents-cli.md` — Chinese (Simplified) translation
- `docs/id/agents-cli.md` — Indonesian translation

**Modified files:**

- `mkdocs.yml` — Added Module 5 and Exercise 12 to nav
- `README.md` — Updated to 5-module structure, fixed repo structure map, fixed delivery durations
- `docs/facilitator-guide.md` — Updated to 5-module, added Module 5 delivery notes, fixed Module 3 SDK references (`google-antigravity` not `google-adk`, removed `SequentialAgent`/`BaseAgent`)
- `docs/index.md` — Added Module 5 card, updated timeline, fixed Module 3 description

### ✅ Audit Remediation (audit-report-2026-06-07)

**Affects:** ex12, facilitator-guide, README

Fixed all critical and medium findings from the June 7 quality audit:

- **ex12 import mismatch** — Added `uv sync` step and note explaining `google-adk` ≠ `google-antigravity`
- **Facilitator guide Module 3** — Corrected SDK references, removed nonexistent `SequentialAgent`/`BaseAgent` classes
- **Duration contradictions** — Aligned delivery format tables across README, facilitator guide, and index
- **README repo structure** — Updated to reflect actual file layout (12 exercises, correct module mapping)

### 🧹 Cleanup

- Removed `tmp/` from git tracking (was accidentally committed)
- Added `tmp/` and `nanobanana-output/` to `.gitignore`

---

## 2026-05-25

### ✅ M09 — Migration Guide Added (Gemini CLI → AGY CLI)

**Affects:** All modules (cross-cutting), new M09 module, `mkdocs.yml` nav

The workshop now includes a dedicated migration guide for participants moving from Gemini CLI to Antigravity CLI.

**What was added:**

- `docs/migration-guide.md` — Full M09 module covering installation, plugin migration, MCP config migration, hook event name changes, and a decision framework
- Korean, Chinese (Simplified), and Indonesian translations via `gemini-3.1-pro-preview` on Vertex AI
- `mkdocs.yml` nav updated with `⚠️ Migration Guide: Gemini CLI → AGY CLI` under Resources
- Glossaries updated with AGY migration terminology (all three languages)

**Key migration differences documented:**

- `gemini` binary → `agy`
- `SessionStart` → `PreInvocation`, `BeforeTool` → `PreToolUse`, `AfterTool` → `PostToolUse`
- `settings.json` MCP block → standalone `mcp.json` with `serverUrl` (not `url`)
- `.gemini/` project dir → `.agents/` project dir
- `GEMINI.md` → `AGENTS.md`

---

### ✅ Workshop Quality Infrastructure Added

**Affects:** CI, scripts, samples, contributing workflow

Ported and AGY-adapted quality infrastructure from the gemini-cli-field-workshop reference:

**New files:**

- `scripts/validate-code-blocks.sh` — Validates JSON/YAML/bash code blocks in docs
- `scripts/detect-drift.sh` — Detects doc↔code drift, stale `gemini` binary refs, and stale Gemini CLI hook names
- `.github/workflows/workshop-structural.yml` — PR quality gate with AGY-specific checks
- `.github/ISSUE_TEMPLATE/bug_report.yml` — Bug report template
- `.github/ISSUE_TEMPLATE/content_improvement.yml` — Improvement suggestion template
- `.github/ISSUE_TEMPLATE/workshop_feedback.yml` — Post-session feedback template (includes migration context field)
- `CONTRIBUTING.md` — Full contributor guide with AGY-specific content guidelines

**New sample files:**

- `samples/configs/settings.json` — AGY settings with PreInvocation/PreToolUse/PostToolUse hooks
- `samples/configs/mcp.json` — Project MCP config (stdio + SSE, `serverUrl` format)
- `samples/configs/mcp_config.json` — Plugin-level MCP config
- `samples/agents/pr-reviewer.md` — Code review subagent
- `samples/agents/doc-writer.md` — Documentation generation subagent
- `samples/agents/security-scanner.md` — Security audit subagent
- `samples/agents/migration-validator.md` — AGY-specific migration validation subagent
- `samples/hooks/session-context.sh` — PreInvocation hook
- `samples/hooks/secret-scanner.sh` — PreToolUse hook
- `samples/hooks/git-context-injector.sh` — PreToolUse hook
- `samples/hooks/test-nudge.sh` — PostToolUse hook

---

## Unreleased

### Placeholders (pending post-Google I/O clarity)

| File | Section | Placeholder |
| :-- | :-- | :-- |
| `docs/setup.md` | Step 2: Authentication | Full auth flow documentation |
| `docs/plugin-ecosystem.md` | Section 2.3 | Plugin marketplace URL |
