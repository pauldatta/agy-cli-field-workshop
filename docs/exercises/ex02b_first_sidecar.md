# Exercise 2B: Your First Sidecar

> **Duration:** 20 min | **Module:** 2 — Plugin Ecosystem

---

## Objective

Build a scheduled **daily standup sidecar** that fires at 9am Monday–Friday, creates a new AGY conversation, and asks it to summarise yesterday's git commits across your repos.

---

## Background

Sidecars are persistent background processes that AGY manages for you — they launch automatically when AGY starts, restart on crash, and run independently of your active conversation. The `schedule` builtin takes a cron expression and a command to run on that schedule.

---

## Part 1: Create the Sidecar Config (5 min)

Create the sidecar directory and configuration file:

```bash
mkdir -p ~/.gemini/config/sidecars/standup
```

Create `~/.gemini/config/sidecars/standup/sidecar.json`:

```json
{
  "description": "Daily standup — summarises yesterday's git commits",
  "builtin": "schedule",
  "args": [
    "0 9 * * 1-5",
    "agentapi",
    "new-conversation",
    "Summarise all git commits from yesterday across my repos. Group by repo, list the most impactful changes first, and flag any commits that touch security-sensitive files."
  ]
}
```

**Key decisions:**

- `builtin: "schedule"` — uses AGY's built-in cron scheduler instead of a raw command
- `0 9 * * 1-5` — fires at 09:00 Monday through Friday
- `agentapi new-conversation` — programmatically opens a new AGY conversation with your standup prompt

---

## Part 2: Enable the Sidecar (5 min)

Sidecars are **disabled by default**. Enable it in `~/.gemini/config/config.json`:

```bash
# View current config (create if it doesn't exist)
cat ~/.gemini/config/config.json 2>/dev/null || echo '{}'
```

Edit `~/.gemini/config/config.json` to include the sidecar entry:

```json
{
  "sidecars": {
    "standup": {
      "enabled": true
    }
  }
}
```

> **Note:** If you already have content in `config.json`, merge the `sidecars` block into your existing JSON — don't replace the file.

---

## Part 3: Verify the Sidecar (5 min)

Start AGY and check that the sidecar was discovered:

```bash
agy
```

Inside the session, ask:

```text
> What sidecars are currently configured? Is the standup sidecar active?
```

Check the sidecar's runtime data directory:

```bash
ls -la ~/.gemini/antigravity-cli/sidecar_data/standup/logs/
```

If the directory exists, the sidecar has been registered. Log files appear here with timestamped stdout/stderr output after each scheduled run.

> **Tip:** The sidecar won't fire until 9am on a weekday. To test immediately, temporarily change the cron to `* * * * *` (every minute), wait 60 seconds, then check logs. **Remember to change it back.**

---

## Part 4: Inspect the Runtime Layout (5 min)

Examine the full sidecar data structure:

```bash
# The sidecar runtime directory layout
find ~/.gemini/antigravity-cli/sidecar_data/standup/ -type f 2>/dev/null
```

Expected structure:

```text
~/.gemini/antigravity-cli/sidecar_data/standup/
├── data/     ← persistent storage (ANTIGRAVITY_EXECUTABLE_DATA_DIR env var)
├── logs/     ← timestamped stdout/stderr logs
└── events/   ← JSON records of agentapi calls
```

---

## Stretch Goal: File-Watcher Sidecar

Add a second sidecar that uses `command: python3` instead of the `schedule` builtin. This one watches a local file for changes and sends a message to an existing conversation when it detects a diff.

Create `~/.gemini/config/sidecars/file-watcher/sidecar.json`:

```json
{
  "description": "Watches a target file and alerts on changes",
  "command": "python3",
  "args": ["watch.py"],
  "restart_policy": "on-failure",
  "env": {
    "WATCH_FILE": "/path/to/your/important-file.yaml"
  }
}
```

Create `~/.gemini/config/sidecars/file-watcher/watch.py`:

```python
import os
import time
import hashlib
import subprocess

WATCH_FILE = os.environ.get("WATCH_FILE", "")
POLL_INTERVAL = 5  # seconds

def file_hash(path: str) -> str:
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()

def main():
    if not os.path.exists(WATCH_FILE):
        print(f"File not found: {WATCH_FILE}")
        return

    last_hash = file_hash(WATCH_FILE)
    print(f"Watching {WATCH_FILE} (initial hash: {last_hash[:12]}...)")

    while True:
        time.sleep(POLL_INTERVAL)
        current_hash = file_hash(WATCH_FILE)
        if current_hash != last_hash:
            print(f"Change detected! {last_hash[:12]} -> {current_hash[:12]}")
            subprocess.run([
                "agentapi", "new-conversation",
                f"The file {WATCH_FILE} was modified. Please review the changes."
            ])
            last_hash = current_hash

if __name__ == "__main__":
    main()
```

Enable it in `~/.gemini/config/config.json`:

```json
{
  "sidecars": {
    "standup": {
      "enabled": true
    },
    "file-watcher": {
      "enabled": true
    }
  }
}
```

---

## Completion Criteria

- [ ] `~/.gemini/config/sidecars/standup/sidecar.json` exists with `schedule` builtin and `0 9 * * 1-5` cron
- [ ] `~/.gemini/config/config.json` has `sidecars.standup.enabled: true`
- [ ] AGY recognises the sidecar (confirmed via session query or log directory presence)
- [ ] Sidecar runtime directory exists at `~/.gemini/antigravity-cli/sidecar_data/standup/`
- [ ] *(Stretch)* File-watcher sidecar created with `command: python3` and a working `watch.py`
