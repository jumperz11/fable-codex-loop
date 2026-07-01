# Example Run - "Add a /health endpoint"

A complete, real-shaped trace of one loop on a tiny API project. Read it in order
to see how Fable, a builder, the repo, and the human interact on a single slice.

| Step | File | What it shows |
| --- | --- | --- |
| 0 | [`before.md`](before.md) | Repo state before the slice |
| 1 | [`fable-spec.md`](fable-spec.md) | Fable's architect output + builder block |
| 2 | [`builder-output.md`](builder-output.md) | Builder PHASE 0-5 run |
| 3 | [`review-verdict.md`](review-verdict.md) | Fable judging raw evidence |
| - | [`repo/docs/`](repo/docs) | The filled repo memory after the slice (passes `doctor`) |

Validate the example's memory:

```bash
python3 scripts/doctor.py examples/demo-run/repo
```
