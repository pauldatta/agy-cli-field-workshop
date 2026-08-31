#!/usr/bin/env python3
"""
tools/generate_scenarios.py — Generates all 22 TermReel declarative scenario manifests.
Reflects authentic, realistic, end-to-end curriculum instructions with clean workspace isolation,
real sample repository cloning (.NET ContosoUniversity, Java Spring PetClinic REST), real toolchains,
modal dismissals, and verification commands matching exercises/ and docs/.
"""

import os
import pathlib
import yaml

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
SCENARIOS = {}

# -------------------------------------------------------------
# Exercise 1: First Session
# -------------------------------------------------------------
SCENARIOS["ex01_first_session.yaml"] = {
    "version": "1.0",
    "metadata": {
        "title": "Antigravity CLI Field Workshop",
        "subtitle": "Exercise 1: First Session & AGENTS.md",
        "output": "video/ex01_first_session.mp4",
        "poster_output": "docs/assets/videos/ex01_poster.png",
        "resolution": [1280, 720],
        "fps": 25,
        "theme": "catppuccin-mocha",
        "statusbar_left": "Antigravity CLI | Ex 1: First Session",
        "statusbar_right": "TermReel HD"
    },
    "environment": {
        "auto_trust": True,
        "setup_commands": [
            "rm -rf /tmp/agy-session-lab && mkdir -p /tmp/agy-session-lab",
            "cp README.md mkdocs.yml /tmp/agy-session-lab/ 2>/dev/null || true",
            "cp -r docs exercises /tmp/agy-session-lab/ 2>/dev/null || true",
            "cd /tmp/agy-session-lab && git init && git add -A && git commit -m 'initial project workspace'"
        ]
    },
    "permissions": {"auto_approve": True},
    "triggers": [
        {"on_match": "Do you trust the contents of this project\\?|Yes, I trust", "action": "Enter", "once": True},
        {"on_match": "\\[y/N\\]|Apply changes\\?|Approve\\?", "action": {"type": "send_key", "value": "y", "delay_before": 0.5}, "once": False}
    ],
    "timeline": [
        {"show_card": {"tag": "Exercise 1", "title": "First Interactive Session (15 min)", "desc": "Explore codebase, test @ autocomplete, and generate AGENTS.md", "duration": 2.5}},
        {"show_card": {"tag": "Part 1", "title": "First Interactive Session", "desc": "Launch agy and explore workspace auto-indexing", "duration": 2.0}},
        {"launch": {"command": "bash"}},
        {"type": {"text": "cd /tmp/agy-session-lab && ls -la", "speed": 0.035, "send_key": "Enter"}},
        {"pause": 1.5},
        {"type": {"text": "agy --dangerously-skip-permissions -p \"What does this project do? Give me a one-paragraph summary.\" --print-timeout 60s", "speed": 0.035, "send_key": "Enter"}},
        {"wait_for_idle": {"timeout": 60.0, "reading_pause": 2.5}},
        {"type": {"text": "agy --dangerously-skip-permissions -p \"What are the top 3 files I should read to understand the core logic?\" --print-timeout 60s", "speed": 0.035, "send_key": "Enter"}},
        {"wait_for_idle": {"timeout": 60.0, "reading_pause": 2.5}},
        {"type": {"text": "agy --dangerously-skip-permissions -p \"@README.md How does the documented architecture match the actual codebase implementation?\" --print-timeout 60s", "speed": 0.035, "send_key": "Enter"}},
        {"wait_for_idle": {"timeout": 60.0, "reading_pause": 2.5}},
        {"show_card": {"tag": "Part 2", "title": "Deep Dive", "desc": "Inspect entry point and integration architecture", "duration": 2.0}},
        {"type": {"text": "agy --dangerously-skip-permissions -p \"Explain mkdocs.yml in detail. Walk me through navigation structure and theme settings.\" --print-timeout 60s", "speed": 0.035, "send_key": "Enter"}},
        {"wait_for_idle": {"timeout": 60.0, "reading_pause": 2.5}},
        {"show_card": {"tag": "Part 3", "title": "Create AGENTS.md", "desc": "Generate persistent project context and quality rules", "duration": 2.0}},
        {"type": {"text": "agy --dangerously-skip-permissions -p \"Based on our conversation, generate an AGENTS.md file for this project. Include: project purpose, tech stack, key conventions, and testing commands.\" --print-timeout 90s > AGENTS.md", "speed": 0.035, "send_key": "Enter"}},
        {"wait_for_idle": {"timeout": 90.0, "reading_pause": 2.0}},
        {"type": {"text": "cat AGENTS.md | head -25", "speed": 0.035, "send_key": "Enter"}},
        {"pause": 2.5},
        {"show_card": {"tag": "Verification", "title": "Headless Session Test", "desc": "Verify AGENTS.md auto-loading with --print", "duration": 2.0}},
        {"type": {"text": "agy --dangerously-skip-permissions --print \"What do you know about this project from AGENTS.md?\" --print-timeout 90s", "speed": 0.035, "send_key": "Enter"}},
        {"wait_for_idle": {"timeout": 90.0, "reading_pause": 3.0}},
        {"show_card": {"tag": "Complete", "title": "Exercise 1 Verified", "desc": "Interactive session, context inspection, and AGENTS.md established", "duration": 2.5}}
    ]
}

# -------------------------------------------------------------
# Exercise 2: Plugin Bridge
# -------------------------------------------------------------
SCENARIOS["ex02_plugin_bridge.yaml"] = {
    "version": "1.0",
    "metadata": {
        "title": "Antigravity CLI Field Workshop",
        "subtitle": "Exercise 2: Plugin Bridge",
        "output": "video/ex02_plugin_bridge.mp4",
        "poster_output": "docs/assets/videos/ex02_poster.png",
        "resolution": [1280, 720],
        "fps": 25,
        "theme": "catppuccin-mocha",
        "statusbar_left": "Antigravity CLI | Ex 2: Plugin Bridge",
        "statusbar_right": "TermReel HD"
    },
    "environment": {
        "auto_trust": True,
        "setup_commands": [
            "rm -rf ~/.gemini/antigravity-cli/plugins/workshop-helpers"
        ]
    },
    "permissions": {"auto_approve": True},
    "triggers": [
        {"on_match": "Do you trust the contents of this project\\?|Yes, I trust", "action": "Enter", "once": True}
    ],
    "timeline": [
        {"show_card": {"tag": "Exercise 2", "title": "Plugin Bridge (20 min)", "desc": "Import plugin library, install custom plugins, and validate manifests", "duration": 2.5}},
        {"show_card": {"tag": "Part 1", "title": "Import & List Plugins", "desc": "Inspect active components and install sample plugin", "duration": 2.0}},
        {"launch": {"command": "bash"}},
        {"type": {"text": "agy plugin list", "speed": 0.035, "send_key": "Enter"}},
        {"wait_for_idle": {"timeout": 15.0, "reading_pause": 2.0}},
        {"type": {"text": "agy plugin install ./samples/plugins/workshop-helpers/", "speed": 0.035, "send_key": "Enter"}},
        {"wait_for_idle": {"timeout": 20.0, "reading_pause": 2.5}},
        {"type": {"text": "agy plugin list | python3 -m json.tool", "speed": 0.035, "send_key": "Enter"}},
        {"wait_for_idle": {"timeout": 15.0, "reading_pause": 2.0}},
        {"show_card": {"tag": "Part 2", "title": "Test Plugin in Session", "desc": "Query custom skills from installed plugins", "duration": 2.0}},
        {"type": {"text": "agy --dangerously-skip-permissions -p \"What custom skills or helper commands are available from my installed plugins?\" --print-timeout 40s", "speed": 0.035, "send_key": "Enter"}},
        {"wait_for_idle": {"timeout": 45.0, "reading_pause": 2.5}},
        {"show_card": {"tag": "Part 3 & 4", "title": "Validate Plugin Schema & Lifecycle", "desc": "Verify plugin.json manifest and disable/enable lifecycle", "duration": 2.0}},
        {"type": {"text": "agy plugin disable workshop-helpers", "speed": 0.035, "send_key": "Enter"}},
        {"wait_for_idle": {"timeout": 15.0, "reading_pause": 2.0}},
        {"type": {"text": "agy plugin list | python3 -m json.tool", "speed": 0.035, "send_key": "Enter"}},
        {"wait_for_idle": {"timeout": 15.0, "reading_pause": 2.0}},
        {"type": {"text": "agy plugin enable workshop-helpers", "speed": 0.035, "send_key": "Enter"}},
        {"wait_for_idle": {"timeout": 15.0, "reading_pause": 2.0}},
        {"type": {"text": "agy plugin validate samples/plugins/workshop-helpers/", "speed": 0.035, "send_key": "Enter"}},
        {"wait_for_idle": {"timeout": 15.0, "reading_pause": 2.5}},
        {"show_card": {"tag": "Complete", "title": "Exercise 2 Verified", "desc": "Plugin import, runtime query, and schema validation confirmed", "duration": 2.5}}
    ]
}

# -------------------------------------------------------------
# Exercise 2B: Your First Sidecar
# -------------------------------------------------------------
SCENARIOS["ex02b_first_sidecar.yaml"] = {
    "version": "1.0",
    "metadata": {
        "title": "Antigravity CLI Field Workshop",
        "subtitle": "Exercise 2B: Your First Sidecar",
        "output": "video/ex02b_first_sidecar.mp4",
        "poster_output": "docs/assets/videos/ex02b_poster.png",
        "resolution": [1280, 720],
        "fps": 25,
        "theme": "catppuccin-mocha",
        "statusbar_left": "Antigravity CLI | Ex 2B: First Sidecar",
        "statusbar_right": "TermReel HD"
    },
    "environment": {
        "auto_trust": True,
        "setup_commands": [
            "mkdir -p ~/.gemini/config/sidecars/standup ~/.gemini/antigravity-cli/sidecar_data/standup/logs ~/.gemini/antigravity-cli/sidecar_data/standup/data"
        ]
    },
    "permissions": {"auto_approve": True},
    "triggers": [
        {"on_match": "Do you trust the contents of this project\\?|Yes, I trust", "action": "Enter", "once": True}
    ],
    "timeline": [
        {"show_card": {"tag": "Exercise 2B", "title": "Your First Sidecar (20 min)", "desc": "Configure scheduled background sidecars and inspect runtime logs", "duration": 2.5}},
        {"show_card": {"tag": "Part 1 & 2", "title": "Create & Enable Sidecar Config", "desc": "Define daily standup schedule in ~/.gemini/config/sidecars/", "duration": 2.0}},
        {"launch": {"command": "bash"}},
        {"type": {"text": "mkdir -p ~/.gemini/config/sidecars/standup", "speed": 0.035, "send_key": "Enter"}},
        {"pause": 1.5},
        {"type": {"text": "cat << 'EOF' > ~/.gemini/config/sidecars/standup/sidecar.json\n{\n  \"description\": \"Daily standup — summarises yesterday's git commits\",\n  \"builtin\": \"schedule\",\n  \"args\": [\n    \"0 9 * * 1-5\",\n    \"agentapi\",\n    \"new-conversation\",\n    \"Summarise all git commits from yesterday across my repos. Group by repo, list the most impactful changes first, and flag any commits that touch security-sensitive files.\"\n  ]\n}\nEOF", "speed": 0.03, "send_key": "Enter"}},
        {"pause": 1.5},
        {"type": {"text": "cat << 'EOF' > ~/.gemini/config/config.json\n{\n  \"sidecars\": {\n    \"standup\": {\n      \"enabled\": true\n    }\n  }\n}\nEOF", "speed": 0.03, "send_key": "Enter"}},
        {"pause": 1.5},
        {"type": {"text": "cat ~/.gemini/config/sidecars/standup/sidecar.json", "speed": 0.035, "send_key": "Enter"}},
        {"pause": 2.0},
        {"show_card": {"tag": "Part 3", "title": "Verify Sidecar Discovery in agy", "desc": "Query active background sidecars and schedules", "duration": 2.0}},
        {"type": {"text": "agy --dangerously-skip-permissions -p \"What sidecars are currently configured? Is the standup sidecar active?\" --print-timeout 40s", "speed": 0.035, "send_key": "Enter"}},
        {"wait_for_idle": {"timeout": 45.0, "reading_pause": 2.5}},
        {"show_card": {"tag": "Part 4", "title": "Inspect Sidecar Runtime Layout", "desc": "Verify data and log directory structure", "duration": 2.0}},
        {"type": {"text": "ls -la ~/.gemini/antigravity-cli/sidecar_data/standup/", "speed": 0.035, "send_key": "Enter"}},
        {"pause": 2.5},
        {"show_card": {"tag": "Complete", "title": "Exercise 2B Verified", "desc": "Sidecar daemon configuration and scheduling verified", "duration": 2.5}}
    ]
}

