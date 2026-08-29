# Antigravity CLI Field Workshop

[![Antigravity CLI](https://img.shields.io/badge/Antigravity_CLI-v1.1.22-blue.svg)](https://antigravity.google)
[![SDK](https://img.shields.io/badge/google--antigravity-v0.1.15-purple.svg)](https://antigravity.google)
[![Updated](https://img.shields.io/badge/Updated-August_2026-success.svg)](#)
[![Languages](https://img.shields.io/badge/Languages-EN%20%7C%20KO%20%7C%20ID%20%7C%20ZH-orange.svg)](#)

> **Hands-on field workshop for Antigravity CLI.**

📚 **Official Docs:** [antigravity.google/docs](https://www.antigravity.google/docs/cli-overview)

---

## Workshop Overview

This workshop teaches engineers how to use agy-cli as a daily-driver AI coding assistant and automation tool. It covers five modules, from first interactive session to building and deploying production ADK agents.

| Module | Topic | Duration |
| :-- | :-- | :-- |
| **1. SDLC Productivity** | First session, code understanding, refactoring, test generation, review + plugins | 75 min |
| **2. Legacy Modernization ⭐** | Strict mode, agent self-onboarding, .NET/Java migration, `/rewind` | 90 min |
| **3. Building AGY Agents** | Antigravity SDK, Agent/Tools/Hooks, session state, Cloud Run deploy | 90 min |
| **4. Multi-Agent & Advanced** | Subagents, `/btw` mid-task steering, scheduling, session resumption | 60 min |
| **5. ADK Agents with agents-cli** | Scaffold, build, evaluate, deploy ADK agents via agents-cli | 75 min |

Total: ~7 hours (extended) · Full day: Modules 1–4 (~5.5 hrs) · Half-day: Modules 1–2 · Lightning: Module 1 + M2 highlights

---

## Quick Start

```bash
# Install agy-cli (if not already installed)
curl -fsSL https://antigravity.google/cli/install.sh | bash

# Clone the workshop repo
git clone https://github.com/pauldatta/agy-cli-field-workshop.git
cd agy-cli-field-workshop

# Validate your environment
chmod +x scripts/check-env.sh
make check-env

# Serve the docs locally
make install-deps
make serve
```

Open [http://localhost:8000](http://localhost:8000) for the workshop site.

---

## Repository Structure

```bash
├── docs/                    # Workshop documentation (MkDocs Material)
│   ├── index.md             # Home page
│   ├── setup.md             # Environment setup
│   ├── sdlc-productivity.md # Module 1
│   ├── legacy-modernization.md # Module 2
│   ├── agy-sdk.md           # Module 3
│   ├── multi-agent-advanced.md # Module 4
│   ├── agents-cli.md        # Module 5
│   ├── cheatsheet.md        # Reference
│   ├── plugin-ecosystem.md  # Reference
│   ├── devops-automation.md # Reference
│   └── facilitator-guide.md
├── exercises/               # Hands-on exercises (12 total)
├── demos/                   # VHS tape scripts for terminal GIFs
├── samples/                 # Sample configs and scripts
├── scripts/
│   ├── check-env.sh         # Pre-workshop validator
│   ├── precommit-checks.sh  # Structural integrity checks
│   └── detect-drift.sh      # Ground truth drift detection
├── AUDIT.md                 # Ground truth for upstream claims
├── VERIFICATION.md          # Maintenance playbook
├── Makefile
└── mkdocs.yml
```

---

## Delivery Formats

| Format | Modules | Duration |
| :-- | :-- | :-- |
| ⚡ Lightning | 1 + 2 highlights | 1.5 hrs |
| 📋 Half-day | 1 + 2 | 2.5 hrs |
| 📦 Full day | Modules 1–4 | ~5.5 hrs |
| 🏗️ Extended | All 5 modules + open lab | 7 hrs |

See [Facilitator Guide](docs/facilitator-guide.md) for delivery instructions.

---

## Prerequisites

- agy-cli installed and authenticated (see [Environment Setup](docs/setup.md))
- Familiarity with terminal, Git, and basic coding workflows

---

*Built with [MkDocs Material](https://squidfundamentals.github.io/mkdocs-material/).*
