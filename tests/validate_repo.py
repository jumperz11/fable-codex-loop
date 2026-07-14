#!/usr/bin/env python3
"""Sanity checks for the JudgeLoop repo. Stdlib only."""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS = ROOT / "skills"
MAX_DESC = 1024
errors: list[str] = []
FORBIDDEN_ROLE_PHRASES = [
    "human judges",
    "human judge",
    "human is the final judge",
    "verdicts belong to fable and the human",
    "judge: fable + human",
    "architect + builder",
    "another strong model to act as architect",
]
STALE_MODEL_IDS = ("gpt-" + "5.5",)
TEXT_SUFFIXES = {".json", ".md", ".ps1", ".py", ".sh", ".toml", ".txt", ".yaml", ".yml"}


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def check_skill(skill_dir: Path) -> None:
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        errors.append(f"{skill_dir.name}: missing SKILL.md")
        return

    text = read(skill_md)
    match = re.match(r"---\n(.*?)\n---\n", text, re.DOTALL)
    if not match:
        errors.append(f"{skill_dir.name}: missing frontmatter")
        return

    frontmatter = match.group(1)
    name = re.search(r"^name:\s*(\S+)", frontmatter, re.MULTILINE)
    if not name or name.group(1) != skill_dir.name:
        errors.append(f"{skill_dir.name}: frontmatter name does not match directory")

    desc = re.search(
        r"^description:\s*>?\s*\n?(.*?)(?=^\w+:|\Z)",
        frontmatter,
        re.MULTILINE | re.DOTALL,
    )
    if not desc:
        errors.append(f"{skill_dir.name}: missing description")
    else:
        flat = re.sub(r"\s+", " ", desc.group(1)).strip()
        if len(flat) > MAX_DESC:
            errors.append(f"{skill_dir.name}: description is {len(flat)} chars > {MAX_DESC}")

    for ref in re.findall(r"`([\w./-]+\.md)`", text):
        if ref.startswith(("docs/", "AGENTS", "README", "HANDOFF", "NEXT_SLICE")):
            continue
        target = skill_dir / ref
        if not target.exists():
            errors.append(f"{skill_dir.name}: referenced file missing: {ref}")


def check_fences(path: Path) -> None:
    if read(path).count("```") % 2:
        errors.append(f"{path.relative_to(ROOT)}: odd number of code fences")


def check_local_links(path: Path) -> None:
    text = read(path)
    for label, target in re.findall(r"\[([^\]]+)\]\(([^)#\s]+)\)", text):
        if target.startswith(("http://", "https://", "mailto:")):
            continue
        if not (path.parent / target).exists() and not (ROOT / target).exists():
            errors.append(f"{path.relative_to(ROOT)}: link '{label}' -> {target} missing")


def check_role_contract() -> None:
    required = {
        "README.md": ["Fable always judges", "Sol, Terra, and Luna", "judgeloop freeze", "docs/verdicts/"],
        "prompts/01-architect-checkpoint.md": ["sole ARCHITECT and JUDGE", "Sol, Terra, Luna"],
        "prompts/02-builder-contract.md": ["Worker: [Sol / Terra / Luna]", "may not issue"],
        "prompts/03-architect-review.md": ["sole JUDGE", "docs/verdicts/<slice>.md"],
        "skills/judge-loop/SKILL.md": ["Fable is the sole architect", "Sol, Terra, and Luna are workers only"],
    }
    for rel, phrases in required.items():
        text = read(ROOT / rel)
        for phrase in phrases:
            if phrase not in text:
                errors.append(f"{rel}: missing fixed-role phrase: {phrase}")

    for path in ROOT.rglob("*.md"):
        if ".git" in path.parts:
            continue
        lower = read(path).lower()
        for phrase in FORBIDDEN_ROLE_PHRASES:
            if phrase in lower:
                errors.append(f"{path.relative_to(ROOT)}: forbidden role phrase: {phrase}")

    mirrors = {
        "prompts/01-architect-checkpoint.md": "skills/judge-loop/references/architect-checkpoint.md",
        "prompts/02-builder-contract.md": "skills/judge-loop/references/builder-contract.md",
        "prompts/03-architect-review.md": "skills/judge-loop/references/architect-review.md",
        "prompts/04-headless-dispatch.md": "skills/judge-loop/references/headless-dispatch.md",
        "prompts/05-research-checkpoint.md": "skills/judge-loop/references/research-checkpoint.md",
    }
    for source, mirror in mirrors.items():
        if read(ROOT / source) != read(ROOT / mirror):
            errors.append(f"{mirror}: does not mirror {source}")


def check_stale_model_ids() -> None:
    for path in ROOT.rglob("*"):
        if not path.is_file() or ".git" in path.parts:
            continue
        if path.suffix.lower() not in TEXT_SUFFIXES and path.name != "Makefile":
            continue
        lower = read(path).lower()
        for model_id in STALE_MODEL_IDS:
            if model_id in lower:
                errors.append(f"{path.relative_to(ROOT)}: stale model id: {model_id}")


def main() -> int:
    skill_dirs = sorted(path for path in SKILLS.iterdir() if path.is_dir())
    if not skill_dirs:
        errors.append("no skills found")

    for skill_dir in skill_dirs:
        check_skill(skill_dir)

    for path in ROOT.rglob("*.md"):
        if ".git" in path.parts:
            continue
        check_fences(path)
        if path.name in {"README.md", "SKILL.md"}:
            check_local_links(path)

    check_role_contract()
    check_stale_model_ids()

    if errors:
        print(f"FAIL: {len(errors)} problem(s)")
        for error in errors:
            print(f"  - {error}")
        return 1

    print(f"OK: {len(skill_dirs)} skill(s), markdown links, and fences validated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