# -------------------------------------------------------------
# Exercise 3: --print Mode Pipeline
# -------------------------------------------------------------
SCENARIOS["ex03_print_mode_pipeline.yaml"] = {
    "version": "1.0",
    "metadata": {
        "title": "Antigravity CLI Field Workshop",
        "subtitle": "Exercise 3: --print Mode Pipeline",
        "output": "video/ex03_print_mode_pipeline.mp4",
        "poster_output": "docs/assets/videos/ex03_poster.png",
        "resolution": [1280, 720],
        "fps": 25,
        "theme": "catppuccin-mocha",
        "statusbar_left": "Antigravity CLI | Ex 3: Print Pipeline",
        "statusbar_right": "TermReel HD"
    },
    "environment": {
        "auto_trust": True,
        "setup_commands": [
            "mkdir -p docs/assets",
            "echo '// TODO: refactor error handling middleware in routes' >> docs/assets/test_edit.js",
            "git add docs/assets/test_edit.js 2>/dev/null || true"
        ],
        "cleanup_commands": [
            "git reset HEAD docs/assets/test_edit.js 2>/dev/null || true",
            "rm -f docs/assets/test_edit.js docs/api-generated.yaml .github/workflows/agy-review.yml"
        ]
    },
    "permissions": {"auto_approve": True},
    "triggers": [
        {"on_match": "Do you trust the contents of this project\\?|Yes, I trust", "action": "Enter", "once": True}
    ],
    "timeline": [
        {"show_card": {"tag": "Exercise 3", "title": "--print Mode Pipeline (20 min)", "desc": "Build headless shell pipelines with stdin/stdout streaming", "duration": 2.5}},
        {"show_card": {"tag": "Part 1", "title": "Review Staged Changes with Git Diff", "desc": "Pipe git diff --cached directly into agy --print", "duration": 2.0}},
        {"launch": {"command": "bash"}},
        {"type": {"text": "git status --short", "speed": 0.035, "send_key": "Enter"}},
        {"pause": 2.0},
        {"type": {"text": "git diff --cached | agy --dangerously-skip-permissions -p \"Review these staged changes. Flag any issues. Output as markdown.\" --print-timeout 45s", "speed": 0.035, "send_key": "Enter"}},
        {"wait_for_idle": {"timeout": 45.0, "reading_pause": 3.0}},
        {"show_card": {"tag": "Part 2", "title": "Generate API Documentation", "desc": "Pipe source/manifest into agy to produce OpenAPI YAML", "duration": 2.0}},
        {"type": {"text": "cat samples/plugins/workshop-helpers/plugin.json | agy --dangerously-skip-permissions -p \"Generate OpenAPI-style documentation for this plugin manifest. Output as YAML.\" --print-timeout 45s > docs/api-generated.yaml", "speed": 0.035, "send_key": "Enter"}},
        {"wait_for_idle": {"timeout": 45.0, "reading_pause": 2.5}},
        {"type": {"text": "cat docs/api-generated.yaml | head -20", "speed": 0.035, "send_key": "Enter"}},
        {"pause": 2.5},
        {"show_card": {"tag": "Part 3 & 4", "title": "Multi-Directory Analysis & CI/CD", "desc": "Cross-folder analysis and automated GitHub Actions workflow generation", "duration": 2.0}},
        {"type": {"text": "agy --dangerously-skip-permissions --add-dir ./exercises --add-dir ./docs -p \"Compare exercise guides with docs structure. Which sections are fully mapped? Output a table.\" --print-timeout 45s", "speed": 0.035, "send_key": "Enter"}},
        {"wait_for_idle": {"timeout": 45.0, "reading_pause": 3.0}},
        {"type": {"text": "agy --dangerously-skip-permissions -p \"Write a GitHub Actions workflow that: (1) checks out the repo, (2) runs agy in print mode to review changed files with --dangerously-skip-permissions, (3) posts the review as a PR comment. Output as complete YAML.\" --print-timeout 45s > .github/workflows/agy-review.yml", "speed": 0.035, "send_key": "Enter"}},
        {"wait_for_idle": {"timeout": 45.0, "reading_pause": 3.0}},
        {"type": {"text": "cat .github/workflows/agy-review.yml | head -25", "speed": 0.035, "send_key": "Enter"}},
        {"pause": 2.5},
        {"show_card": {"tag": "Complete", "title": "Exercise 3 Verified", "desc": "Headless --print automation pipeline established", "duration": 2.5}}
    ]
}

# -------------------------------------------------------------
# Exercise 4: Built-In & Custom Subagents
# -------------------------------------------------------------
SCENARIOS["ex04_subagents.yaml"] = {
    "version": "1.0",
    "metadata": {
        "title": "Antigravity CLI Field Workshop",
        "subtitle": "Exercise 4: Built-In & Custom Subagents",
        "output": "video/ex04_subagents.mp4",
        "poster_output": "docs/assets/videos/ex04_poster.png",
        "resolution": [1280, 720],
        "fps": 25,
        "theme": "catppuccin-mocha",
        "statusbar_left": "Antigravity CLI | Ex 4: Subagents",
        "statusbar_right": "TermReel HD"
    },
    "environment": {
        "auto_trust": True,
        "setup_commands": [
            "rm -rf /tmp/subagent-demo && mkdir -p /tmp/subagent-demo/.agents/agents",
            "cd /tmp/subagent-demo && git init && git commit --allow-empty -m 'initial'"
        ]
    },
    "permissions": {"auto_approve": True},
    "triggers": [
        {"on_match": "Do you trust the contents of this project\\?|Yes, I trust", "action": "Enter", "once": True}
    ],
    "timeline": [
        {"show_card": {"tag": "Exercise 4", "title": "Built-In & Custom Subagents (25 min)", "desc": "Parallel delegation, custom agents in .agents/agents/, and teamwork orchestration", "duration": 2.5}},
        {"show_card": {"tag": "Part 1", "title": "Dispatch Parallel Subagents", "desc": "Spawn security and coverage auditors in branch workspace mode", "duration": 2.0}},
        {"launch": {"command": "bash"}},
        {"type": {"text": "cd /tmp/subagent-demo && ls -la", "speed": 0.035, "send_key": "Enter"}},
        {"pause": 1.5},
        {"type": {"text": "agy --dangerously-skip-permissions -p \"Spawn two subagents in parallel using branch workspace mode: 1. A security auditor — scan for hardcoded credentials, injection vulnerabilities, and exposed sensitive data 2. A test coverage auditor — identify untested functions and integration test gaps. Report back when both complete with a combined findings summary.\" --print-timeout 90s", "speed": 0.035, "send_key": "Enter"}},
        {"wait_for_idle": {"timeout": 90.0, "reading_pause": 2.5}},
        {"show_card": {"tag": "Part 2", "title": "Define Custom Subagent (.agents/agents/)", "desc": "Define security-auditor with YAML frontmatter and strict tools", "duration": 2.0}},
        {"type": {"text": "mkdir -p .agents/agents", "speed": 0.035, "send_key": "Enter"}},
        {"pause": 1.0},
        {"type": {"text": "cat << 'EOF' > .agents/agents/security-auditor.md\n---\nname: security-auditor\ndescription: Specialized subagent for security audits, OWASP Top 10 scanning, and vulnerability reviews.\ntools:\n  - view_file\n  - grep_search\n  - find_by_name\n  - run_command\nmainAgent: false\nsubagent: true\nmodel: pro\ncommandExecutionPolicy: sandbox\n---\n\n# System Prompt\nYou are a principal security engineer conducting a deep source code audit.\n\n# Review Guidelines\n1. Systematically check for SQL injection, unescaped user input (XSS), missing authorization middleware, and hardcoded secrets.\n2. For every finding, provide: Severity, File path, Line number, Problem explanation, and concrete remediation code.\nEOF", "speed": 0.03, "send_key": "Enter"}},
        {"pause": 1.5},
        {"type": {"text": "cat .agents/agents/security-auditor.md | head -20", "speed": 0.035, "send_key": "Enter"}},
        {"pause": 2.0},
        {"show_card": {"tag": "Part 3 & 4", "title": "Custom Subagent & Teamwork", "desc": "Delegate to specialist agent and preview teamwork orchestration", "duration": 2.0}},
        {"type": {"text": "cat .agents/agents/security-auditor.md", "speed": 0.035, "send_key": "Enter"}},
        {"pause": 1.5},
        {"type": {"text": "agy", "speed": 0.035, "send_key": "Enter"}},
        {"wait_for_idle": {"timeout": 20.0, "reading_pause": 2.0}},
        {"type": {"text": "/agents", "speed": 0.035, "send_key": "Enter"}},
        {"pause": 2.0},
        {"send_key": {"key": "Escape", "pause": 1.0}},
        {"type": {"text": "/exit", "speed": 0.035, "send_key": "Enter"}},
        {"pause": 1.5},
        {"type": {"text": "agy --dangerously-skip-permissions --agent security-auditor -p \"Delegate a security review of our source code to the security-auditor subagent.\" --print-timeout 90s", "speed": 0.035, "send_key": "Enter"}},
        {"wait_for_idle": {"timeout": 90.0, "reading_pause": 2.5}},
        {"type": {"text": "agy --dangerously-skip-permissions -p \"Coordinate a team to refactor our database query layer to use prepared statements across all controllers and verify with unit tests.\" --print-timeout 90s", "speed": 0.035, "send_key": "Enter"}},
        {"wait_for_idle": {"timeout": 90.0, "reading_pause": 2.5}},
        {"show_card": {"tag": "Complete", "title": "Exercise 4 Verified", "desc": "Parallel subagent orchestration and custom agents verified", "duration": 2.5}}
    ]
}

# -------------------------------------------------------------
# Exercise 5: /btw Steering & Scheduling
# -------------------------------------------------------------
SCENARIOS["ex05_btw_scheduling.yaml"] = {
    "version": "1.0",
    "metadata": {
        "title": "Antigravity CLI Field Workshop",
        "subtitle": "Exercise 5: /btw Steering & Scheduling",
        "output": "video/ex05_btw_scheduling.mp4",
        "poster_output": "docs/assets/videos/ex05_poster.png",
        "resolution": [1280, 720],
        "fps": 25,
        "theme": "catppuccin-mocha",
        "statusbar_left": "Antigravity CLI | Ex 5: /btw Steering",
        "statusbar_right": "TermReel HD"
    },
    "environment": {"auto_trust": True},
    "permissions": {"auto_approve": True},
    "triggers": [
        {"on_match": "Do you trust the contents of this project\\?|Yes, I trust", "action": "Enter", "once": True}
    ],
    "timeline": [
        {"show_card": {"tag": "Exercise 5", "title": "/btw Steering & Scheduling (20 min)", "desc": "Inject side queries without derailing tasks, and schedule cron jobs", "duration": 2.5}},
        {"show_card": {"tag": "Part 1", "title": "Mid-Task Steering with /btw", "desc": "Inject real-time constraints during active model generation", "duration": 2.0}},
        {"launch": {"command": "bash"}},
        {"type": {"text": "agy", "speed": 0.035, "send_key": "Enter"}},
        {"wait_for_idle": {"timeout": 20.0, "reading_pause": 2.0}},
        {"type": {"text": "I want to refactor the error handling across this entire project to use a consistent pattern. Start by analyzing all error handling in the codebase, then propose and implement a unified approach. This will touch multiple files — start with the analysis phase.", "speed": 0.035, "send_key": "Enter"}},
        {"wait_for_idle": {"timeout": 40.0, "reading_pause": 2.5}},
        {"type": {"text": "/btw Only touch files in the backend/ directory for now. Leave frontend untouched.", "speed": 0.035, "send_key": "Enter"}},
        {"wait_for_idle": {"timeout": 35.0, "reading_pause": 2.0}},
        {"type": {"text": "/btw Use the Result<T, E> pattern if the language supports it. Otherwise use a custom Error class hierarchy.", "speed": 0.035, "send_key": "Enter"}},
        {"wait_for_idle": {"timeout": 35.0, "reading_pause": 2.0}},
        {"type": {"text": "/exit", "speed": 0.03, "send_key": "Enter", "pause": 1.5}},
        {"show_card": {"tag": "Part 2", "title": "Session Continuation with agy -c", "desc": "Resume conversation context using --continue flag", "duration": 2.0}},
        {"type": {"text": "agy --dangerously-skip-permissions -c --print \"Remind me what we decided about the error handling refactor. What was the approach?\" --print-timeout 35s", "speed": 0.035, "send_key": "Enter"}},
        {"wait_for_idle": {"timeout": 35.0, "reading_pause": 3.0}},
        {"show_card": {"tag": "Part 3", "title": "Schedule Recurring Background Report", "desc": "Configure periodic dependency checks with cron syntax", "duration": 2.0}},
        {"type": {"text": "agy --dangerously-skip-permissions -p \"Schedule a daily dependency check every weekday morning at 8am. It should: 1. Check for outdated dependencies with security advisories 2. List any new CVEs affecting our current dependency versions 3. Save the report to reports/deps-YYYY-MM-DD.md. Create the reports/ directory if it doesn't exist.\" --print-timeout 40s", "speed": 0.035, "send_key": "Enter"}},
        {"wait_for_idle": {"timeout": 40.0, "reading_pause": 2.5}},
        {"type": {"text": "agy --dangerously-skip-permissions -p \"What scheduled tasks are currently active?\" --print-timeout 30s", "speed": 0.035, "send_key": "Enter"}},
        {"wait_for_idle": {"timeout": 30.0, "reading_pause": 2.0}},
        {"show_card": {"tag": "Complete", "title": "Exercise 5 Verified", "desc": "Session continuity, /btw steering, and scheduled tasks confirmed", "duration": 2.5}}
    ]
}

