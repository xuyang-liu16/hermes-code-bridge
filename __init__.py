"""Hermes Code Bridge plugin.

This plugin intentionally stays lightweight: the real workflow lives in
``skills/hermes-code-bridge/SKILL.md`` so it can also be installed as a normal
Hermes skill. The plugin adds one convenience slash command, ``/code-bridge``,
that injects a skill-loading instruction into the current Hermes session.
"""

from __future__ import annotations

from pathlib import Path

_SKILL_NAME = "hermes-code-bridge"
_PLUGIN_DIR = Path(__file__).resolve().parent


def _code_bridge_command(raw_args: str = "") -> str:
    """Return a skill-loading instruction for Hermes to process."""
    user_request = (raw_args or "").strip()
    qualified = f"{_SKILL_NAME}:{_SKILL_NAME}"
    if user_request:
        return (
            f"Please load and follow the `{qualified}` skill for this request.\n\n"
            f"User request:\n{user_request}"
        )
    return (
        f"Please load the `{qualified}` skill. Use it whenever the user wants "
        "Hermes to dispatch work to local coding CLIs such as Codex, Kimi Code, "
        "Claude Code, OpenCode, Gemini CLI, or another terminal-based coding assistant."
    )


def register(ctx) -> None:
    """Register the plugin skill and /code-bridge slash command."""
    ctx.register_skill(
        _SKILL_NAME,
        _PLUGIN_DIR / "skills" / _SKILL_NAME / "SKILL.md",
        description="Bridge Hermes Agent to local coding CLIs such as Codex, Kimi Code, Claude Code, OpenCode, and Gemini CLI.",
    )
    ctx.register_command(
        "code-bridge",
        handler=_code_bridge_command,
        description=(
            "Load Hermes Code Bridge for dispatching tasks to local coding CLIs "
            "such as Codex, Kimi Code, Claude Code, OpenCode, and Gemini CLI."
        ),
        args_hint="[request]",
    )
