# CONTRACTS

> Fable freezes APIs, commands, and ownership before workers start.

## Freeze status

| Field | Value |
| --- | --- |
| Current slice | S-003 |
| Freeze timestamp | 2026-07-13 16:10 Africa/Tunis |
| Frozen by | Fable |
| Can change this slice? | No; Fable must review and re-freeze first |

## Public interfaces

| Name | Type | Location | Contract |
| --- | --- | --- | --- |
| GET / | HTTP route | src/server.js | Returns 200 text/plain with body ok. |
| GET /health | HTTP route | src/server.js | Returns 200 application/json with status ok and integer uptime_s. |

## Commands

| Command | Purpose | Expected result |
| --- | --- | --- |
| npm test | Run route tests. | Exit 0. |

## File ownership rules

| Area | Owner worker | Allowed files | Forbidden files |
| --- | --- | --- | --- |
| Route behavior | Sol | src/server.js, test/server.test.js, docs/lanes/S-003-sol.md | docs/gates/ |
| Review | Luna | docs/lanes/S-003-luna-review.md | feature files, docs/gates/ |

## Out of scope

- Authentication.
- Metrics libraries.
- Deployment.