# -------------------------------------------------------------
# Exercise 6: Sandbox Governance
# -------------------------------------------------------------
SCENARIOS["ex06_sandbox_governance.yaml"] = {
    "version": "1.0",
    "metadata": {
        "title": "Antigravity CLI Field Workshop",
        "subtitle": "Exercise 6: Sandbox & Governance",
        "output": "video/ex06_sandbox_governance.mp4",
        "poster_output": "docs/assets/videos/ex06_poster.png",
        "resolution": [1280, 720],
        "fps": 25,
        "theme": "catppuccin-mocha",
        "statusbar_left": "Antigravity CLI | Ex 6: Sandbox & Governance",
        "statusbar_right": "TermReel HD"
    },
    "environment": {
        "auto_trust": True,
        "setup_commands": [
            "rm -rf /tmp/agy-sandbox-lab && mkdir -p /tmp/agy-sandbox-lab/src",
            "cat << 'EOF' > /tmp/agy-sandbox-lab/src/app.py\nimport os\n\nDB_URL = os.getenv('DATABASE_URL', 'postgres://admin:secret123@localhost:5432/app')\n\ndef get_user(db, user_id):\n    # TODO: Add input sanitization and parameterized queries\n    query = f'SELECT * FROM users WHERE id = {user_id}'\n    return db.execute(query)\nEOF",
            "cd /tmp/agy-sandbox-lab && git init && git add -A && git commit -m 'initial sandbox lab'"
        ]
    },
    "permissions": {"auto_approve": True},
    "triggers": [
        {"on_match": "Do you trust the contents of this project\\?|Yes, I trust", "action": "Enter", "once": True}
    ],
    "timeline": [
        {"show_card": {"tag": "Exercise 6", "title": "Sandbox & Governance (15 min)", "desc": "Read-only audits with --sandbox and enterprise two-phase workflows", "duration": 2.5}},
        {"show_card": {"tag": "Part 1", "title": "Sandbox Mode Safe Audit", "desc": "Execute restricted read-only analysis without shell side effects", "duration": 2.0}},
        {"launch": {"command": "bash"}},
        {"pause": 1.0},
        {"type": {"text": "cd /tmp/agy-sandbox-lab && ls -la src/", "speed": 0.035, "send_key": "Enter"}},
        {"pause": 1.5},
        {"type": {"text": "agy --sandbox --dangerously-skip-permissions -p \"Review src/app.py for security vulnerabilities: check for hardcoded credentials and SQL injection.\" --print-timeout 45s", "speed": 0.035, "send_key": "Enter"}},
        {"wait_for_idle": {"timeout": 45.0, "reading_pause": 2.5}},
        {"show_card": {"tag": "Part 2", "title": "Auto-Approve with Sandbox Gating", "desc": "Combine --dangerously-skip-permissions with sandbox gating", "duration": 2.0}},
        {"type": {"text": "agy --sandbox --dangerously-skip-permissions -p \"List all TODO comments in src/app.py and generate a prioritized remediation backlog.\" --print-timeout 45s", "speed": 0.035, "send_key": "Enter"}},
        {"wait_for_idle": {"timeout": 45.0, "reading_pause": 2.5}},
        {"show_card": {"tag": "Part 3", "title": "Two-Phase Governance Workflow", "desc": "Phase 1 safe analysis followed by human-approved remediation", "duration": 2.0}},
        {"type": {"text": "agy --dangerously-skip-permissions -p \"Propose parameterized query fixes for src/app.py to eliminate the SQL injection flaw with diffs.\" --print-timeout 45s", "speed": 0.035, "send_key": "Enter"}},
        {"wait_for_idle": {"timeout": 45.0, "reading_pause": 2.5}},
        {"show_card": {"tag": "Complete", "title": "Exercise 6 Verified", "desc": "Sandbox execution and governance guardrails verified", "duration": 2.5}}
    ]
}

# -------------------------------------------------------------
# Exercise 7: Migration Walkthrough
# -------------------------------------------------------------
SCENARIOS["ex07_migration_walkthrough.yaml"] = {
    "version": "1.0",
    "metadata": {
        "title": "Antigravity CLI Field Workshop",
        "subtitle": "Exercise 7: Migration Walkthrough",
        "output": "video/ex07_migration_walkthrough.mp4",
        "poster_output": "docs/assets/videos/ex07_poster.png",
        "resolution": [1280, 720],
        "fps": 25,
        "theme": "catppuccin-mocha",
        "statusbar_left": "Antigravity CLI | Ex 7: Migration Guide",
        "statusbar_right": "TermReel HD"
    },
    "environment": {
        "auto_trust": True,
        "setup_commands": [
            "rm -rf /tmp/gemini-migration-lab && mkdir -p /tmp/gemini-migration-lab/.gemini/hooks /tmp/gemini-migration-lab/scripts /tmp/gemini-migration-lab/.github/workflows",
            "cat << 'EOF' > /tmp/gemini-migration-lab/.gemini/settings.json\n{\n  \"mcpServers\": {\n    \"github\": {\n      \"command\": \"npx\",\n      \"args\": [\"-y\", \"github-mcp-server\"],\n      \"env\": { \"GITHUB_PERSONAL_ACCESS_TOKEN\": \"$GITHUB_TOKEN\" }\n    }\n  },\n  \"hooks\": {\n    \"SessionStart\": [\n      {\n        \"hooks\": [{\n          \"name\": \"session-context\",\n          \"type\": \"command\",\n          \"command\": \"$GEMINI_PROJECT_DIR/.gemini/hooks/session-context.sh\",\n          \"timeout\": 3000\n        }]\n      }\n    ],\n    \"BeforeTool\": [\n      {\n        \"matcher\": \"write_file|replace_in_file\",\n        \"hooks\": [{\n          \"name\": \"secret-scanner\",\n          \"type\": \"command\",\n          \"command\": \"$GEMINI_PROJECT_DIR/.gemini/hooks/secret-scanner.sh\",\n          \"timeout\": 2000\n        }]\n      }\n    ]\n  }\n}\nEOF",
            "cat << 'EOF' > /tmp/gemini-migration-lab/.gemini/GEMINI.md\n# Project Context\n\nThis is a Node.js API service. Always run npm test after changes.\nUse gemini for code reviews before merging PRs.\nEOF",
            "cat << 'EOF' > /tmp/gemini-migration-lab/scripts/review.sh\n#!/usr/bin/env bash\ngemini -p \"Review the diff: $(git diff HEAD~1 2>/dev/null || echo 'initial commit')\" > review.md\nEOF",
            "chmod +x /tmp/gemini-migration-lab/scripts/review.sh",
            "cd /tmp/gemini-migration-lab && git init && git add -A && git commit -m 'initial legacy gemini cli app'"
        ]
    },
    "permissions": {"auto_approve": True},
    "triggers": [
        {"on_match": "Do you trust the contents of this project\\?|Yes, I trust", "action": "Enter", "once": True}
    ],
    "timeline": [
        {"show_card": {"tag": "Exercise 7", "title": "Migration Walkthrough (20 min)", "desc": "Migrate Gemini CLI projects to Antigravity CLI standards", "duration": 2.5}},
        {"show_card": {"tag": "Part 1", "title": "Inspect Legacy Project Layout", "desc": "Examine .gemini/ directory, settings.json, and legacy hook definitions", "duration": 2.0}},
        {"launch": {"command": "bash"}},
        {"type": {"text": "cd /tmp/gemini-migration-lab && ls -la .gemini/", "speed": 0.035, "send_key": "Enter"}},
        {"pause": 2.0},
        {"type": {"text": "cat .gemini/settings.json", "speed": 0.035, "send_key": "Enter"}},
        {"pause": 2.5},
        {"show_card": {"tag": "Part 2", "title": "Migrate Config to .agents/ Standards", "desc": "Move to AGENTS.md, mcp_config.json, and hooks.json lifecycle contracts", "duration": 2.0}},
        {"type": {"text": "mkdir -p .agents/hooks", "speed": 0.035, "send_key": "Enter"}},
        {"pause": 1.0},
        {"type": {"text": "cp .gemini/GEMINI.md .agents/AGENTS.md", "speed": 0.035, "send_key": "Enter"}},
        {"pause": 1.0},
        {"type": {"text": "cat << 'EOF' > .agents/mcp_config.json\n{\n  \"mcpServers\": {\n    \"github\": {\n      \"type\": \"stdio\",\n      \"command\": \"npx\",\n      \"args\": [\"-y\", \"github-mcp-server\"],\n      \"env\": { \"GITHUB_PERSONAL_ACCESS_TOKEN\": \"$GITHUB_TOKEN\" }\n    }\n  }\n}\nEOF", "speed": 0.03, "send_key": "Enter"}},
        {"pause": 1.5},
        {"type": {"text": "cat << 'EOF' > .agents/hooks.json\n{\n  \"session-context\": {\n    \"PreInvocation\": [\n      {\n        \"type\": \"command\",\n        \"command\": \"$AGY_PROJECT_DIR/.agents/hooks/session-context.sh\",\n        \"timeout\": 5\n      }\n    ]\n  },\n  \"secret-scanner\": {\n    \"PreToolUse\": [\n      {\n        \"matcher\": \"write_to_file|replace_file_content\",\n        \"hooks\": [\n          {\n            \"type\": \"command\",\n            \"command\": \"$AGY_PROJECT_DIR/.agents/hooks/secret-scanner.sh\",\n            \"timeout\": 5\n          }\n        ]\n      }\n    ]\n  }\n}\nEOF", "speed": 0.03, "send_key": "Enter"}},
        {"pause": 1.5},
        {"type": {"text": "sed -i 's/gemini -p/agy -p/g' scripts/review.sh", "speed": 0.035, "send_key": "Enter"}},
        {"pause": 1.5},
        {"type": {"text": "cat scripts/review.sh", "speed": 0.035, "send_key": "Enter"}},
        {"pause": 2.0},
        {"show_card": {"tag": "Part 3", "title": "Verify Migrated Workspace in agy", "desc": "Launch session and confirm AGENTS.md auto-loading and active hooks", "duration": 2.0}},
        {"type": {"text": "agy --dangerously-skip-permissions -p \"Verify our migrated configuration: summarize .agents/AGENTS.md, active hooks in .agents/hooks.json, and MCP servers in .agents/mcp_config.json.\" --print-timeout 90s", "speed": 0.035, "send_key": "Enter"}},
        {"wait_for_idle": {"timeout": 90.0, "reading_pause": 2.5}},
        {"show_card": {"tag": "Complete", "title": "Exercise 7 Verified", "desc": "Project migration rules and schema mappings confirmed", "duration": 2.5}}
    ]
}

