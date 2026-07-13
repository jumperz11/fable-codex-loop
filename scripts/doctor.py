#!/usr/bin/env python3
"""JudgeLoop Doctor.

Validates repo memory, fixed roles, frozen gates, worker evidence, and Fable
verdicts. Exit code 0 = ready, 1 = not ready. No third-party dependencies.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

from gates import verify_all

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
    "docs/verdicts",
]
ALLOWED_WORKERS = {"Sol", "Terra", "Luna"}
FINAL_VERDICTS = {"PASS", "FAIL", "PARTIAL"}

GREEN = "\033[32m"
RED = "\033[31m"
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
    r"<worker",
    r"<engine",
    r"<judge",
    r"<Fable verdict",
]


def _color(text: str, code: str, enabled: bool) -> str:
    return f"{code}{text}{RESET}" if enabled else text


def _table_value(text: str, field: str) -> str | None:
    pattern = rf"^\|\s*{re.escape(field)}\s*\|\s*(.*?)\s*\|$"
    match = re.search(pattern, text, re.MULTILINE | re.IGNORECASE)
    if not match:
        return None
    value = match.group(1).strip()
    return value.strip("`").strip()


def _slice_id(text: str) -> str | None:
    value = _table_value(text, "Slice ID")
    if value and re.fullmatch(r"S-\d+", value):
        return value
    return None


def _field_slice(text: str, field: str) -> str | None:
    value = _table_value(text, field)
    if not value:
        return None
    match = re.search(r"\bS-\d+\b", value)
    return match.group(0) if match else None


def _placeholder_hits(text: str) -> list[str]:
    hits: list[str] = []
    for pattern in PLACEHOLDER_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            hits.append(pattern)
    return hits


def _has_real_value(text: str, field: str) -> bool:
    value = _table_value(text, field)
    if not value or value in {"N/A", "-"}:
        return False
    return not bool(_placeholder_hits(value))


def _workers(value: str | None) -> list[str] | None:
    if not value:
        return None
    clean = re.sub(r"\band\b", ",", value, flags=re.IGNORECASE)
    parts = [part.strip().strip("`") for part in re.split(r"[,/]", clean) if part.strip()]
    if not parts or any(part not in ALLOWED_WORKERS for part in parts):
        return None
    if len(parts) != len(set(parts)):
        return None
    return parts


def _lane_value(text: str, field: str) -> str | None:
    table = _table_value(text, field)
    if table:
        return table
    match = re.search(rf"^{re.escape(field)}\s*:\s*(.+?)\s*$", text, re.MULTILINE | re.IGNORECASE)
    if not match:
        return None
    return match.group(1).strip().strip("`").strip()


def _worker_verdict(text: str) -> str | None:
    patterns = [
        r"^\s*(?:\*\*)?VERDICT(?:\*\*)?\s*:\s*(?:\*\*)?(PASS|FAIL|PARTIAL)\b",
        r"^\|\s*Verdict\s*\|\s*`?(PASS|FAIL|PARTIAL)`?\s*\|$",
        r"^\s*(?:\*\*)?FINAL VERDICT(?:\*\*)?\s*:\s*(?:\*\*)?(PASS|FAIL|PARTIAL)\b",
    ]
    for pattern in patterns:
        match = re.search(pattern, text, re.MULTILINE | re.IGNORECASE)
        if match:
            return match.group(1).upper()
    return None


def _check_roles(text: str, rel: str, problems: list[str], ok: list[str]) -> None:
    judge = _table_value(text, "Judge")
    if judge == "Fable":
        ok.append(f"{rel} fixes Judge as Fable")
    else:
        problems.append(f"{rel} must set Judge to Fable")

    workers = _workers(_table_value(text, "Workers"))
    if workers:
        ok.append(f"{rel} uses fixed workers: {', '.join(workers)}")
    else:
        problems.append(f"{rel} Workers must be a unique subset of Sol, Terra, Luna")


def check(root: Path, color: bool) -> tuple[list[str], list[str]]:
    root = root.resolve()
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
            _check_roles(text, rel, problems, ok)

        if rel == "docs/NEXT_SLICE.md":
            has_ac = re.search(r"`?AC-\d+`?\s*\|\s*\S", text)
            if not has_ac:
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
            _check_roles(text, rel, problems, ok)

        if rel == "docs/EVALS.md":
            if re.search(r"`?G-\d+`?\s*\|\s*\S", text):
                ok.append("EVALS has success gates")
            else:
                problems.append("docs/EVALS.md has no filled success gates")

        if rel == "docs/CONTRACTS.md":
            if "Freeze timestamp" in text and (
                "`<YYYY" in text or re.search(r"Freeze timestamp\s*\|\s*$", text, re.MULTILINE)
            ):
                problems.append("docs/CONTRACTS.md has no freeze timestamp")
            else:
                ok.append("CONTRACTS has a freeze status")
            if _table_value(text, "Frozen by") == "Fable":
                ok.append("CONTRACTS are frozen by Fable")
            else:
                problems.append("docs/CONTRACTS.md must set Frozen by to Fable")

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

    next_text = docs_text.get("docs/NEXT_SLICE.md", "")
    current_slice = _slice_id(next_text)
    if current_slice:
        for rel in ("docs/HANDOFF.md", "docs/CONTRACTS.md", "docs/EVALS.md"):
            actual = _field_slice(docs_text.get(rel, ""), "Current slice")
            if actual == current_slice:
                ok.append(f"{rel} current slice matches {current_slice}")
            else:
                problems.append(
                    f"{rel} Current slice must match NEXT_SLICE {current_slice}; found {actual or 'none'}"
                )

        handoff = docs_text.get("docs/HANDOFF.md", "")
        expected_gate = f"docs/gates/{current_slice}.md"
        expected_lanes = f"docs/lanes/{current_slice}-*.md"
        if _table_value(handoff, "Frozen gate file") != expected_gate:
            problems.append(f"docs/HANDOFF.md Frozen gate file must be {expected_gate}")
        if _table_value(handoff, "Lane reports") != expected_lanes:
            problems.append(f"docs/HANDOFF.md Lane reports must be {expected_lanes}")
        if _table_value(next_text, "Frozen gate file") != expected_gate:
            problems.append(f"docs/NEXT_SLICE.md Frozen gate file must be {expected_gate}")

    gate_ok, gate_problems = verify_all(root)
    ok.extend(gate_ok)
    problems.extend(gate_problems)

    lane_dir = root / "docs" / "lanes"
    lane_reports = sorted(path for path in lane_dir.glob("S-*.md") if path.is_file()) if lane_dir.is_dir() else []
    for lane_report in lane_reports:
        rel = str(lane_report.relative_to(root))
        lane_text = lane_report.read_text(encoding="utf-8", errors="replace")
        worker = _lane_value(lane_text, "Worker")
        if worker in ALLOWED_WORKERS:
            ok.append(f"{rel} worker is {worker}")
        else:
            problems.append(f"{rel} Worker must be Sol, Terra, or Luna")
        if _lane_value(lane_text, "Engine"):
            ok.append(f"{rel} records its engine")
        else:
            problems.append(f"{rel} has no Engine field")
        verdict = _worker_verdict(lane_text)
        if verdict:
            problems.append(f"{rel} illegally issues worker verdict {verdict}")
        if re.search(
            r"^`?STATUS:\s*(COMPLETE|COMPLETE_WITH_CONCERNS|BLOCKED)`?\s*$",
            lane_text,
            re.MULTILINE,
        ):
            ok.append(f"{rel} has final STATUS")
        else:
            problems.append(f"{rel} has no final STATUS line")

    handoff = docs_text.get("docs/HANDOFF.md", "")
    attempted = _table_value(handoff, "Slice attempted")
    final_status = _table_value(handoff, "Final status")
    if attempted and re.fullmatch(r"S-\d+", attempted) and final_status in FINAL_VERDICTS:
        completed_lanes = sorted(lane_dir.glob(f"{attempted}-*.md")) if lane_dir.is_dir() else []
        if completed_lanes:
            ok.append(f"lane report exists for last attempted slice {attempted}")
        else:
            problems.append(f"missing lane report for completed slice: docs/lanes/{attempted}-*.md")

        verdict_rel = _table_value(handoff, "Fable verdict")
        expected_verdict_rel = f"docs/verdicts/{attempted}.md"
        if verdict_rel != expected_verdict_rel:
            problems.append(f"docs/HANDOFF.md Fable verdict must be {expected_verdict_rel}")
        else:
            verdict_file = root / verdict_rel
            if not verdict_file.exists():
                problems.append(f"missing Fable verdict: {verdict_rel}")
            else:
                verdict_text = verdict_file.read_text(encoding="utf-8", errors="replace")
                if _table_value(verdict_text, "Judge") != "Fable":
                    problems.append(f"{verdict_rel} must set Judge to Fable")
                elif _table_value(verdict_text, "Verdict") != final_status:
                    problems.append(f"{verdict_rel} verdict must match HANDOFF Final status {final_status}")
                else:
                    ok.append(f"Fable verdict verified for {attempted}: {final_status}")

    return ok, problems


def main(argv: list[str]) -> int:
    root = Path(argv[1]) if len(argv) > 1 else Path.cwd()
    color = sys.stdout.isatty()

    print(_color("JudgeLoop Doctor", BOLD, color))
    print(f"repo: {root.resolve()}\n")

    ok, problems = check(root, color)

    for item in ok:
        print(f"{_color('OK', GREEN, color)}   {item}")
    for item in problems:
        print(f"{_color('FAIL', RED, color)} {item}")

    print()
    if problems:
        print(_color(f"Status: NOT READY ({len(problems)} issue(s))", RED, color))
        print("Fix the issues above before starting a worker run.")
        return 1

    print(_color("Status: READY", GREEN, color))
    print("Repo memory, fixed roles, and gate locks are healthy. Start the loop.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
