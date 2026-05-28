<div align="center">

# 🌉 Hermes Code Bridge

<p>
  <img src="https://img.shields.io/badge/Hermes-Plugin%20%2B%20Skill-6C5CE7?style=for-the-badge" alt="Hermes Plugin + Skill">
  <img src="https://img.shields.io/badge/Local-CLI%20Coding%20Agents-2F9E44?style=for-the-badge" alt="Local CLI Coding Agents">
  <img src="https://img.shields.io/badge/Codex%20%7C%20Kimi%20Code%20%7C%20Claude%20Code%20%7C%20OpenCode%20%7C%20Gemini-blue?style=for-the-badge" alt="Supported CLIs">
</p>

<p>
  <a href="#-coffee-break-demo">Coffee demo</a> ·
  <a href="#-install-in-10-seconds">Install</a> ·
  <a href="#-what-you-can-ask-it-to-do">Use cases</a> ·
  <a href="#-how-it-works">How it works</a> ·
  <a href="#-usage">Usage</a> ·
  <a href="README_zh.md">中文</a>
</p>

**English** | [中文](README_zh.md)

### Turn Hermes Agent into a command center for Codex, Kimi Code, Claude Code, OpenCode, Gemini CLI, and other local coding agents.

Stop copy-pasting prompts between terminals. Give Hermes one request; it can route the work to Codex, Kimi Code, Claude Code, OpenCode, or Gemini CLI, then come back with commands, diffs, tests, artifacts, and risks.

</div>

---

## ☕ Coffee break demo

Imagine this: you are stepping out to buy coffee. Before you leave, you tell Hermes:

```text
/code-bridge Use Codex to run the experiment, then ask Claude Code to review the result. When I get back, summarize the commands, changed files, test results, failures, and remaining risks.
```

You come back with your coffee. Hermes has already coordinated the local coding agents: one ran the experiment, another reviewed it, and Hermes collected the evidence instead of leaving you to dig through terminal scrollback.

That is the point of Hermes Code Bridge: give Hermes the skill to command your local coding agents in about 10 seconds.

---

## 🚀 Install in 10 seconds

```bash
hermes plugins install https://github.com/xuyang-liu16/hermes-code-bridge --enable
```

Then ask Hermes:

```text
/code-bridge Use Codex to review my current diff. Read-only. Focus on bugs, security risks, and missing tests.
```

Or try the coffee-break workflow:

```text
/code-bridge Use Kimi Code to understand this repo, ask Codex to implement the smallest fix, then ask Claude Code to review the diff. Report evidence, tests, and risks.
```

Prefer installing only the skill?

```bash
hermes skills install https://raw.githubusercontent.com/xuyang-liu16/hermes-code-bridge/main/skills/hermes-code-bridge/SKILL.md --name hermes-code-bridge
```

---

## 🔥 Why people want this

AI coding is no longer one assistant in one chat window. Real work often looks like this:

- Codex is already deep inside a repo session.
- Claude Code is better suited for a careful review pass.
- Kimi Code has the long context needed for a messy codebase.
- OpenCode is the local tool you use for project navigation.
- Gemini CLI is handy for quick inspection.

Without a bridge, you become the router: copy prompts, remember which terminal had which context, check whether an agent actually ran tests, and paste summaries back into your main assistant.

Hermes Code Bridge makes Hermes the router.

```text
You
  -> Hermes: "Fix this bug with Kimi Code, then ask Claude Code to review it."
  -> Hermes checks tools, repo, session, and safety constraints
  -> Hermes dispatches the right local CLI agents
  -> Hermes monitors output and artifacts
  -> Hermes reports: commands, files changed, tests run, failures, risks
```

---

## 💡 What you can ask it to do

### 🧪 Run implementation + review loops

```text
Use Codex to implement the smallest fix for this failing test. Then use Claude Code as a read-only reviewer. Report both agents' evidence.
```

### 🔍 Get a second opinion before merging

```text
Use a different local coding agent to review my latest diff. Do not edit files. Look for correctness bugs, security issues, and test gaps.
```

### 🧭 Send the right task to the right model

```text
Use Kimi Code for long-context repo understanding. Ask it where this feature should live and what files are likely affected. Read-only.
```

### ♻️ Resume an existing coding-agent session

```text
Continue the existing Codex session for this project. Do not start a new session unless no matching session exists.
```

### 🧱 Coordinate multi-agent local workspaces

```text
Use one local agent to implement and another to review. If both need to edit files, use separate worktrees and confirm the plan first.
```

### 📦 Turn vague requests into structured agent tasks

```text
Use OpenCode to inspect this repo and produce a concrete implementation plan. Include success criteria and the exact tests to run.
```

---

## 🧠 What it teaches Hermes

Hermes Code Bridge gives Hermes a disciplined workflow for local coding agents:

