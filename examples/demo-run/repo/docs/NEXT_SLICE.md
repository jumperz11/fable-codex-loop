# NEXT SLICE

> One small PR-sized mission. If it cannot be reviewed in one sitting, it is too big.

## Slice

| Field | Value |
| --- | --- |
| Slice ID | `S-003` |
| Title | Document CLI wrapper |
| Objective | Show the `bin/judgeloop` wrapper in README and validate it against the demo repo. |
| Builder | `GPT-5.5 Codex` |
| Architect checkpoint | `Fable` |
| Human judge | `human` |
| Frozen gate file | `docs/gates/S-003.md` |

## Acceptance criteria

| ID | Criteria | Evidence required |
| --- | --- | --- |
| `AC-001` | README shows `bin/judgeloop init`, `doctor`, and `validate`. | README inspection |
| `AC-002` | `python3 bin/judgeloop doctor examples/demo-run/repo` exits 0. | command output |
| `AC-003` | `make validate` exits 0. | command output |

## Gate file

The frozen gate file for this slice is `docs/gates/S-003.md`.

## Explicit out-of-scope

- Package publishing.
- Shell completion.
- `freeze` and `verify` commands.

## Required reality checks before coding

| Check | Why | Evidence |
| --- | --- | --- |
| Confirm wrapper can run from repo root. | Avoid documenting a command that fails. | `python3 bin/judgeloop doctor examples/demo-run/repo` |

## Suggested lanes

| Lane | Responsibility | Allowed files | Must not touch |
| --- | --- | --- | --- |
| `lane-1` | Document and validate CLI wrapper. | `README.md`, `Makefile`, `bin/judgeloop`, `docs/*` | demo source files |
| `reviewer` | Review only, no feature code. | `docs/HANDOFF.md` only if reporting | feature files |

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
