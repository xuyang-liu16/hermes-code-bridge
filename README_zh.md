<div align="center">

# 🌉 Hermes Code Bridge

<p>
  <img src="https://img.shields.io/badge/Hermes-Plugin%20%2B%20Skill-6C5CE7?style=for-the-badge" alt="Hermes Plugin + Skill">
  <img src="https://img.shields.io/badge/Local-CLI%20Coding%20Agents-2F9E44?style=for-the-badge" alt="Local CLI Coding Agents">
  <img src="https://img.shields.io/badge/Codex%20%7C%20Kimi%20Code%20%7C%20Claude%20Code%20%7C%20OpenCode%20%7C%20Gemini-blue?style=for-the-badge" alt="Supported CLIs">
</p>

<p>
  <a href="#-咖啡时间-demo">咖啡 demo</a> ·
  <a href="#-10-秒安装">安装</a> ·
  <a href="#-你可以让它做什么">使用场景</a> ·
  <a href="#-工作原理">工作原理</a> ·
  <a href="#-使用方式">使用方式</a> ·
  <a href="README.md">English</a>
</p>

[English](README.md) | **中文**

### 把 Hermes Agent 变成 Codex、Kimi Code、Claude Code、OpenCode、Gemini CLI 等本地代码智能体的指挥塔。

不用再在一堆终端之间复制 prompt。你给 Hermes 一个要求，它可以把任务路由给 Codex、Kimi Code、Claude Code、OpenCode 或 Gemini CLI，再带着命令、diff、测试、产物和风险回来汇报。

</div>

---

## ☕ 咖啡时间 demo

想象一下：你下楼买杯咖啡。出门前，你只对 Hermes 说一句：

```text
/code-bridge 用 Codex 跑一下这个实验，再让 Claude Code review 一遍结果。等我回来时，把命令、改动文件、测试结果、失败点和剩余风险整理给我。
```

等你拿着咖啡回来，Hermes 已经在本地协调好了 coding agents：一个负责跑实验，一个负责复查，Hermes 负责监控过程、收集证据，而不是让你回来后翻一堆 terminal 日志。

这就是 Hermes Code Bridge 的核心价值：大约 10 秒安装，让 Hermes 具备指挥本地 coding agents 的能力。

---

## 🚀 10 秒安装

```bash
hermes plugins install https://github.com/xuyang-liu16/hermes-code-bridge --enable
```

然后在 Hermes 里这样问：

```text
/code-bridge 用 Codex 审查我当前的 diff。只读，不要改文件。重点看 bug、安全风险和缺失的测试。
```

也可以直接试试“咖啡时间工作流”：

```text
/code-bridge 用 Kimi Code 理解这个 repo，让 Codex 实现最小修复，再让 Claude Code review diff。最后汇报证据、测试和风险。
```

只想安装 skill 文件也可以：

```bash
hermes skills install https://raw.githubusercontent.com/xuyang-liu16/hermes-code-bridge/main/skills/hermes-code-bridge/SKILL.md --name hermes-code-bridge
```

---

## 🔥 为什么大家会需要它？

AI coding 现在已经不是“一个助手，一个聊天窗口”的形态了。真实工作流经常长这样：

- Codex 已经在某个 repo session 里跑得很深；
- Claude Code 更适合做一轮仔细 review；
- Kimi Code 更适合吃长上下文、读复杂项目；
- OpenCode 是你本地常用的项目导航和 coding 工具；
- Gemini CLI 适合做轻量检查和快速问答。

没有 bridge 的时候，你自己就变成了 router：复制 prompt、记住哪个 terminal 里有什么上下文、检查 agent 有没有真的跑测试、再把结果粘回主助手。

Hermes Code Bridge 让 Hermes 来做这个 router。

```text
你
  -> Hermes: "用 Kimi Code 修这个 bug，再让 Claude Code review 一遍。"
  -> Hermes 检查工具、仓库、session 和安全约束
  -> Hermes 派发给正确的本地 CLI agent
  -> Hermes 监控输出和产物
  -> Hermes 汇报：命令、改动文件、测试、失败点、风险
```

---

## 💡 你可以让它做什么

### 🧪 实现 + review 闭环

```text
用 Codex 为这个失败测试实现最小修复。然后用 Claude Code 做只读 review。最后汇报两个 agent 的证据。
```

### 🔍 合并前找另一个 agent 复查

```text
用另一个本地 coding agent 审查我最新的 diff。不要改文件。重点找正确性 bug、安全问题和测试缺口。
```

### 🧭 把任务交给最适合的模型

```text
用 Kimi Code 做长上下文 repo 理解。让它判断这个功能应该放在哪里、可能影响哪些文件。只读。
```

### ♻️ 继续已有 coding-agent session

```text
继续这个项目已有的 Codex session。除非找不到匹配 session，否则不要新开。
```

### 🧱 协调多 agent 本地工作区

```text
用一个本地 agent 实现改动，再用另一个 agent review。如果两个 agent 都需要改文件，先使用独立 worktree，并在派发前确认计划。
```

### 📦 把模糊需求变成结构化任务

```text
用 OpenCode 检查这个 repo，并产出一份具体实现计划。计划里要包含成功标准和需要运行的测试命令。
```

---

## 🧠 它教会 Hermes 什么？

Hermes Code Bridge 给 Hermes 一套更稳的本地 coding-agent 工作流：

