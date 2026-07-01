# Fable + Builder Loop

> **Fable decides. A builder builds. The repo remembers. You judge.**

Use Claude Fable 5 as the architect and judge. Use any capable coding agent as
the builder. GPT-5.5 Codex is the default because it is fast, strong in the
terminal, and easy to run on a subscription, but the loop does not depend on one
builder model.

Codex, Opus, GLM, Kimi, local agents, OpenClaw, or another coding lane can fill
the builder role as long as it can edit files, run checks, and write raw
evidence back to the repo.

[![Repo](https://img.shields.io/badge/GitHub-jumperz11%2Ffable--codex--loop-181717?logo=github)](https://github.com/jumperz11/fable-codex-loop)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

```txt
[FABLE] writes the spec and judges evidence
   |
   v
[BUILDER] builds, tests, and records raw results
   |
   v
[REPO DOCS] remember decisions, contracts, gates, and handoffs
   |
   v
[YOU] make the final kill / continue call
```

The point is simple: do not spend frontier-model time on typing. Spend it on
deciding what deserves to be typed.

---

## Why Use This

Fable is strong at judgment, planning, arbitration, and long-horizon review.
The builder should be whatever coding agent is best or cheapest for your current
job.

This loop separates those jobs.

| Bad default | Better loop |
| --- | --- |
| One model plans, codes, and grades itself. | Fable judges. A builder builds. |
| Success criteria move after seeing results. | Gates freeze before coding. |
| Context lives in chat scrollback. | State lives in `docs/`. |
| The builder says "looks good." | The repo stores raw commands and exit codes. |
| Expensive model types for hours. | Expensive model checks high-leverage decisions. |

Use this when a task is big enough to deserve a PR-sized slice, explicit gates,
and a real handoff.

Skip it for tiny edits.

---

## First Run

### 1. Clone

```bash
git clone https://github.com/jumperz11/fable-codex-loop
cd fable-codex-loop
```

### 2. Optional: install the Codex skill

```bash
./install.sh
```

Windows:

```powershell
.\install.ps1
```

### 3. Add loop memory to your project

From inside the project you want to work on:

```bash
python3 /path/to/fable-codex-loop/scripts/init.py .
```

This creates:

```txt
docs/HANDOFF.md
docs/CONTRACTS.md
docs/DECISIONS.md
docs/EVALS.md
docs/NEXT_SLICE.md
docs/gates/
docs/lanes/
docs/prd/
docs/research/
```

### 4. Write one small slice

Edit:

```txt
docs/NEXT_SLICE.md
```

Example:

```txt
Add GET /health returning:
{"status":"ok","uptime_s":<integer>}

Out of scope:
- auth
- metrics
- deployment
```

### 5. Check readiness

```bash
python3 /path/to/fable-codex-loop/scripts/doctor.py .
```

If it says `READY`, start the loop.

---

## The Loop

### Step A: Fable architects

Paste this into Fable:

```txt
prompts/01-fable-architect.md
```

Fable reads the repo docs, freezes the slice, calls out risks, and ends with a
paste-ready builder block.

### Step B: your builder builds

Paste Fable's block into your builder.

The builder must:

- disagree before coding
- cite real repo files
- verify APIs, schemas, commands, and formats
- freeze contracts and gates before implementation
- build the slice
- run tests
- write raw evidence to `docs/HANDOFF.md` and `docs/lanes/`

### Step C: Fable reviews

After the builder finishes, paste this into Fable:

```txt
prompts/03-fable-review.md
```

Give Fable the raw results:

- `docs/HANDOFF.md`
- `docs/gates/<slice>.md`
- `docs/lanes/<slice>-*.md`
- test output
- git diff summary

Fable returns:

```txt
PASS / FAIL / PARTIAL
```

Then Fable writes the next slice.

Repeat.

---

## The Core Files

| File | Purpose |
| --- | --- |
| [`prompts/01-fable-architect.md`](prompts/01-fable-architect.md) | Start a Fable checkpoint. |
| [`prompts/02-builder-contract.md`](prompts/02-builder-contract.md) | Base builder contract. Codex is the default example. |
| [`prompts/03-fable-review.md`](prompts/03-fable-review.md) | Review builder output with Fable. |
| [`prompts/04-headless-dispatch.md`](prompts/04-headless-dispatch.md) | Optional `codex exec` / worktree adapter. |
| [`prompts/05-fable-research.md`](prompts/05-fable-research.md) | Optional research checkpoint. |
| [`docs/BUILDERS.md`](docs/BUILDERS.md) | How to use Codex, Opus, GLM, Kimi, or another builder. |
| [`docs/HANDOFF.md`](docs/HANDOFF.md) | Raw state after every work block. |
| [`docs/CONTRACTS.md`](docs/CONTRACTS.md) | Frozen APIs, schemas, interfaces, commands. |
| [`docs/EVALS.md`](docs/EVALS.md) | Scoreboard for success gates. |
| [`docs/gates/`](docs/gates/) | Per-slice frozen gate files. |
| [`docs/lanes/`](docs/lanes/) | Per-lane builder reports. |

If it is not in repo docs, it did not happen.

---

## Manual vs Headless

Most people should start with **manual mode**.

| Mode | Use when | How |
| --- | --- | --- |
| Manual | You want to watch the run and paste between Fable and your builder. | Fable prompt -> builder run -> Fable review. |
| Headless | The slice is big enough for unattended or parallel lanes. | Fable writes `.architect/` dispatch blocks; `codex exec` runs per lane. |

Manual mode is the product. Headless mode is the Codex adapter.

---

## The Rules

1. Fable is for judgment, not typing.
2. The builder is for building, testing, and evidence.
3. Repo docs are memory.
4. The builder never grades its own work.
5. Disagreement is mandatory.
6. Gates freeze before results exist.
7. Builder edits to frozen gates fail the slice.
8. Parallel lanes need disjoint file ownership.
9. If Fable is down or expensive, the builder continues only from frozen specs and records unresolved decisions for the next Fable checkpoint.

That last rule matters. If the workflow dies when Fable is unavailable, you
built dependency, not leverage.

---

## Validate The Kit

Inside this repo:

```bash
make validate
```

This checks:

- demo repo memory
- Python scripts
- skill metadata
- markdown links
- code fences

---

## What Is Included

```txt
fable-codex-loop/
|-- README.md
|-- Makefile
|-- install.sh
|-- install.ps1
|-- docs/
|-- prompts/
|-- scripts/
|-- skills/fable-codex-loop/
|-- examples/demo-run/
|-- templates/
`-- tests/
```

See the worked example:

```txt
examples/demo-run/
```

See what was borrowed and what stayed intentionally simpler:

```txt
docs/REFERENCE_GAPS.md
```

See how to swap builders:

```txt
docs/BUILDERS.md
```

---

## FAQ

**Do I need API keys?**

No by default. The intended flow uses subscriptions. The headless mode can use
`codex exec` if you have the Codex CLI set up.

**Do I need two different models?**

No. The roles matter more than the names. But a separate architect/judge model
helps because the builder does not get to grade itself.

**Can I use Opus, GLM, Kimi, or another builder instead of Codex?**

Yes. Codex is the default builder path, not a hard dependency. Use any builder
that can follow the builder contract: disagree first, touch only declared files,
run checks, and write raw evidence to `docs/HANDOFF.md` / `docs/lanes/`.

**Why not let Fable code too?**

You can. It is usually a waste. Use Fable where judgment changes the outcome:
scope, architecture, arbitration, evidence review, and next-slice planning.

**What if Fable is limited, down, or expensive?**

The builder continues only from frozen specs. Any strategic decision or unresolved
disagreement gets written to `docs/HANDOFF.md` for the next Fable checkpoint.

**Is this tied to one language or framework?**

No. It is just repo memory, frozen gates, and role separation.

---

## License

MIT. Share it, remix it, ship with it.
