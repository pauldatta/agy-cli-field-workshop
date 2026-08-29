# 模块 2：遗留代码库现代化

<div class="module-header" markdown>
**时长：** 约 75 分钟  
**目标：** 使用 Antigravity CLI 原语安全地迁移遗留应用程序——严格的权限控制、代理自主引导、并行子代理分析、作为护栏的钩子，以及作为安全网的 `/rewind`。  
**练习 PRD：** [.NET 现代化](exercises/ex08_dotnet_modernization.md) · [Java 升级](exercises/ex09_java_upgrade.md)
</div>

> 📖 参考资料：[权限](https://antigravity.google/docs/permissions) · [严格模式](https://antigravity.google/docs/strict-mode) · [子代理](https://antigravity.google/docs/subagents) · [技能](https://antigravity.google/docs/skills) · [钩子](https://antigravity.google/docs/hooks) · [CLI 功能](https://antigravity.google/docs/cli-features) · [CLI 使用](https://antigravity.google/docs/cli-using)

---

## 为什么遗留系统现代化如此困难

大型迁移的风险不在于代码更改，而在于**未知因素**。在东西被破坏之前，你根本不知道会破坏什么。三种失败模式是：

1. **范围蔓延** — 代理重构了你没有要求它触碰的东西
2. **上下文崩溃** — 在长时间的会话后，代理会丢失对你迁移约束的跟踪
3. **无法回滚** — 错误的更改在你能够阻止它之前就产生了级联效应

AGY 的原语直接解决了这三个问题。

---

## 2.1 — 严格权限：先读后写 <span class="duration-badge">15 min</span>

AGY 中等同于“计划模式”的功能是**严格权限**——这是一个硬性关卡，在您明确允许之前，它会拒绝所有文件写入和 shell 命令。

### 在探索之前锁定

```bash
/permissions
```

将级别设置为 `strict`：

```bash
# In the permissions dialog, select: strict
# Or set directly in settings.json:
```

```json
{
  "permissions": {
    "mode": "strict"
  }
}
```

在 `strict` 模式下，代理可以读取文件、搜索网络和进行推理——但**不能写入、删除或执行任何操作**。这是一堵硬墙，而不是软性的提示词。

> 📖 来源：[严格模式](https://antigravity.google/docs/strict-mode) · [权限](https://antigravity.google/docs/permissions)

### 现在自由调查

在写入被锁定的情况下，赋予代理不受限制的读取权限：

```text
Analyze this entire codebase for a migration. Map:
1. Framework versions and dependency tree (check package.json / pom.xml / .csproj)
2. Architectural patterns in use (MVC, layered, hexagonal)
3. All deprecated API usage (javax.* imports, legacy auth patterns, XML config)
4. Configuration files and external property sources
5. Test frameworks and coverage gaps
6. Migration risks ordered by severity
```

> **发生了什么：** 代理会读取它所需的所有文件，追踪导入和调用链，并构建一个心智模型——所有这些都具有零修改风险。这是您的侦察阶段。

### 在您的编辑器中审查计划

一旦代理生成了迁移计划，请在您的编辑器中打开它以进行完善：

```text
ctrl+g
```

这将使您进入带有当前代理输出的 `$EDITOR`。编辑约束条件，添加团队特定的要求，划掉您不需要的范围。当您保存并退出时，代理会合并您的编辑。

> 📖 来源：[cli-using — 快捷键](https://antigravity.google/docs/cli-using) — uid 3_276–3_280："在默认的 shell 编辑器中编辑提示词"

### 解锁写入——但仅限于您批准的内容

一旦计划获得批准，有选择地恢复写入权限：

```bash
/permissions
# Select: request-review
```

在 `request-review` 模式下，代理在执行每次写入或 shell 命令之前都会请求批准。在它执行操作之前，您可以确切地看到它想要做什么。

> **流程：** `strict`（调查）→ 批准计划 → `request-review`（在监督下执行）→ `always-proceed` 仅用于受信任、经过充分测试的最终步骤。

---

## 2.2 — AGENTS.md：编码迁移标准 <span class="duration-badge">10 分钟</span>

在长时间的会话中，上下文会逐渐丢失。AGENTS.md 就是用来防止这种情况的——无论对话持续多久，它都会自动注入到每个会话中。

### 代理自我引导

最强大的模式是让代理根据其在调查过程中发现的内容**编写自己的 AGENTS.md**。它将学到的知识编码为护栏，用于指导其后续的工作。

```text
Based on your codebase analysis, write an AGENTS.md that:
1. Documents current state (Spring Boot 2.6, Java 8, javax.* namespaces)
2. Defines target state (Spring Boot 3.3, Java 21, jakarta.* namespaces)
3. Sets migration rules:
   - Migrate one module at a time — never touch more than one bounded context per session
   - Every migrated class must have a passing test before moving on
   - Preserve all existing API contracts — no breaking changes to callers
   - Commit after each completed phase with a structured message
4. Flags the specific risks you identified in your analysis
5. Lists files that are off-limits in this phase

Write this to AGENTS.md in the project root.
```

> **为什么自我引导有效：** 代理正在为自己编写指令。从此时起，它做出的每一个迁移决策都会根据其编写的约束条件进行检查。这是一个自我强化的循环——更好的上下文产生更好的更改，从而浮现出更多模式，进而改善上下文。

### 使用 @file 导入的模块化上下文

对于大型项目，请保持 AGENTS.md 精简并导入详细的规范：

```markdown
# AGENTS.md

@./docs/migration/architecture-target.md
@./docs/migration/api-contracts.md
@./docs/migration/phase-1-checklist.md
```

> 📖 来源：[cli-using](https://antigravity.google/docs/cli-using) — AGENTS.md 导入语法

### 用于硬约束的规则文件

对于不可协商的要求，请使用 `.agents/rules.md`——这些将作为系统提示词指令注入，而不仅仅是上下文：

```markdown
# .agents/rules.md

- NEVER delete migration files (MIGRATION.md, phase-*.md)
- NEVER modify files outside the current migration module's directory
- ALWAYS run the test suite before declaring a phase complete
- ALWAYS commit with message format: "migrate(phase-N): <description>"
```

> 📖 来源：[cli-using](https://antigravity.google/docs/cli-using) — `.agents/rules.md` 系统提示词指令

---

## 2.3 — 子代理：并行分析团队 <span class="duration-badge">15 分钟</span>

大型迁移有多个独立的关注点——安全性、性能、API 契约、测试覆盖率。按顺序运行它们速度很慢，并且会浪费代理的上下文窗口。使用子代理进行并行化。

### 生成并行分析团队

```text
I need three parallel analyses before we start migrating. Please spawn:

1. A security-analysis subagent: scan every auth and session-handling class
   for OWASP Top 10 issues. Read-only. Report back with file paths and line numbers.

2. A dependency-map subagent: trace all inter-module dependencies and identify
   which modules can be migrated independently vs which have shared state.
   Produce a migration-order recommendation.

3. A test-coverage subagent: list every public method in the auth module with
   no test coverage. Produce a test-gap report.

Run all three concurrently. I'll review the reports before we start Phase 1.
```

### 从子代理面板进行监控

```bash
/agents
```

面板显示所有正在运行的子代理及其状态：`running`、`done`、`killed`。观察这三个子代理同时完成。

```text
ctrl+j
```

将您传送到下一个等待您批准的子代理——如果某个子代理触及权限边界并需要放行，这将非常有用。

```text
ctrl+k
```

从主对话中快速批准子代理的权限请求，而无需离开您当前的上下文。

> 📖 来源：[cli-features — 子代理](https://antigravity.google/docs/cli-features) — uid 5_278–5_316

### 自定义子代理定义

在 `.agents/agents/security-scanner.md` 中创建一个只读的安全扫描器：

```markdown
---
model: gemini-3.7-flash
tools:
  allow:
    - read_file
    - list_directory
    - grep_search
# No write_file, no run_command — this agent is read-only
---

You are a security analyst specializing in migration risk assessment.
Your job is to identify vulnerabilities in legacy code that could be
amplified during a modernization effort.

Focus on:
- Authentication and session management anti-patterns
- SQL injection vectors in legacy data access layers
- Hardcoded credentials or secrets in configuration files
- Deprecated cryptographic primitives (MD5, SHA-1, DES)
- Unvalidated redirects or file path traversal risks

Always report: file path, line number, severity (HIGH/MEDIUM/LOW), and remediation.
Never modify any file. Never execute any command.
```

> 📖 来源：[子代理](https://antigravity.google/docs/subagents) · [cli-features](https://antigravity.google/docs/cli-features) — uid 5_274: 细粒度权限 JSON 格式

---

## 2.4 — 技能：可重用的迁移专业知识 <span class="duration-badge">10 min</span>

技能是代理在适用时读取并激活的指令集。对于可重复的迁移（Java 8→21、.NET Framework→.NET 8、Express→Fastify），只需将该模式一次性编码为一项技能即可。

### 浏览可用技能

```bash
/skills
```

### 创建迁移技能

```bash
mkdir -p ~/.gemini/antigravity-cli/skills/java-migration
```

创建 `~/.gemini/antigravity-cli/skills/java-migration/SKILL.md`：

```markdown
---
name: java-migration
description: >
  Guides Java 8 to Java 21 + Spring Boot 3.x migration. Activates when
  the user mentions javax.*, Spring Boot 2.x, or Java upgrade. Provides
  phase-by-phase migration steps, jakarta.* namespace rules, and
  mandatory test-gate requirements between phases.
---

## Java 8 → 21 Migration Protocol

### Phase 0 — Inventory (always first)
- Run: grep -r "javax\." src/ | grep -v test | sort | uniq -c | sort -rn
- Identify all Spring Boot starter versions in pom.xml
- Check for removed APIs: sun.misc.*, com.sun.*, internal packages

### Phase 1 — Dependency Upgrade
- Update Spring Boot parent to 3.3.x
- Replace javax.* with jakarta.* (use: sed -i 's/javax\./jakarta\./g')
- Update Hibernate to 6.x — @Entity annotation semantics changed
- Gate: mvn clean verify must pass before Phase 2

### Phase 2 — Configuration Migration

**Goal:** Migrate XML/property-file config to type-safe structured config.

**Steps:**
1. Identify all config sources (XML, .properties, environment variables)
2. Map to typed configuration classes
3. Replace with framework-native config (Spring Boot `@ConfigurationProperties`, .NET `IOptions<T>`)
4. Add validation annotations
5. Remove legacy config loading code

**Validation:** All tests pass with new config loading path.
```

> 📖 来源：[技能](https://antigravity.google/docs/skills) · [CLI 功能 — /skills](https://antigravity.google/docs/cli-features) — uid 5_251–5_253

---

## 2.5 — 钩子：自动化护栏 <span class="duration-badge">10 min</span>

对于企业级迁移，您需要自动化的关卡——而不仅仅是手动审查。钩子在 CLI 事件触发时执行，并可以在工具使用发生之前进行拦截、警告或记录。

### 工具前置钩子：拦截迁移范围外的写入操作

创建 `.agents/hooks/scope-guard.sh`：

```bash
#!/bin/bash
# AGY CLI hook event: PreToolUse
# Blocks writes to files outside the current migration module

TOOL_NAME="$1"
FILE_PATH="$2"
MIGRATION_MODULE="${MIGRATION_MODULE:-src/auth}"  # Set before starting each phase

if [[ "$TOOL_NAME" == "write_file" || "$TOOL_NAME" == "edit" ]]; then
  if [[ "$FILE_PATH" != *"$MIGRATION_MODULE"* ]]; then
    echo "BLOCK: Write to $FILE_PATH is outside migration scope ($MIGRATION_MODULE)" >&2
    exit 1  # Non-zero exit blocks the tool call
  fi
fi
```

在 `settings.json` 中注册：

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "write_file|edit",
        "command": ".agents/hooks/scope-guard.sh"
      }
    ]
  }
}
```

### 工具后置钩子：在每次文件写入后自动运行测试

```bash
#!/bin/bash
# AGY CLI hook event: PostToolUse
# Runs tests automatically after every source file write

TOOL_NAME="$1"
FILE_PATH="$2"

if [[ "$TOOL_NAME" == "write_file" && "$FILE_PATH" == *".java" ]]; then
  echo "Running test gate after $FILE_PATH was modified..."
  mvn test -pl "$(dirname $FILE_PATH | sed 's|src/main/java||')" -q 2>&1
  if [[ $? -ne 0 ]]; then
    echo "⚠️  Tests failed after writing $FILE_PATH — consider /rewind"
  fi
fi
```

> 📖 来源：[钩子](https://antigravity.google/docs/hooks)

---

## 2.6 — /rewind 和 /fork：你的安全网 <span class="duration-badge">5 分钟</span>

### /rewind — 回滚对话

如果代理偏离了轨道，你不需要重新开始。`/rewind` 可以回滚对话历史记录：

```bash
/rewind
```

这将打开一个历史记录选择器。选择要还原到的对话轮次。代理对代码库的理解将重置到该点 —— 如果它在长时间的会话中积累了错误的假设，这将非常有用。

> 📖 来源：[cli-features](https://antigravity.google/docs/cli-features) — uid 5_220–5_226："`/rewind`（别名 `/undo`）—— 回滚对话历史记录"

### /fork — 无风险探索

在尝试有风险的迁移步骤之前，请 fork 对话：

```bash
/fork
```

这将创建一个平行的工作区。你可以在 fork 出的分支中尝试有风险的方法。如果成功了，那很好。如果失败了，关闭该分支并从主对话继续 —— 主对话从未改变过。

> 📖 来源：[cli-using](https://antigravity.google/docs/cli-using) — uid 3_219–3_224："`/fork` 启动一个独立的工作区"

### /resume — 继续漫长的迁移

大型迁移会跨越好几天。当你返回时：

```bash
/resume
```

这将打开一个会话选择器，显示你之前的迁移会话及其时间戳和对话名称。选择正确的会话，即可准确地从你离开的地方继续。

> 📖 来源：[cli-features](https://antigravity.google/docs/cli-features) — uid 5_213–5_219

重命名会话以保持迁移井然有序：

```bash
/rename "Java 21 Migration — Phase 2: Jakarta namespace"
```

---

## 2.7 — 打印模式：非交互式迁移流水线 <span class="duration-badge">5 min</span>

对于 CI/CD 门禁或夜间迁移运行，请使用打印模式以管道方式处理迁移任务，而无需交互：

```bash
# Dry-run: analyze and report issues — no writes
agy -p "Review the migration changes in the last commit. \
  Check for: javax.* references that weren't updated, \
  missing jakarta.* imports, and test files that weren't \
  updated to match renamed packages. \
  Output a structured report with file paths and line numbers."
```

```bash
# Chain: analyze → generate migration report → save
agy -p "Scan src/auth/ for javax.persistence.* usage" | \
  agy -p "Convert this javax.persistence usage report into \
  a step-by-step migration plan with exact sed commands" > migration-plan.md
```

> 📖 来源：[cli-getting-started](https://antigravity.google/docs/cli-getting-started) — `agy --help`："-p: --print 的简写别名"

---

## 动手练习

<div class="exercise-card" markdown>

### :material-file-document: 练习 8：遗留系统现代化

**文件：** [`ex08_dotnet_modernization.md`](exercises/ex08_dotnet_modernization.md) · [`ex09_java_upgrade.md`](exercises/ex09_java_upgrade.md)  
**时长：** 45 分钟  
**目标：** 使用本模块中的 AGY 原语完成一次完整的迁移。

**选择你的路线：**

#### 路线 A：计划优先（严格 → 调查 → 执行）

1. 将 `/permissions` 设置为 `strict` — 锁定所有写入操作
2. 赋予代理全面的调查权限（第 2.1 节）
3. 使用 `ctrl+g` 在编辑器中打开计划并添加团队约束
4. 编写一个包含迁移规则的 AGENTS.md（或让代理编写）
5. 添加一个包含不可协商的硬性规定的 `.agents/rules.md`
6. 切换到 `request-review` — 在监督下开始第一阶段
7. 如果代理偏离范围，请使用 `/rewind`
8. 重命名会话：`/rename "迁移 — 第一阶段完成"`

#### 路线 B：子代理优先（并行分析 → 上下文 → 执行）

1. 生成三个并行的子代理：安全扫描、依赖项映射、测试覆盖率
2. 通过 `/agents` 进行监控 — 使用 `ctrl+j` 和 `ctrl+k` 进行审批
3. 将它们的报告汇总到一个 AGENTS.md 中（让代理进行综合）
4. 安装 `java-migration` 技能（第 2.4 节）
5. 在最危险的步骤之前使用 `/fork` — 先在那里进行尝试
6. 使用打印模式生成阶段后报告

</div>

---

## 总结：用于遗留系统现代化的 AGY 原语

| 原语 | 功能说明 | 适用场景 |
| :-- | :-- | :-- |
| `/permissions strict` | 严格的只读限制 — 禁止写入或执行命令 | 调查阶段 |
| `/permissions request-review` | 代理在每次写入前请求批准 | 受控执行 |
| `ctrl+g` | 在 `$EDITOR` 中打开计划以进行协作编辑 | 计划完善 |
| **AGENTS.md** | 跨会话的持久化迁移标准 | 始终适用 — 编码约束条件 |
| `.agents/rules.md` | 严格的系统提示词指令 | 不可协商的护栏 |
| **子代理** | 并行分析团队 | 多关注点调查 |
| `/agents` + `ctrl+j` + `ctrl+k` | 监控并批准子代理的工作 | 并行运行期间 |
| **钩子** (PreToolUse) | 阻止迁移范围之外的写入 | 自动化护栏 |
| **钩子** (PostToolUse) | 每次更改后自动运行测试 | 测试关卡自动化 |
| `/rewind` | 如果代理偏离方向则回滚对话 | 会话中途纠正方向 |
| `/fork` | 在隔离的分支中尝试有风险的步骤 | 高风险更改之前 |
| `/resume` | 恢复跨越多天的迁移 | 返回会话时 |
| `/rename` | 按阶段标记会话 | 会话管理 |
| `agy -p` | 非交互式迁移流水线 | CI 关卡、夜间运行 |
| **技能** | 可重用的迁移剧本 | 可重复的迁移模式 |

---

## 下一步

→ 继续前往 **[模块 3：使用 SDK 构建 AGY 代理](agy-sdk.md)**

→ **[速查表](cheatsheet.md)** — 所有命令汇集于此
