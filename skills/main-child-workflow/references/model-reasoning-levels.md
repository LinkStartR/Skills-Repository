# Model And Reasoning Levels

Use these levels when creating child-thread task cards and updating `docs/codex/thread-index.md`. If the environment cannot switch model or reasoning depth, still record the recommendation.

## 低复杂度 / 低思考

Use for:

- Small documentation edits.
- Simple style adjustments.
- Single-file small fixes.
- Low-risk mechanical changes.

Expected behavior:

- Keep the task narrow.
- Avoid broad discovery.
- Verify with the smallest relevant check.

## 中复杂度 / 中思考

Use for:

- Normal feature implementation.
- Small refactors.
- Local module changes.
- Routine test additions.

Expected behavior:

- Inspect nearby patterns.
- Keep file scope bounded.
- Run focused tests or checks.

## 高复杂度 / 高思考

Use for:

- Cross-module features.
- Architecture design.
- Concurrent or async logic.
- Data structure design.
- Complex bug localization.

Expected behavior:

- Build a short plan before edits.
- Track dependencies and shared files.
- Verify behavior across affected modules.

## 高风险 / 最高可用模型 + 深度思考

Use for:

- Data safety.
- Git history changes.
- Migrations.
- Permissions.
- Storage formats.
- Long-term compatibility.
- Core architecture.

Expected behavior:

- Require explicit assumptions and risk notes.
- Avoid irreversible actions without confirmation.
- Prefer staged, rollback-friendly changes.
- Use the strongest available verification.
