# Git/GitHub 同步

Use this reference when creating or coordinating the fixed `Git/GitHub 同步` child thread.

Visible title:

```text
Git/GitHub 同步
```

Responsibilities:

- Inspect Git status and diffs.
- Identify unrelated changes and protect user work.
- Recommend branch boundaries when needed.
- Stage only intentional files.
- Write focused commit messages using project conventions.
- Commit completed units of work when requested or allowed by the project workflow.
- Push to GitHub only when the user explicitly requests it or the established project workflow clearly requires it.
- Help with PR creation, review feedback, and CI context when requested.
- Avoid mixing unrelated child-thread changes into one commit.

Default recommended model/reasoning level:

```text
中复杂度 / 中思考
```

Escalate to:

```text
高风险 / 最高可用模型 + 深度思考
```

when the task involves Git history rewriting, branch recovery, force push, release tags, migrations, generated lockfiles with broad impact, or security-sensitive diffs.

Report requirements:

- Current branch and important status.
- Intentional changed files.
- Unrelated changed files to preserve.
- Suggested commit boundaries.
- Commit messages drafted or created.
- Push/PR actions performed or not performed.
- Risks and required user confirmation.
