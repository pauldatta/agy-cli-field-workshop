# agy-cli 速查表

> 本工作坊涵盖的所有内容的快速参考。
> 所有命令均已根据 [antigravity.google/docs](https://antigravity.google/docs/cli-overview) 验证。

---

## 安装与版本

```bash
curl -fsSL https://antigravity.google/cli/install.sh | bash
agy --help         # Show all flags and subcommands
agy changelog      # Show release notes
agy update         # Self-update
agy install        # Configure PATH and shell aliases
```

---

## 启动模式

| 模式 | 命令 | 何时使用 |
| :-- | :-- | :-- |
| **交互模式** | `agy` | 默认 — 完整的对话会话 |
| **预设交互模式** | `agy -i "<提示词>"` | 以特定方向开始，然后继续对话 |
| **打印（无头模式）** | `agy -p "<提示词>"` | 单次执行，通过管道输出到标准输出 |
| **继续上一次** | `agy -c` | 恢复最近的会话 |
| **按 ID 恢复** | `agy --conversation <id>` | 恢复特定的历史会话 |
| **会话内恢复** | `/resume` 或 `/switch` | 在不离开 agy 的情况下切换会话 |

---

## 关键标志

> 来源：[`agy --help`](https://antigravity.google/docs/cli-getting-started) · [cli-using](https://antigravity.google/docs/cli-using)

| 标志 | 简写 | 描述 |
| :-- | :-- | :-- |
| `--print "<prompt>"` | `-p` | 非交互式单次提示词 |
| `--prompt-interactive "<prompt>"` | `-i` | 带有初始提示词的交互式会话 |
| `--continue` | `-c` | 恢复最近的对话 |
| `--conversation <id>` | — | 通过对话 ID 恢复 |
| `--add-dir <path>` | — | 将目录添加到工作区（可重复） |
| `--sandbox` | — | 启用终端沙盒限制 |
| `--dangerously-skip-permissions` | — | 自动批准所有工具请求（仅限 CI） |
| `--print-timeout <duration>` | — | 打印模式的超时时间（默认：5分钟） |
| `--log-file <path>` | — | 覆盖日志输出路径 |

> **注意：** 模型选择和严格模式通过 `/model` 和 `/permissions` 斜杠命令设置，而不是 CLI 标志。请参阅 [功能文档](https://antigravity.google/docs/cli-features)。

---

## 斜杠命令（交互模式）

> 来源：[CLI 功能 — 核心斜杠命令](https://antigravity.google/docs/cli-features) · [使用 Antigravity CLI](https://antigravity.google/docs/cli-using)

| 命令 | 类别 | 用途 |
| :-- | :-- | :-- |
| `/resume` (`/switch`) | 会话 | 打开会话选择器以恢复或切换会话 |
| `/rewind` (`/undo`) | 会话 | 将会话历史记录回滚到之前的检查点 |
| `/fork` | 会话 | 将当前会话分支到一个平行的隔离工作区 — 尝试有风险的步骤而不影响原始内容 |
| `/rename <name>` | 会话 | 重命名活动会话线程 |
| `/permissions` | 配置 | 设置自治级别：`request-review`、`always-proceed`、`strict` |
| `/model` | 配置 | 选择默认推理模型（跨会话持久化） |
| `/config` (`/settings`) | 配置 | 打开全屏设置覆盖层 |
| `/keybindings` | 配置 | 打开交互式键盘快捷键编辑器 |
| `/statusline` | 配置 | 自定义实时 CLI 状态栏指示器 |
| `/tasks` | 监控 | 监控、查看日志或终止后台任务 |
| `/skills` | 监控 | 浏览本地和全局代理技能 |
| `/mcp` | 监控 | 配置和管理 MCP 服务器 |
| `/agents` | 监控 | 查看、管理和批准子代理操作 |
| `/open <path>` | 实用工具 | 在您首选的外部编辑器中打开文件 |
| `/usage` | 实用工具 | 打开内联交互式帮助手册 |
| `/logout` | 账户 | 登出并清除缓存的凭据 |

---

## 快速提示

> 来源：[使用 Antigravity CLI — 快速提示与快捷键绑定](https://antigravity.google/docs/cli-using)

| 快捷键 / 提示 | 操作 |
| :-- | :-- |
| `@` | 文件路径自动补全（输入 `@` 触发路径建议） |
| `!` | 直接从提示词运行终端命令 |
| `esc esc` | 清空提示词输入框（当没有活动的流式传输时） |
| `?` | 获取帮助并列出所有斜杠命令 |
| `alt+enter` / `shift+enter` | 插入换行符而不提交 |
| `ctrl+g` | 在默认的 shell 编辑器中编辑提示词 |
| `ctrl+l` | 清除 TUI 屏幕 |
| `ctrl+d` | 退出 CLI 会话 |
| `ctrl+z` | 将 CLI 挂起到终端后台 |
| `ctrl+j`（在 `/agents` 中） | 跳转到下一个待处理的子代理审批 |
| `ctrl+k` | 从主对话中快速批准待处理的子代理权限 |

---

## 插件命令

```bash
# List all active plugins (JSON)
agy plugin list

# Import from Gemini CLI
agy plugin import gemini

# Import from Claude Code
agy plugin import claude

# Force re-import (after plugin updates)
agy plugin import gemini --force

# Install a plugin
agy plugin install <name>
agy plugin install <name>@<version>

# Enable / disable
agy plugin enable <name>
agy plugin disable <name>

# Validate a plugin directory
agy plugin validate ./my-plugin

# Generate marketplace link
agy plugin link <marketplace> <target>
```

---

## 边车 (Sidecars)

> AGY 为您管理的后台进程 —— 启动、重启并独立于任何对话运行。来源：[antigravity.google/docs/sidecars](https://antigravity.google/docs/sidecars)

```bash
# Config locations:
~/.gemini/config/sidecars/<name>/sidecar.json                         # global
~/.gemini/config/plugins/<plugin>/sidecars/<name>/sidecar.json        # plugin-scoped

# Enable (disabled by default) — edit ~/.gemini/config/config.json:
#   { "sidecars": { "<name>": { "enabled": true } } }

# Check logs:
ls ~/.gemini/antigravity-cli/sidecar_data/<name>/logs/

# agentapi (auto-available inside sidecars):
agentapi new-conversation "<prompt>"
agentapi send-message <conversation_id> "<prompt>"
```

极简 `sidecar.json` —— 后台脚本：

```json
{ "command": "python3", "args": ["worker.py"], "restart_policy": "on-failure" }
```

极简 `sidecar.json` —— 定时循环任务：

```json
{
  "builtin": "schedule",
  "args": ["0 9 * * 1-5", "agentapi", "new-conversation", "Summarise open PRs."]
}
```

---

## 工作区与上下文

```bash
# Project config directory:
.agents/                    # settings.json, mcp.json, hooks.json, rules.md, skills/, plugins/

# Global config directory:
~/.gemini/config/           # settings.json, mcp.json, hooks.json, rules.md, skills/, plugins/

# User settings:
~/.gemini/antigravity-cli/settings.json

# Context file (hierarchical: cwd → parent → home):
AGENTS.md

# agy also reads:
.gemini/                    # Gemini CLI config (compatible)
```

### AGENTS.md 模式

```markdown
# Project Context

Brief description of what this project is.

## Conventions
- Language: TypeScript, Node 20
- Testing: Jest + Supertest
- DO NOT run database migrations without explicit approval
```

---

## 实用模式

```bash
# Review staged changes before commit
git diff --cached | agy -p "Review for bugs, security issues, missing tests."

# Generate docs for a file
cat src/api.ts | agy -p "Generate OpenAPI documentation for all exported functions."

# Analyze logs
tail -n 500 app.log | agy -p "Group these errors by root cause. Output as JSON."

# Multi-dir cross-repo analysis
agy --add-dir ../api --add-dir ../frontend \
    -p "Map data flow from frontend form submission to database write."

# Full headless CI audit (safe)
agy --sandbox --dangerously-skip-permissions \
    -p "Audit for hardcoded secrets and insecure patterns." \
    --print-timeout 5m > audit.md

# Schedule a recurring task (in interactive mode)
# > Schedule a daily code quality report at 9am weekdays.
```

---

## 多代理模式

```text
# Spawn parallel subagents (in interactive mode)
> Spawn a security auditor and a performance auditor in parallel (branch mode).

# Adversarial review
> Spawn an adversarial reviewer subagent — its job is to find reasons to NOT merge this PR.

# Steer mid-task
/btw Focus only on the authentication module, skip the frontend.

# Background task
> In the background, audit all dependencies for known CVEs. Notify me when done.
```

---

## 打印模式管道示例

```bash
# Step 1: plan
agy -p "Create a refactoring plan for moving from callbacks to async/await. JSON output." \
  > plan.json

# Step 2: execute
cat plan.json | agy -p "Execute step 1 of this plan."

# Batch: process multiple files
for f in src/*.ts; do
  agy --add-dir "$(dirname $f)" \
      -p "Add JSDoc to all exported functions in $(basename $f)."
done
```

---

## 官方文档

| 主题 | 链接 |
| :-- | :-- |
| CLI 概述 | [antigravity.google/docs/cli-overview](https://antigravity.google/docs/cli-overview) |
| 入门指南 | [antigravity.google/docs/cli-getting-started](https://antigravity.google/docs/cli-getting-started) |
| 使用 Antigravity CLI（设置、技巧、快捷键） | [antigravity.google/docs/cli-using](https://antigravity.google/docs/cli-using) |
| 功能（插件、沙盒、斜杠命令、子代理） | [antigravity.google/docs/cli-features](https://antigravity.google/docs/cli-features) |
| 从 Gemini CLI 迁移 | [antigravity.google/docs/gcli-migration](https://antigravity.google/docs/gcli-migration) |
| 权限 | [antigravity.google/docs/permissions](https://antigravity.google/docs/permissions) |
| 严格模式 | [antigravity.google/docs/strict-mode](https://antigravity.google/docs/strict-mode) |
| 插件 | [antigravity.google/docs/plugins](https://antigravity.google/docs/plugins) |
| MCP | [antigravity.google/docs/mcp](https://antigravity.google/docs/mcp) |
| 技能 | [antigravity.google/docs/skills](https://antigravity.google/docs/skills) |
| 规则 | [antigravity.google/docs/rules-workflows](https://antigravity.google/docs/rules-workflows) |
| 钩子 | [antigravity.google/docs/hooks](https://antigravity.google/docs/hooks) |
| 边车 (Sidecars) | [antigravity.google/docs/sidecars](https://antigravity.google/docs/sidecars) |
| 子代理 | [antigravity.google/docs/subagents](https://antigravity.google/docs/subagents) |
| 企业级 | [antigravity.google/docs/enterprise](https://antigravity.google/docs/enterprise) |
