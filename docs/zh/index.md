---
title: ""
hide:
  - navigation
  - toc
---

<div class="hero-banner" markdown>
  <img src="assets/banner.png" alt="Antigravity CLI 现场工作坊">
</div>

<div class="workshop-meta-bar" markdown>
<span class="workshop-meta-item">:material-update: **最近更新：** 2026 年 8 月</span>
<span class="workshop-meta-item">:material-check-decagram: **Antigravity 2.11 · CLI 1.1.22 · SDK 0.1.15**</span>
<span class="workshop-meta-item">:material-translate: **English · 한국어 · Bahasa Indonesia · 简体中文**</span>
</div>

---

## 研讨会模块

<div class="grid cards" markdown>

- :material-rocket-launch:{ .lg .middle } **模块 1 — SDLC 生产力提升**

    ---

    您的第一次 Antigravity CLI 会话。解释、重构、测试、审查 — 加上自主目标 (`/goal`)、需求访谈 (`/grill-me`)、可视化 diff 与插件。

    **75 分钟** · 练习：ex01–ex03, ex13, ex14

    [:octicons-arrow-right-24: 开始模块 1](sdlc-productivity.md)

- :material-wrench:{ .lg .middle } **模块 2 — 遗留系统现代化 ⭐**

    ---

    旗舰模块。使用严格模式、代理自我引导和子代理规划来迁移真实的遗留代码库（.NET 或 Java）。

    **90 分钟** · 练习：ex07–ex09

    [:octicons-arrow-right-24: 开始模块 2](legacy-modernization.md)

- :material-code-braces:{ .lg .middle } **模块 3 — 构建 AGY 代理**

    ---

    使用 Antigravity SDK 构建生产级代理。工具、会话状态、多代理编排，并部署到 Cloud Run。

    **90 分钟** · 练习：ex10, ex11

    [:octicons-arrow-right-24: 开始模块 3](agy-sdk.md)

- :material-sitemap:{ .lg .middle } **模块 4 — 多代理与高级功能**

    ---

    生成隔离的子代理，使用 `/btw` 在运行中途引导任务，调度周期性作业，通过 DevTools MCP 自动化浏览器测试，并通过 ID 恢复会话。

    **60 分钟** · 练习：ex04–ex06, ex15

    [:octicons-arrow-right-24: 开始模块 4](multi-agent-advanced.md)

- :material-rocket-launch-outline:{ .lg .middle } **模块 5 — 使用 agents-cli 的 ADK 代理**

    ---

    使用 agents-cli 来搭建、构建、评估和部署生产级 ADK 代理 — 从原型到 Cloud Run 的完整 7 阶段生命周期。

    **75 分钟** · 练习：ex12

    [:octicons-arrow-right-24: 开始模块 5](../agents-cli.md)

</div>

---

## 工作坊时间表

| 时间 | 内容 | 时长 |
| :-- | :-- | :-- |
| `0:00` | 环境设置 + 首次运行 | 20 分钟 |
| `0:20` | **模块 1：** SDLC 生产力提升 + 插件 | 75 分钟 |
| `1:35` | :coffee: 休息 | 10 分钟 |
| `1:45` | **模块 2：** 遗留代码库现代化 | 90 分钟 |
| `3:15` | :coffee: 休息 | 10 分钟 |
| `3:25` | **模块 3：** 使用 SDK 构建 AGY 代理 | 90 分钟 |
| `4:55` | **模块 4：** 多代理与高级模式 | 60 分钟 |
| `5:55` | :coffee: 休息 | 10 分钟 |
| `6:05` | **模块 5：** 使用 agents-cli 的 ADK 代理 | 75 分钟 |
| `7:20` | 总结与问答 | 15 分钟 |

> **全天：** 模块 1–4（约 5.5 小时）。**扩展：** 全部 5 个模块（7 小时）。**半天：** 模块 1 + 2（2.5 小时）。**闪电：** 模块 1 + 模块 2 亮点（1.5 小时）。

---

## 开始之前

!!! warning "课前准备"
    请在研讨会开始前完成[环境设置](setup.md)。您需要安装并验证 Antigravity CLI。

!!! info "官方文档"
    完整参考请访问 [antigravity.google/docs](https://www.antigravity.google/docs/cli-overview)。

!!! info "先决条件"
    熟悉终端、Git 以及基本的编码工作流。无需具备 AI 编码助手的相关经验。
