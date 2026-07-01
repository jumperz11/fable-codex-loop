#!/usr/bin/env python3
"""Initialize repo memory for JudgeLoop.

Copies the docs/ memory files into a target repo if they do not already exist.
Safe by default: never overwrites existing files unless --force is passed.
"""
from __future__ import annotations

import argparse
import shutil
from pathlib import Path

KIT_ROOT = Path(__file__).resolve().parent.parent
DOC_FILES = [
    "HANDOFF.md",
    "CONTRACTS.md",
    "DECISIONS.md",
    "EVALS.md",
    "NEXT_SLICE.md",
]
DOC_DIRS = [
    "gates",
    "lanes",
    "prd",
    "research",
]


def ensure_architect_gitignore(target: Path) -> str:
    """Ensure JudgeLoop runtime files stay out of git."""
    gitignore = target / ".gitignore"
    entry = ".architect/"

    if not gitignore.exists():
        gitignore.write_text(f"{entry}\n", encoding="utf-8")
        return "created .gitignore (.architect/)"

    text = gitignore.read_text(encoding="utf-8", errors="replace")
    lines = [line.strip() for line in text.splitlines()]
    if entry in lines or ".architect" in lines:
        return "skipped .gitignore (.architect/ already ignored)"

    suffix = "" if text.endswith("\n") or not text else "\n"
    with gitignore.open("a", encoding="utf-8") as handle:
        handle.write(f"{suffix}{entry}\n")
    return "updated .gitignore (.architect/)"


def main() -> int:
    parser = argparse.ArgumentParser(description="Set up JudgeLoop repo memory.")
    parser.add_argument("target", nargs="?", default=".", help="Target repo directory.")
    parser.add_argument("--force", action="store_true", help="Overwrite existing docs.")
    args = parser.parse_args()

    target = Path(args.target).resolve()
    docs_dir = target / "docs"
    docs_dir.mkdir(parents=True, exist_ok=True)

    created, skipped = [], []
    for name in DOC_FILES:
        src = KIT_ROOT / "docs" / name
        dst = docs_dir / name
        if dst.exists() and not args.force:
            skipped.append(name)
            continue
        shutil.copyfile(src, dst)
        created.append(name)

    created_dirs, skipped_dirs = [], []
    for name in DOC_DIRS:
        src = KIT_ROOT / "docs" / name
        dst = docs_dir / name
        if dst.exists() and not args.force:
            skipped_dirs.append(name)
            continue
        if dst.exists():
            shutil.rmtree(dst)
        shutil.copytree(src, dst)
        created_dirs.append(name)

    for name in created:
        print(f"created docs/{name}")
    for name in skipped:
        print(f"skipped docs/{name} (already exists)")
    for name in created_dirs:
        print(f"created docs/{name}/")
    for name in skipped_dirs:
        print(f"skipped docs/{name}/ (already exists)")
    print(ensure_architect_gitignore(target))

    print("\nRepo memory ready. Next: fill docs/NEXT_SLICE.md, then run scripts/doctor.py")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
