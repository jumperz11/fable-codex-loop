# Example Run - "Add a /health endpoint"

A complete, real-shaped trace of one loop on a tiny API project. Read it in
order to see Fable judge, Sol and Luna work, the repo store proof, and the human
choose whether to continue.

| Step | File | What it shows |
| --- | --- | --- |
| 0 | [`before.md`](before.md) | Repo state before the slice |
| 1 | [`architect-spec.md`](architect-spec.md) | Fable checkpoint + worker blocks |
| 2 | [`builder-output.md`](builder-output.md) | Sol implementation and Luna review evidence |
| 3 | [`review-verdict.md`](review-verdict.md) | Fable judging raw evidence |
| - | [`repo/docs/`](repo/docs) | The filled repo memory after the slice (passes `doctor`) |

Validate the example's memory:

```bash
python3 scripts/doctor.py examples/demo-run/repo
```

Verify the frozen gate locks:

```bash
python3 bin/judgeloop verify examples/demo-run/repo
```

Run the demo project's tests:

```bash
cd examples/demo-run/repo
npm test
```
