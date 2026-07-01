# NEXT SLICE

> One small PR-sized mission. If it cannot be reviewed in one sitting, it is too big.

## Slice

| Field | Value |
| --- | --- |
| Slice ID | `S-002` |
| Title | Assert `/health` content type |
| Objective | Add a test that confirms `/health` responds with `application/json`. |
| Builder | `GPT-5.5 Codex` |
| Architect checkpoint | `Fable` |
| Human judge | `human` |

## Acceptance criteria

| ID | Criteria | Evidence required |
| --- | --- | --- |
| `AC-001` | `/health` test asserts JSON content type. | `node --test`, exit 0 |
| `AC-002` | No production behavior changes beyond tests unless test exposes a real defect. | `git diff` |

## Explicit out-of-scope

- New endpoints.
- Monitoring integration.
- Dependency changes.

## Required reality checks before coding

| Check | Why | Evidence |
| --- | --- | --- |
| Confirm Node HTTP header casing behavior. | Avoid brittle test. | Existing test helper or Node response headers. |

## Suggested lanes

| Lane | Responsibility | Allowed files | Must not touch |
| --- | --- | --- | --- |
| `lane-1` | Add content-type assertion. | `test/server.test.js`; `src/server.js` only if test fails | package files |
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
