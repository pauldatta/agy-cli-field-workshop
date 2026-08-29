# 练习 7 — 迁移演练

> **模块：** 附录 — 迁移指南
> **时间：** 20 分钟
> **形式：** 个人或结对

---

## 目标

逐步演练一个真实的 Gemini CLI 项目目录，并将其迁移到 AGY CLI。您将更新配置文件位置、MCP 服务器定义、钩子事件名称以及 AGENTS.md 内容 —— 然后使用 `migration-validator` 子代理进行验证。

---

## 背景

当团队从 Gemini CLI 迁移到 AGY CLI 时，有四个常见的故障点：

| 故障内容 | 原因 |
| :-- | :-- |
| 钩子事件 `SessionStart`、`BeforeTool`、`AfterTool` | 重命名为 `PreInvocation`、`PreToolUse`、`PostToolUse` |
| `settings.json` 中的 MCP `url` 键 | AGY 在单独的 `mcp.json` 中使用 `serverUrl` |
| `.gemini/` 项目配置目录 | AGY 使用 `.agents/` |
| 脚本中的 `gemini` 二进制文件 | 必须更新为 `agy` |

---

## 环境设置

您需要一个示例 Gemini CLI 项目来进行迁移。创建启动项目：

```bash
mkdir ~/gemini-migration-lab && cd ~/gemini-migration-lab

# Create a legacy Gemini CLI settings.json
mkdir -p .gemini/hooks
cat > .gemini/settings.json << 'EOF'
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "github-mcp-server"],
      "env": { "GITHUB_PERSONAL_ACCESS_TOKEN": "$GITHUB_TOKEN" }
    }
  },
  "hooks": {
    "SessionStart": [
      {
        "hooks": [{
          "name": "session-context",
          "type": "command",
          "command": "$GEMINI_PROJECT_DIR/.gemini/hooks/session-context.sh",
          "timeout": 3000
        }]
      }
    ],
    "BeforeTool": [
      {
        "matcher": "write_file|replace_in_file",
        "hooks": [{
          "name": "secret-scanner",
          "type": "command",
          "command": "$GEMINI_PROJECT_DIR/.gemini/hooks/secret-scanner.sh",
          "timeout": 2000
        }]
      }
    ]
  }
}
EOF

# Create a legacy GEMINI.md
cat > .gemini/GEMINI.md << 'EOF'
# Project Context

This is a Node.js API service. Always run `npm test` after changes.
Use gemini for code reviews before merging PRs.
EOF

# Create a CI script that calls the old binary
mkdir -p .github/workflows
cat > scripts/review.sh << 'EOF'
#!/usr/bin/env bash
gemini -p "Review the diff: $(git diff HEAD~1)" > review.md
EOF
```

---

## 第 1 部分 — 手动迁移 (10 分钟)

自行迁移项目：

### 第 1 步：将配置移动到 AGY 目录

```bash
mkdir -p .agents/hooks
# AGY reads .agents/ instead of .gemini/ for project config
cp .gemini/GEMINI.md .agents/AGENTS.md
cp .gemini/settings.json .agents/settings.json
```

### 第 2 步：分离 MCP 配置

```bash
# AGY uses mcp.json, not mcpServers in settings.json
cat > .agents/mcp_config.json << 'EOF'
{
  "mcpServers": {
    "github": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "github-mcp-server"],
      "env": { "GITHUB_PERSONAL_ACCESS_TOKEN": "$GITHUB_TOKEN" }
    }
  }
}
EOF
```

### 第 3 步：重写 settings.json 中的钩子事件名称

```json
{
  "hooks": {
    "PreInvocation": [
      {
        "hooks": [{
          "name": "session-context",
          "type": "command",
          "command": "$AGY_PROJECT_DIR/.agents/hooks/session-context.sh",
          "timeout": 3000
        }]
      }
    ],
    "PreToolUse": [
      {
        "matcher": "write_file|edit",
        "hooks": [{
          "name": "secret-scanner",
          "type": "command",
          "command": "$AGY_PROJECT_DIR/.agents/hooks/secret-scanner.sh",
          "timeout": 2000
        }]
      }
    ]
  }
}
```

### 第 4 步：更新二进制文件引用

```bash
sed -i 's/\bgemini\b/agy/g' scripts/review.sh
```

---

## 第 2 部分 — 使用迁移验证器代理进行验证（5 分钟）

启动 AGY CLI 并运行迁移验证器：

```bash
cd ~/gemini-migration-lab
agy
```

在 AGY REPL 中：

```text
Use the migration-validator agent to check this project directory for any remaining Gemini CLI configuration.
```

`migration-validator` 子代理将检查：

- [ ] 钩子事件名称（没有 `SessionStart`、`BeforeTool`、`AfterTool`）
- [ ] MCP 格式（SSE 使用 `serverUrl`，存在 `type` 字段）
- [ ] 二进制文件引用（脚本中使用 `agy` 而不是 `gemini`）
- [ ] 配置路径（使用 `.agents/` 而不是 `.gemini/`）

---

## 第 3 部分 — 讨论 (5 分钟)

**思考问题：**

1. 如果你忘记更新钩子事件名称，CI 中最先崩溃的会是什么？
2. 为什么 AGY 将 MCP 配置分离到 `mcp.json` 中，而不是将其捆绑在 `settings.json` 中？
3. 如果你有一个包含 10 个项目的单体仓库，你的迁移脚本会是什么样子的？

---

## 额外挑战

向迁移后的项目添加一个 `PreToolUse` 钩子，以阻止代理在未经确认的情况下调用 `git push`。使用钩子的 `decision: deny` 模式。

参考 [`samples/hooks/secret-scanner.sh`](https://github.com/pauldatta/agy-cli-field-workshop/blob/main/samples/hooks/secret-scanner.sh) 作为决策模式的模板。

---

## 核心要点

| Gemini CLI | AGY CLI |
| :-- | :-- |
| `SessionStart` | `PreInvocation` |
| `BeforeTool` | `PreToolUse` |
| `AfterTool` | `PostToolUse` |
| `replace_in_file` 工具 | `edit` 工具 |
| `.gemini/` 项目目录 | `.agents/` 项目目录 |
| `GEMINI.md` | `AGENTS.md` |
| `settings.json` MCP 块 | 包含 `serverUrl` 的 `mcp.json` |
| 用于 SSE 的 `url:` | 用于 SSE 的 `serverUrl:` |
| `gemini` 二进制文件 | `agy` 二进制文件 |