- 🔎 发现已安装的 CLIs，并在必要时检查 help 输出；
- 🧭 有意识地选择 backend、工作目录和 session；
- ♻️ 复用已有 session，不浪费上下文；
- 📝 生成带角色、背景、任务、约束、成功标准和汇报格式的 prompt；
- 🖥️ 真的调用用户指定的 CLI，不用别的工具冒充；
- ⏱️ 通过 terminal、tmux 或 process logs 监控长任务；
- 📦 收集原始输出、diff、产物和验证结果；
- ✅ 汇报实际发生了什么，包括失败和不确定性。

---

## 🧩 支持哪些后端？

| 后端 | 适合什么 |
| --- | --- |
| 🧩 Codex | 实现、debug、聚焦的 repo 改动 |
| 🌙 Kimi Code | 长上下文代码理解，中英文混合工作流 |
| 🟣 Claude Code | 细致 code review、重构计划、复杂 debug 推理 |
| 🛠️ OpenCode | 本地项目导航，terminal-first coding 工作流 |
| ✨ Gemini CLI | 快速检查、轻量 review、repo Q&A |
| 🪟 tmux sessions | 持久化多 pane 本地 agent 工作区 |
| 🧱 CCB / 其他 bridge | 带 panes、worktrees 和路由能力的可视化多 agent 工作区 |

skill 使用的是命令模式，而不是写死某个版本的参数。CLI flags 会变，Hermes 应该针对当前安装版本检查 `<command> --help`。

---

## ⚙️ 工作原理

```text
1. 理解用户请求
2. 识别用户指定的 backend，或在用户允许时选择一个
3. 检查 repo / session 上下文
4. 对高风险动作先确认再派发
5. 为 coding agent 构造结构化 prompt
6. 调用本地 CLI，或 attach 到已有 tmux/session
7. 监控直到完成或阻塞
8. 验证产物、diff 和测试
9. 带证据向用户汇报
```

它不是“随便再起一个 LLM”。核心是归因：用户要 Codex，Hermes 就运行 Codex；用户要 Claude Code，Hermes 就运行 Claude Code。

---

## 🛡️ 安全模型

Hermes Code Bridge 对安全和证据很严格：

- 🧾 汇报实际使用的命令或 session；
- 🔐 公开文档不泄露 secrets、私人路径、真实 session ID 或私有项目名；
- 🛑 不在用户未明确接受风险时绕过 sandbox 或 approval prompts；
- 🚫 不编辑 coding-agent 的数据库、transcript 或隐藏 session 内部文件；
- 🧪 说任务成功前先验证测试和产物；
- 🧯 阻塞就说阻塞，不编造成功结果。

---

## 📌 使用方式

### Plugin command

```text
/code-bridge 用 Kimi Code 实现能修复这个 bug 的最小改动。如果已有项目 session，就复用它；不要重构无关文件；运行相关测试，并汇报证据。
```

### Plain skill

```text
/skill hermes-code-bridge
```

或者启动 Hermes 时预加载：

```bash
hermes -s hermes-code-bridge
```

---

## 🧪 更多 prompt 示例

```text
用 Codex 复现这个 bug，定位根因，并提出最小 patch。计划明确前不要改文件。
```

```text
用 Claude Code review 最新 diff。只读。把阻塞问题和可选改进分开写，并提供文件路径和行级证据。
```

```text
用 Kimi Code 阅读整个 repo 上下文，解释这个测试为什么 flaky。如果需要运行命令，遇到破坏性操作前先确认。
```

```text
用 OpenCode 检查项目结构，并建议新的 API endpoint 应该实现在哪些位置。不要改文件。
```

---

## 🧩 Plugin 和 Skill 的区别

| 模式 | 路径 | 适合什么 |
| --- | --- | --- |
| 🔌 Plugin wrapper | `plugin.yaml`, `__init__.py` | 从 GitHub 一行安装；提供 `/code-bridge` 命令。 |
| 📄 Plain skill | `skills/hermes-code-bridge/SKILL.md` | 只想要可复用工作流文档的用户。 |

plugin 保持轻量。真正的工作流在 `SKILL.md` 里，所以两种方式都能用。

---

## 🧱 可以配合 CCB 和 tmux workspace

Hermes Code Bridge 不替代完整的多 agent workspace 工具。

CCB（`claude_codex_bridge`）这类工具提供可见的 tmux panes、配置好的 agent slots、worktrees、sidebar 和 agent 间通信。Hermes Code Bridge 更轻量：它告诉 Hermes 怎么驱动本地已经安装好的 coding CLIs。

如果 CCB 可用，Hermes 可以把它当成另一个 bridge backend：读取 CCB config、attach 到 workspace、给正确 pane 发送 prompt，并捕获输出。

---

## 📁 仓库结构

```text
hermes-code-bridge/
  README.md
  README_zh.md
  LICENSE
  plugin.yaml
  __init__.py
  after-install.md
  skills/
    hermes-code-bridge/
      SKILL.md
```

---

## 🔐 隐私

这个 repo 设计成可以公开发布。它使用 `<PROJECT_DIR>`、`<SESSION_ID>`、`<PROMPT>`、`<TEST_COMMAND>` 等占位符，不包含私人路径、私有项目名、真实 session ID 或 credentials。

发布 fork 前可以跑：

```bash
grep -RInE "(/Users/|/home/|API_KEY|TOKEN|SECRET|PRIVATE|@)" . 2>/dev/null || true
```

人工检查命中结果。有些占位符是有意保留的；真实密钥不应该出现在这里。

---

## 📜 License

MIT
