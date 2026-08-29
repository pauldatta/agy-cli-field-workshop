# 环境设置

> 在开始任何模块之前请完成此操作。大约需要 15 分钟。

---

## 系统要求

| 组件 | 最低要求 | 备注 |
| :-- | :-- | :-- |
| **agy** | 最新版本 | 安装说明见下文 |
| **Git** | v2.30+ | 用于练习仓库 |
| **终端** | 任意 | iTerm2、macOS Terminal 或 VS Code 集成终端 |
| **jq** | 可选 | 用于解析 `--print` JSON 输出 |

---

## 第 1 步：安装 agy

> 📖 完整说明：[入门文档](https://www.antigravity.google/docs/cli-getting-started)

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

安装完成后，验证二进制文件是否可用：

```bash
# Verify the binary is in your PATH
which agy

# Confirm the version
agy --version
```

---

## 第 2 步：身份验证

agy 使用 **基于浏览器的 Google 登录**。在首次运行时，它将：

- **本地机器：** 自动打开您的默认浏览器进行登录。
- **SSH / 远程会话：** 打印一个 URL 供您粘贴到任何浏览器中，然后将验证码粘贴回终端。

```bash
# Start agy — auth will trigger automatically on first run
agy
```

要退出登录：

```text
# Run this inside an agy interactive session (not in your terminal):
/logout
```

> 📖 有关通过 GCP 项目进行的企业级身份验证，请参阅 [企业级文档](https://www.antigravity.google/docs/enterprise)。

配置好身份验证后，运行一个快速的冒烟测试：

```bash
agy --print "Say 'Workshop ready!' in exactly two words." --print-timeout 30s
```

预期输出：`Workshop ready!`

---

## 第 3 步：初始化您的项目工作区

agy 通过从当前目录向上遍历来自动发现项目配置，查找 `.agents/` 文件夹。为本次研讨会创建一个：

```bash
# Clone the workshop exercises repo
git clone https://github.com/pauldatta/agy-cli-field-workshop.git
cd agy-cli-field-workshop

# agy will create .agents/ on first run
agy --print "List the files in the current directory."
```

您会看到创建了一个包含项目配置文件的 `.agents/` 文件夹（settings.json、mcp.json 等）。

!!! info ".gemini/ 兼容性"
    agy 也会读取 `.gemini/` 目录 —— 如果您已经有 Gemini CLI 项目环境设置，这将非常有用。这两个配置位置都会被识别。

---

## 第 4 步：验证所有内容

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

工作坊开始前的检查清单：

- [ ] `agy --help` 显示标志和子命令
- [ ] `agy plugin list` 成功返回
- [ ] `agy --print "..."` 返回响应

---

## 故障排除

| 问题 | 解决方案 |
| :-- | :-- |
| `agy: command not found` | 检查该二进制文件是否在您的 PATH 中。运行 `echo $PATH` 并确保包含安装目录。如果需要，请重新运行安装脚本 |
| 身份验证错误 / 浏览器未打开 | 对于 SSH 会话，请手动复制打印的 URL。对于本地环境，请检查默认浏览器设置。运行 `/logout` 并重试 |
| `agy plugin list` 返回 `No imported plugins.` | 全新安装时的预期行为（非 JSON）。您将在模块 2 中填充插件 |
| 首次响应缓慢 | 首次运行可能会比较慢，因为 agy 正在索引您的工作区 |
| 配置未加载 | 检查 `~/.gemini/antigravity-cli/settings.json`（用户设置）和 `.agents/`（项目设置） |

---

## 下一步

→ 从 **[模块 1：SDLC 生产力提升](sdlc-productivity.md)** 开始
