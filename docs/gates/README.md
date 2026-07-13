# Frozen Gates

Each slice gets one frozen gate file here before implementation starts:

```txt
docs/gates/S-001.md
```

Gate files are read-only after freeze. If a worker edits a gate file after
results exist, the slice fails.

Freeze the current slice before any worker starts:

```bash
judgeloop freeze .
```

This creates `docs/gates/<slice>.sha256`. `judgeloop doctor .` and
`judgeloop verify .` fail if a gate changes or lacks a lock. If requirements
must change, stop the workers, record the reason, let Fable review the new gate,
then run `judgeloop freeze . --force` before work resumes.

Use gate files for exact commands, thresholds, and manual checks that decide
PASS / FAIL / INVALID.
