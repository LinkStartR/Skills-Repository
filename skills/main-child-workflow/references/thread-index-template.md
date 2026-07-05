# Thread Index Template

Use this template for `docs/codex/thread-index.md`. Keep the document concise and update it whenever a child thread is created, reassigned, completed, blocked, merged, tested, committed, or archived.

```markdown
# Codex Thread Index

Last updated: YYYY-MM-DD HH:mm

## Overview

Project goal:

Current stage:

Main thread responsibilities:

## Child Threads

| ID | 子线程标题 | 负责任务 | 当前状态 | 模块或文件范围 | 分支 / PR / 提交范围 | 可见或可定位 | 推荐模型 / 思考深度 | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| C1 | Git/GitHub 同步 | Git 状态、分支、提交、PR 协调 | 常驻 | `.git`, branch, PR | TBD | 是 / 待确认 | 中复杂度 / 中思考 | 不得擅自 push |
| C2 | 用户测试与下一步建议 | 测试清单、用户反馈、下一步优先级 | 常驻 | tests, QA notes | TBD | 是 / 待确认 | 中复杂度 / 中思考 | 记录未验证项 |

## Status Legend

- `待创建`: The thread is planned but not created.
- `待确认可见`: The thread exists but visibility or locatability is not confirmed.
- `待开始`: The thread is visible or locatable and ready for assignment.
- `进行中`: The thread is working on its assigned task.
- `待回报`: The main thread is waiting for a report.
- `待合并`: Work is complete and needs main-thread integration.
- `待验证`: Work needs automated or user testing.
- `已完成`: Work is integrated and verified for the current stage.
- `阻塞`: Progress needs user input, external access, or conflict resolution.
- `常驻`: Long-running support thread.

## Coordination Notes

- Shared files:
- Cross-thread dependencies:
- Known risks:
- Next decision:
```

Rules:

- Use child-thread IDs only in this index, not in visible child-thread titles.
- Mark visibility as `是`, `否`, or `待确认`.
- Record recommended model/reasoning level even when the environment cannot switch models.
- Keep branch, PR, and commit ranges blank or `TBD` until confirmed.
