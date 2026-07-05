# Child Thread Report Template

Ask each child thread to report back with this structure.

```markdown
## 子线程回报

标题:

当前状态:

完成了什么:

修改了哪些文件:

未完成事项:

风险:

需要主线程合并:

需要 Git/GitHub 子线程处理提交:

需要测试子线程验证:

建议下一步:
```

Main-thread handling:

- Update `docs/codex/thread-index.md` after receiving the report.
- Resolve overlap or conflicts before merging work.
- Send completed implementation work to testing when risk or user-facing behavior changed.
- Send commit-ready completed work to `Git/GitHub 同步` only when the user or project workflow allows Git operations.
