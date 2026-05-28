# Hermes Code Bridge installed

Enable the plugin and restart Hermes/Gateway if needed:

```bash
hermes plugins enable hermes-code-bridge
hermes gateway restart   # gateway users only
```

Use it inside Hermes:

```text
/code-bridge Use Codex to do a read-only review of the current repository diff.
```

If you prefer direct skill installation instead of the plugin wrapper:

```bash
hermes skills install https://raw.githubusercontent.com/<OWNER>/hermes-code-bridge/main/skills/hermes-code-bridge/SKILL.md --name hermes-code-bridge
```