# -------------------------------------------------------------
# Exercise 8: .NET Modernization (Pure Interactive TUI Mode)
# -------------------------------------------------------------
SCENARIOS["ex08_dotnet_modernization.yaml"] = {
    "version": "1.0",
    "metadata": {
        "title": "Antigravity CLI Field Workshop",
        "subtitle": "Exercise 8: .NET 5 to .NET 8 Cloud-Native Migration",
        "output": "video/ex08_dotnet_modernization.mp4",
        "poster_output": "docs/assets/videos/ex08_poster.png",
        "resolution": [1280, 720],
        "fps": 25,
        "theme": "catppuccin-mocha",
        "statusbar_left": "Antigravity CLI | Ex 8: .NET Modernization",
        "statusbar_right": "TermReel HD"
    },
    "environment": {
        "auto_trust": True,
        "setup_commands": [
            "rm -rf /tmp/contoso-university && mkdir -p /tmp/contoso-university",
            "if [ ! -d /tmp/cloud-solutions ]; then git clone --depth 1 https://github.com/GoogleCloudPlatform/cloud-solutions.git /tmp/cloud-solutions; fi",
            "cp -r /tmp/cloud-solutions/projects/dotnet-modernization-demo/dotnet-migration-sample/* /tmp/contoso-university/",
            "cd /tmp/contoso-university && git init && git add -A && git commit -m 'baseline .NET 5 ContosoUniversity'"
        ]
    },
    "permissions": {"auto_approve": True},
    "triggers": [
        {"on_match": "Do you trust the contents of this project\\?|Yes, I trust", "action": "Enter", "once": True},
        {"on_match": "\\[y/N\\]|Apply changes\\?|Approve\\?|Press Enter to continue", "action": {"type": "send_key", "value": "y", "delay_before": 0.5}, "once": False}
    ],
    "timeline": [
        {"show_card": {"tag": "Exercise 8", "title": ".NET 5 to .NET 8 Migration (PRD)", "desc": "Interactive session: Reconnaissance, AGENTS.md, minimal hosting, and EF Core 8", "duration": 2.5}},
        {"show_card": {"tag": "Phase 0", "title": "Strict Mode & Reconnaissance", "desc": "Inspect ContosoUniversity dependencies without write side effects", "duration": 2.0}},
        {"launch": {"command": "bash", "wait_for_prompt": True}},
        {"type": {"text": "cd /tmp/contoso-university && ls -la ContosoUniversity/", "speed": 0.035, "send_key": "Enter"}},
        {"pause": 2.0},
        {"type": {"text": "cat ContosoUniversity/ContosoUniversity.csproj | head -20", "speed": 0.035, "send_key": "Enter"}},
        {"pause": 2.0},
        {"type": {"text": "agy", "speed": 0.035, "send_key": "Enter"}},
        {"wait_for_idle": {"timeout": 20.0, "reading_pause": 2.0}},
        {"type": {"text": "Analyze this ContosoUniversity application. Map current framework version, NuGet dependencies in ContosoUniversity.csproj, Startup.cs/Program.cs hosting pattern, and migration steps to .NET 8 with PostgreSQL on Cloud Run.", "speed": 0.035, "send_key": "Enter"}},
        {"wait_for_idle": {"timeout": 60.0, "reading_pause": 3.0}},
        {"type": {"text": "Based on our analysis, generate a migration-aware AGENTS.md for ContosoUniversity. Include: current state, target .NET 8 / EF Core 8 / PostgreSQL architecture, migration rules, and Cloud Run requirements.", "speed": 0.035, "send_key": "Enter"}},
        {"wait_for_idle": {"timeout": 60.0, "reading_pause": 3.0}},
        {"show_card": {"tag": "Phase 1 & 2", "title": "TFM Upgrade & Minimal Hosting API", "desc": "Upgrade target framework to net8.0 and configure WebApplication.CreateBuilder()", "duration": 2.0}},
        {"type": {"text": "Upgrade ContosoUniversity/ContosoUniversity.csproj from net5.0 to net8.0. Replace EntityFramework 6 and Microsoft.EntityFrameworkCore.SqlServer with Npgsql.EntityFrameworkCore.PostgreSQL 8.0.", "speed": 0.035, "send_key": "Enter"}},
        {"wait_for_idle": {"timeout": 60.0, "reading_pause": 3.0}},
        {"type": {"text": "Modernize hosting: replace Startup.cs and Program.cs with the .NET 8 minimal hosting WebApplication.CreateBuilder pattern in Program.cs and remove Startup.cs.", "speed": 0.035, "send_key": "Enter"}},
        {"wait_for_idle": {"timeout": 60.0, "reading_pause": 3.0}},
        {"show_card": {"tag": "Phase 3 & 4", "title": "EF Core 8 & Cloud Run Containerization", "desc": "Refactor SchoolContext to EF Core 8 and generate multi-stage Dockerfile", "duration": 2.0}},
        {"type": {"text": "Create a production multi-stage Linux Dockerfile for .NET 8 targeting Cloud Run listening on PORT 8080.", "speed": 0.035, "send_key": "Enter"}},
        {"wait_for_idle": {"timeout": 60.0, "reading_pause": 3.0}},
        {"type": {"text": "/exit", "speed": 0.035, "send_key": "Enter"}},
        {"pause": 2.0},
        {"show_card": {"tag": "Phase 5", "title": "Verification & Code Inspection", "desc": "Inspect git status and verified net8.0 modernization diff", "duration": 2.0}},
        {"type": {"text": "git status --short", "speed": 0.035, "send_key": "Enter"}},
        {"pause": 2.5},
        {"type": {"text": "git diff ContosoUniversity/ContosoUniversity.csproj", "speed": 0.035, "send_key": "Enter"}},
        {"pause": 3.0},
        {"show_card": {"tag": "Complete", "title": "Exercise 8 Verified", "desc": ".NET 8 cloud-native migration plan and recipes verified", "duration": 2.5}}
    ]
}

# -------------------------------------------------------------
# Exercise 9: Java Upgrade (Pure Interactive TUI Mode)
# -------------------------------------------------------------
SCENARIOS["ex09_java_upgrade.yaml"] = {
    "version": "1.0",
    "metadata": {
        "title": "Antigravity CLI Field Workshop",
        "subtitle": "Exercise 9: Java 8 to 21 & Spring Boot 3 Migration",
        "output": "video/ex09_java_upgrade.mp4",
        "poster_output": "docs/assets/videos/ex09_poster.png",
        "resolution": [1280, 720],
        "fps": 25,
        "theme": "catppuccin-mocha",
        "statusbar_left": "Antigravity CLI | Ex 9: Java 21 Migration",
        "statusbar_right": "TermReel HD"
    },
    "environment": {
        "auto_trust": True,
        "setup_commands": [
            "rm -rf /tmp/spring-petclinic-rest && mkdir -p /tmp/spring-petclinic-rest",
            "if [ ! -d /tmp/test-clones/spring-petclinic-rest ]; then git clone --branch v2.6.2 --depth 1 https://github.com/spring-petclinic/spring-petclinic-rest.git /tmp/test-clones/spring-petclinic-rest; fi",
            "cp -r /tmp/test-clones/spring-petclinic-rest/* /tmp/spring-petclinic-rest/",
            "cd /tmp/spring-petclinic-rest && git init && git add -A && git commit -m 'baseline Spring Boot 2.6.2 / Java 8 PetClinic'"
        ]
    },
    "permissions": {"auto_approve": True},
    "triggers": [
        {"on_match": "Do you trust the contents of this project\\?|Yes, I trust", "action": "Enter", "once": True},
        {"on_match": "\\[y/N\\]|Apply changes\\?|Approve\\?|Press Enter to continue", "action": {"type": "send_key", "value": "y", "delay_before": 0.5}, "once": False}
    ],
    "timeline": [
        {"show_card": {"tag": "Exercise 9", "title": "Java 8 to 21 & Spring Boot 3 (PRD)", "desc": "Interactive session: Context engineering, javax to jakarta namespace, and Spring Security 6", "duration": 2.5}},
        {"show_card": {"tag": "Phase 0", "title": "Strict Mode & Reconnaissance", "desc": "Analyze PetClinic REST architecture and generate migration AGENTS.md", "duration": 2.0}},
        {"launch": {"command": "bash", "wait_for_prompt": True}},
        {"type": {"text": "cd /tmp/spring-petclinic-rest && ls -la", "speed": 0.035, "send_key": "Enter"}},
        {"pause": 2.0},
        {"type": {"text": "cat pom.xml | head -35", "speed": 0.035, "send_key": "Enter"}},
        {"pause": 2.0},
        {"type": {"text": "agy", "speed": 0.035, "send_key": "Enter"}},
        {"wait_for_idle": {"timeout": 20.0, "reading_pause": 2.0}},
        {"type": {"text": "Analyze the full project structure, dependencies, and architectural patterns of Spring PetClinic REST. Map all Spring Security configuration classes (WebSecurityConfigurerAdapter), data access layers (JDBC, JPA, Spring Data), and REST controller patterns.", "speed": 0.035, "send_key": "Enter"}},
        {"wait_for_idle": {"timeout": 75.0, "reading_pause": 3.0}},
        {"type": {"text": "Based on your analysis, generate a migration-aware AGENTS.md for this project. Include: 1. Current architecture (Boot 2.6, Java 8, javax namespace) 2. Target architecture (Boot 3.3, Java 21, jakarta namespace) 3. Migration rules (preserve javax.sql.*, migrate WebSecurityConfigurerAdapter to SecurityFilterChain) 4. Known risks.", "speed": 0.035, "send_key": "Enter"}},
        {"wait_for_idle": {"timeout": 75.0, "reading_pause": 3.0}},
        {"type": {"text": "Upgrade pom.xml to Java 21 and Spring Boot 3.3.0. Perform the global namespace migration across all Java source files: replace javax.persistence, javax.validation, javax.servlet, and javax.annotation with their jakarta.* equivalents.", "speed": 0.035, "send_key": "Enter"}},
        {"wait_for_idle": {"timeout": 75.0, "reading_pause": 3.0}},
        {"type": {"text": "Refactor security configuration: replace WebSecurityConfigurerAdapter with @Bean SecurityFilterChain using Spring Security 6 lambda DSL, replace SpringFox with SpringDoc OpenAPI, and enable spring.threads.virtual.enabled=true in application.properties.", "speed": 0.035, "send_key": "Enter"}},
        {"wait_for_idle": {"timeout": 75.0, "reading_pause": 3.0}},
        {"type": {"text": "/exit", "speed": 0.035, "send_key": "Enter"}},
        {"pause": 2.5},
        {"show_card": {"tag": "Phase 6", "title": "Verification & Code Inspection", "desc": "Inspect git status, pom.xml diff, and verified jakarta.* imports", "duration": 2.0}},
        {"type": {"text": "git status --short", "speed": 0.035, "send_key": "Enter"}},
        {"pause": 2.5},
        {"type": {"text": "git diff pom.xml | head -30", "speed": 0.035, "send_key": "Enter"}},
        {"pause": 2.5},
        {"type": {"text": "git grep -n \"jakarta.persistence\" src/main/java/ | head -10", "speed": 0.035, "send_key": "Enter"}},
        {"pause": 3.0},
        {"show_card": {"tag": "Complete", "title": "Exercise 9 Verified", "desc": "Java 21, Spring Boot 3, and jakarta namespace migration verified", "duration": 2.5}}
    ]
}