- 🔎 discover installed CLIs and check their help output when needed;
- 🧭 choose backend, working directory, and session intentionally;
- ♻️ reuse existing sessions instead of throwing away context;
- 📝 dispatch prompts with role, background, task, constraints, success criteria, and report format;
- 🖥️ run the real requested CLI, not a fake substitute;
- ⏱️ monitor long-running jobs through terminal, tmux, or process logs;
- 📦 collect raw output, diffs, artifacts, and verification results;
- ✅ report what actually happened, including failures and uncertainty.

---

## 🧩 Supported backends

| Backend | Good for |
| --- | --- |
| 🧩 Codex | implementation, debugging, focused repo changes |
| 🌙 Kimi Code | long-context codebase understanding and Chinese/English mixed workflows |
| 🟣 Claude Code | careful code review, refactoring plans, reasoning-heavy debugging |
| 🛠️ OpenCode | local project navigation and terminal-first coding workflows |
| ✨ Gemini CLI | quick inspection, lightweight review, repo Q&A |
| 🪟 tmux sessions | persistent multi-pane local agent workspaces |
| 🧱 CCB / other bridges | visible multi-agent workspaces with panes, worktrees, and routing |

The skill uses command patterns rather than hard-coded assumptions. CLI flags change; Hermes should verify `<command> --help` for the installed version.

---

## ⚙️ How it works

```text
1. Understand the request
2. Identify the requested backend or choose one if the user allows it
3. Inspect repo/session context
4. Confirm risky actions before dispatch
5. Build a structured prompt for the coding agent
6. Run the local CLI or attach to the existing tmux/session
7. Monitor until completion or blockage
8. Verify artifacts, diffs, and tests
9. Report evidence back to the user
```

This is intentionally not "just spawn another LLM." The point is attribution: if the user asks for Codex, Hermes runs Codex. If the user asks for Claude Code, Hermes runs Claude Code.

---

## 🛡️ Safety model

Hermes Code Bridge is strict about safety and evidence:

- 🧾 report the exact command or session used;
- 🔐 never leak secrets, private paths, real session IDs, or project names in public docs;
- 🛑 do not bypass sandbox or approval prompts unless the user explicitly accepts the risk;
- 🚫 do not edit coding-agent databases, transcripts, or hidden session internals;
- 🧪 verify tests and artifacts before saying a task succeeded;
- 🧯 say "blocked" when blocked instead of inventing a successful result.

---

## 📌 Usage

### Plugin command

```text
/code-bridge Use Kimi Code to implement the smallest change that fixes this bug. Reuse the existing project session if available, do not refactor unrelated files, run relevant tests, and report evidence.
```

### Plain skill

```text
/skill hermes-code-bridge
```

or start Hermes with the skill preloaded:

```bash
hermes -s hermes-code-bridge
```

---

## 🧪 More prompt examples

```text
Use Codex to reproduce this bug, identify the root cause, and propose the smallest patch. Do not edit files until the plan is clear.
```

```text
Use Claude Code to review the latest diff. Read-only. Separate blockers from nice-to-haves. Include file paths and line-level evidence.
```

```text
Use Kimi Code to read the whole repo context and explain why this test is flaky. If it needs to run commands, ask before running anything destructive.
```

```text
Use OpenCode to inspect the project structure and recommend where a new API endpoint should be implemented. No file edits.
```

---

## 🧩 Plugin vs Skill

| Mode | Path | Best for |
| --- | --- | --- |
| 🔌 Plugin wrapper | `plugin.yaml`, `__init__.py` | One-line install from GitHub; adds `/code-bridge`. |
| 📄 Plain skill | `skills/hermes-code-bridge/SKILL.md` | Users who only want the reusable workflow document. |

The plugin stays lightweight. The real workflow lives in `SKILL.md`, so people can install it either way.

---

## 🧱 Works with CCB and tmux workspaces

Hermes Code Bridge does not replace full multi-agent workspace tools.

Tools such as CCB (`claude_codex_bridge`) provide visible tmux panes, configured agent slots, worktrees, sidebars, and inter-agent communication. Hermes Code Bridge is lighter: it tells Hermes how to drive whatever local coding CLIs are already installed.

If CCB is available, Hermes can treat it as another bridge backend: inspect the CCB config, attach to the workspace, send prompts to the right pane, and capture output.

---

## 📁 Repository layout

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

## 🔐 Privacy

This repo is designed to be public. It uses placeholders such as `<PROJECT_DIR>`, `<SESSION_ID>`, `<PROMPT>`, and `<TEST_COMMAND>` instead of personal paths, private project names, real session IDs, or credentials.

Before publishing a fork, run:

```bash
grep -RInE "(/Users/|/home/|API_KEY|TOKEN|SECRET|PRIVATE|@)" . 2>/dev/null || true
```

Review matches manually. Placeholders may be intentional; real secrets should not be there.

---

## 📜 License

MIT
