---
name: judge-loop
description: Run JudgeLoop with fixed authority: Fable is always the architect and sole judge; Sol, Terra, and Luna are always workers powered by Codex or another engine; repo docs store frozen gates, SHA-256 locks, lane evidence, Fable verdicts, and the next PR-sized slice. Use for evidence-gated AI software work, explicit disagreement, worker lanes, raw handoffs, or Fable PASS, FAIL, and PARTIAL reviews.
---

# JudgeLoop

> **Fable always judges. Sol, Terra, and Luna work. Repo stores proof. Human ships.**

## Fixed authority

1. Fable is the sole architect and protocol judge.
2. Sol, Terra, and Luna are workers only.
3. Worker engines may vary; identities and authority may not.
4. Workers report evidence or reviewer findings and never issue PASS, FAIL, or PARTIAL.
5. The human owns the final ship or stop decision after Fable's verdict.

## Set up repo memory

Prefer the installed CLI:

```bash
judgeloop init .
```

This creates HANDOFF, CONTRACTS, DECISIONS, EVALS, NEXT_SLICE, gates, lanes,
verdicts, PRD, and research memory under `docs/`.

For exact file shapes, read `references/repo-memory.md`.

## Run a Fable checkpoint

Fable reads the repo memory, narrows one PR-sized slice, assigns a subset of
Sol, Terra, and Luna, writes objective gates, and freezes them:

```bash
judgeloop freeze .
judgeloop doctor .
```

Do not dispatch workers until both commands succeed. For the exact checkpoint
prompt, read `references/architect-checkpoint.md`.

## Direct workers

Every worker block must include:

- Worker: Sol, Terra, or Luna
- Engine: model or tool powering that worker
- exact file ownership
- mandatory disagreement and reality checks
- `judgeloop verify .` before edits
- raw commands, exits, changed files, and risks
- one allowed final status: COMPLETE, COMPLETE_WITH_CONCERNS, or BLOCKED

Workers must not edit `docs/gates/`, `.sha256` locks, HANDOFF Final status, or
the Fable verdict field. Workers must not write protocol verdicts.

For the complete worker block, read `references/builder-contract.md`.

## Review evidence with Fable

Fable verifies locks and memory before judging:

```bash
judgeloop verify .
judgeloop doctor .
```

Fable alone writes `docs/verdicts/<slice>.md` with Judge `Fable` and Verdict
`PASS`, `FAIL`, or `PARTIAL`, then updates HANDOFF and freezes the next slice.
The human then chooses ship or stop.

For the exact review structure, read `references/architect-review.md`.

## Headless dispatch

Use headless Codex only when parallel work is worth the overhead. Every process
still runs as Sol, Terra, or Luna, keeps disjoint ownership, writes a lane
report, and leaves judgment to Fable. Read `references/headless-dispatch.md`.

## Research

Research workers gather evidence; Fable synthesizes and judges. Use no more than
the three fixed workers. Read `references/research-checkpoint.md`.

## Failure rules

- Gate or lock changed after freeze: stop; Fable must review and explicitly re-freeze.
- Worker issued a protocol verdict: reject the lane report.
- Slice IDs disagree across memory: do not dispatch.
- Missing Fable verdict after a completed slice: the loop is incomplete.
- Fable unavailable: workers continue only from frozen specs; unresolved decisions wait.
