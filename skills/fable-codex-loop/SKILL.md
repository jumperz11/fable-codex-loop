---
name: fable-codex-loop
description: Run the Fable + Builder scarce-architect loop for software projects. Use when the user wants Claude Fable 5 to act as architect, judge, scope killer, or checkpoint; Codex, Opus, GLM, Kimi, OpenClaw, or another coding agent to act as builder; repo docs to act as persistent memory; PR-sized slice planning; mandatory disagreement; frozen contracts; evaluator gates; reviewer lanes; raw handoffs; or a shareable AI-agent workflow.
---

# Fable + Builder Loop

Use this skill to run or set up the workflow:

> **Fable decides. The builder builds. The repo remembers. The human judges.**

Fable is used for scarce judgment, not endless typing. The selected builder does
the sustained execution work and records raw evidence. Codex is the default
builder path in this kit, but it is not required.

## Core rules

1. Fable is for judgment, not typing.
2. The selected builder is for building, testing, and evidence.
3. Repo docs are memory. If it is not in `docs/`, treat it as unknown.
4. Disagreement is mandatory before implementation.
5. Freeze success criteria before results exist.
6. Keep work PR-sized.
7. The builder never grades its own work.
8. If Fable is unavailable or expensive, the builder continues only from frozen specs and records unresolved decisions for the next Fable checkpoint.

## Set up a repo

If the repo does not already have memory docs, create:

- `docs/HANDOFF.md` - raw state after every work block
- `docs/CONTRACTS.md` - frozen APIs, schemas, file formats, ownership
- `docs/DECISIONS.md` - accepted/rejected decisions and why
- `docs/EVALS.md` - success gates frozen before results
- `docs/NEXT_SLICE.md` - one PR-sized next mission
- `docs/gates/` - per-slice frozen gates
- `docs/lanes/` - per-lane raw builder reports
- `docs/prd/` - optional short product and implementation briefs
- `docs/research/` - optional Fable-reviewed research reports

Use the templates in `references/repo-memory.md` if blank files are needed.

## Run a Fable checkpoint

Read these files first:

- `docs/HANDOFF.md`
- `docs/CONTRACTS.md`
- `docs/DECISIONS.md`
- `docs/EVALS.md`
- `docs/NEXT_SLICE.md`

Then produce:

1. current state from repo memory only
2. disagreements / risks
3. contracts to verify or freeze
4. next PR-sized slice spec
5. explicit out-of-scope
6. max 3 non-conflicting builder lanes
7. exactly one reviewer lane that writes no feature code
8. paste-ready builder block

For exact output structure, read `references/fable-architect.md`.

## Direct the builder

The selected builder must:

1. disagree before coding
2. cite real repo files checked
3. verify APIs/schemas/formats against reality
4. freeze `docs/CONTRACTS.md`, `docs/EVALS.md`, and `docs/NEXT_SLICE.md`
5. build in max 3 lanes only when file ownership does not conflict
6. run one reviewer lane that returns only `APPROVE` or numbered defects
7. update `docs/HANDOFF.md` with raw facts only
8. record unresolved strategic decisions instead of inventing them silently

For the paste-ready builder block, read `references/builder-contract.md`.

## Use headless dispatch only when it buys something

Manual mode is the default: Fable writes a block and the human pastes it into
the selected builder.

For larger Codex slices, Fable may prepare headless `codex exec` dispatch:

1. freeze gates in `docs/gates/<slice>.md`
2. write builder blocks into `.architect/`
3. run one fresh Codex process per lane
4. use git worktrees for parallel lanes
5. require every lane to write `docs/lanes/<slice>-<lane>.md`
6. verify gates and lane boundaries before integration

For the procedure, read `references/headless-dispatch.md`. This headless path
is Codex-specific. Other builders use the generic builder contract.

## Research checkpoint

Do not research every slice. Use research only when the team is deciding what
to build, choosing technology, or checking facts too large for routine builder
reality checks.

Builder/researcher agents gather. Fable designs lanes, verifies claims, and writes the
report. Final reports go in `docs/research/`; implementation briefs go in
`docs/prd/`.

For the procedure, read `references/fable-research.md`.

## Review builder output

When the builder returns results:

1. judge only raw evidence
2. compare against `docs/EVALS.md`
3. fail any mid-slice contract changes not explicitly approved by the human
4. fail if reviewer did not approve
5. rule PASS / FAIL / PARTIAL
6. accept, modify, or reject unresolved builder decisions
7. write the next slice or kill/rollback recommendation

For review structure, read `references/fable-review.md`.
