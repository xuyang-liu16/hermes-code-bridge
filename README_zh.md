<div align="center">

# Hermes Code Bridge

<p>
  <img src="https://img.shields.io/badge/Hermes-Skill-6C5CE7?style=for-the-badge" alt="Hermes Skill">
  <img src="https://img.shields.io/badge/CLI-Coding%20Agents-2F9E44?style=for-the-badge" alt="CLI Coding Agents">
  <img src="https://img.shields.io/badge/Codex%20%7C%20Kimi%20Code%20%7C%20Claude%20Code%20%7C%20OpenCode-blue?style=for-the-badge" alt="Supported CLIs">
</p>

[English](README.md) | **中文**

把 Hermes Agent 变成本地代码智能体的控制层。

</div>

---

## Hermes Code Bridge 是什么？

Hermes Code Bridge 是一个可复用的 [Hermes Agent](https://github.com/NousResearch/hermes-agent) skill，用来把 Hermes 连接到本地终端里的代码智能体，例如 Codex、Kimi Code、Claude Code、OpenCode、Gemini CLI，以及其他 terminal-based coding assistants。

它让 Hermes 学会：

- 发现本机已安装的 coding CLI；
- 选择正确的后端、项目目录和工作方式；
- 尽量复用已有 CLI agent session，而不是无意义地新开 session；
- 生成带有约束、成功标准和汇报格式的结构化派活 prompt；
- 调用真实的本地 CLI，而不是用 Hermes 自己冒充；
- 监控后台任务；
- 收集原始输出、产物、diff 和验证结果；
- 清楚汇报实际发生了什么、验证是否通过、还有哪些风险。

核心流程很简单：

```text
用户请求
  -> Hermes 规划并路由任务
  -> Codex / Kimi Code / Claude Code / OpenCode 在本地执行
  -> Hermes 监控、验证并汇报证据
```

Hermes 是协调者；本地 coding CLIs 是执行后端。

## 为什么需要它？

很多开发者会同时使用多个代码智能体：一个适合实现，一个适合 review，一个适合 debug 或长上下文调研。如果没有统一工作流，很容易丢 session 上下文、发出模糊 prompt、忘记验证，甚至把某个 agent 的工作错误地说成另一个 agent 做的。

Hermes Code Bridge 提供了一套更稳的桥接工作流：

| 需求 | skill 提供什么 |
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

## 安装方式

### 方式一：复制 skill 到 Hermes skills 目录

```bash
mkdir -p ~/.hermes/skills/autonomous-ai-agents/hermes-code-bridge
cp skills/hermes-code-bridge/SKILL.md ~/.hermes/skills/autonomous-ai-agents/hermes-code-bridge/SKILL.md
```

然后开启新的 Hermes session，并加载 skill：

```text
/skill hermes-code-bridge
```

也可以启动 Hermes 时预加载：

```bash
hermes -s hermes-code-bridge
```

### 方式二：通过 raw URL 安装

如果你的 Hermes 版本支持从 raw URL 安装 skill：

```bash
hermes skills install https://raw.githubusercontent.com/<OWNER>/<REPO>/main/skills/hermes-code-bridge/SKILL.md --name hermes-code-bridge
```

把 `<OWNER>/<REPO>` 替换成你的仓库路径即可。

## 快速开始

你可以这样对 Hermes 说：

```text
Use Codex to do a read-only review of the current repository diff. Do not modify files. Report correctness, security, and maintainability risks with evidence.
```

Hermes 应该按桥接流程执行：

1. 加载 `hermes-code-bridge`；
2. 检查 Codex 是否已安装；
3. 确认当前项目目录；
4. 选择已有 session 或 one-shot run；
5. 把结构化 prompt 发给真实 Codex CLI；
6. 检查输出和仓库状态；
7. 汇报命令、结果、证据和风险。

示例派活命令模式：

```bash
cd <PROJECT_DIR>
codex exec "Read-only review: inspect the current git diff and identify correctness, security, and maintainability risks. Do not modify files. Report file paths, line references when possible, severity, and recommended fixes."
```

## 示例 prompt

### 让 Kimi Code 做一个小范围实现

```text
Use Kimi Code to implement the smallest change that satisfies this bug fix. Reuse the existing project session if available. Do not refactor unrelated files. Run the relevant tests and report files changed, commands run, and remaining risks.
```

### 让 Claude Code 做只读 review

```text
Use Claude Code as a read-only reviewer for the latest diff. Do not modify files. List blockers, non-blockers, test gaps, and exact evidence from the diff.
```

### 让 OpenCode 检查项目结构

```text
Use OpenCode to inspect this repository structure and suggest where a new feature should be implemented. Read-only only; do not create or edit files.
```

### 协调一个实现 agent 和一个 review agent

```text
Use one local coding agent to implement the change and a different one to review it. Confirm the backend/session plan before dispatch. Use separate worktrees if both agents need to edit files.
```

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

CCB（`claude_codex_bridge`）这类工具提供可见的 tmux workspace、配置好的 agent panes、sidebar、worktrees 和 agent 之间的通信路由。Hermes Code Bridge 更轻量：它只是一个 Hermes skill，让 Hermes 能驱动本地已经安装好的 coding CLIs。

二者可以一起用。如果安装了 CCB，Hermes 可以把 CCB 当作另一个 bridge backend：读取 CCB 配置、attach 到 workspace、给正确 pane 发送 prompt，并捕获输出。

## 仓库结构

```text
hermes-code-bridge/
  README.md
  README_zh.md
  LICENSE
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
