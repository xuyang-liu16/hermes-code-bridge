<div align="center">

# Hermes Code Bridge

<p>
  <img src="https://img.shields.io/badge/Hermes-Plugin%20%2B%20Skill-6C5CE7?style=for-the-badge" alt="Hermes Plugin + Skill">
  <img src="https://img.shields.io/badge/Local-CLI%20Coding%20Agents-2F9E44?style=for-the-badge" alt="Local CLI Coding Agents">
  <img src="https://img.shields.io/badge/Codex%20%7C%20Kimi%20Code%20%7C%20Claude%20Code%20%7C%20OpenCode%20%7C%20Gemini-blue?style=for-the-badge" alt="Supported CLIs">
</p>

<p>
  <a href="#一行安装">安装</a> ·
  <a href="#它能做什么">它能做什么</a> ·
  <a href="#怎么用">怎么用</a> ·
  <a href="#plugin-和-skill-的区别">Plugin vs Skill</a> ·
  <a href="README.md">English</a>
</p>

[English](README.md) | **中文**

把 Hermes Agent 变成本地代码智能体的控制层。

</div>

---

## 一行安装

作为 Hermes plugin 安装：

```bash
hermes plugins install https://github.com/ImSingee/hermes-code-bridge --enable
```

然后在 Hermes 里使用：

```text
/code-bridge Use Codex to do a read-only review of the current repository diff.
```

plugin 会注册 `/code-bridge`，它会告诉 Hermes 针对当前请求加载并遵循 plugin 内置的 `hermes-code-bridge:hermes-code-bridge` skill。

如果你只想安装 skill 文件，不需要 plugin wrapper：

```bash
hermes skills install https://raw.githubusercontent.com/ImSingee/hermes-code-bridge/main/skills/hermes-code-bridge/SKILL.md --name hermes-code-bridge
```

## 它能做什么