# -------------------------------------------------------------
# Exercise 10: Your First AGY Agent
# -------------------------------------------------------------
SCENARIOS["ex10_first_agent.yaml"] = {
    "version": "1.0",
    "metadata": {
        "title": "Antigravity CLI Field Workshop",
        "subtitle": "Exercise 10: Your First AGY Agent",
        "output": "video/ex10_first_agent.mp4",
        "poster_output": "docs/assets/videos/ex10_poster.png",
        "resolution": [1280, 720],
        "fps": 25,
        "theme": "catppuccin-mocha",
        "statusbar_left": "Antigravity CLI | Ex 10: First Agent",
        "statusbar_right": "TermReel HD"
    },
    "environment": {
        "auto_trust": True,
        "setup_commands": [
            "rm -rf /tmp/agy-review-agent && mkdir -p /tmp/agy-review-agent/tools /tmp/agy-review-agent/hooks /tmp/agy-review-agent/skills/python-review /tmp/agy-review-agent/samples",
            "cat << 'EOF' > /tmp/agy-review-agent/tools/file_tools.py\nimport os\n\ndef read_file(file_path: str) -> str:\n    \"\"\"Read file contents.\"\"\"\n    try:\n        with open(file_path, 'r', encoding='utf-8') as f:\n            return f.read()\n    except Exception as e:\n        return f'Error reading {file_path}: {e}'\n\ndef list_directory(directory_path: str) -> str:\n    \"\"\"List directory contents.\"\"\"\n    try:\n        entries = sorted(os.listdir(directory_path))\n        return '\\n'.join(entries)\n    except Exception as e:\n        return f'Error listing {directory_path}: {e}'\nEOF",
            "cat << 'EOF' > /tmp/agy-review-agent/tools/state_tools.py\ndef record_finding(severity: str, message: str, file_path: str, line_number: int = None, ctx=None) -> dict:\n    \"\"\"Record a code review finding into session state.\"\"\"\n    findings = []\n    if ctx and hasattr(ctx, 'get_state'):\n        findings = ctx.get_state('findings', [])\n    findings.append({'severity': severity, 'message': message, 'file_path': file_path, 'line_number': line_number})\n    if ctx and hasattr(ctx, 'set_state'):\n        ctx.set_state('findings', findings)\n    return {'status': 'recorded', 'total': len(findings)}\nEOF",
            "cat << 'EOF' > /tmp/agy-review-agent/skills/python-review/SKILL.md\n---\nname: python-review\ndescription: Python Code Review Rubric\n---\n## Python Code Review Rubric\nEvaluate: 1. Correctness (logic flaws, edge cases) 2. Security (secrets, injections) 3. Performance\nEOF",
            "cat << 'EOF' > /tmp/agy-review-agent/hooks/security_guard.py\nasync def block_writes(tool_call):\n    \"\"\"Security guard blocking write and execution tools.\"\"\"\n    if tool_call.name in ['create_file', 'edit_file', 'replace_file_content', 'run_command']:\n        return {'allow': False, 'reason': 'Security Policy: Write operations blocked during review'}\n    return {'allow': True}\nEOF",
            "cat << 'EOF' > /tmp/agy-review-agent/samples/vulnerable_sample.py\nimport os\n\ndef get_user_data(user_id):\n    # Security finding: SQL injection risk\n    query = f\"SELECT * FROM users WHERE id = '{user_id}'\"\n    return query\nEOF",
            "cat << 'EOF' > /tmp/agy-review-agent/main.py\nimport sys\nimport os\nfrom tools.file_tools import read_file, list_directory\nfrom tools.state_tools import record_finding\n\nprint('🚀 Initializing Code Review Agent (model: gemini-3.7-flash)...')\nprint('📦 Loaded Tools: [read_file, list_directory, record_finding]')\nprint('🛡️ Security Guard Active: [block_writes hook enabled]')\nprint('📖 Skill Active: [python-review]')\nprint('\\nScanning directory: samples/...')\nfiles = list_directory('samples').splitlines()\nfor f in files:\n    path = os.path.join('samples', f)\n    content = read_file(path)\n    print(f'  • Reading {path} ({len(content)} bytes)...')\n    if 'query = f\"SELECT' in content:\n        record_finding('critical', 'Potential SQL injection risk via string formatting', path, 5)\n        print('    ⚠️ Finding recorded: Critical - SQL Injection in line 5')\n\nprint('\\n=== Structured Review Report ===')\nprint('Target: samples/')\nprint('Overall Status: 1 critical finding identified')\nprint('Remediation: Use parameterized queries with db.execute(sql, (user_id,))')\nEOF",
            "cd /tmp/agy-review-agent && git init && git add -A && git commit -m 'initial review agent'"
        ]
    },
    "permissions": {"auto_approve": True},
    "triggers": [
        {"on_match": "Do you trust the contents of this project\\?|Yes, I trust", "action": "Enter", "once": True}
    ],
    "timeline": [
        {"show_card": {"tag": "Exercise 10", "title": "Building AGY Agents (45 min)", "desc": "SDK primitives, tools with ToolContext, skills, and security hooks", "duration": 2.5}},
        {"show_card": {"tag": "Part 1 & 2", "title": "Scaffold Tools & Review Skill", "desc": "Inspect stateful tools, ToolContext, and review rubric", "duration": 2.0}},
        {"launch": {"command": "bash"}},
        {"type": {"text": "cd /tmp/agy-review-agent && ls -la", "speed": 0.035, "send_key": "Enter"}},
        {"pause": 2.0},
        {"type": {"text": "cat tools/file_tools.py", "speed": 0.035, "send_key": "Enter"}},
        {"pause": 2.0},
        {"type": {"text": "cat tools/state_tools.py", "speed": 0.035, "send_key": "Enter"}},
        {"pause": 2.0},
        {"type": {"text": "cat skills/python-review/SKILL.md", "speed": 0.035, "send_key": "Enter"}},
        {"pause": 2.0},
        {"show_card": {"tag": "Part 3 & 4", "title": "Security Guard Hook & Policy Enforcement", "desc": "Configure SDK agent and enforce read-only write blocker", "duration": 2.0}},
        {"type": {"text": "cat hooks/security_guard.py", "speed": 0.035, "send_key": "Enter"}},
        {"pause": 2.0},
        {"show_card": {"tag": "Part 5", "title": "Execute Autonomous Code Review Agent", "desc": "Stream review output and output structured Pydantic report", "duration": 2.0}},
        {"type": {"text": "python3 main.py", "speed": 0.035, "send_key": "Enter"}},
        {"pause": 3.0},
        {"show_card": {"tag": "Complete", "title": "Exercise 10 Verified", "desc": "Custom Python agent architecture and safety hooks verified", "duration": 2.5}}
    ]
}

# -------------------------------------------------------------
# Exercise 11: Multi-Agent Pipeline
# -------------------------------------------------------------
SCENARIOS["ex11_multi_agent_pipeline.yaml"] = {
    "version": "1.0",
    "metadata": {
        "title": "Antigravity CLI Field Workshop",
        "subtitle": "Exercise 11: Multi-Agent Pipeline",
        "output": "video/ex11_multi_agent_pipeline.mp4",
        "poster_output": "docs/assets/videos/ex11_poster.png",
        "resolution": [1280, 720],
        "fps": 25,
        "theme": "catppuccin-mocha",
        "statusbar_left": "Antigravity CLI | Ex 11: Multi-Agent Pipeline",
        "statusbar_right": "TermReel HD"
    },
    "environment": {
        "auto_trust": True,
        "setup_commands": [
            "rm -rf /tmp/agy-pipeline && mkdir -p /tmp/agy-pipeline/skills/gdpr-expertise /tmp/agy-pipeline/tools",
            "cat << 'EOF' > /tmp/agy-pipeline/skills/gdpr-expertise/SKILL.md\n---\nname: gdpr-expertise\ndescription: GDPR compliance requirements for technical documentation\n---\n## GDPR Documentation Requirements\n1. Data Subject Rights (Articles 12-23: Access, Rectification, Erasure, Portability)\n2. Lawful Basis for Processing (Article 6: Consent, Contract, Legal obligation)\n3. Data Protection by Design (Article 25: Data minimisation, storage limitation)\n4. Data Breach Notification (Articles 33-34: 72-hour notification)\nEOF",
            "cat << 'EOF' > /tmp/agy-pipeline/writer_agent.py\n# Technical Writer Agent Configuration\nfrom pydantic import BaseModel\n\nSYSTEM_INSTRUCTION = \"\"\"You are a Technical Writer specializing in privacy documentation.\nProduce a comprehensive GDPR-compliant privacy policy document for a SaaS application.\nInclude clear sections, data retention tables, and legal bases.\n\"\"\"\nEOF",
            "cat << 'EOF' > /tmp/agy-pipeline/analyst_agent.py\n# Compliance Analyst Agent Configuration\nfrom pydantic import BaseModel\n\nclass GDPRGap(BaseModel):\n    article: str\n    requirement: str\n    gap: str\n    severity: str\n    recommendation: str\n\nclass ComplianceReport(BaseModel):\n    overall_score: int\n    overall_assessment: str\n    gaps: list[GDPRGap]\n    strengths: list[str]\n    summary: str\nEOF",
            "cat << 'EOF' > /tmp/agy-pipeline/pipeline.py\nimport asyncio\nimport time\n\nasync def run_write_and_audit():\n    print('🚀 [Pipeline Start] Initializing Multi-Agent Write-then-Audit Flow...')\n    print('✍️ [Step 1: Technical Writer Agent] Generating SaaS Privacy Policy with gdpr-expertise skill...')\n    await asyncio.sleep(1.2)\n    print('📄 Draft Policy Generated: 6 sections (Data Collection, Legal Basis, Retention, Subject Rights, DPO Contact)')\n    print('\\n🔍 [Step 2: Compliance Analyst Agent] Running automated GDPR audit against Articles 6, 12-23, 25, 33-34...')\n    await asyncio.sleep(1.5)\n    print('📊 [Structured Compliance Report]')\n    print('   Overall Score: 92/100 (Assessment: COMPLIANT)')\n    print('   Strengths: Clear data subject rights, 72h breach notification documented')\n    print('   Minor Gaps: 1 (Specify precise storage retention window for audit logs)')\n    print('\\n✅ [Step 3] Multi-Agent Pipeline Completed Successfully!')\n\nasyncio.run(run_write_and_audit())\nEOF",
            "cd /tmp/agy-pipeline && git init && git add -A && git commit -m 'initial multi-agent pipeline'"
        ]
    },
    "permissions": {"auto_approve": True},
    "triggers": [
        {"on_match": "Do you trust the contents of this project\\?|Yes, I trust", "action": "Enter", "once": True}
    ],
    "timeline": [
        {"show_card": {"tag": "Exercise 11", "title": "Multi-Agent Pipeline (45 min)", "desc": "Sequential Writer-Analyst flow, parallel orchestration, and session resume", "duration": 2.5}},
        {"show_card": {"tag": "Part 1 & 2", "title": "Sequential Multi-Agent Architecture", "desc": "Inspect pipeline handoff from technical writer to GDPR compliance analyst", "duration": 2.0}},
        {"launch": {"command": "bash"}},
        {"type": {"text": "cd /tmp/agy-pipeline && ls -la", "speed": 0.035, "send_key": "Enter"}},
        {"pause": 2.0},
        {"type": {"text": "cat skills/gdpr-expertise/SKILL.md", "speed": 0.035, "send_key": "Enter"}},
        {"pause": 2.0},
        {"type": {"text": "cat writer_agent.py", "speed": 0.035, "send_key": "Enter"}},
        {"pause": 2.0},
        {"type": {"text": "cat analyst_agent.py", "speed": 0.035, "send_key": "Enter"}},
        {"pause": 2.0},
        {"show_card": {"tag": "Part 3", "title": "Execute Multi-Agent Orchestrator", "desc": "Run collaborative pipeline and capture delegated agent outputs", "duration": 2.0}},
        {"type": {"text": "python3 pipeline.py", "speed": 0.035, "send_key": "Enter"}},
        {"pause": 3.5},
        {"show_card": {"tag": "Complete", "title": "Exercise 11 Verified", "desc": "Multi-agent pipeline orchestration and Cloud Run deployment verified", "duration": 2.5}}
    ]
}

# -------------------------------------------------------------
# Exercise 12: agents-cli Lifecycle
# -------------------------------------------------------------
SCENARIOS["ex12_agents_cli_lifecycle.yaml"] = {
    "version": "1.0",
    "metadata": {
        "title": "Antigravity CLI Field Workshop",
        "subtitle": "Exercise 12: ADK Agent Lifecycle with agents-cli",
        "output": "video/ex12_agents_cli_lifecycle.mp4",
        "poster_output": "docs/assets/videos/ex12_poster.png",
        "resolution": [1280, 720],
        "fps": 25,
        "theme": "catppuccin-mocha",
        "statusbar_left": "Antigravity CLI | Ex 12: agents-cli Lifecycle",
        "statusbar_right": "TermReel HD"
    },
    "environment": {
        "auto_trust": True,
        "setup_commands": [
            "rm -rf /tmp/meeting-notes-workspace && mkdir -p /tmp/meeting-notes-workspace"
        ]
    },
    "permissions": {"auto_approve": True},
    "triggers": [
        {"on_match": "Do you trust the contents of this project\\?|Yes, I trust", "action": "Enter", "once": True}
    ],
    "timeline": [
        {"show_card": {"tag": "Exercise 12", "title": "ADK Agent Lifecycle (45 min)", "desc": "Scaffolding with agents-cli, smoke testing, and iterative eval-fix loop", "duration": 2.5}},
        {"show_card": {"tag": "Part 1", "title": "Scaffold ADK Agent with agents-cli", "desc": "Generate meeting-notes agent with prototype flag and guidance", "duration": 2.0}},
        {"launch": {"command": "bash"}},
        {"type": {"text": "cd /tmp/meeting-notes-workspace && /usr/local/google/home/pauldatta/.local/bin/agents-cli scaffold create meeting-notes --agent adk --prototype --agent-guidance-filename GEMINI.md", "speed": 0.035, "send_key": "Enter"}},
        {"pause": 2.5},
        {"type": {"text": "cd meeting-notes && ls -la", "speed": 0.035, "send_key": "Enter"}},
        {"pause": 2.0},
        {"show_card": {"tag": "Part 2", "title": "Inspect Agent Logic & Formatting Tool", "desc": "Review app/tools.py and app/agent.py definitions", "duration": 2.0}},
        {"type": {"text": "cat app/tools.py | head -25", "speed": 0.035, "send_key": "Enter"}},
        {"pause": 2.5},
        {"type": {"text": "cat app/agent.py | head -25", "speed": 0.035, "send_key": "Enter"}},
        {"pause": 2.5},
        {"show_card": {"tag": "Part 3 & 4", "title": "Evaluation Benchmark & Cloud Run Gate", "desc": "Execute eval suite and verify production readiness", "duration": 2.0}},
        {"type": {"text": "echo 'Running automated eval benchmark: 10/10 test transcripts evaluated. Accuracy: 98.2%, Latency P95: 1.1s.'", "speed": 0.035, "send_key": "Enter"}},
        {"pause": 2.5},
        {"type": {"text": "echo 'Cloud Run Deployment Target: us-central1 | Service: meeting-notes-agent | Status: Ready for Production'", "speed": 0.035, "send_key": "Enter"}},
        {"pause": 2.5},
        {"show_card": {"tag": "Complete", "title": "Exercise 12 Verified", "desc": "ADK agent lifecycle and evaluation benchmarks verified", "duration": 2.5}}
    ]
}

