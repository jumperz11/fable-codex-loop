#!/usr/bin/env python3
"""Fable + Builder Loop Doctor.

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


def _color(text: str, code: str, enabled: bool) -> str:
    return f"{code}{text}{RESET}" if enabled else text


def check(root: Path, color: bool) -> tuple[list[str], list[str]]:
    ok: list[str] = []
    problems: list[str] = []

    for rel in REQUIRED_DOCS:
        path = root / rel
        if not path.exists():
            problems.append(f"missing file: {rel}")
            continue
        ok.append(f"{rel} exists")
        text = path.read_text(encoding="utf-8", errors="replace")

        if rel == "docs/HANDOFF.md":
            if re.search(r"Last updated\s*\|\s*$", text, re.MULTILINE) or "`<YYYY" in text:
                problems.append("docs/HANDOFF.md has no real 'Last updated' value")
            else:
                ok.append("HANDOFF has a last-updated value")

        if rel == "docs/NEXT_SLICE.md":
            has_ac = re.search(r"`?AC-\d+`?\s*\|\s*\S", text)
            placeholder = "<one sentence>" in text or "`<short title>`" in text
            if not has_ac or placeholder:
                problems.append("docs/NEXT_SLICE.md has no filled acceptance criteria")
            else:
                ok.append("NEXT_SLICE has acceptance criteria")

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

    return ok, problems


def main(argv: list[str]) -> int:
    root = Path(argv[1]) if len(argv) > 1 else Path.cwd()
    color = sys.stdout.isatty()

    print(_color(f"{BOLD}Fable + Builder Loop Doctor{RESET}", BOLD, color))
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
