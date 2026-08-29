# Environment Setup

> Complete this before starting any module. Takes ~15 minutes.

---

## System Requirements

| Component | Minimum | Notes |
| :-- | :-- | :-- |
| **agy** | Latest | Install instructions below |
| **Git** | v2.30+ | For exercise repos |
| **Terminal** | Any | iTerm2, macOS Terminal, or VS Code integrated |
| **jq** | Optional | Useful for parsing `--print` JSON output |

---

## Step 1: Install agy

> 📖 Full instructions: [Getting Started docs](https://www.antigravity.google/docs/cli-getting-started)

### macOS / Linux

```bash
curl -fsSL https://antigravity.google/cli/install.sh | bash
```

### Windows

```powershell
# PowerShell
irm https://antigravity.google/cli/install.ps1 | iex

# Or via WSL (recommended)
curl -fsSL https://antigravity.google/cli/install.sh | bash
```

After install, verify the binary is available:

```bash
# Verify the binary is in your PATH
which agy

# Confirm the version
agy --version
```

---

## Step 2: Authentication

agy uses **browser-based Google Sign-In**. On first run, it will:

- **Local machine:** Automatically open your default browser for sign-in.
- **SSH / remote session:** Print a URL to paste into any browser, then paste the auth code back into the terminal.

```bash
# Start agy — auth will trigger automatically on first run
agy
```

To sign out:

```text
# Run this inside an agy interactive session (not in your terminal):
/logout
```

> 📖 For enterprise authentication via GCP project, see the [Enterprise docs](https://www.antigravity.google/docs/enterprise).

Once auth is configured, run a quick smoke test:

```bash
agy --print "Say 'Workshop ready!' in exactly two words." --print-timeout 30s
```

Expected output: `Workshop ready!`

---

## Step 3: Initialize Your Project Workspace

agy auto-discovers project config by walking up from your current directory, looking for a `.agents/` folder. Create one for the workshop:

```bash
# Clone the workshop exercises repo
git clone https://github.com/pauldatta/agy-cli-field-workshop.git
cd agy-cli-field-workshop

# agy will create .agents/ on first run
agy --print "List the files in the current directory."
```

You'll see a `.agents/` folder created with project config files (settings.json, mcp_config.json, etc.).

!!! info ".gemini/ compatibility"
    agy also reads `.gemini/` directories — useful if you already have a Gemini CLI project setup. Both config locations are respected.

---

## Step 4: Verify Everything

```bash
# Check agy is accessible
agy --help

# List installed plugins (output is JSON)
agy plugin list

# Pretty-print the plugin list (works once plugins are installed in Module 2)
# agy plugin list | python3 -m json.tool

# Quick print-mode smoke test
agy --print "What is 2 + 2?" --print-timeout 30s
```

Checklist before the workshop starts:

- [ ] `agy --help` shows flags and subcommands
- [ ] `agy plugin list` returns successfully
- [ ] `agy --print "..."` returns a response

---

## Troubleshooting

| Issue | Solution |
| :-- | :-- |
| `agy: command not found` | Check that the binary is in your PATH. Run `echo $PATH` and ensure the install dir is included. Re-run the install script if needed |
| Auth errors / browser doesn't open | For SSH sessions, copy the printed URL manually. For local, check default browser settings. Run `/logout` and retry |
| `agy plugin list` returns `No imported plugins.` | Expected on a fresh install (not JSON). You'll populate plugins in Module 2 |
| Slow first response | First run may be slower as agy indexes your workspace |
| Config not loading | Check `~/.gemini/antigravity-cli/settings.json` (user settings) and `.agents/` (project settings) |

---

## Next Step

→ Start with **[Module 1: SDLC Productivity](sdlc-productivity.md)**
