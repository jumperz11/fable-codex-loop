# Builder Adapters

Fable is the architect and judge. The builder can be any coding agent that can
operate on the repo and report raw evidence.

Codex is the default builder in this kit because it has a good terminal workflow
and a clean headless path with `codex exec`. It is not required.

## Builder Requirements

A builder must be able to:

1. read repo files
2. disagree before implementation
3. cite real files for assumptions and objections
4. touch only declared files
5. avoid editing frozen gates in `docs/gates/`
6. run verification commands
7. write raw evidence to `docs/HANDOFF.md`
8. write lane reports to `docs/lanes/<slice>-<lane>.md`
9. avoid grading its own work

If a tool cannot write files directly, it can still be a builder by producing a
patch plus raw verification instructions, but a human or coding agent must apply
and verify it.

## Good Builder Choices

| Builder | Good for | Notes |
| --- | --- | --- |
| GPT-5.5 Codex | terminal work, tests, long implementation loops | Default path in this kit. |
| Claude Opus 4.8 | careful code reasoning and review-heavy work | Use the same builder contract. |
| GLM 5.2 | cheaper implementation passes or broad code edits | Good if it follows boundaries well. |
| Kimi / other long-context models | large-repo reading and mechanical changes | Keep gates external and raw. |
| OpenClaw / worker agents | repetitive operational work | Use `agent-runs/` or lane reports for handoffs. |
| Local coding agents | private repos or low-cost loops | Must still write raw evidence. |

## Adapter Template

Paste this after Fable writes the slice:

```txt
You are the BUILDER for this slice.

Architect: Fable.
Judge: Fable + human.
Repo docs are memory.

You do not grade your own work.

Before coding:
1. read the listed repo files
2. state your plan
3. state every disagreement or ambiguity
4. cite real files
5. verify APIs, commands, schemas, and formats against reality

During coding:
1. touch only declared files
2. do not edit `docs/gates/`
3. do not add hidden scope
4. run the agreed commands

After coding:
1. update `docs/HANDOFF.md` with raw facts only
2. write `docs/lanes/<slice>-<lane>.md`
3. include commands, exit codes, changed files, and blockers
4. do not claim PASS; verdicts belong to Fable and the human
```

## When To Use Codex-Specific Headless Mode

Use `prompts/04-headless-dispatch.md` only when the builder is Codex CLI.

For every other builder, use the normal manual loop:

```txt
Fable architect prompt -> builder contract -> Fable review prompt
```

The loop is model-agnostic. The enforcement comes from repo memory, frozen
gates, lane reports, and human judgment.
