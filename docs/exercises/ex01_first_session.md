# Exercise 1: First Session

> **Duration:** 15 min (Fast: 10 min · Average: 15 min · Thorough: 20 min) | **Module:** 1 — SDLC Productivity

---

## Objective

Launch agy-cli, explore an unfamiliar codebase with interactive questions and `@` path autocomplete, and create a production `AGENTS.md` that makes every future session smarter.

---

## Setup

You need a Git repository to work with. Use the sample app in this repo or bring your own:

```bash
# Option A: Use this workshop repository (you're already here)
# No need to cd — just start agy from the repo root

# Option B: Use any of your own Git repos
cd /path/to/your/project
```

---

## Part 1: First Interactive Session (5 min)

```bash
agy
```

At the prompt, ask:

```text
> What does this project do? Give me a one-paragraph summary.
```

Then follow up with interactive file mentions using `@` autocomplete:

```text
> What are the top 3 files I should read to understand the core logic?
```

```text
> @README.md How does the documented architecture match the actual codebase implementation?
```

Check active session context and token usage:

```text
> /context
```

**Notice:** agy reads and indexes your git repository automatically without requiring manual file uploads.

---

## Part 2: Deep Dive (5 min)

Pick one file from agy's suggestions and go deeper:

```text
> Explain [filename] in detail. Walk me through what each function does and how they connect.
```

```text
> If I wanted to add a health-check endpoint or logging middleware, where would I start?
```

---

## Part 3: Create AGENTS.md (5 min)

Now codify what you've learned so every future session starts with context:

```text
> Based on our conversation, generate an AGENTS.md file for this project. Include: project purpose, tech stack, key conventions, and anything I should tell an AI assistant before asking it to modify this code.
```

Review what agy generates. Edit it if anything is wrong. Then write it:

```text
> Write that AGENTS.md to the project root.
```

Start a new headless session and verify the context is loaded:

```bash
agy --print "What do you know about this project?" --print-timeout 30s
```

---

## ⚠️ Field Gotchas & Failure Modes

!!! warning "Common Workshop Gotchas"
    1. **Non-Git Directories:** If you launch `agy` in a folder without a `.git/` directory, repository auto-indexing and branch detection are disabled. Always initialize git (`git init`) or run from a git root.
    2. **Vague AGENTS.md:** If you simply ask for "an AGENTS.md", the model may produce generic boilerplate. Ensure your prompt asks for *project purpose, architecture rules, test commands, and styling conventions*.
    3. **First-Launch Auth:** On initial launch, your browser will open for Google Sign-In. If you are in a remote SSH session without a GUI browser, `agy` will print an authorization URL directly in your terminal.

---

## Completion Criteria

- [ ] agy launched and responded in interactive mode
- [ ] Explored at least 3 follow-up questions using `@` autocomplete and `/context`
- [ ] AGENTS.md exists at the project root with concrete conventions
- [ ] `agy --print "What do you know about this project?"` returns accurate info

