#!/usr/bin/env python3
"""Freeze and verify JudgeLoop gate files with tracked SHA-256 locks."""
from __future__ import annotations

import argparse
import hashlib
import re
from pathlib import Path

SLICE_RE = re.compile(r"S-\d+")
LOCK_RE = re.compile(r"[0-9a-f]{64}")


def table_value(text: str, field: str) -> str | None:
    pattern = rf"^\|\s*{re.escape(field)}\s*\|\s*(.*?)\s*\|$"
    match = re.search(pattern, text, re.MULTILINE | re.IGNORECASE)
    if not match:
        return None
    return match.group(1).strip().strip("`").strip()


def current_slice(root: Path) -> str | None:
    path = root / "docs" / "NEXT_SLICE.md"
    if not path.exists():
        return None
    value = table_value(path.read_text(encoding="utf-8", errors="replace"), "Slice ID")
    if value and SLICE_RE.fullmatch(value):
        return value
    return None


def gate_path(root: Path, slice_id: str) -> Path:
    return root / "docs" / "gates" / f"{slice_id}.md"


def lock_path(root: Path, slice_id: str) -> Path:
    return root / "docs" / "gates" / f"{slice_id}.sha256"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def freeze_gate(root: Path, slice_id: str | None = None, force: bool = False) -> tuple[bool, str]:
    root = root.resolve()
    slice_id = slice_id or current_slice(root)
    if not slice_id or not SLICE_RE.fullmatch(slice_id):
        return False, "NEXT_SLICE.md has no concrete Slice ID like S-001"

    gate = gate_path(root, slice_id)
    if not gate.exists():
        return False, f"missing gate file: {gate.relative_to(root)}"

    text = gate.read_text(encoding="utf-8", errors="replace")
    if not re.search(r"`?G-\d+`?\s*\|", text):
        return False, f"{gate.relative_to(root)} has no gate rows"

    value = digest(gate)
    lock = lock_path(root, slice_id)
    if lock.exists():
        old = lock.read_text(encoding="utf-8", errors="replace").strip()
        if old == value:
            return True, f"already frozen: {gate.relative_to(root)} ({value})"
        if not force:
            return False, (
                f"refusing to replace changed lock: {lock.relative_to(root)}; "
                "Fable must review the change, then rerun with --force"
            )

    lock.write_text(f"{value}\n", encoding="utf-8")
    action = "re-froze" if force else "froze"
    return True, f"{action} {gate.relative_to(root)} -> {lock.relative_to(root)} ({value})"


def gate_slice_ids(root: Path) -> list[str]:
    gate_dir = root / "docs" / "gates"
    if not gate_dir.is_dir():
        return []
    result: list[str] = []
    for path in gate_dir.glob("S-*.md"):
        if SLICE_RE.fullmatch(path.stem):
            result.append(path.stem)
    return sorted(result)


def verify_gate(root: Path, slice_id: str) -> str | None:
    gate = gate_path(root, slice_id)
    lock = lock_path(root, slice_id)
    if not gate.exists():
        return f"missing gate file: {gate.relative_to(root)}"
    if not lock.exists():
        return f"missing gate lock: {lock.relative_to(root)}; run judgeloop freeze"
    expected = lock.read_text(encoding="utf-8", errors="replace").strip()
    if not LOCK_RE.fullmatch(expected):
        return f"invalid gate lock: {lock.relative_to(root)}"
    actual = digest(gate)
    if actual != expected:
        return (
            f"frozen gate changed: {gate.relative_to(root)} "
            f"(expected {expected}, got {actual})"
        )
    return None


def verify_all(root: Path) -> tuple[list[str], list[str]]:
    root = root.resolve()
    ok: list[str] = []
    problems: list[str] = []
    slice_ids = gate_slice_ids(root)
    if not slice_ids:
        return ok, ["no frozen slice gates found in docs/gates/"]
    for slice_id in slice_ids:
        problem = verify_gate(root, slice_id)
        if problem:
            problems.append(problem)
        else:
            ok.append(f"gate lock verified: docs/gates/{slice_id}.sha256")
    return ok, problems


def main() -> int:
    parser = argparse.ArgumentParser(description="Freeze or verify JudgeLoop gates.")
    sub = parser.add_subparsers(dest="command", required=True)

    freeze_parser = sub.add_parser("freeze", help="Write a SHA-256 lock for a gate file.")
    freeze_parser.add_argument("target", nargs="?", default=".", help="Target repo directory.")
    freeze_parser.add_argument("--slice", dest="slice_id", help="Slice ID; defaults to NEXT_SLICE.")
    freeze_parser.add_argument(
        "--force",
        action="store_true",
        help="Replace a changed lock after Fable explicitly approves the gate revision.",
    )

    verify_parser = sub.add_parser("verify", help="Verify every tracked gate lock.")
    verify_parser.add_argument("target", nargs="?", default=".", help="Target repo directory.")

    args = parser.parse_args()
    root = Path(args.target)

    if args.command == "freeze":
        success, message = freeze_gate(root, args.slice_id, args.force)
        print(message)
        return 0 if success else 1

    ok, problems = verify_all(root)
    for item in ok:
        print(f"OK   {item}")
    for item in problems:
        print(f"FAIL {item}")
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main())
