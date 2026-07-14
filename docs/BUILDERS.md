# Worker Engines

JudgeLoop fixes the roles and allows the engines to vary.

- Fable is always the architect and sole judge.
- Sol, Terra, and Luna are always workers.
- The human owns the ship or stop decision.

JudgeLoop requires no default worker engine. Choose a model or tool for the
task, record it in the lane report, and keep the authority boundary unchanged.

## Worker Requirements

Every worker must:

1. identify itself as Sol, Terra, or Luna
2. record the engine powering it
3. disagree before implementation
4. cite real repo files for assumptions and objections
5. touch only declared files
6. avoid editing frozen gates or `.sha256` locks
7. run verification commands
8. write raw evidence to `docs/HANDOFF.md`
9. write lane reports to `docs/lanes/<slice>-<worker>.md`
10. never issue `PASS`, `FAIL`, or `PARTIAL` as a protocol verdict

A worker may return `APPROVE` or `DEFECTS` when assigned review work. Those are
review findings for Fable, not JudgeLoop verdicts.

## Engine Choices

| Worker engine or tool | Good for | Notes |
| --- | --- | --- |
| Codex CLI | terminal work, tests, long implementation loops | Record the active model in the lane. |
| Claude | careful code reasoning and review-heavy work | Still runs as Sol, Terra, or Luna. |
| GLM | cheaper implementation passes or broad code edits | Keep file boundaries explicit. |
| Kimi | large-repo reading and mechanical changes | Keep gates external and locked. |
| DeepSeek | batch implementation and transformations | Require raw evidence. |
| Qwen | broad edits and multilingual codebases | Require exact file ownership. |
| Another LLM or tool | whatever it is good or cheap at | It remains a worker engine. |

## Adapter Template

Paste this after Fable writes and freezes the slice:

```txt
You are [Sol / Terra / Luna], a WORKER for this slice.
Engine: [model/tool].

Architect and sole judge: Fable.
Human role: owner and shipper.
Repo docs are memory.

You do not grade your own work and do not issue protocol verdicts.

Before coding:
1. read the listed repo files
2. state your plan, disagreements, and ambiguities
3. cite real files
4. verify APIs, commands, schemas, and formats against reality
5. run `judgeloop verify .`

During coding:
1. touch only declared files
2. do not edit `docs/gates/` or gate locks
3. do not add hidden scope
4. run the agreed commands

After coding:
1. update `docs/HANDOFF.md` with raw facts only
2. write `docs/lanes/<slice>-<worker>.md`
3. include Worker, Engine, commands, exit codes, changed files, and blockers
4. end with STATUS: COMPLETE, COMPLETE_WITH_CONCERNS, or BLOCKED
5. do not write VERDICT: PASS, FAIL, or PARTIAL
```

## Headless Mode

Use `prompts/04-headless-dispatch.md` only when a worker engine is Codex CLI.
Every headless process must still be assigned the identity Sol, Terra, or Luna.

The normal manual loop remains:

```txt
Fable checkpoint -> frozen gate lock -> workers -> Fable verdict -> human ship/stop
```