Hermes Code Bridge 用来把 [Hermes Agent](https://github.com/NousResearch/hermes-agent) 连接到本地终端里的代码智能体，例如 Codex、Kimi Code、Claude Code、OpenCode、Gemini CLI，以及其他 terminal-based coding assistants。

它让 Hermes 学会：

- 发现本机已安装的 coding CLI；
- 选择正确的后端、项目目录和 session；
- 尽量复用已有 CLI-agent session，而不是无意义地新开；
- 生成带有角色、任务、约束、成功标准和汇报格式的结构化派活 prompt；
- 调用真实的本地 CLI，而不是用 Hermes 自己冒充；
- 通过 terminal、tmux 或 process logs 监控后台任务；
- 收集原始输出、产物、diff 和验证结果；
- 清楚汇报实际发生了什么、什么通过了、什么失败了、还有哪些风险。

核心桥接流程：

```text
用户请求
  -> Hermes 规划并路由任务
  -> Codex / Kimi Code / Claude Code / OpenCode 在本地执行
  -> Hermes 监控、验证并汇报证据
```

Hermes 是协调者；本地 coding CLIs 是执行后端。

## 为什么需要它？

很多开发者会同时使用多个代码智能体：一个适合实现，一个适合 review，一个适合 debug，另一个适合长上下文调研。如果没有统一工作流，很容易丢 session 上下文、发出模糊 prompt、忘记验证，甚至把某个 agent 的工作错误地说成另一个 agent 做的。

Hermes Code Bridge 提供了一套更稳的桥接工作流：

| 需求 | Hermes Code Bridge 提供什么 |
| --- | --- |
| 真实本地执行 | 用户要求哪个 CLI，Hermes 就必须真的调用哪个 CLI。 |
| 复用 session | 优先使用已有项目/session 上下文，而不是随便新开。 |
| 安全派活 | 对有歧义或有副作用的任务，先确认再发送。 |
| 更好的 prompt | 包含角色、背景、任务、约束、成功标准和汇报格式。 |
| 过程监控 | 通过 terminal/tmux/process 输出追踪长任务。 |
| 可验证证据 | 汇报实际命令、输出片段、改动文件、产物和验证结果。 |
| 隐私保护 | 开源材料不包含私人路径、session ID、密钥或私有项目名。 |

## 支持哪些后端？

skill 内包含这些工具的命令模式和安全说明：

- Codex
- Kimi Code
- Claude Code
- OpenCode
- Gemini CLI
- 通用 terminal-based coding assistants
- 基于 tmux 的交互式 session
- 可选的多 agent workspace 工具，例如 CCB（`claude_codex_bridge`）

命令示例故意写成 pattern，因为各个 CLI 的参数会随版本变化。实际使用时，Hermes 仍然应该在必要时运行 `<command> --help` 检查当前版本。

## 怎么用

### 通过 plugin slash command 加载

```text
/code-bridge Use Kimi Code to implement the smallest change that fixes this bug. Reuse the existing project session if available, do not refactor unrelated files, run relevant tests, and report evidence.
```

plugin 会注册 `/code-bridge`，它会告诉 Hermes 针对当前请求加载并遵循 `hermes-code-bridge` skill。

### 作为普通 skill 加载

```text
/skill hermes-code-bridge
```

也可以启动 Hermes 时预加载：

```bash
hermes -s hermes-code-bridge
```

### 示例 prompt

让 Codex 做只读 review：

```text
Use Codex to do a read-only review of the current repository diff. Do not modify files. Report correctness, security, and maintainability risks with evidence.
```

让 Claude Code 做只读 review：

```text
Use Claude Code as a read-only reviewer for the latest diff. Do not modify files. List blockers, non-blockers, test gaps, and exact evidence from the diff.
```

让 OpenCode 检查项目结构：

```text
Use OpenCode to inspect this repository structure and suggest where a new feature should be implemented. Read-only only; do not create or edit files.
```

协调一个实现 agent 和一个 review agent：

```text
Use one local coding agent to implement the change and a different one to review it. Confirm the backend/session plan before dispatch. Use separate worktrees if both agents need to edit files.
```

## Plugin 和 Skill 的区别

这个仓库同时提供两种形态：

| 模式 | 路径 | 适合什么场景 |
| --- | --- | --- |
| Plugin wrapper | `plugin.yaml`, `__init__.py` | 通过 `hermes plugins install ... --enable` 从 GitHub 一键安装；额外提供 `/code-bridge` 命令。 |
| Plain skill | `skills/hermes-code-bridge/SKILL.md` | 只想安装 skill 文档，并通过 `/skill hermes-code-bridge` 使用的用户。 |

plugin 本身故意保持轻量。真正的工作流都在 `SKILL.md` 里，所以两种方式都能用。

## 安全模型

Hermes Code Bridge 对“归因”和“证据”要求很严格：

- 用户要求 Codex，Hermes 就应该真的运行 Codex。
- 用户要求 Kimi Code，Hermes 就应该真的运行 Kimi Code。
- Hermes 不能用自己的 subagent 或 Python 脚本冒充其他本地 coding CLI。
- Hermes 不应该编辑 coding agent 的 session 数据库或内部历史文件。
- Hermes 不应该在用户未确认的情况下绕过 sandbox 或 approval prompts。
- Hermes 汇报成功前应该验证产物和测试结果。

## 和 CCB / tmux workspace 的关系

Hermes Code Bridge 不是完整多 agent workspace 工具的替代品。

CCB（`claude_codex_bridge`）这类工具提供可见的 tmux workspace、配置好的 agent panes、sidebar、worktrees 和 agent 之间的通信路由。Hermes Code Bridge 更轻量：它只是一个 Hermes skill/plugin，让 Hermes 能驱动本地已经安装好的 coding CLIs。

二者可以一起用。如果安装了 CCB，Hermes 可以把 CCB 当作另一个 bridge backend：读取 CCB 配置、attach 到 workspace、给正确 pane 发送 prompt，并捕获输出。

## 仓库结构

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

## 隐私

这个仓库设计成可以公开发布。skill 使用 `<PROJECT_DIR>`、`<SESSION_ID>`、`<PROMPT>`、`<TEST_COMMAND>` 等占位符，不包含私人路径、私有项目名、真实 session ID 或密钥。

发布你自己的 fork 前，可以跑一下隐私扫描：

```bash
grep -RInE "(/Users/|/home/|API_KEY|TOKEN|SECRET|PRIVATE|@)" . 2>/dev/null || true
```

对命中结果做人工检查。有些占位符可能是故意保留的；真正的密钥或个人信息应该删除。

## License

MIT
