# Repo Memory Contract

Initialize the target repo with:

```bash
judgeloop init .
```

Required directories:

```txt
docs/gates/
docs/lanes/
docs/verdicts/
docs/prd/
docs/research/
```

## HANDOFF required fields

```md
| Field | Value |
| --- | --- |
| Current slice | S-001 / title |
| Frozen gate file | docs/gates/S-001.md |
| Lane reports | docs/lanes/S-001-*.md |
| Last updated | timestamp |
| Judge | Fable |
| Workers | Sol, Terra, and/or Luna |
```

For a completed slice, HANDOFF also records `Slice attempted`, `Final status`,
and `Fable verdict` pointing to `docs/verdicts/<slice>.md`.

## CONTRACTS required fields

```md
| Field | Value |
| --- | --- |
| Current slice | S-001 |
| Freeze timestamp | timestamp |
| Frozen by | Fable |
| Can change this slice? | No |
```

## EVALS required fields

EVALS records the same `Current slice` and at least one objective `G-001` row.

## NEXT_SLICE required fields

```md
| Field | Value |
| --- | --- |
| Slice ID | S-001 |
| Workers | Sol, Terra, and/or Luna |
| Worker engine | model-or-tool (required) |
| Judge | Fable |
| Human owner | name |
| Frozen gate file | docs/gates/S-001.md |
```

NEXT_SLICE also needs at least one `AC-001` acceptance row.

## Freeze and verify

After Fable writes `docs/gates/S-001.md`:

```bash
judgeloop freeze .
judgeloop doctor .
```

This creates `docs/gates/S-001.sha256`. Workers run `judgeloop verify .` before
editing and never modify the gate or lock.

## Lane reports

Every lane report records Worker (`Sol`, `Terra`, or `Luna`), Engine, raw
evidence, and one final status: COMPLETE, COMPLETE_WITH_CONCERNS, or BLOCKED.
Worker reports never contain protocol verdicts.

## Fable verdicts

Every completed slice has `docs/verdicts/<slice>.md`:

```md
| Field | Value |
| --- | --- |
| Slice | S-001 |
| Judge | Fable |
| Verdict | PASS / FAIL / PARTIAL |
```
