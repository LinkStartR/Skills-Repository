# Skills Repository

This repository stores reusable Codex skills maintained by HorizonZhi.

## Repository Layout

Skills are stored under `skills/<skill-name>/` so this repository can grow as more skills are added.

Each skill should keep the standard Codex skill structure:

```text
skills/
  <skill-name>/
    SKILL.md
    agents/
      openai.yaml
    scripts/       # optional
    references/    # optional
    assets/        # optional
```

## Current Skills

| Skill | Description |
| --- | --- |
| `horizonzhi-format-remane` | Renames Codex conversations using HorizonZhi's standard Chinese conversation-title format. Triggered by `按标准格式命名此对话` or `mmdh`. |

## Notes

- Use lowercase letters, digits, and hyphens for skill directory names.
- Keep each skill self-contained inside its own folder.
- Add future skills under `skills/` without changing existing skill contents unless an update is intentional.
