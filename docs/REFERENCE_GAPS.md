# Reference Gaps

Notes from comparing this kit with `DanMcInerney/architect-loop`.

## Added

| Gap | Added here | Why |
| --- | --- | --- |
| Installer | `install.sh`, `install.ps1` | Makes the skill easy to install globally or per project. |
| Installer safety | Existing skill folders are backed up by default; `--force` is explicit. | Avoids silent local skill deletion. |
| Package validation | `tests/validate_repo.py`, `make validate` | Catches broken skill metadata, links, and markdown fences before publishing. |
| Runtime scratch area | `.architect/` in `.gitignore` | Gives headless runs a safe place for dispatch blocks, JSONL logs, and worktrees. |
| Frozen gate files | `docs/gates/` | Makes gate tampering easier to detect than one shared eval file alone. |
| Gate locks | `judgeloop freeze`, `verify`, tracked `.sha256` files | Makes post-freeze gate edits fail deterministically. |
| Fixed role checks | `scripts/doctor.py` | Rejects non-Fable judges, unknown workers, worker verdicts, and slice drift. |
| Fable verdict receipts | `docs/verdicts/` | Proves completed slices were judged by Fable rather than a worker. |
| Lane reports | `docs/lanes/` | Gives every worker lane a raw evidence file. |
| Concrete gate examples | `examples/demo-run/repo/docs/gates/S-001.md`, `S-002.md` | Shows frozen gates as real review artifacts. |
| Concrete lane report | `examples/demo-run/repo/docs/lanes/S-001-sol.md` | Shows raw worker evidence with a final `STATUS`. |
| Runnable demo project | `examples/demo-run/repo/src`, `test`, `package.json` | Lets people run the demo instead of only reading it. |
| Stricter doctor | `scripts/doctor.py` checks roles, slice consistency, gate locks, handoff pointers, lane reports, and Fable verdicts. | Makes drift and authority leaks fail visibly. |
| Tiny CLI wrapper | `bin/judgeloop init`, `freeze`, `verify`, `doctor` | Makes the kit feel like a tool without hiding the simple scripts. |
| Product/research artifacts | `docs/prd/`, `docs/research/` | Keeps research and product decisions out of the handoff file. |
| Headless dispatch guide | `prompts/04-headless-dispatch.md` | Optional path for `codex exec`, worktrees, and unattended lanes. |
| Research checkpoint | `prompts/05-research-checkpoint.md` | Keeps discovery work separate from build work. |

## Intentionally Kept Simpler

| Reference feature | Decision here | Why |
| --- | --- | --- |
| Always Fable-owned worktree fan-out | Optional advanced mode | The main audience should succeed with paste-ready Fable + workers flow first. |
| Long cited design manifesto | Short README + gap notes | This repo is meant to be a usable kit and post companion, not a research paper. |
| Separate installed research skill | One optional research prompt inside the same kit | Avoids making research feel mandatory for every build slice. |
| Hard dependency on headless `codex exec` | Manual `/goal` mode first | Your original idea is subscription-native and easy to run without automation. |

## Still Worth Adding Later

- A stricter optional machine-readable lane report file, such as `lane-report.yaml`.
- A hosted HTML explainer page showing the full process visually.
