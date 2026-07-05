---
name: main-child-workflow
description: Use before planning, creating child threads, or editing code for large Codex projects, multi-module work, long-running engineering tasks, complex refactors, or high-risk changes that need a main-thread plus child-thread workflow. Coordinates task decomposition, child-thread creation, visibility checks, thread indexing, model/reasoning recommendations, Git/GitHub hygiene, user testing, Chinese progress reporting, and staged verification. Do not force this workflow for small tasks, single-file edits, or simple bug fixes.
---

# Main Child Workflow

Use this skill to coordinate large Codex work with one main thread and multiple small, visible, indexed child threads.

Default communication with the user in Chinese for planning, progress updates, thread index explanations, test notes, stage summaries, risk notes, and next-step recommendations. Preserve the project's existing conventions for code, commands, filenames, APIs, logs, package names, technical identifiers, and commit messages.

## Activation

Invoke this skill before planning, creating child threads, or editing code when the task is any of these:

- Large, multi-step, multi-module, long-running, or complex engineering work.
- Work that benefits from parallel, low-coupling subtasks.
- Work involving risky areas such as data safety, Git history, migrations, permissions, storage formats, long-term compatibility, or core architecture.
- Work where separate implementation, Git/GitHub, and testing responsibilities would make review and rollback safer.

Do not force the full workflow for small tasks, single-file edits, simple bug fixes, or low-risk mechanical changes. For those, state the assumption and proceed with the smallest reversible change.

If this skill cannot be loaded or applied, explain why in Chinese, then continue with the simplified main-thread plus child-thread workflow from `AGENTS.md`.

## Required References

Load only the references needed for the current step:

- `references/model-reasoning-levels.md`: read before assigning child-thread model/reasoning recommendations.
- `references/child-thread-task-card.md`: read before creating or assigning any child thread.
- `references/thread-index-template.md`: read before creating or updating `docs/codex/thread-index.md`.
- `references/child-thread-report-template.md`: read before asking a child thread to report back or when summarizing a child report.
- `references/git-github-thread.md`: read when creating or coordinating `Git/GitHub 同步`.
- `references/testing-next-step-thread.md`: read when creating or coordinating `用户测试与下一步建议`.

## Main Thread Workflow

1. Decide whether the full workflow is justified. If not, explain briefly and avoid over-orchestration.
2. Inspect the project structure, current task, existing instructions, Git state when relevant, and risk areas before decomposition.
3. Split work into small, low-coupling subtasks that are clear, verifiable, commit-ready, and rollback-friendly.
4. Define each child thread using the task card reference: title, role, goal, editable scope, forbidden scope, dependencies, verification, risk/conflict points, reporting expectations, and recommended model/reasoning level.
5. Create or identify required child threads. Long-running projects must include `Git/GitHub 同步` and `用户测试与下一步建议` unless clearly irrelevant.
6. Confirm each child thread was created successfully and is visible or locatable to the user before assigning critical work.
7. Register every child thread in the main-thread index and update `docs/codex/thread-index.md`.
8. Coordinate conflicts between child threads, especially shared files, branch boundaries, and test ownership.
9. Receive child-thread reports, update overall progress and `docs/codex/thread-index.md`, then decide whether to merge, test, commit, or continue.
10. Before finishing a stage, report what changed, why, how it was verified, what was not verified, risks, and next recommended steps.

## Child Thread Rules

Each child thread handles one bounded task only.

Child threads should:

- Modify the smallest reasonable set of related files.
- Avoid editing the same core files as other child threads unless coordinated by the main thread.
- Avoid mixing implementation, tests, documentation, Git commits, and release operations in one task.
- Report completed work, changed files, unfinished items, risks, merge needs, Git/GitHub needs, and testing needs.

Use the subtask name directly as the child-thread title. Do not add numbering, project prefixes, parent-child markers, status prefixes, or other decoration. Track numbering, parent relationship, status, file scope, branch, PR, commit range, visibility, recommended model/reasoning level, and notes only in the index.

Valid title examples:

```text
Keyboard Worker
Storage Worker
Settings 页面
Git/GitHub 同步
用户测试与下一步建议
```

## Visibility And Indexing

After creating a child thread, the main thread must:

1. Confirm creation succeeded.
2. Confirm the user can see or locate the child thread.
3. Set the child-thread title to the subtask name only.
4. Output a child-thread index table in the main thread.
5. Update `docs/codex/thread-index.md`.

If a child thread is invisible or cannot be located, troubleshoot in this order:

1. Ask the user to refresh the current Codex interface.
2. Ask the user to switch to another project, then switch back.
3. Ask the user to restart the Codex App.
4. Check whether the child thread entered archived chats.
5. Only then consider visibility operations from the main thread.

Pinning is not the default. Use pinning only as a fallback for abnormal display, poor locatability, or unstable UI state. Do not assign critical work to a child thread before it is visible or locatable.

## Fixed Long-Running Threads

For long-running projects, maintain at least:

- `Git/GitHub 同步`
- `用户测试与下一步建议`

Keep these threads visible or locatable, register them in `docs/codex/thread-index.md`, and update them as project state changes.

## Done Criteria

Before closing a stage or final response, provide in Chinese:

- Created or updated child threads and their current status.
- Files changed and why.
- Verification completed.
- Verification not completed.
- Risks and follow-up work.
- Whether Git/GitHub handling or user testing is still needed.
