---
name: redact-privacy-leaks
description: Strict privacy and personal-information leak review for code, generated documents, prompts, notes, datasets, logs, Markdown, JSON, CSV, and other text artifacts. Use when the user asks to find, audit, remove, redact, anonymize, sanitize, or interactively review possible exposure of names, student IDs, locations, ages, preferences, hobbies, personality traits, demographics, contact details, identifiers, secrets, or any information that could identify, profile, track, or re-identify a person.
---

# Redact Privacy Leaks

## Core Rule

Treat privacy broadly and conservatively. Flag direct identifiers, quasi-identifiers, sensitive attributes, personal traits, preferences, and combinations that could identify or profile a person. False positives are acceptable; silent misses are not.

Never modify original user files until the user has selected what to change. Default to writing redacted copies.

## Workflow

1. Define scope: identify the files, directories, or generated text to review. For generated chat content, write it to a temporary text file first.
2. Inspect text-like artifacts only unless the user asks for binary/document handling. Skip dependency folders and generated caches unless explicitly in scope.
3. Run the scanner:

```bash
python <skill>/scripts/privacy_scan.py scan <target...> --out-dir <review-dir>
```

Add `--open` when the environment can open a browser for the user.

4. Give the user the generated HTML page explicitly. This is mandatory: include a clickable path or local URL for `<review-dir>/privacy_review.html`.
5. Direct the user to tick the items they want changed. The page automatically builds a Chinese "copy to Agent" instruction containing `privacy_findings.json`, the selected ids, replacements, and the output directory. Prefer this path over asking non-technical users to manage JSON files manually.
6. If the user pastes the generated Agent instruction back into chat, save the embedded `selection` JSON to a temporary file, then apply it:

```bash
python <skill>/scripts/privacy_scan.py apply <review-dir>/privacy_findings.json <selection.json> --out-dir <redacted-dir>
```

Use `--in-place` only when the user explicitly asks to overwrite the originals.

7. Verify the output by rescanning the redacted files and checking that selected items no longer appear. Mention unselected items without repeating sensitive values.

## Review Standards

Read `references/privacy_taxonomy.md` when:

- The artifact contains personal narratives, education, health, minors, locations, demographic details, or preference/personality data.
- The user asks for the strictest possible review.
- You are unsure whether something is personal information.

Default classifications:

- Critical: secrets, government IDs, financial IDs, health or biometric details, precise locations, credentials.
- High: names plus context, student/employee IDs, contact details, exact birth dates, account handles, personal URLs.
- Medium: city/region, age, school/workplace, schedule, relationship/family details, hobbies, preferences, personality traits, demographics.
- Low: weak contextual hints that may become identifying when combined.

## False Positives

Do not blindly redact structural metadata. Skill names, package names, plugin names, service identifiers, YAML frontmatter such as `name: main-child-workflow`, package metadata such as `package.json` `name`, and configuration keys such as `name`, `title`, `id`, `identifier`, `slug`, `display_name`, `service_name`, or `*_id` are usually not personal information.

Use context-aware handling:

- Skip structural metadata when the value is a machine identifier, slug, package name, service name, workflow name, or internal title.
- Keep reporting when the value itself looks like a real person's name, such as `name: Alice Zhang` or `name: 张三`.
- Always report explicitly personal fields such as `full_name`, `real_name`, `legal_name`, `preferred_name`, `contact_name`, `姓名`, `真实姓名`, or `联系人`.
- If unsure, keep the finding in the HTML page but explain that it may be a false positive so the user can leave it unchecked.

If a selected finding appears in code or metadata where replacement could break syntax, choose a syntactically valid placeholder and run relevant validators or tests.

## Applying Redactions

Prefer replacements that preserve utility without exposing the person:

- Direct identifiers: `[REDACTED_NAME]`, `[REDACTED_EMAIL]`, `[REDACTED_PHONE]`.
- Quasi-identifiers: generalize, for example `Shanghai` -> `[REGION]`, `19` -> `[AGE_RANGE]`.
- Traits and preferences: replace with `[PERSONAL_PREFERENCE]`, `[PERSONAL_TRAIT]`, or remove if unnecessary.
- Code fixtures/tests: use clearly fake examples such as `example.com`, `000000`, `Student A`, or `Test User`.

## Reporting

Do not paste raw sensitive values back to the user unless necessary for confirmation. Summarize by category, file, and count. If examples are needed, mask most of the value.

Always include the review HTML location in the final answer after scanning, for example:

```text
Review page: <absolute path to privacy_review.html>
```

State whether changes were written to copies or in place, and list the verification performed.
