---
name: linkstartr-format-remane
description: Rename the current Codex conversation using LinkStartR's standard Chinese title format. Use when the user says "按标准格式命名此对话" or "mmdh" in any conversation, or asks to apply the LinkStartR standard conversation naming format.
---

# LinkStartR Format Remane

## Overview

Rename the current conversation with a concise Chinese title that preserves the original conversation topic and uses the conversation's true start date.

## Trigger

Use this skill when the user says either of these commands:

- `按标准格式命名此对话`
- `mmdh`

## Required Format

For non-project conversations, rename the conversation using this exact structure:

```text
【领域】对话主题标题 yyyy-mm-dd
```

For conversations that are currently in a project, omit the domain bracket and use this exact structure:

```text
对话主题标题 yyyy-mm-dd
```

The final title must be written in Chinese. Keep English only for proper nouns or technical terms such as `ChatGPT`, `Codex`, `PDF`, or `LaTeX`.

## Rules

1. First determine whether the current conversation is in a project. If the conversation has an active project/workspace/repository context, or the visible context shows a project root or project-specific files, treat it as a project conversation.
2. If the current conversation is in a project, do not add `【领域】` or any other leading domain bracket. 中文：如果当前对话在一个项目中，就无需加 `【领域】`。
3. If the current conversation is not in a project, choose a broad domain category, such as `音乐`, `ChatGPT`, `Codex`, `大学物理`, `临时`, or `文档处理`.
4. Write a concise topic title that accurately summarizes the original main topic of the conversation.
5. If the conversation later drifted away from the original topic, base the title on the original topic.
6. Use the date of the user's first message in the current conversation as the start date, formatted as `yyyy-mm-dd`.
7. Do not use today's date unless today is actually the date of the user's first message in the current conversation.
8. If the true start date is unavailable, use the earliest date that can be reliably inferred from visible conversation context.
9. If no reliable start date can be inferred, ask the user for the conversation start date before renaming.

## Workflow

1. Inspect the visible conversation context to identify the original topic and the earliest reliable start date.
2. Determine whether the conversation is in a project.
3. If it is not in a project, choose the broad domain. If it is in a project, skip the domain.
4. Compose the Chinese title in the required format.
5. Use the available thread title or conversation rename tool to rename the current conversation. If no rename tool is available, provide the exact title to use.

## Examples

- Non-project: `【Codex】Skill 管理与运行记录 2026-06-02`
- Non-project: `【文档处理】PDF 格式转换与批注整理 2026-05-28`
- Non-project: `【ChatGPT】模型选择与提示词优化 2026-06-01`
- Project: `Skill 下载与封装管理 2026-06-02`
- Project: `登录流程修复与测试 2026-05-30`