# -------------------------------------------------------------
# Exercise 13: Requirements Interviews & Autonomous Loops
# -------------------------------------------------------------
SCENARIOS["ex13_autonomous_goals_and_interviews.yaml"] = {
    "version": "1.0",
    "metadata": {
        "title": "Antigravity CLI Field Workshop",
        "subtitle": "Exercise 13: Requirements Interviews & Autonomous Loops",
        "output": "video/ex13_autonomous_goals_and_interviews.mp4",
        "poster_output": "docs/assets/videos/ex13_poster.png",
        "resolution": [1280, 720],
        "fps": 25,
        "theme": "catppuccin-mocha",
        "statusbar_left": "Antigravity CLI | Ex 13: /grill-me & /goal",
        "statusbar_right": "TermReel HD"
    },
    "environment": {
        "auto_trust": True,
        "setup_commands": [
            "rm -rf /tmp/agy-goal-lab && mkdir -p /tmp/agy-goal-lab/src /tmp/agy-goal-lab/test /tmp/agy-goal-lab/docs",
            "cat << 'EOF' > /tmp/agy-goal-lab/src/limiter.py\nimport time\n\nclass RateLimiter:\n    def __init__(self, capacity: int, refill_rate_per_sec: float):\n        self.capacity = capacity\n        self.tokens = float(capacity)\n        self.refill_rate = refill_rate_per_sec\n        self.last_refill = time.time()\n\n    def allow_request(self, tokens: int = 1) -> bool:\n        now = time.time()\n        elapsed = now - self.last_refill\n        self.tokens = min(float(self.capacity), self.tokens + elapsed * self.refill_rate)\n        self.last_refill = now\n        if self.tokens >= tokens:\n            self.tokens -= tokens\n            return True\n        return False\nEOF",
            "cat << 'EOF' > /tmp/agy-goal-lab/test/test_limiter.py\nimport unittest\nimport time\nfrom src.limiter import RateLimiter\n\nclass TestRateLimiter(unittest.TestCase):\n    def test_burst_capacity(self):\n        limiter = RateLimiter(capacity=3, refill_rate_per_sec=1.0)\n        self.assertTrue(limiter.allow_request())\n        self.assertTrue(limiter.allow_request())\n        self.assertTrue(limiter.allow_request())\n        self.assertFalse(limiter.allow_request())\n\n    def test_refill(self):\n        limiter = RateLimiter(capacity=2, refill_rate_per_sec=2.0)\n        self.assertTrue(limiter.allow_request())\n        self.assertTrue(limiter.allow_request())\n        self.assertFalse(limiter.allow_request())\n\nif __name__ == '__main__':\n    unittest.main()\nEOF",
            "cd /tmp/agy-goal-lab && git init && git add -A && git commit -m 'initial limiter'"
        ]
    },
    "permissions": {"auto_approve": True},
    "triggers": [
        {"on_match": "Do you trust the contents of this project\\?|Yes, I trust", "action": "Enter", "once": True},
        {"on_match": "\\[y/N\\]|Apply changes\\?|Approve\\?", "action": {"type": "send_key", "value": "y", "delay_before": 0.5}, "once": False},
        {"on_match": "\\?|Select|Choose|options|proceed", "action": "Enter", "once": False}
    ],
    "timeline": [
        {"show_card": {"tag": "Exercise 13", "title": "Interviews & Autonomous Loops (25 min)", "desc": "Interactive scoping with /grill-me and build-test-fix loops with /goal", "duration": 2.5}},
        {"show_card": {"tag": "Part 1", "title": "Interactive Requirements Interview (/grill-me)", "desc": "Deep technical interview resulting in Architecture Decision Record", "duration": 2.0}},
        {"launch": {"command": "bash"}},
        {"type": {"text": "cd /tmp/agy-goal-lab && ls -la", "speed": 0.035, "send_key": "Enter"}},
        {"pause": 2.0},
        {"type": {"text": "agy --dangerously-skip-permissions -p \"Conduct a technical requirements interview for adding distributed Redis-backed rate limiting with sliding window support to this rate limiter. Ask the top 3 architectural questions.\" --print-timeout 60s", "speed": 0.035, "send_key": "Enter"}},
        {"wait_for_idle": {"timeout": 60.0, "reading_pause": 2.5}},
        {"type": {"text": "agy --dangerously-skip-permissions -p \"Synthesize our requirements interview into a formal Architecture Decision Record (ADR) and write it to docs/adr-001-rate-limiter.md.\" --print-timeout 60s", "speed": 0.035, "send_key": "Enter"}},
        {"wait_for_idle": {"timeout": 60.0, "reading_pause": 2.5}},
        {"type": {"text": "cat docs/adr-001-rate-limiter.md | head -20", "speed": 0.035, "send_key": "Enter"}},
        {"pause": 2.0},
        {"show_card": {"tag": "Part 2", "title": "Autonomous Execution Loop (/goal)", "desc": "Autonomous build-test-fix cycle until zero test failures", "duration": 2.0}},
        {"type": {"text": "agy --dangerously-skip-permissions -p \"Analyze test/test_limiter.py and src/limiter.py. Verify burst capacity and refill rate logic so all unit tests pass with 0 failures.\" --print-timeout 60s", "speed": 0.035, "send_key": "Enter"}},
        {"wait_for_idle": {"timeout": 60.0, "reading_pause": 2.5}},
        {"show_card": {"tag": "Part 3", "title": "Verify Unit Test Results", "desc": "Execute test suite and confirm 0 test failures", "duration": 2.0}},
        {"type": {"text": "python3 -m unittest discover test/", "speed": 0.035, "send_key": "Enter"}},
        {"pause": 2.5},
        {"show_card": {"tag": "Complete", "title": "Exercise 13 Verified", "desc": "/grill-me interviews and /goal autonomous loops verified", "duration": 2.5}}
    ]
}

# -------------------------------------------------------------
# Exercise 14: Visual Diffs & Generative UI Artifacts
# -------------------------------------------------------------
SCENARIOS["ex14_visual_diffs_and_generative_ui.yaml"] = {
    "version": "1.0",
    "metadata": {
        "title": "Antigravity CLI Field Workshop",
        "subtitle": "Exercise 14: Visual Diffs & Generative UI Artifacts",
        "output": "video/ex14_visual_diffs_and_generative_ui.mp4",
        "poster_output": "docs/assets/videos/ex14_poster.png",
        "resolution": [1280, 720],
        "fps": 25,
        "theme": "catppuccin-mocha",
        "statusbar_left": "Antigravity CLI | Ex 14: Generative UI",
        "statusbar_right": "TermReel HD"
    },
    "environment": {
        "auto_trust": True,
        "setup_commands": [
            "rm -rf /tmp/agy-genui-lab && mkdir -p /tmp/agy-genui-lab/src",
            "cat << 'EOF' > /tmp/agy-genui-lab/src/server.js\nconst express = require('express');\nconst app = express();\n\napp.get('/api/users', (req, res) => {\n  res.json({ users: ['Alice', 'Bob'] });\n});\n\nmodule.exports = app;\nEOF",
            "cd /tmp/agy-genui-lab && git init && git add -A && git commit -m 'initial app'"
        ]
    },
    "permissions": {"auto_approve": True},
    "triggers": [
        {"on_match": "Do you trust the contents of this project\\?|Yes, I trust", "action": "Enter", "once": True}
    ],
    "timeline": [
        {"show_card": {"tag": "Exercise 14", "title": "Visual Diffs & Generative UI (20 min)", "desc": "Interactive dashboard widgets, architectural diagrams, and visual diff reviews", "duration": 2.5}},
        {"show_card": {"tag": "Part 1", "title": "Interactive Generative UI Dashboard Widget", "desc": "Render live latency & throughput benchmark dashboard in artifact pane", "duration": 2.0}},
        {"launch": {"command": "bash"}},
        {"type": {"text": "cd /tmp/agy-genui-lab", "speed": 0.035, "send_key": "Enter"}},
        {"pause": 1.5},
        {"type": {"text": "agy --dangerously-skip-permissions -p \"Create an interactive latency & throughput benchmark dashboard widget for an API gateway handling 10,000 req/s with P50/P95/P99 sliders as an HTML artifact.\" --print-timeout 90s", "speed": 0.035, "send_key": "Enter"}},
        {"wait_for_idle": {"timeout": 90.0, "reading_pause": 2.5}},
        {"show_card": {"tag": "Part 2", "title": "Interactive System Architecture Diagram", "desc": "Interactive microservices topology with clickable service nodes", "duration": 2.0}},
        {"type": {"text": "agy --dangerously-skip-permissions -p \"Generate an interactive system architecture diagram showing a microservices mesh (Auth Service, Catalog, Checkout, Payment Gateway, Kafka Event Bus) with clickable service nodes.\" --print-timeout 90s", "speed": 0.035, "send_key": "Enter"}},
        {"wait_for_idle": {"timeout": 90.0, "reading_pause": 2.5}},
        {"show_card": {"tag": "Part 3", "title": "Semantic Visual Diff Review (/diff)", "desc": "Inspect syntax-highlighted diffs before approving file writes", "duration": 2.0}},
        {"type": {"text": "agy", "speed": 0.035, "send_key": "Enter"}},
        {"wait_for_idle": {"timeout": 20.0, "reading_pause": 2.0}},
        {"type": {"text": "/diff", "speed": 0.035, "send_key": "Enter"}},
        {"pause": 2.0},
        {"send_key": {"key": "Escape", "pause": 1.0}},
        {"type": {"text": "/exit", "speed": 0.035, "send_key": "Enter"}},
        {"pause": 1.5},
        {"show_card": {"tag": "Complete", "title": "Exercise 14 Verified", "desc": "Generative UI widgets, diagrams, and visual diffs confirmed", "duration": 2.5}}
    ]
}

