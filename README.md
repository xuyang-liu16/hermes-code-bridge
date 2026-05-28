<div align="center">

# Hermes Code Bridge

<p>
  <img src="https://img.shields.io/badge/Hermes-Plugin%20%2B%20Skill-6C5CE7?style=for-the-badge" alt="Hermes Plugin + Skill">
  <img src="https://img.shields.io/badge/Local-CLI%20Coding%20Agents-2F9E44?style=for-the-badge" alt="Local CLI Coding Agents">
  <img src="https://img.shields.io/badge/Codex%20%7C%20Kimi%20Code%20%7C%20Claude%20Code%20%7C%20OpenCode%20%7C%20Gemini-blue?style=for-the-badge" alt="Supported CLIs">
</p>

<p>
  <a href="#one-line-install">Install</a> ·
  <a href="#what-it-does">What it does</a> ·
  <a href="#usage">Usage</a> ·
  <a href="#plugin-vs-skill">Plugin vs Skill</a> ·
  <a href="README_zh.md">中文</a>
</p>

**English** | [中文](README_zh.md)

Use Hermes Agent as the control plane for local coding agents.

</div>

---

## One-line install

Install it as a Hermes plugin:

```bash
hermes plugins install https://github.com/xuyang-liu16/hermes-code-bridge --enable
```

Then use it inside Hermes:

```text
/code-bridge Use Codex to do a read-only review of the current repository diff.
```

The plugin registers `/code-bridge`, which tells Hermes to load and follow the plugin-provided `hermes-code-bridge:hermes-code-bridge` skill for the request.

If you only want the skill file without the plugin wrapper:

```bash
hermes skills install https://raw.githubusercontent.com/xuyang-liu16/hermes-code-bridge/main/skills/hermes-code-bridge/SKILL.md --name hermes-code-bridge
```

## What it does

Hermes Code Bridge connects [Hermes Agent](https://github.com/NousResearch/hermes-agent) to local terminal-based coding agents such as Codex, Kimi Code, Claude Code, OpenCode, Gemini CLI, and other coding CLIs.

It teaches Hermes how to:

- discover installed coding CLIs;
- choose the right backend, working directory, and session;
- reuse existing CLI-agent sessions instead of creating unnecessary new ones;
- write structured dispatch prompts with role, task, constraints, success criteria, and report format;
- run the real local CLI, not a fake substitute;
- monitor background execution through terminal, tmux, or process logs;
- collect raw evidence, artifacts, diffs, and verification results;
- report what happened, what passed, what failed, and what remains risky.

The bridge pattern:

```text
User request
  -> Hermes plans and routes the task
  -> Codex / Kimi Code / Claude Code / OpenCode executes it locally
  -> Hermes monitors, verifies, and reports evidence
```

Hermes is the coordinator. Your local coding CLIs are the execution backends.

## Why use it?

Modern developers often use several coding agents at once. One tool might be better for implementation, another for review, another for debugging, and another for long-context research. Without a workflow, it is easy to lose session context, send vague prompts, forget verification, or accidentally pretend that one agent did work that another agent actually did.

Hermes Code Bridge gives Hermes a disciplined bridge workflow:

| Need | What Hermes Code Bridge provides |
| --- | --- |
| Real local execution | Hermes must call the actual requested CLI. |
| Session reuse | Prefer existing project/session context over fresh throwaway runs. |
| Safe dispatch | Confirm ambiguous or side-effectful tasks before sending. |
| Better prompts | Include role, background, task, constraints, success criteria, and report format. |
| Monitoring | Track long-running agent jobs through terminal/tmux/process output. |
| Evidence | Report exact command, output excerpt, changed files, artifacts, and verification. |
| Privacy | Keep public workflows free of private paths, session IDs, secrets, and project names. |

## Supported backends

The skill includes command patterns and safety notes for:

- Codex
- Kimi Code
- Claude Code
- OpenCode
- Gemini CLI
- generic terminal-based coding assistants
- tmux-based interactive sessions
- optional multi-agent workspace tools such as CCB (`claude_codex_bridge`)

The command recipes are intentionally written as patterns because CLI flags change over time. Hermes should still check `<command> --help` when using a new version.

## Usage

### Load by plugin slash command

```text
/code-bridge Use Kimi Code to implement the smallest change that fixes this bug. Reuse the existing project session if available, do not refactor unrelated files, run relevant tests, and report evidence.
```

The plugin registers `/code-bridge`, which tells Hermes to load and follow the `hermes-code-bridge` skill for the request.

### Load as a normal skill

```text
/skill hermes-code-bridge
```

or start Hermes with it preloaded:

```bash
hermes -s hermes-code-bridge
```

### Example prompts

Ask Codex for a read-only review:

```text
Use Codex to do a read-only review of the current repository diff. Do not modify files. Report correctness, security, and maintainability risks with evidence.
```

Ask Claude Code to review a change:

```text
Use Claude Code as a read-only reviewer for the latest diff. Do not modify files. List blockers, non-blockers, test gaps, and exact evidence from the diff.
```

Ask OpenCode to inspect a project:

```text
Use OpenCode to inspect this repository structure and suggest where a new feature should be implemented. Read-only only; do not create or edit files.
```

Coordinate implementation and review:

```text
Use one local coding agent to implement the change and a different one to review it. Confirm the backend/session plan before dispatch. Use separate worktrees if both agents need to edit files.
```

## Plugin vs Skill

This repository ships both:

| Mode | Path | Best for |
| --- | --- | --- |
| Plugin wrapper | `plugin.yaml`, `__init__.py` | Easy GitHub install via `hermes plugins install ... --enable`; adds `/code-bridge`. |
| Plain skill | `skills/hermes-code-bridge/SKILL.md` | Users who only want the skill document and prefer `/skill hermes-code-bridge`. |

The plugin is intentionally lightweight. The real workflow lives in `SKILL.md`, so users can install it either way.

## Safety model

Hermes Code Bridge is strict about attribution and evidence:

- If the user asks for Codex, Hermes should run Codex.
- If the user asks for Kimi Code, Hermes should run Kimi Code.
- Hermes should not use a Hermes subagent or Python script and pretend it was a different local coding CLI.
- Hermes should not edit coding-agent session databases or internal history files.
- Hermes should not bypass sandbox or approval prompts unless the user explicitly accepts that risk.
- Hermes should verify artifacts and test results before reporting success.

## Relationship to CCB and tmux workspaces

Hermes Code Bridge is not a replacement for full multi-agent workspace tools.

Tools such as CCB (`claude_codex_bridge`) provide visible tmux workspaces, configured agent panes, sidebars, worktrees, and inter-agent communication routes. Hermes Code Bridge is lighter: it is a Hermes skill/plugin that helps Hermes drive whatever local coding CLIs are already installed.

They can work together. If CCB is installed, Hermes can treat it as another bridge backend: inspect the CCB config, attach to the workspace, send prompts to the correct pane, and capture output.

## Repository layout

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

## Privacy

This repository is designed to be public. The skill uses placeholders such as `<PROJECT_DIR>`, `<SESSION_ID>`, `<PROMPT>`, and `<TEST_COMMAND>` instead of personal paths, private project names, real session IDs, or credentials.

Before publishing your own fork, run a privacy scan:

```bash
grep -RInE "(/Users/|/home/|API_KEY|TOKEN|SECRET|PRIVATE|@)" . 2>/dev/null || true
```

Review any matches manually. Some placeholders may be intentional; real secrets or personal data should be removed.

## License

MIT
