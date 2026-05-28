<div align="center">

# Hermes Code Bridge

<p>
  <img src="https://img.shields.io/badge/Hermes-Skill-6C5CE7?style=for-the-badge" alt="Hermes Skill">
  <img src="https://img.shields.io/badge/CLI-Coding%20Agents-2F9E44?style=for-the-badge" alt="CLI Coding Agents">
  <img src="https://img.shields.io/badge/Codex%20%7C%20Kimi%20Code%20%7C%20Claude%20Code%20%7C%20OpenCode-blue?style=for-the-badge" alt="Supported CLIs">
</p>

**English** | [中文](README_zh.md)

Use Hermes Agent as the control plane for local coding agents.

</div>

---

## What is Hermes Code Bridge?

Hermes Code Bridge is a reusable [Hermes Agent](https://github.com/NousResearch/hermes-agent) skill for connecting Hermes to local terminal-based coding agents such as Codex, Kimi Code, Claude Code, OpenCode, Gemini CLI, and other coding CLIs.

It teaches Hermes how to:

- discover installed coding CLIs;
- choose the right backend and working directory;
- reuse existing CLI-agent sessions instead of creating unnecessary new ones;
- write structured dispatch prompts with constraints and success criteria;
- run the real local CLI, not a fake substitute;
- monitor background execution;
- collect raw evidence, artifacts, diffs, and verification results;
- report clearly what happened, what passed, and what remains risky.

The main idea is simple:

```text
User request
  -> Hermes plans and routes the task
  -> Codex / Kimi Code / Claude Code / OpenCode executes it locally
  -> Hermes monitors, verifies, and reports evidence
```

Hermes is the coordinator. Your local coding CLIs are the execution backends.

## Why use it?

Modern developers often use several coding agents at once. One tool might be better for implementation, another for review, another for debugging or long-context research. Without a workflow, it is easy to lose session context, send vague prompts, forget verification, or accidentally pretend that one agent did work that another agent actually did.

Hermes Code Bridge gives Hermes a disciplined bridge workflow:

| Need | What the skill provides |
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

The command recipes are intentionally written as patterns, because CLI flags change over time. Hermes should still check `<command> --help` when using a new version.

## Installation

### Option 1: Copy the skill into your Hermes skills directory

```bash
mkdir -p ~/.hermes/skills/autonomous-ai-agents/hermes-code-bridge
cp skills/hermes-code-bridge/SKILL.md ~/.hermes/skills/autonomous-ai-agents/hermes-code-bridge/SKILL.md
```

Then start a new Hermes session and load the skill:

```text
/skill hermes-code-bridge
```

or start Hermes with the skill preloaded:

```bash
hermes -s hermes-code-bridge
```

### Option 2: Install from a raw URL

If your Hermes version supports installing skills from raw URLs:

```bash
hermes skills install https://raw.githubusercontent.com/<OWNER>/<REPO>/main/skills/hermes-code-bridge/SKILL.md --name hermes-code-bridge
```

Replace `<OWNER>/<REPO>` with your repository path.

## Quick start

Ask Hermes something like:

```text
Use Codex to do a read-only review of the current repository diff. Do not modify files. Report correctness, security, and maintainability risks with evidence.
```

Hermes should then follow the bridge workflow:

1. load `hermes-code-bridge`;
2. check that Codex is installed;
3. confirm the working directory;
4. choose an existing session or a one-shot run;
5. dispatch a structured prompt to the real Codex CLI;
6. inspect output and repository state;
7. report command, result, evidence, and risks.

Example dispatch pattern:

```bash
cd <PROJECT_DIR>
codex exec "Read-only review: inspect the current git diff and identify correctness, security, and maintainability risks. Do not modify files. Report file paths, line references when possible, severity, and recommended fixes."
```

## Example prompts

### Ask Kimi Code to implement a scoped change

```text
Use Kimi Code to implement the smallest change that satisfies this bug fix. Reuse the existing project session if available. Do not refactor unrelated files. Run the relevant tests and report files changed, commands run, and remaining risks.
```

### Ask Claude Code to review a change

```text
Use Claude Code as a read-only reviewer for the latest diff. Do not modify files. List blockers, non-blockers, test gaps, and exact evidence from the diff.
```

### Ask OpenCode to inspect a project

```text
Use OpenCode to inspect this repository structure and suggest where a new feature should be implemented. Read-only only; do not create or edit files.
```

### Coordinate implementation and review

```text
Use one local coding agent to implement the change and a different one to review it. Confirm the backend/session plan before dispatch. Use separate worktrees if both agents need to edit files.
```

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

Tools such as CCB (`claude_codex_bridge`) provide visible tmux workspaces, configured agent panes, sidebars, worktrees, and inter-agent communication routes. Hermes Code Bridge is lighter: it is a Hermes skill that helps Hermes drive whatever local coding CLIs are already installed.

They can work together. If CCB is installed, Hermes can treat it as another bridge backend: inspect the CCB config, attach to the workspace, send prompts to the correct pane, and capture output.

## Repository layout

```text
hermes-code-bridge/
  README.md
  README_zh.md
  LICENSE
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
