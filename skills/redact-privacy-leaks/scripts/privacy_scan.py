#!/usr/bin/env python3
"""Strict local privacy scanner with an HTML selection workflow."""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import os
import re
import shutil
import webbrowser
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable


SKIP_DIRS = {
    ".git",
    ".hg",
    ".svn",
    ".venv",
    "venv",
    "node_modules",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    "dist",
    "build",
}

TEXT_EXTENSIONS = {
    ".txt",
    ".md",
    ".markdown",
    ".rst",
    ".py",
    ".js",
    ".jsx",
    ".ts",
    ".tsx",
    ".java",
    ".go",
    ".rs",
    ".cs",
    ".cpp",
    ".c",
    ".h",
    ".hpp",
    ".php",
    ".rb",
    ".swift",
    ".kt",
    ".json",
    ".jsonl",
    ".yaml",
    ".yml",
    ".toml",
    ".ini",
    ".cfg",
    ".csv",
    ".tsv",
    ".xml",
    ".html",
    ".css",
    ".sql",
    ".sh",
    ".ps1",
    ".bat",
    ".env",
    ".log",
}


@dataclass
class Finding:
    id: str
    file: str
    line: int
    column: int
    start: int
    end: int
    category: str
    sensitivity: str
    value: str
    masked_value: str
    reason: str
    suggested_replacement: str
    excerpt: str


