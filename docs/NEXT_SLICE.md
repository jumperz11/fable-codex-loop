# NEXT SLICE

> One small PR-sized mission. If it cannot be reviewed in one sitting, it is too big.

## Slice

| Field | Value |
| --- | --- |
| Slice ID | `S-001` |
| Title | `<short title>` |
| Objective | `<one sentence>` |
| Workers | `<workers: Sol, Terra, and/or Luna>` |
| Worker engine | `<engine/model; GPT-5.5 Codex by default>` |
| Judge | `Fable` |
| Human owner | `<human owner>` |
| Frozen gate file | `docs/gates/S-001.md` |
| Gate lock | `docs/gates/S-001.sha256` |

## Acceptance criteria

| ID | Criteria | Evidence required |
| --- | --- | --- |
| `AC-001` | `<specific outcome>` | `<test/command/file>` |

## Gate file

Before coding starts, copy the acceptance criteria and verification commands to
`docs/gates/<slice>.md`, then run `judgeloop freeze .`. The gate and its
`.sha256` lock are read-only for workers. Only Fable may review a revision and
explicitly re-freeze it before workers resume.

## Explicit out-of-scope

- `<non-goal>`
- `<non-goal>`
- `<non-goal>`

## Required reality checks before coding

| Check | Why | Evidence |
| --- | --- | --- |
| `<API/doc/schema check>` | `<why>` | `<file/link/command>` |

## Suggested lanes

| Lane | Responsibility | Allowed files | Must not touch |
| --- | --- | --- | --- |
| `Sol` | `<task or not assigned>` | `<paths>` | `<paths>` |
| `Terra` | `<task or not assigned>` | `<paths>` | `<paths>` |
| `Luna` | `Review or implementation worker` | `<paths>` | `<paths>` |

## Reviewer requirements

Reviewer returns only:

```txt
APPROVE
```

or:

```txt
DEFECTS:
1. <specific defect>
2. <specific defect>
```

`APPROVE` and `DEFECTS` are reviewer evidence, not protocol verdicts. Fable
alone issues `PASS`, `FAIL`, or `PARTIAL`. The human then chooses ship or stop.
