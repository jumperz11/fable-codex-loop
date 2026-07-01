# Prompt 04 - Codex Headless Dispatch

Use this only after the manual loop works. Headless dispatch is for larger
slices where unattended Codex CLI runs or parallel lanes are worth the overhead.

This prompt is Codex-specific. For Opus, GLM, Kimi, OpenClaw, or another
builder, use the generic builder contract in `prompts/02-builder-contract.md`.

You are FABLE, preparing headless Codex dispatch.

Use this only if the slice is too large for one interactive Codex session.
Otherwise say: "Use manual mode."

Before dispatch:

1. Confirm `codex --version`.
2. Create or confirm `.architect/` is gitignored.
3. Freeze gates in `docs/gates/<slice>.md`.
4. Confirm lane file ownership is disjoint.
5. Write one builder block per lane into `.architect/<slice>-<lane>.md`.

Dispatch shape:

Single lane:

```bash
codex exec -C <repo-root> --sandbox workspace-write \
  -m gpt-5.5 -c model_reasoning_effort="xhigh" \
  --json -o .architect/<slice>-last-run.jsonl \
  - < .architect/<slice>-lane-1.md
```

Parallel lanes:

```bash
git -C <repo-root> worktree add .architect/wt/<slice>-<lane> \
  -b lane/<slice>-<lane> <freeze-sha>

codex exec -C <repo-root>/.architect/wt/<slice>-<lane> --sandbox workspace-write \
  -m gpt-5.5 -c model_reasoning_effort="xhigh" \
  --json -o .architect/wt/<slice>-<lane>.jsonl \
  - < .architect/wt/<slice>-<lane>.md
```

Builder block requirements:

- PHASE 0 disagreement first, citing real files.
- Do not edit files outside lane boundaries.
- Do not edit `docs/gates/`.
- Write raw results to `docs/lanes/<slice>-<lane>.md`.
- Do not commit.
- Give long commands explicit timeouts.
- End with one status line:
  `STATUS: COMPLETE`, `STATUS: COMPLETE_WITH_CONCERNS`, or `STATUS: BLOCKED`.

Post-flight checks:

1. Read each lane report.
2. Check builder raised PHASE 0 disagreements or explicitly said what it checked.
3. Check `docs/gates/` was not modified.
4. Check each lane touched only declared files.
5. Run gate commands yourself.
6. Merge only passing lanes.
7. Update `docs/HANDOFF.md` with raw facts.

Do not let builders commit or merge. Integration belongs to Fable + human.