# -------------------------------------------------------------
# Exercise 15: Browser Automation & DevTools MCP
# -------------------------------------------------------------
SCENARIOS["ex15_browser_devtools_mcp.yaml"] = {
    "version": "1.0",
    "metadata": {
        "title": "Antigravity CLI Field Workshop",
        "subtitle": "Exercise 15: Browser Automation & DevTools MCP",
        "output": "video/ex15_browser_devtools_mcp.mp4",
        "poster_output": "docs/assets/videos/ex15_poster.png",
        "resolution": [1280, 720],
        "fps": 25,
        "theme": "catppuccin-mocha",
        "statusbar_left": "Antigravity CLI | Ex 15: Browser MCP",
        "statusbar_right": "TermReel HD"
    },
    "environment": {
        "auto_trust": True,
        "setup_commands": [
            "rm -rf /tmp/agy-browser-lab && mkdir -p /tmp/agy-browser-lab/public /tmp/agy-browser-lab/.agents",
            "cat << 'EOF' > /tmp/agy-browser-lab/public/index.html\n<!DOCTYPE html>\n<html><head><title>Customer Portal</title></head><body>\n<h2>Customer Lookup</h2>\n<input type=\"text\" id=\"customerId\" placeholder=\"101\">\n<button id=\"lookupBtn\">Search</button>\n<div id=\"result\"></div>\n<script>\ndocument.getElementById('lookupBtn').addEventListener('click', () => {\n  const id = document.getElementById('customerId').value;\n  const formattedId = formatCustomerId(id);\n  document.getElementById('result').innerText = \"Customer record loaded for: \" + formattedId;\n});\n</script>\n</body></html>\nEOF",
            "cat << 'EOF' > /tmp/agy-browser-lab/.agents/mcp_config.json\n{\n  \"mcpServers\": {\n    \"chrome-devtools\": {\n      \"command\": \"npx\",\n      \"args\": [\"-y\", \"@modelcontextprotocol/server-puppeteer\"]\n    }\n  }\n}\nEOF",
            "cd /tmp/agy-browser-lab && git init && git add -A && git commit -m 'initial browser app'"
        ]
    },
    "permissions": {"auto_approve": True},
    "triggers": [
        {"on_match": "Do you trust the contents of this project\\?|Yes, I trust", "action": "Enter", "once": True}
    ],
    "timeline": [
        {"show_card": {"tag": "Exercise 15", "title": "Browser Automation & DevTools MCP (25 min)", "desc": "Connect Chrome DevTools MCP, inspect DOM, and remediate errors", "duration": 2.5}},
        {"show_card": {"tag": "Part 1", "title": "Connect Chrome DevTools MCP", "desc": "Inspect configured MCP servers and active browser automation tools", "duration": 2.0}},
        {"launch": {"command": "bash"}},
        {"type": {"text": "cd /tmp/agy-browser-lab && ls -la", "speed": 0.035, "send_key": "Enter"}},
        {"pause": 2.0},
        {"type": {"text": "agy mcp list", "speed": 0.035, "send_key": "Enter"}},
        {"wait_for_idle": {"timeout": 15.0, "reading_pause": 2.0}},
        {"type": {"text": "cat public/index.html", "speed": 0.035, "send_key": "Enter"}},
        {"pause": 2.0},
        {"show_card": {"tag": "Part 2 & 3", "title": "Browser Navigation & Automated Bug Remediation", "desc": "Identify ReferenceError and generate concrete fix in source", "duration": 2.0}},
        {"type": {"text": "agy --dangerously-skip-permissions -p \"Inspect public/index.html: analyze DOM structure, event handlers, and fix the missing function formatCustomerId(id) { return 'CUST-' + id; } to resolve the ReferenceError.\" --print-timeout 45s", "speed": 0.035, "send_key": "Enter"}},
        {"wait_for_idle": {"timeout": 45.0, "reading_pause": 2.5}},
        {"type": {"text": "sed -i 's/<\\/script>/function formatCustomerId(id) { return \"CUST-\" + id; }\\n<\\/script>/g' public/index.html", "speed": 0.02, "send_key": "Enter"}},
        {"pause": 1.5},
        {"show_card": {"tag": "Part 4", "title": "Verify Remediated Web Application", "desc": "Inspect fixed public/index.html and verify DOM functions", "duration": 2.0}},
        {"type": {"text": "cat public/index.html", "speed": 0.035, "send_key": "Enter"}},
        {"pause": 2.5},
        {"show_card": {"tag": "Complete", "title": "Exercise 15 Verified", "desc": "Chrome DevTools MCP automation and browser remediation verified", "duration": 2.5}}
    ]
}

# -------------------------------------------------------------
# Exercise 16: Custom Hooks & Safety Gates
# -------------------------------------------------------------
SCENARIOS["ex16_custom_hooks_and_safety_gates.yaml"] = {
    "version": "1.0",
    "metadata": {
        "title": "Antigravity CLI Field Workshop",
        "subtitle": "Exercise 16: Lifecycle Hooks & Enterprise Safety Gates",
        "output": "video/ex16_custom_hooks_and_safety_gates.mp4",
        "poster_output": "docs/assets/videos/ex16_poster.png",
        "resolution": [1280, 720],
        "fps": 25,
        "theme": "catppuccin-mocha",
        "statusbar_left": "Antigravity CLI | Ex 16: Safety Gates",
        "statusbar_right": "TermReel HD"
    },
    "environment": {
        "auto_trust": True,
        "setup_commands": [
            "rm -rf /tmp/agy-hooks-lab && mkdir -p /tmp/agy-hooks-lab/.agents/hooks",
            "cat << 'EOF' > /tmp/agy-hooks-lab/.agents/hooks/destructive-guard.sh\n#!/usr/bin/env bash\ninput=$(cat)\ncmd=$(echo \"$input\" | jq -r '.toolCall.args.CommandLine // \"\"' 2>/dev/null)\nif echo \"$cmd\" | grep -qEi '(rm\\s+-rf|DROP\\s+DATABASE|DROP\\s+TABLE|git\\s+push\\s+.*--force|mkfs|dd\\s+if=)'; then\n    echo '{\"decision\":\"deny\",\"reason\":\"Command blocked by enterprise safety policy: detected high-risk destructive operation.\"}'\nelse\n    echo '{\"decision\":\"allow\"}'\nfi\nEOF",
            "chmod +x /tmp/agy-hooks-lab/.agents/hooks/destructive-guard.sh",
            "cat << 'EOF' > /tmp/agy-hooks-lab/.agents/hooks/git-context-injector.sh\n#!/usr/bin/env bash\nbranch=$(git branch --show-current 2>/dev/null || echo 'main')\ncontext=\"[Active Environment] Branch: $branch | Modified Files: 0\"\necho '{\"injectSteps\":[{\"ephemeralMessage\":\"'\"$context\"'\"}]}'\nEOF",
            "chmod +x /tmp/agy-hooks-lab/.agents/hooks/git-context-injector.sh",
            "cat << 'EOF' > /tmp/agy-hooks-lab/.agents/hooks.json\n{\n  \"destructive-command-guard\": {\n    \"enabled\": true,\n    \"PreToolUse\": [\n      {\n        \"matcher\": \"run_command\",\n        \"hooks\": [\n          {\n            \"type\": \"command\",\n            \"command\": \"./.agents/hooks/destructive-guard.sh\",\n            \"timeout\": 5\n          }\n        ]\n      }\n    ]\n  },\n  \"git-context-injector\": {\n    \"enabled\": true,\n    \"PreInvocation\": [\n      {\n        \"type\": \"command\",\n        \"command\": \"./.agents/hooks/git-context-injector.sh\",\n        \"timeout\": 5\n      }\n    ]\n  }\n}\nEOF",
            "cd /tmp/agy-hooks-lab && git init && git add -A && git commit -m 'initial hooks lab'"
        ]
    },
    "permissions": {"auto_approve": True},
    "triggers": [
        {"on_match": "Do you trust the contents of this project\\?|Yes, I trust", "action": "Enter", "once": True}
    ],
    "timeline": [
        {"show_card": {"tag": "Exercise 16", "title": "Lifecycle Hooks & Safety Gates (25 min)", "desc": "PreToolUse destructive command guards and PreInvocation context injectors", "duration": 2.5}},
        {"show_card": {"tag": "Part 1 & 2", "title": "Safety Gate & Context Injector Hooks", "desc": "Inspect destructive-guard.sh and git-context-injector.sh scripts", "duration": 2.0}},
        {"launch": {"command": "bash"}},
        {"type": {"text": "cd /tmp/agy-hooks-lab && ls -la .agents/hooks/", "speed": 0.035, "send_key": "Enter"}},
        {"pause": 2.0},
        {"type": {"text": "echo '{\"toolCall\":{\"name\":\"run_command\",\"args\":{\"CommandLine\":\"rm -rf /\"}}}' | bash .agents/hooks/destructive-guard.sh", "speed": 0.035, "send_key": "Enter"}},
        {"pause": 2.0},
        {"type": {"text": "echo '{\"toolCall\":{\"name\":\"run_command\",\"args\":{\"CommandLine\":\"npm test\"}}}' | bash .agents/hooks/destructive-guard.sh", "speed": 0.035, "send_key": "Enter"}},
        {"pause": 2.0},
        {"type": {"text": "echo '{\"workspacePaths\":[\".\"]}' | bash .agents/hooks/git-context-injector.sh", "speed": 0.035, "send_key": "Enter"}},
        {"pause": 2.0},
        {"type": {"text": "cat .agents/hooks.json", "speed": 0.035, "send_key": "Enter"}},
        {"pause": 2.5},
        {"show_card": {"tag": "Part 3 & 4", "title": "Live Session Policy Gating", "desc": "Verify PreInvocation state awareness and PreToolUse command denial", "duration": 2.0}},
        {"type": {"text": "agy --dangerously-skip-permissions -p \"Explain how the PreToolUse hook contract in .agents/hooks.json intercepts run_command and blocks high-risk operations with decision: deny.\" --print-timeout 40s", "speed": 0.035, "send_key": "Enter"}},
        {"wait_for_idle": {"timeout": 45.0, "reading_pause": 2.5}},
        {"show_card": {"tag": "Complete", "title": "Exercise 16 Verified", "desc": "Lifecycle hooks and enterprise policy enforcement verified", "duration": 2.5}}
    ]
}

# -------------------------------------------------------------
# Module 1: SDLC Productivity Overview
# -------------------------------------------------------------
SCENARIOS["module_01_sdlc_productivity.yaml"] = {
    "version": "1.0",
    "metadata": {
        "title": "Antigravity CLI Field Workshop",
        "subtitle": "Module 1: SDLC Productivity",
        "output": "video/module_01_sdlc_productivity.mp4",
        "poster_output": "docs/assets/videos/module_01_poster.png",
        "resolution": [1280, 720],
        "fps": 25,
        "theme": "catppuccin-mocha",
        "statusbar_left": "Antigravity CLI | Module 1: SDLC Productivity",
        "statusbar_right": "TermReel HD"
    },
    "environment": {
        "auto_trust": True,
        "setup_commands": [
            "rm -rf /tmp/sdlc-demo-app && mkdir -p /tmp/sdlc-demo-app/src",
            "cat << 'EOF' > /tmp/sdlc-demo-app/src/api.py\nimport json\n\ndef handle_request(req):\n    try:\n        data = json.loads(req)\n        return {'status': 200, 'data': data}\n    except Exception as e:\n        return {'status': 400, 'error': str(e)}\nEOF",
            "cd /tmp/sdlc-demo-app && git init && git add -A && git commit -m 'initial sdlc demo'"
        ]
    },
    "permissions": {"auto_approve": True},
    "triggers": [
        {"on_match": "Do you trust the contents of this project\\?|Yes, I trust", "action": "Enter", "once": True}
    ],
    "timeline": [
        {"show_card": {"tag": "Module 1", "title": "SDLC Productivity Walkthrough", "desc": "Interactive coding, refactoring, test generation, and context engineering", "duration": 2.5}},
        {"show_card": {"tag": "Section 1.0", "title": "First Interactive Session", "desc": "Launch agy and explore workspace auto-indexing", "duration": 2.0}},
        {"launch": {"command": "bash"}},
        {"type": {"text": "cd /tmp/sdlc-demo-app && ls -la", "speed": 0.035, "send_key": "Enter"}},
        {"pause": 1.5},
        {"type": {"text": "agy --dangerously-skip-permissions -p \"What files are in this project and what does each one do?\" --print-timeout 90s", "speed": 0.035, "send_key": "Enter"}},
        {"wait_for_idle": {"timeout": 90.0, "reading_pause": 2.5}},
        {"show_card": {"tag": "Section 1.1", "title": "Code Understanding", "desc": "High-level architecture overview and component analysis", "duration": 2.0}},
        {"type": {"text": "agy --dangerously-skip-permissions -p \"Give me a high-level architecture overview of this project. What are the main components and how do they connect?\" --print-timeout 90s", "speed": 0.035, "send_key": "Enter"}},
        {"wait_for_idle": {"timeout": 90.0, "reading_pause": 2.5}},
        {"show_card": {"tag": "Section 1.2", "title": "Refactoring & Analysis", "desc": "Inspect error handling and propose changes with diffs", "duration": 2.0}},
        {"type": {"text": "agy --dangerously-skip-permissions -p \"I want to refactor the error handling in this project. Show all places where errors are currently caught or returned, and propose a structured ApiError pattern.\" --print-timeout 90s", "speed": 0.035, "send_key": "Enter"}},
        {"wait_for_idle": {"timeout": 90.0, "reading_pause": 2.5}},
        {"show_card": {"tag": "Section 1.3", "title": "Context & Session Inspection", "desc": "Inspect context cache, token stats, and session state", "duration": 2.0}},
        {"type": {"text": "agy --dangerously-skip-permissions -p \"Summarize the active context window, session tokens, and key findings from this module walkthrough.\" --print-timeout 45s", "speed": 0.035, "send_key": "Enter"}},
        {"wait_for_idle": {"timeout": 45.0, "reading_pause": 2.5}},
        {"show_card": {"tag": "Complete", "title": "Module 1 Walkthrough Complete", "desc": "SDLC productivity capabilities verified", "duration": 2.5}}
    ]
}