PATTERNS = [
    ("email", "high", r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b", "[REDACTED_EMAIL]"),
    ("phone", "high", r"(?<!\d)(?:\+?\d{1,3}[-.\s]?)?(?:\(?\d{2,4}\)?[-.\s]?)?\d{3,4}[-.\s]?\d{4}(?!\d)", "[REDACTED_PHONE]"),
    ("ip-address", "medium", r"\b(?:\d{1,3}\.){3}\d{1,3}\b", "[REDACTED_IP]"),
    ("mac-address", "medium", r"\b[0-9A-Fa-f]{2}(?::[0-9A-Fa-f]{2}){5}\b", "[REDACTED_MAC]"),
    ("credential-or-token", "critical", r"(?i)\b(?:api[_-]?key|token|secret|password|passwd|pwd|session[_-]?id|cookie)\b\s*[:=]\s*['\"]?[^'\"\s,;]{6,}", "[REDACTED_SECRET]"),
    ("private-key", "critical", r"-----BEGIN [A-Z ]*PRIVATE KEY-----", "[REDACTED_PRIVATE_KEY]"),
    ("government-id", "critical", r"\b\d{6}(?:19|20)?\d{2}(?:0[1-9]|1[0-2])(?:0[1-9]|[12]\d|3[01])\d{3}[\dXx]\b", "[REDACTED_ID]"),
    ("student-or-employee-id", "high", r"(?i)\b(?:student|stu|school|employee|emp|学号|工号|学生证号)\s*(?:id|number|no\.?|编号|号码)?\s*[:：=]?\s*[A-Z0-9-]{4,20}\b", "[REDACTED_ID]"),
    ("birth-date", "high", r"(?i)\b(?:birth(?:day|date)?|dob|出生|生日)\s*[:：=]?\s*\d{4}[-/.年]\d{1,2}[-/.月]\d{1,2}日?\b", "[DATE_OF_BIRTH]"),
    ("age", "medium", r"(?i)\b(?:age|年龄)\s*[:：=]?\s*(?:1[0-9]|[2-9][0-9])\b|\b(?:1[0-9]|[2-9][0-9])\s*(?:years old|岁)\b", "[AGE_RANGE]"),
    ("personal-name-labeled", "high", r"(?im)\b(?:name|full[ _-]?name|real[ _-]?name|legal[ _-]?name|preferred[ _-]?name|contact[ _-]?name|姓名|名字|真实姓名|联系人)\s*[:：=]\s*[^\n,;|]{1,80}", "[REDACTED_NAME]"),
    ("location-labeled", "medium", r"(?im)\b(?:address|location|city|province|region|hometown|home town|地址|住址|地区|城市|省份|家乡|籍贯)\s*[:：=]\s*[^\n,;|]{1,120}", "[REGION]"),
    ("school-or-workplace", "medium", r"(?im)\b(?:school|university|college|employer|company|workplace|学校|大学|学院|公司|单位)\s*[:：=]\s*[^\n,;|]{1,120}", "[ORGANIZATION]"),
    ("profile-url", "high", r"https?://(?:www\.)?(?:github|gitlab|linkedin|facebook|instagram|x|twitter|weibo|zhihu|bilibili)\.com/[A-Za-z0-9_.@/-]+", "[PROFILE_URL]"),
    ("handle", "medium", r"(?i)\b(?:wechat|weixin|qq|telegram|discord|github|twitter|x handle|微博|微信|QQ)\s*[:：=]\s*@?[A-Za-z0-9_.-]{3,40}\b", "[ACCOUNT_HANDLE]"),
    ("preference-or-hobby", "medium", r"(?im)\b(?:hobby|hobbies|interest|interests|favorite|likes?|dislikes?|preference|爱好|兴趣|喜欢|偏好|讨厌)\s*[:：=]\s*[^\n.;。；]{1,120}", "[PERSONAL_PREFERENCE]"),
    ("personality-or-trait", "medium", r"(?im)\b(?:personality|mbti|trait|temperament|性格|人格|内向|外向)\s*[:：=]?\s*[^\n.;。；]{1,120}", "[PERSONAL_TRAIT]"),
    ("demographic-labeled", "medium", r"(?im)\b(?:gender|sex|nationality|ethnicity|race|religion|marital status|性别|民族|国籍|宗教|婚姻)\s*[:：=]\s*[^\n,;|]{1,80}", "[DEMOGRAPHIC_DETAIL]"),
    ("family-or-relationship", "medium", r"(?im)\b(?:family|parent|mother|father|sibling|roommate|friend|spouse|家庭|父母|妈妈|爸爸|室友|朋友|配偶)\s*[:：=]\s*[^\n.;。；]{1,120}", "[RELATIONSHIP_DETAIL]"),
    ("routine-or-schedule", "medium", r"(?im)\b(?:schedule|commute|class time|shift|route|日程|课表|通勤|路线|上课时间)\s*[:：=]\s*[^\n.;。；]{1,120}", "[ROUTINE_DETAIL]"),
    ("self-description", "low", r"(?im)\b(?:I am|I'm|my name is|my hometown is|我叫|我是|我的家乡|我来自)\s+[^\n.;。；]{2,120}", "[PERSONAL_DESCRIPTION]"),
]

COMPILED_PATTERNS = [(name, sev, re.compile(pattern), repl) for name, sev, pattern, repl in PATTERNS]


def is_probably_text_file(path: Path) -> bool:
    if path.name in {".env", ".npmrc", ".pypirc"}:
        return True
    if path.suffix.lower() in TEXT_EXTENSIONS:
        return True
    try:
        with path.open("rb") as handle:
            sample = handle.read(2048)
        return b"\x00" not in sample
    except OSError:
        return False


def iter_files(targets: Iterable[Path]) -> Iterable[Path]:
    for target in targets:
        if target.is_file():
            if is_probably_text_file(target):
                yield target
            continue
        if not target.is_dir():
            continue
        for root, dirs, files in os.walk(target):
            dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
            for name in files:
                path = Path(root) / name
                if is_probably_text_file(path):
                    yield path


def read_text(path: Path) -> str:
    for encoding in ("utf-8", "utf-8-sig", "gb18030", "latin-1"):
        try:
            return path.read_text(encoding=encoding)
        except UnicodeDecodeError:
            continue
    return path.read_text(errors="replace")


def line_col(text: str, index: int) -> tuple[int, int]:
    line = text.count("\n", 0, index) + 1
    last_newline = text.rfind("\n", 0, index)
    column = index + 1 if last_newline == -1 else index - last_newline
    return line, column


def mask_value(value: str) -> str:
    value = value.strip()
    if len(value) <= 4:
        return "*" * len(value)
    if len(value) <= 12:
        return value[:1] + "*" * (len(value) - 2) + value[-1:]
    return value[:3] + "*" * min(12, len(value) - 6) + value[-3:]


def make_excerpt(text: str, start: int, end: int) -> str:
    left = max(0, start - 60)
    right = min(len(text), end + 60)
    excerpt = text[left:start] + "[[" + text[start:end] + "]]" + text[end:right]
    return " ".join(excerpt.split())


def finding_id(path: Path, start: int, end: int, category: str, value: str) -> str:
    raw = f"{path}|{start}|{end}|{category}|{value}".encode("utf-8", errors="ignore")
    return hashlib.sha1(raw).hexdigest()[:16]


def scan_file(path: Path) -> list[Finding]:
    text = read_text(path)
    findings: list[Finding] = []
    seen: set[tuple[int, int, str]] = set()
    for category, sensitivity, pattern, replacement in COMPILED_PATTERNS:
        for match in pattern.finditer(text):
            start, end = match.span()
            key = (start, end, category)
            if key in seen:
                continue
            seen.add(key)
            value = match.group(0).strip()
            if not value or is_structural_false_positive(path, text, start, end, category, value):
                continue
            line, column = line_col(text, start)
            findings.append(
                Finding(
                    id=finding_id(path, start, end, category, value),
                    file=str(path.resolve()),
                    line=line,
                    column=column,
                    start=start,
                    end=end,
                    category=category,
                    sensitivity=sensitivity,
                    value=value,
                    masked_value=mask_value(value),
                    reason=reason_for(category),
                    suggested_replacement=replacement,
                    excerpt=make_excerpt(text, start, end),
                )
            )
    return sorted(findings, key=lambda item: (item.file, item.start, item.category))


def is_structural_false_positive(path: Path, text: str, start: int, end: int, category: str, value: str) -> bool:
    line_start = text.rfind("\n", 0, start) + 1
    line_end = text.find("\n", end)
    if line_end == -1:
        line_end = len(text)
    line = text[line_start:line_end].strip()
    lower_name = path.name.lower()
    if category == "personal-name-labeled":
        key, field_value = parse_key_value(line)
        if not key:
            return False
        if is_personal_name_key(key):
            return False
        if is_structural_key(key):
            return not looks_like_person_name(field_value)
        if lower_name in {"package.json", "package-lock.json", "pnpm-lock.yaml", "yarn.lock", "plugin.json", "openai.yaml"}:
            return not looks_like_person_name(field_value)
    return False


def parse_key_value(line: str) -> tuple[str, str]:
    match = re.match(r"^[\s\"']*([A-Za-z0-9_. -]+|[\u4e00-\u9fff]+)[\s\"']*[:=]\s*(.+?)\s*,?\s*$", line)
    if not match:
        return "", ""
    key = match.group(1).strip().strip("\"'").lower().replace("-", "_").replace(" ", "_")
    value = match.group(2).strip().strip(",").strip().strip("\"'")
    return key, value


def is_personal_name_key(key: str) -> bool:
    return key in {
        "full_name",
        "real_name",
        "legal_name",
        "preferred_name",
        "contact_name",
        "person_name",
        "student_name",
        "employee_name",
        "姓名",
        "名字",
        "真实姓名",
        "联系人",
    }


def is_structural_key(key: str) -> bool:
    if key in {"name", "title", "id", "identifier", "slug", "label", "display_name"}:
        return True
    return key.endswith("_name") or key.endswith("_id") or key.endswith("_title")


def looks_like_person_name(value: str) -> bool:
    cleaned = value.strip().strip("\"'")
    if not cleaned:
        return False
    if re.fullmatch(r"[A-Z][a-z]+(?:\s+[A-Z][a-z]+){1,3}", cleaned):
        return True
    if re.fullmatch(r"[\u4e00-\u9fff]{2,4}", cleaned):
        return True
    return False


def reason_for(category: str) -> str:
    reasons = {
        "credential-or-token": "可能授予访问权限，或用于认证个人/账号。",
        "preference-or-hobby": "个人偏好和爱好可能形成画像，或与其他信息组合后重新识别个人。",
        "personality-or-trait": "性格、人格和心理特征属于画像信息，尤其在个人叙述中风险更高。",
        "self-description": "自由文本中的自我描述可能识别作者，或暴露可画像信息。",
        "location-labeled": "地点信息可能用于定位个人，或与其他线索组合后重新识别。",
        "routine-or-schedule": "日程、路线和规律性活动可能造成跟踪风险。",
    }
    return reasons.get(category, "严格审查下的潜在个人信息或可关联信息。")


def write_report(findings: list[Finding], out_dir: Path) -> tuple[Path, Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    findings_json = {"findings": [asdict(f) for f in findings]}
    findings_path = out_dir / "privacy_findings.json"
    html_path = out_dir / "privacy_review.html"
    findings_path.write_text(json.dumps(findings_json, ensure_ascii=False, indent=2), encoding="utf-8")
    html_path.write_text(render_html(findings, findings_path), encoding="utf-8")
    return findings_path, html_path


def render_html(findings: list[Finding], findings_path: Path) -> str:
    severity_order = ["critical", "high", "medium", "low"]
    severity_labels = {"critical": "严重", "high": "高风险", "medium": "中风险", "low": "低风险"}
    severity_notes = {
        "critical": "密钥、凭据、证件号、金融、健康、生物识别或精确追踪类信息。",
        "high": "姓名、学号、联系方式、个人主页、账号句柄等直接标识符。",
        "medium": "地区、年龄、学校、偏好、爱好、性格等准标识符和画像信息。",
        "low": "单独看较弱，但与其他上下文组合后可能识别个人的线索。",
    }
    category_labels = {
        "email": "电子邮箱",
        "phone": "电话号码/长数字",
        "ip-address": "IP 地址",
        "mac-address": "MAC 地址",
        "credential-or-token": "凭据或令牌",
        "private-key": "私钥",
        "government-id": "证件号码",
        "student-or-employee-id": "学号/工号",
        "birth-date": "出生日期",
        "age": "年龄",
        "personal-name-labeled": "姓名",
        "location-labeled": "地区/地址",
        "school-or-workplace": "学校/工作单位",
        "profile-url": "个人主页链接",
        "handle": "账号句柄",
        "preference-or-hobby": "偏好/爱好",
        "personality-or-trait": "性格/人格特征",
        "demographic-labeled": "人口统计信息",
        "family-or-relationship": "家庭/关系信息",
        "routine-or-schedule": "日程/路线",
        "self-description": "自我描述",
    }
    grouped: dict[str, list[str]] = {key: [] for key in severity_order}
    counts = {key: 0 for key in severity_order}
    for finding in findings:
        counts[finding.sensitivity] = counts.get(finding.sensitivity, 0) + 1
        grouped.setdefault(finding.sensitivity, []).append(
            f"""
            <details class="finding {html.escape(finding.sensitivity)}" open>
              <summary>
                <label class="pick" onclick="event.stopPropagation()">
                  <input type="checkbox" data-id="{html.escape(finding.id)}" data-severity="{html.escape(finding.sensitivity)}" data-replacement="{html.escape(finding.suggested_replacement)}">
                  <span class="finding-title">{html.escape(category_labels.get(finding.category, finding.category))}</span>
                </label>
                <span class="masked">{html.escape(finding.masked_value)}</span>
              </summary>
              <div class="finding-body">
                <div class="path">{html.escape(finding.file)}:{finding.line}:{finding.column}</div>
                <div class="reason">{html.escape(finding.reason)}</div>
                <pre>{html.escape(finding.excerpt)}</pre>
                <label class="replacement-label">替换为</label>
                <input class="replacement" data-for="{html.escape(finding.id)}" value="{html.escape(finding.suggested_replacement)}">
              </div>
            </details>
            """
        )

    sections = []
    for severity in severity_order:
        items = grouped.get(severity, [])
        sections.append(
            f"""
            <section class="sec">
              <div class="sec-head">
                <div>
                  <h2>{severity_labels[severity]} <span>{len(items)}</span></h2>
                  <p>{html.escape(severity_notes[severity])}</p>
                </div>
                <div class="sec-actions">
                  <button onclick="selectSeverity('{severity}', true)">选择本组</button>
                  <button class="ghost" onclick="selectSeverity('{severity}', false)">清空本组</button>
                </div>
              </div>
              {''.join(items) if items else '<div class="empty">这一风险级别暂无发现。</div>'}
            </section>
            """
        )

    findings_abs = str(findings_path.resolve())
    script_abs = str(Path(__file__).resolve())
    default_out = str((findings_path.parent.parent / "redacted-output").resolve())
    apply_command = f'python "{script_abs}" apply "{findings_abs}" "privacy_selection.json" --out-dir "{default_out}"'
    findings_json_for_js = json.dumps(findings_abs, ensure_ascii=False)
    default_out_for_js = json.dumps(default_out, ensure_ascii=False)

    return f"""<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>隐私泄露检查报告</title>
<style>
  :root {{
    --bg:#f6f7f9; --card:#ffffff; --ink:#1d2129; --sub:#6b7280;
    --line:#e5e7eb; --accent:#165dff; --accent-bg:#e8f3ff;
    --critical:#9f1239; --high:#c2410c; --medium:#b08900; --low:#4b5563;
    --shadow:0 1px 3px rgba(0,0,0,.04),0 8px 24px rgba(0,0,0,.04);
  }}
  * {{ box-sizing:border-box; }}
  body {{ margin:0; background:var(--bg); color:var(--ink); font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",system-ui,sans-serif; line-height:1.55; }}
  .wrap {{ max-width:1120px; margin:0 auto; padding:28px 20px 72px; }}
  header {{ margin-bottom:22px; }}
  h1 {{ margin:0; font-size:28px; line-height:1.2; }}
  .meta {{ color:var(--sub); font-size:13px; margin-top:8px; }}
  .overview,.agent-panel {{ background:var(--card); border-radius:14px; box-shadow:var(--shadow); padding:22px; margin-bottom:22px; }}
  .stats {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(150px,1fr)); gap:12px; margin-top:16px; }}
  .stat {{ border:1px solid var(--line); border-radius:10px; padding:12px; background:#fafbfc; }}
  .stat .k {{ color:var(--sub); font-size:12px; }}
  .stat .v {{ font-size:22px; font-weight:700; font-variant-numeric:tabular-nums; }}
  .bar {{ display:flex; height:14px; border-radius:999px; overflow:hidden; background:var(--line); margin-top:16px; }}
  .bar i {{ display:block; min-width:2px; }}
  .bar .critical {{ background:var(--critical); }} .bar .high {{ background:var(--high); }}
  .bar .medium {{ background:var(--medium); }} .bar .low {{ background:var(--low); }}
  .toolbar {{ position:sticky; top:0; z-index:2; display:flex; gap:8px; flex-wrap:wrap; align-items:center; background:rgba(246,247,249,.94); backdrop-filter:blur(10px); padding:12px 0; border-bottom:1px solid var(--line); margin-bottom:18px; }}
  button {{ border:0; border-radius:8px; padding:8px 13px; background:var(--accent); color:#fff; font-weight:650; cursor:pointer; }}
  button.ghost {{ background:#eef0f3; color:var(--ink); }}
  button.primary {{ background:#0f766e; }}
  .cmd {{ flex:1 1 520px; min-width:280px; background:#1d2129; color:#e5e7eb; border-radius:10px; padding:10px 12px; font:12px/1.55 ui-monospace,SFMono-Regular,Consolas,monospace; overflow:auto; white-space:pre; }}
  .agent-head {{ display:flex; gap:10px; align-items:center; justify-content:space-between; flex-wrap:wrap; margin-bottom:10px; }}
  .agent-head strong {{ font-size:15px; }}
  .agent-panel textarea {{ width:100%; min-height:220px; resize:vertical; border:1px solid #cfd4dc; border-radius:10px; padding:12px; font:13px/1.6 ui-monospace,SFMono-Regular,Consolas,monospace; }}
  .sec {{ margin:24px 0; }}
  .sec-head {{ display:flex; gap:16px; justify-content:space-between; align-items:flex-end; margin-bottom:12px; }}
  h2 {{ margin:0; font-size:18px; }} h2 span {{ color:var(--sub); font-weight:500; }}
  .sec-head p {{ margin:4px 0 0; color:var(--sub); font-size:13px; max-width:760px; }}
  .sec-actions {{ display:flex; gap:8px; }}
  .finding {{ background:var(--card); border:1px solid var(--line); border-left:5px solid var(--line); border-radius:12px; box-shadow:var(--shadow); margin-bottom:10px; overflow:hidden; }}
  .finding.critical {{ border-left-color:var(--critical); }} .finding.high {{ border-left-color:var(--high); }}
  .finding.medium {{ border-left-color:var(--medium); }} .finding.low {{ border-left-color:var(--low); }}
  summary {{ display:flex; align-items:center; gap:12px; padding:14px 16px; cursor:pointer; list-style:none; }}
  summary::-webkit-details-marker {{ display:none; }}
  .pick {{ display:flex; align-items:center; gap:10px; min-width:220px; font-weight:700; cursor:pointer; }}
  .pick input {{ width:18px; height:18px; }}
  .masked {{ color:var(--sub); font-family:ui-monospace,SFMono-Regular,Consolas,monospace; overflow-wrap:anywhere; }}
  .finding-body {{ padding:0 16px 16px; }}
  .path,.reason,.replacement-label {{ color:var(--sub); font-size:13px; overflow-wrap:anywhere; }}
  pre {{ white-space:pre-wrap; overflow-wrap:anywhere; background:#f3f4f6; padding:12px; border-radius:8px; margin:10px 0; }}
  .replacement {{ width:100%; border:1px solid #cfd4dc; border-radius:8px; padding:9px 10px; margin-top:4px; font:13px ui-monospace,SFMono-Regular,Consolas,monospace; }}
  .empty {{ background:var(--card); border:1px dashed var(--line); border-radius:12px; padding:18px; color:var(--sub); }}
  .note {{ color:var(--sub); font-size:13px; margin-top:10px; }}
  @media (max-width:680px) {{ summary,.sec-head {{ display:block; }} .masked {{ display:block; margin-top:8px; }} .sec-actions {{ margin-top:10px; }} }}
</style>
</head>
<body>
<div class="wrap">
  <header>
    <h1>隐私泄露检查报告</h1>
    <div class="meta">严格本地审查。报告中会遮盖原始值；导出选择前可以先调整每一项的替换文本。</div>
  </header>
  <section class="overview">
    <strong>发现 {len(findings)} 个可能暴露隐私的项目。</strong>
    <div class="stats">
      <div class="stat"><div class="k">严重</div><div class="v">{counts.get("critical", 0)}</div></div>
      <div class="stat"><div class="k">高风险</div><div class="v">{counts.get("high", 0)}</div></div>
      <div class="stat"><div class="k">中风险</div><div class="v">{counts.get("medium", 0)}</div></div>
      <div class="stat"><div class="k">低风险</div><div class="v">{counts.get("low", 0)}</div></div>
    </div>
    <div class="bar">
      <i class="critical" style="width:{(counts.get("critical", 0) / max(1, len(findings)) * 100):.2f}%"></i>
      <i class="high" style="width:{(counts.get("high", 0) / max(1, len(findings)) * 100):.2f}%"></i>
      <i class="medium" style="width:{(counts.get("medium", 0) / max(1, len(findings)) * 100):.2f}%"></i>
      <i class="low" style="width:{(counts.get("low", 0) / max(1, len(findings)) * 100):.2f}%"></i>
    </div>
    <div class="note">只勾选你希望更改的项目，然后复制给 Agent 的修改指令，或导出选择 JSON。</div>
  </section>
  <div class="toolbar">
    <button onclick="setAll(true)">全选</button>
    <button class="ghost" onclick="setAll(false)">清空选择</button>
    <button onclick="downloadSelection()">导出选择 JSON</button>
    <button class="primary" onclick="copyAgentInstruction()">复制给 Agent 的修改指令</button>
    <button class="ghost" onclick="copyApplyCommand()">复制应用命令</button>
    <div class="cmd" id="applyCommand">{html.escape(apply_command)}</div>
  </div>
  <section class="agent-panel">
    <div class="agent-head">
      <strong>发给 Agent 的下一步指令</strong>
      <button class="primary" onclick="copyAgentInstruction()">复制这段指令</button>
    </div>
    <textarea id="agentInstruction" readonly></textarea>
    <div class="note">勾选项目或修改替换文本后，这段指令会自动更新。复制后直接发给 Codex/Agent，即可让它按你的选择生成脱敏副本并复扫验证。</div>
  </section>
  <main>
    {''.join(sections)}
  </main>
</div>
<script>
const FINDINGS_JSON = {findings_json_for_js};
const OUTPUT_DIR = {default_out_for_js};

function currentSelection() {{
  return Array.from(document.querySelectorAll('input[type=checkbox]:checked')).map(cb => {{
    const id = cb.dataset.id;
    const input = document.querySelector(`input[data-for="${{id}}"]`);
    return {{ id, replacement: input ? input.value : cb.dataset.replacement }};
  }});
}}
function setAll(value) {{
  document.querySelectorAll('input[type=checkbox]').forEach(cb => cb.checked = value);
  updateAgentInstruction();
}}
function selectSeverity(severity, value) {{
  document.querySelectorAll(`input[data-severity="${{severity}}"]`).forEach(cb => cb.checked = value);
  updateAgentInstruction();
}}
function downloadSelection() {{
  const selected = currentSelection();
  const blob = new Blob([JSON.stringify({{ selected }}, null, 2)], {{ type: 'application/json' }});
  const link = document.createElement('a');
  link.href = URL.createObjectURL(blob);
  link.download = 'privacy_selection.json';
  link.click();
}}
function buildAgentInstruction() {{
  const selected = currentSelection();
  if (!selected.length) {{
    return '请先在页面中勾选至少一个需要更改的隐私项。';
  }}
  const selectionJson = JSON.stringify({{ selected }}, null, 2);
  return `请使用 $redact-privacy-leaks 根据我在隐私检查 HTML 页面中勾选的项目进行隐私脱敏修改。

findings_json:
${{FINDINGS_JSON}}

请不要覆盖原文件，把修改后的副本输出到:
${{OUTPUT_DIR}}

selection:
\\`\\`\\`json
${{selectionJson}}
\\`\\`\\`

请执行对应 apply 流程。完成后请复扫修改后的文件，确认我勾选的隐私项不再出现，并把修改后的文件路径发给我。`;
}}
function updateAgentInstruction() {{
  const box = document.getElementById('agentInstruction');
  if (box) box.value = buildAgentInstruction();
}}
async function copyAgentInstruction() {{
  updateAgentInstruction();
  if (!currentSelection().length) {{
    alert('请先勾选至少一个需要更改的项目。');
    return;
  }}
  await navigator.clipboard.writeText(document.getElementById('agentInstruction').value);
}}
async function copyApplyCommand() {{
  const text = document.getElementById('applyCommand').innerText;
  await navigator.clipboard.writeText(text);
}}
document.querySelectorAll('input[type=checkbox], .replacement').forEach(el => {{
  el.addEventListener('change', updateAgentInstruction);
  el.addEventListener('input', updateAgentInstruction);
}});
updateAgentInstruction();
</script>
</body>
</html>
"""


def command_scan(args: argparse.Namespace) -> int:
    targets = [Path(item).expanduser() for item in args.targets]
    findings: list[Finding] = []
    for path in iter_files(targets):
        findings.extend(scan_file(path))
    findings_path, html_path = write_report(findings, Path(args.out_dir))
    print(f"Wrote {len(findings)} finding(s).")
    print(f"Review HTML: {html_path.resolve()}")
    print(f"Findings JSON: {findings_path.resolve()}")
    if args.open:
        webbrowser.open(html_path.resolve().as_uri())
    return 0


def load_selection(path: Path) -> dict[str, str]:
    data = load_json(path)
    selected = data.get("selected", data)
    if isinstance(selected, dict):
        return {str(k): str(v) for k, v in selected.items()}
    return {str(item["id"]): str(item.get("replacement", "[REDACTED]")) for item in selected}


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def command_apply(args: argparse.Namespace) -> int:
    findings_data = load_json(Path(args.findings_json))
    selection = load_selection(Path(args.selection_json))
    findings = [item for item in findings_data.get("findings", []) if item["id"] in selection]
    by_file: dict[str, list[dict]] = {}
    for finding in findings:
        by_file.setdefault(finding["file"], []).append(finding)

    skipped_overlaps = 0
    for file_name, file_findings in by_file.items():
        source = Path(file_name)
        text = read_text(source)
        changed = text
        non_overlapping, skipped = choose_non_overlapping(file_findings)
        skipped_overlaps += skipped
        for finding in sorted(non_overlapping, key=lambda item: item["start"], reverse=True):
            replacement = selection[finding["id"]]
            changed = changed[: finding["start"]] + replacement + changed[finding["end"] :]
        if args.in_place:
            destination = source
        else:
            out_root = Path(args.out_dir)
            try:
                relative = source.resolve().relative_to(Path.cwd().resolve())
            except ValueError:
                relative = Path(source.name)
            destination = out_root / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            if source.exists() and not destination.exists():
                shutil.copy2(source, destination)
        destination.write_text(changed, encoding="utf-8")
        print(f"Redacted {len(non_overlapping)} item(s): {destination}")
    if skipped_overlaps:
        print(f"Skipped {skipped_overlaps} overlapping selected finding(s) in favor of wider or more sensitive selections.")
    print(f"Applied {len(findings) - skipped_overlaps} selected redaction(s).")
    return 0


def choose_non_overlapping(findings: list[dict]) -> tuple[list[dict], int]:
    severity_rank = {"low": 1, "medium": 2, "high": 3, "critical": 4}
    chosen: list[dict] = []
    skipped = 0
    for finding in sorted(findings, key=lambda item: (item["start"], -(item["end"] - item["start"]))):
        if not chosen or finding["start"] >= chosen[-1]["end"]:
            chosen.append(finding)
            continue
        previous = chosen[-1]
        previous_score = (
            previous["end"] - previous["start"],
            severity_rank.get(previous.get("sensitivity", "low"), 0),
        )
        current_score = (
            finding["end"] - finding["start"],
            severity_rank.get(finding.get("sensitivity", "low"), 0),
        )
        if current_score > previous_score:
            chosen[-1] = finding
        skipped += 1
    return chosen, skipped


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Scan text files for strict privacy leaks and apply selected redactions.")
    subparsers = parser.add_subparsers(required=True)

    scan = subparsers.add_parser("scan", help="Create privacy_findings.json and privacy_review.html.")
    scan.add_argument("targets", nargs="+", help="Files or directories to scan.")
    scan.add_argument("--out-dir", default="privacy-review", help="Directory for review artifacts.")
    scan.add_argument("--open", action="store_true", help="Open privacy_review.html in the default browser after scanning.")
    scan.set_defaults(func=command_scan)

    apply = subparsers.add_parser("apply", help="Apply selected findings exported from the HTML review page.")
    apply.add_argument("findings_json", help="privacy_findings.json from scan.")
    apply.add_argument("selection_json", help="Selection JSON exported by privacy_review.html.")
    apply.add_argument("--out-dir", default="redacted-output", help="Directory for redacted copies.")
    apply.add_argument("--in-place", action="store_true", help="Overwrite original files.")
    apply.set_defaults(func=command_apply)
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
