# EVALS

> The scoreboard. Success criteria must be frozen before results exist.
> Do not move goalposts after seeing output.
> Per-slice frozen gate files live in `docs/gates/`.

| Field | Value |
| --- | --- |
| Current slice | `<slice id>` |

## Current slice gates

| Gate ID | Requirement | Verification command / method | Pass condition | Status |
| --- | --- | --- | --- | --- |
| `G-001` | `<requirement>` | `<command or inspection>` | `<objective pass condition>` | `pending` |

## Required commands

| Command | Why | Required for PASS? |
| --- | --- | --- |
| `<command>` | `<reason>` | `yes/no` |

## Manual checks

| Check | Steps | Pass condition |
| --- | --- | --- |
| `<check>` | `<steps>` | `<condition>` |

## Non-negotiables

- No silent scope additions.
- No editing frozen contracts after results exist.
- No claiming success without raw command output or inspection evidence.
- No worker self-grading. Sol, Terra, and Luna never issue protocol verdicts.
- No "mostly works" PASS.

## Results history

| Date | Slice | Gate | Result | Evidence |
| --- | --- | --- | --- | --- |
| `<date>` | `<slice>` | `<gate>` | `PASS/FAIL` | `<output>` |
