# 练习 2B：你的第一个 Sidecar

> **时长：** 20 分钟 | **模块：** 2 — 插件生态系统

---

## 目标

构建一个定时执行的 **每日站会 sidecar**，在周一至周五上午 9 点触发，创建一个新的 AGY 对话，并要求它总结昨天在你所有代码仓库中的 git 提交。

---

## 背景

Sidecar 是 AGY 为您管理的持久后台进程——它们会在 AGY 启动时自动启动，在崩溃时重新启动，并且独立于您的活动对话运行。`schedule` 内置命令接受一个 cron 表达式以及一个要按照该时间表运行的命令。

---

## 第 1 部分：创建 Sidecar 配置 (5 分钟)

创建 sidecar 目录和配置文件：

```bash
mkdir -p ~/.gemini/config/sidecars/standup
```

创建 `~/.gemini/config/sidecars/standup/sidecar.json`：

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

**关键决策：**

- `builtin: "schedule"` — 使用 AGY 内置的 cron 调度程序，而不是原始命令
- `0 9 * * 1-5` — 在周一至周五的 09:00 触发
- `agentapi new-conversation` — 以编程方式打开一个新的 AGY 会话，并使用你的站会提示词

---

## 第 2 部分：启用 Sidecar（5 分钟）

Sidecar **默认处于禁用状态**。请在 `~/.gemini/config/config.json` 中启用它：

```bash
# View current config (create if it doesn't exist)
cat ~/.gemini/config/config.json 2>/dev/null || echo '{}'
```

编辑 `~/.gemini/config/config.json` 以包含 sidecar 条目：

```json
{
  "sidecars": {
    "standup": {
      "enabled": true
    }
  }
}
```

> **注意：** 如果您的 `config.json` 中已有内容，请将 `sidecars` 块合并到您现有的 JSON 中——不要替换该文件。

---

## 第 3 部分：验证 Sidecar（5 分钟）

启动 AGY 并检查是否发现了该 Sidecar：

```bash
agy
```

在会话中，提问：

```text
> What sidecars are currently configured? Is the standup sidecar active?
```

检查 Sidecar 的运行时数据目录：

```bash
ls -la ~/.gemini/antigravity-cli/sidecar_data/standup/logs/
```

如果该目录存在，则说明 Sidecar 已注册。每次计划运行后，带有时间戳的 stdout/stderr 输出日志文件将出现在这里。

> **提示：** Sidecar 在工作日上午 9 点之前不会触发。要立即进行测试，请暂时将 cron 更改为 `* * * * *`（每分钟），等待 60 秒，然后检查日志。**记得将其改回。**

---

## 第 4 部分：检查运行时布局（5 分钟）

检查完整的 sidecar 数据结构：

```bash
# The sidecar runtime directory layout
find ~/.gemini/antigravity-cli/sidecar_data/standup/ -type f 2>/dev/null
```

预期结构：

```text
~/.gemini/antigravity-cli/sidecar_data/standup/
├── data/     ← persistent storage (ANTIGRAVITY_EXECUTABLE_DATA_DIR env var)
├── logs/     ← timestamped stdout/stderr logs
└── events/   ← JSON records of agentapi calls
```

---

## 延伸目标：文件监视器 Sidecar

添加第二个 Sidecar，它使用 `command: python3` 而不是 `schedule` 内置功能。这个 Sidecar 监视本地文件的更改，并在检测到差异时向现有对话发送消息。

创建 `~/.gemini/config/sidecars/file-watcher/sidecar.json`：

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

创建 `~/.gemini/config/sidecars/file-watcher/watch.py`：

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

在 `~/.gemini/config/config.json` 中启用它：

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

## 完成标准

- [ ] `~/.gemini/config/sidecars/standup/sidecar.json` 存在，包含 `schedule` 内置功能和 `0 9 * * 1-5` cron 表达式
- [ ] `~/.gemini/config/config.json` 包含 `sidecars.standup.enabled: true`
- [ ] AGY 能够识别该 Sidecar（通过会话查询或日志目录的存在来确认）
- [ ] Sidecar 运行时目录存在于 `~/.gemini/antigravity-cli/sidecar_data/standup/`
- [ ] *(扩展目标)* 创建了文件监听 Sidecar，使用 `command: python3` 和一个可运行的 `watch.py`
