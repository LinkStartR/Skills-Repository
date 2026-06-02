---
name: horizonzhi-format-remane
description: Rename the current Codex conversation using HorizonZhi's standard Chinese title format. Use when the user says "按标准格式命名此对话" or "mmdh" in any conversation, or asks to apply the HorizonZhi standard conversation naming format.
---

# HorizonZhi Format Remane

## Overview

Rename the current conversation with a concise Chinese title that preserves the original conversation topic and uses the conversation's true start date.

## Trigger

Use this skill when the user says either of these commands:

- `按标准格式命名此对话`
- `mmdh`

## Required Format

Rename the conversation using this exact structure:

```text
【领域】对话主题标题 对话开始日期
```

The final title must be written in Chinese. Keep English only for proper nouns or technical terms such as `ChatGPT`, `Codex`, `PDF`, or `LaTeX`.

## Rules

1. Choose a broad domain category, such as `音乐`, `ChatGPT`, `Codex`, `大学物理`, `临时`, or `文档处理`.
2. Write a concise topic title that accurately summarizes the original main topic of the conversation.
3. If the conversation later drifted away from the original topic, base the title on the original topic.
4. Use the date of the user's first message in the current conversation as the start date, formatted as `yyyy-mm-dd`.
5. Do not use today's date unless today is actually the date of the user's first message in the current conversation.
6. If the true start date is unavailable, use the earliest date that can be reliably inferred from visible conversation context.
7. If no reliable start date can be inferred, ask the user for the conversation start date before renaming.

## Workflow

1. Inspect the visible conversation context to identify the original topic and the earliest reliable start date.
2. Choose the broad domain.
3. Compose the Chinese title in the required format.
4. Use the available thread title or conversation rename tool to rename the current conversation. If no rename tool is available, provide the exact title to use.

## Examples

- `【Codex】Skill 管理与运行记录 2026-06-02`
- `【文档处理】PDF 格式转换与批注整理 2026-05-28`
- `【ChatGPT】模型选择与提示词优化 2026-06-01`
