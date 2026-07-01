#!/usr/bin/env python3
"""JudgeLoop Doctor.

Validates that a repo's memory (docs/) is healthy enough to start a build block.
Exit code 0 = ready, 1 = not ready. No third-party dependencies.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

REQUIRED_DOCS = [
    "docs/HANDOFF.md",
    "docs/CONTRACTS.md",
    "docs/DECISIONS.md",
    "docs/EVALS.md",
    "docs/NEXT_SLICE.md",
]
REQUIRED_DIRS = [
    "docs/gates",
    "docs/lanes",
]

GREEN = "\033[32m"
RED = "\033[31m"
YELLOW = "\033[33m"
BOLD = "\033[1m"
RESET = "\033[0m"
PLACEHOLDER_PATTERNS = [
    r"<project name>",
    r"<human owner>",
    r"<slice>",
    r"<one sentence",
    r"<slice id",
    r"<short title>",
    r"<specific outcome>",
    r"<test/command/file>",
    r"<API/doc/schema check>",
    r"<why>",
    r"<file/link/command>",
    r"<task>",
    r"<paths>",
    r"<timestamp>",
    r"<fact>",
    r"<command output>",
    r"<raw note>",
    r"<name>",
    r"<fields>",
    r"<notes>",
]


def _color(text: str, code: str, enabled: bool) -> str:
    return f"{code}{text}{RESET}" if enabled else text


def _table_value(text: str, field: str) -> str | None:
    pattern = rf"^\|\s*{re.escape(field)}\s*\|\s*(.*?)\s*\|$"
    match = re.search(pattern, text, re.MULTILINE)
    if not match:
        return None
    value = match.group(1).strip()
    return value.strip("`").strip()


def _slice_id(text: str) -> str | None:
    value = _table_value(text, "Slice ID")
    if value and re.fullmatch(r"S-\d+", value):
        return value
    return None


def _placeholder_hits(text: str) -> list[str]:
    hits: list[str] = []
    for pattern in PLACEHOLDER_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            hits.append(pattern)
    return hits


def _has_real_value(text: str, field: str) -> bool:
    value = _table_value(text, field)
    if not value:
        return False
    if value in {"N/A", "-", ""}:
        return False
    return not bool(_placeholder_hits(value))


def check(root: Path, color: bool) -> tuple[list[str], list[str]]:
    ok: list[str] = []
    problems: list[str] = []
    docs_text: dict[str, str] = {}

    for rel in REQUIRED_DOCS:
        path = root / rel
        if not path.exists():
            problems.append(f"missing file: {rel}")
            continue
        ok.append(f"{rel} exists")
        text = path.read_text(encoding="utf-8", errors="replace")
        docs_text[rel] = text
        placeholders = _placeholder_hits(text)
        if placeholders:
            problems.append(f"{rel} has placeholder text: {', '.join(placeholders[:3])}")

        if rel == "docs/HANDOFF.md":
            if re.search(r"Last updated\s*\|\s*$", text, re.MULTILINE) or "`<YYYY" in text:
                problems.append("docs/HANDOFF.md has no real 'Last updated' value")
            else:
                ok.append("HANDOFF has a last-updated value")
            for field in ("Current slice", "Frozen gate file", "Lane reports"):
                if _has_real_value(text, field):
                    ok.append(f"HANDOFF has {field}")
                else:
                    problems.append(f"docs/HANDOFF.md has no real '{field}' value")

        if rel == "docs/NEXT_SLICE.md":
            has_ac = re.search(r"`?AC-\d+`?\s*\|\s*\S", text)
            placeholder = "<one sentence>" in text or "`<short title>`" in text
            if not has_ac or placeholder:
                problems.append("docs/NEXT_SLICE.md has no filled acceptance criteria")
            else:
                ok.append("NEXT_SLICE has acceptance criteria")
            sid = _slice_id(text)
            if sid:
                ok.append(f"NEXT_SLICE has slice id {sid}")
                gate_file = root / "docs" / "gates" / f"{sid}.md"
                if gate_file.exists():
                    ok.append(f"matching gate file exists: docs/gates/{sid}.md")
                    gate_text = gate_file.read_text(encoding="utf-8", errors="replace")
                    gate_placeholders = _placeholder_hits(gate_text)
                    if gate_placeholders:
                        problems.append(
                            f"docs/gates/{sid}.md has placeholder text: {', '.join(gate_placeholders[:3])}"
                        )
                    if not re.search(r"`?G-\d+`?\s*\|", gate_text):
                        problems.append(f"docs/gates/{sid}.md has no gate rows")
                    else:
                        ok.append(f"docs/gates/{sid}.md has gate rows")
                else:
                    problems.append(f"missing matching gate file: docs/gates/{sid}.md")
            else:
                problems.append("docs/NEXT_SLICE.md has no concrete Slice ID like S-001")

        if rel == "docs/EVALS.md":
            has_gate = re.search(r"`?G-\d+`?\s*\|\s*\S", text)
            placeholder = "`<requirement>`" in text
            if not has_gate or placeholder:
                problems.append("docs/EVALS.md has no filled success gates")
            else:
                ok.append("EVALS has success gates")

        if rel == "docs/CONTRACTS.md":
            if "Freeze timestamp" in text and ("`<YYYY" in text or re.search(r"Freeze timestamp\s*\|\s*$", text, re.MULTILINE)):
                problems.append("docs/CONTRACTS.md has no freeze timestamp")
            else:
                ok.append("CONTRACTS has a freeze status")

    for rel in REQUIRED_DIRS:
        path = root / rel
        if path.is_dir():
            ok.append(f"{rel}/ exists")
        else:
            problems.append(f"missing directory: {rel}/")

    gitignore = root / ".gitignore"
    if gitignore.exists():
        text = gitignore.read_text(encoding="utf-8", errors="replace")
        if ".architect/" in text or ".architect" in text:
            ok.append(".architect runtime directory is gitignored")
        else:
            problems.append(".gitignore should include .architect/")
    else:
        problems.append("missing .gitignore entry for .architect/")

    handoff = docs_text.get("docs/HANDOFF.md", "")
    attempted = _table_value(handoff, "Slice attempted")
    final_status = _table_value(handoff, "Final status")
    if attempted and re.fullmatch(r"S-\d+", attempted) and final_status in {"PASS", "FAIL", "PARTIAL"}:
        lane_dir = root / "docs" / "lanes"
        lane_reports = sorted(lane_dir.glob(f"{attempted}-*.md"))
        if lane_reports:
            ok.append(f"lane report exists for last attempted slice {attempted}")
            for lane_report in lane_reports:
                lane_text = lane_report.read_text(encoding="utf-8", errors="replace")
                if re.search(r"^`?STATUS:\s*(COMPLETE|COMPLETE_WITH_CONCERNS|BLOCKED)`?\s*$", lane_text, re.MULTILINE):
                    ok.append(f"{lane_report.relative_to(root)} has final STATUS")
                else:
                    problems.append(f"{lane_report.relative_to(root)} has no final STATUS line")
        else:
            problems.append(f"missing lane report for completed slice: docs/lanes/{attempted}-*.md")

    return ok, problems


def main(argv: list[str]) -> int:
    root = Path(argv[1]) if len(argv) > 1 else Path.cwd()
    color = sys.stdout.isatty()

    print(_color(f"{BOLD}JudgeLoop Doctor{RESET}", BOLD, color))
    print(f"repo: {root.resolve()}\n")

    ok, problems = check(root, color)

    for item in ok:
        print(f"{_color('OK', GREEN, color)}   {item}")
    for item in problems:
        print(f"{_color('FAIL', RED, color)} {item}")

    print()
    if problems:
        print(_color(f"Status: NOT READY ({len(problems)} issue(s))", RED, color))
        print("Fix the issues above before starting a builder run.")
        return 1

    print(_color("Status: READY", GREEN, color))
    print("Repo memory looks healthy. Start the loop.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
