# EVALS

> The scoreboard. Success criteria must be frozen before results exist.
> Per-slice gate files live in `docs/gates/`.

## Current slice gates

| Gate ID | Requirement | Verification command / method | Pass condition | Status |
| --- | --- | --- | --- | --- |
| `G-001` | `/health` test asserts JSON content type. | `npm --prefix examples/demo-run/repo test` | Test named `/health returns application/json content type` passes. | `PASS` |
| `G-002` | Existing `/health` response behavior remains unchanged. | `npm --prefix examples/demo-run/repo test` | S-001 health endpoint tests still pass. | `PASS` |
| `G-003` | No production behavior changes unless the new test exposes a real defect. | `git diff` | Production diff is empty or justified in `docs/HANDOFF.md`. | `PASS` |

## Required commands

| Command | Why | Required for PASS? |
| --- | --- | --- |
| `npm --prefix examples/demo-run/repo test` | Verify demo route behavior. | `yes` |
| `make validate` | Verify JudgeLoop package and demo. | `yes` |

## Manual checks

| Check | Steps | Pass condition |
| --- | --- | --- |
| Diff scope | Inspect changed files. | Only test and docs changed for S-002. |

## Non-negotiables

- No silent scope additions.
- No editing frozen contracts after results exist.
- No claiming success without raw command output or inspection evidence.
- No builder self-grading.
- No "mostly works" PASS.

## Results history

| Date | Slice | Gate | Result | Evidence |
| --- | --- | --- | --- | --- |
| `2026-06-22` | `S-001` | `G-001..G-003` | `PASS` | `node --test`, exit 0 |
| `2026-07-01` | `S-002` | `G-001..G-003` | `PASS` | `npm --prefix examples/demo-run/repo test`, exit 0; `make validate`, exit 0 |
