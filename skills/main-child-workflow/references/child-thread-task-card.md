# Child Thread Task Card

Use this task card before creating or assigning a child thread. Keep the card focused enough that the child thread can finish one commit-ready unit of work.

```markdown
## 子线程任务卡

标题:

推荐模型 / 思考深度:

职责:

任务目标:

可修改范围:

不应修改范围:

依赖关系:

验证方式:

风险和冲突点:

完成后回报:
- 完成了什么
- 修改了哪些文件
- 未完成事项
- 风险
- 是否需要主线程合并
- 是否需要 Git/GitHub 子线程处理提交
- 是否需要测试子线程验证
```

Assignment rules:

- Use the subtask name directly as the visible thread title.
- Do not include IDs, status, project name, or prefixes in the title.
- Prefer file/module scopes that do not overlap with other child threads.
- Do not assign critical work until the child thread is visible or locatable.
- Put IDs, status, visibility, model recommendation, branch, PR, and commit range in the index only.