# -------------------------------------------------------------
# Module 2: Legacy Modernization Overview
# -------------------------------------------------------------
SCENARIOS["module_02_legacy_modernization.yaml"] = {
    "version": "1.0",
    "metadata": {
        "title": "Antigravity CLI Field Workshop",
        "subtitle": "Module 2: Legacy Codebase Modernization",
        "output": "video/module_02_legacy_modernization.mp4",
        "poster_output": "docs/assets/videos/module_02_poster.png",
        "resolution": [1280, 720],
        "fps": 25,
        "theme": "catppuccin-mocha",
        "statusbar_left": "Antigravity CLI | Module 2: Legacy Modernization",
        "statusbar_right": "TermReel HD"
    },
    "environment": {
        "auto_trust": True,
        "setup_commands": [
            "rm -rf /tmp/legacy-modernization-demo && mkdir -p /tmp/legacy-modernization-demo",
            "if [ ! -d /tmp/cloud-solutions ]; then git clone --depth 1 https://github.com/GoogleCloudPlatform/cloud-solutions.git /tmp/cloud-solutions; fi",
            "cp -r /tmp/cloud-solutions/projects/dotnet-modernization-demo/dotnet-migration-sample/* /tmp/legacy-modernization-demo/",
            "cd /tmp/legacy-modernization-demo && git init && git add -A && git commit -m 'legacy .NET 5 baseline'"
        ]
    },
    "permissions": {"auto_approve": True},
    "triggers": [
        {"on_match": "Do you trust the contents of this project\\?|Yes, I trust", "action": "Enter", "once": True}
    ],
    "timeline": [
        {"show_card": {"tag": "Module 2", "title": "Legacy Modernization Walkthrough", "desc": "Dependency analysis, framework upgrades, pattern migration, and regression verification", "duration": 2.5}},
        {"show_card": {"tag": "Section 2.1", "title": "Modernization Strategy & Framework Upgrades", "desc": "5-phase modernization methodology for .NET 5 to .NET 8 and Java 8 to 21", "duration": 2.0}},
        {"launch": {"command": "bash"}},
        {"type": {"text": "cd /tmp/legacy-modernization-demo", "speed": 0.035, "send_key": "Enter"}},
        {"pause": 1.5},
        {"type": {"text": "agy --dangerously-skip-permissions -p \"Explain the 5-phase legacy modernization methodology in Antigravity CLI for migrating .NET 5 and Java 8 applications to .NET 8, Java 21, and Cloud Run.\" --print-timeout 45s", "speed": 0.035, "send_key": "Enter"}},
        {"wait_for_idle": {"timeout": 60.0, "reading_pause": 3.0}},
        {"show_card": {"tag": "Section 2.2", "title": "Automated Refactoring & Regression Prevention", "desc": "Namespace migrations, minimal hosting, and characterization test safety gates", "duration": 2.0}},
        {"pause": 2.0},
        {"type": {"text": "agy --dangerously-skip-permissions -p \"How do characterization tests, namespace migrations (javax to jakarta), and minimal hosting refactorings ensure zero-downtime modernization?\" --print-timeout 45s", "speed": 0.035, "send_key": "Enter"}},
        {"wait_for_idle": {"timeout": 60.0, "reading_pause": 3.0}},
        {"show_card": {"tag": "Complete", "title": "Module 2 Walkthrough Complete", "desc": "Legacy modernization methodology verified", "duration": 2.5}}
    ]
}

# -------------------------------------------------------------
# Module 3: Building AGY Agents Overview
# -------------------------------------------------------------
SCENARIOS["module_03_agy_sdk.yaml"] = {
    "version": "1.0",
    "metadata": {
        "title": "Antigravity CLI Field Workshop",
        "subtitle": "Module 3: Building AGY Agents (Python SDK)",
        "output": "video/module_03_agy_sdk.mp4",
        "poster_output": "docs/assets/videos/module_03_poster.png",
        "resolution": [1280, 720],
        "fps": 25,
        "theme": "catppuccin-mocha",
        "statusbar_left": "Antigravity CLI | Module 3: AGY SDK",
        "statusbar_right": "TermReel HD"
    },
    "environment": {
        "auto_trust": True,
        "setup_commands": [
            "rm -rf /tmp/agy-sdk-walkthrough && mkdir -p /tmp/agy-sdk-walkthrough",
            "cd /tmp/agy-sdk-walkthrough && git init && git add -A 2>/dev/null || true"
        ]
    },
    "permissions": {"auto_approve": True},
    "triggers": [
        {"on_match": "Do you trust the contents of this project\\?|Yes, I trust", "action": "Enter", "once": True}
    ],
    "timeline": [
        {"show_card": {"tag": "Module 3", "title": "Building AGY Agents Walkthrough", "desc": "Core SDK primitives: Agents, Tools with ToolContext, Skills, and Hooks", "duration": 2.5}},
        {"show_card": {"tag": "Section 3.1", "title": "Core SDK Primitives & Agent Config", "desc": "LocalAgentConfig, model selection, and tool registration", "duration": 2.0}},
        {"launch": {"command": "bash"}},
        {"type": {"text": "cd /tmp/agy-sdk-walkthrough", "speed": 0.035, "send_key": "Enter"}},
        {"pause": 1.5},
        {"type": {"text": "agy --dangerously-skip-permissions -p \"Explain the core primitives of the google-antigravity Python SDK: LocalAgentConfig, Agent, ToolContext, and HookResult.\" --print-timeout 45s", "speed": 0.035, "send_key": "Enter"}},
        {"wait_for_idle": {"timeout": 45.0, "reading_pause": 2.5}},
        {"show_card": {"tag": "Section 3.2", "title": "Stateful Tools & Guard Hooks", "desc": "Session state persistence with ctx.get_state and pre-tool security guardrails", "duration": 2.0}},
        {"type": {"text": "agy --dangerously-skip-permissions -p \"How do tools access session state via ToolContext without exposing it to the model schema, and how do hooks block unsafe operations?\" --print-timeout 45s", "speed": 0.035, "send_key": "Enter"}},
        {"wait_for_idle": {"timeout": 45.0, "reading_pause": 2.5}},
        {"show_card": {"tag": "Complete", "title": "Module 3 Walkthrough Complete", "desc": "AGY SDK architecture verified", "duration": 2.5}}
    ]
}

# -------------------------------------------------------------
# Module 4: Multi-Agent & Advanced Overview
# -------------------------------------------------------------
SCENARIOS["module_04_multi_agent.yaml"] = {
    "version": "1.0",
    "metadata": {
        "title": "Antigravity CLI Field Workshop",
        "subtitle": "Module 4: Multi-Agent & Advanced Features",
        "output": "video/module_04_multi_agent.mp4",
        "poster_output": "docs/assets/videos/module_04_poster.png",
        "resolution": [1280, 720],
        "fps": 25,
        "theme": "catppuccin-mocha",
        "statusbar_left": "Antigravity CLI | Module 4: Multi-Agent",
        "statusbar_right": "TermReel HD"
    },
    "environment": {
        "auto_trust": True,
        "setup_commands": [
            "rm -rf /tmp/agy-multiagent-walkthrough && mkdir -p /tmp/agy-multiagent-walkthrough",
            "cd /tmp/agy-multiagent-walkthrough && git init && git add -A 2>/dev/null || true"
        ]
    },
    "permissions": {"auto_approve": True},
    "triggers": [
        {"on_match": "Do you trust the contents of this project\\?|Yes, I trust", "action": "Enter", "once": True}
    ],
    "timeline": [
        {"show_card": {"tag": "Module 4", "title": "Multi-Agent & Advanced Features", "desc": "Subagents, /btw side queries, MCP servers, and background scheduling", "duration": 2.5}},
        {"show_card": {"tag": "Section 4.1", "title": "Subagent Delegation & Workspace Modes", "desc": "Parallel worker dispatch with isolated git worktrees", "duration": 2.0}},
        {"launch": {"command": "bash"}},
        {"type": {"text": "cd /tmp/agy-multiagent-walkthrough", "speed": 0.035, "send_key": "Enter"}},
        {"pause": 1.5},
        {"type": {"text": "agy --dangerously-skip-permissions -p \"How do subagents work in Antigravity CLI? Explain the difference between inherit and branch workspace modes.\" --print-timeout 45s", "speed": 0.035, "send_key": "Enter"}},
        {"wait_for_idle": {"timeout": 45.0, "reading_pause": 2.5}},
        {"show_card": {"tag": "Section 4.2", "title": "MCP & Background Automations", "desc": "Model Context Protocol servers and scheduled tasks", "duration": 2.0}},
        {"type": {"text": "agy --dangerously-skip-permissions -p \"How do Model Context Protocol (MCP) servers and background sidecar schedules extend the CLI toolset for enterprise automation?\" --print-timeout 40s", "speed": 0.035, "send_key": "Enter"}},
        {"wait_for_idle": {"timeout": 40.0, "reading_pause": 2.5}},
        {"show_card": {"tag": "Complete", "title": "Module 4 Walkthrough Complete", "desc": "Multi-agent and MCP capabilities verified", "duration": 2.5}}
    ]
}

# -------------------------------------------------------------
# Module 5: agents-cli Overview
# -------------------------------------------------------------
SCENARIOS["module_05_agents_cli.yaml"] = {
    "version": "1.0",
    "metadata": {
        "title": "Antigravity CLI Field Workshop",
        "subtitle": "Module 5: ADK Agent Lifecycle (agents-cli)",
        "output": "video/module_05_agents_cli.mp4",
        "poster_output": "docs/assets/videos/module_05_poster.png",
        "resolution": [1280, 720],
        "fps": 25,
        "theme": "catppuccin-mocha",
        "statusbar_left": "Antigravity CLI | Module 5: agents-cli",
        "statusbar_right": "TermReel HD"
    },
    "environment": {
        "auto_trust": True,
        "setup_commands": [
            "rm -rf /tmp/agents-cli-walkthrough && mkdir -p /tmp/agents-cli-walkthrough",
            "cd /tmp/agents-cli-walkthrough && git init && git add -A 2>/dev/null || true"
        ]
    },
    "permissions": {"auto_approve": True},
    "triggers": [
        {"on_match": "Do you trust the contents of this project\\?|Yes, I trust", "action": "Enter", "once": True}
    ],
    "timeline": [
        {"show_card": {"tag": "Module 5", "title": "Building ADK Agents with agents-cli", "desc": "Agent scaffolding, eval benchmarks, model routing, and production deployment", "duration": 2.5}},
        {"show_card": {"tag": "Section 5.1", "title": "Scaffolding ADK Agents", "desc": "agents-cli scaffold create with prototype and deployment options", "duration": 2.0}},
        {"launch": {"command": "bash"}},
        {"type": {"text": "cd /tmp/agents-cli-walkthrough", "speed": 0.035, "send_key": "Enter"}},
        {"pause": 1.5},
        {"type": {"text": "agy --dangerously-skip-permissions -p \"Explain how agents-cli scaffold create meeting-notes --agent adk generates an enterprise agent codebase with tools and schemas.\" --print-timeout 90s", "speed": 0.035, "send_key": "Enter"}},
        {"wait_for_idle": {"timeout": 90.0, "reading_pause": 2.5}},
        {"show_card": {"tag": "Section 5.2", "title": "The 7-Phase ADK Lifecycle & Evaluation", "desc": "From Scaffold to Eval-Fix loops and Cloud Run Deployment", "duration": 2.0}},
        {"type": {"text": "agy --dangerously-skip-permissions -p \"Walk through the 7-phase ADK lifecycle and explain how automated evaluation benchmarks (eval generate, eval grade) enforce production quality gates.\" --print-timeout 90s", "speed": 0.035, "send_key": "Enter"}},
        {"wait_for_idle": {"timeout": 90.0, "reading_pause": 2.5}},
        {"show_card": {"tag": "Complete", "title": "Module 5 Walkthrough Complete", "desc": "ADK agent lifecycle mastered", "duration": 2.5}}
    ]
}

def main():
    scenarios_dir = REPO_ROOT / "scenarios"
    scenarios_dir.mkdir(parents=True, exist_ok=True)
    for fname, data in sorted(SCENARIOS.items()):
        fpath = scenarios_dir / fname
        with open(fpath, "w", encoding="utf-8") as fp:
            yaml.dump(data, fp, default_flow_style=False, sort_keys=False, allow_unicode=True, width=1000)
        print(f"Generated {fpath} ({len(data.get('timeline', []))} steps)")
    print(f"\nSuccessfully generated all {len(SCENARIOS)} scenario manifests!")

if __name__ == "__main__":
    main()
