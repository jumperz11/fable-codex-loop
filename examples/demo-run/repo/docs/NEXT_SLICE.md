# NEXT SLICE

> One PR-sized mission frozen by Fable.

| Field | Value |
| --- | --- |
| Slice ID | S-003 |
| Title | Reject POST health |
| Objective | Ensure POST /health cannot be mistaken for the GET health endpoint. |
| Workers | Sol, Luna |
| Worker engine | GPT-5.5 Codex |
| Judge | Fable |
| Human owner | human |
| Frozen gate file | docs/gates/S-003.md |
| Gate lock | docs/gates/S-003.sha256 |

## Acceptance criteria

| ID | Criteria | Evidence required |
| --- | --- | --- |
| AC-001 | POST /health does not return the GET health JSON. | npm test exits 0 |
| AC-002 | Existing GET / and GET /health tests remain green. | npm test exits 0 |

## Out of scope

- Authentication.
- Monitoring integration.
- Dependency changes.

## Worker assignments

| Worker | Responsibility | Allowed files | Must not touch |
| --- | --- | --- | --- |
| Sol | Implement and test the method behavior. | src/server.js, test/server.test.js, docs/lanes/S-003-sol.md | docs/gates/ |
| Luna | Review only and report APPROVE or DEFECTS. | docs/lanes/S-003-luna-review.md | feature files, docs/gates/ |
