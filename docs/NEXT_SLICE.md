# NEXT SLICE

> One small PR-sized mission. If it cannot be reviewed in one sitting, it is too big.

## Slice

| Field | Value |
| --- | --- |
| Slice ID | `S-001` |
| Title | `<short title>` |
| Objective | `<one sentence>` |
| Builder | `<tool/model, e.g. GPT-5.5 Codex / Opus 4.8 / GLM 5.2>` |
| Architect checkpoint | `Fable` |
| Human judge | `<name>` |
| Frozen gate file | `docs/gates/S-001.md` |

## Acceptance criteria

| ID | Criteria | Evidence required |
| --- | --- | --- |
| `AC-001` | `<specific outcome>` | `<test/command/file>` |

## Gate file

Before coding starts, copy the acceptance criteria and verification commands to
`docs/gates/<slice>.md`. After freeze, that file is read-only unless the human
explicitly approves a change.

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
| `lane-1` | `<task>` | `<paths>` | `<paths>` |
| `lane-2` | `<task>` | `<paths>` | `<paths>` |
| `reviewer` | `Review only, no feature code` | `docs/HANDOFF.md only if reporting` | `feature files` |

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

Nothing merges without reviewer approval.
