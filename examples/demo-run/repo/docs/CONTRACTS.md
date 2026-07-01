# CONTRACTS

> Frozen APIs, schemas, interfaces, file formats, commands, and ownership rules.

## Freeze status

| Field | Value |
| --- | --- |
| Current slice | `S-001` |
| Freeze timestamp | `2026-06-22 12:20 Africa/Tunis` |
| Frozen by | `Fable + Builder` |
| Can change this slice? | `No, unless human explicitly approves` |

## Public interfaces

| Name | Type | Location | Contract |
| --- | --- | --- | --- |
| `GET /` | HTTP route | `src/server.js` | Returns `200 text/plain` with body `ok`. |
| `GET /health` | HTTP route | `src/server.js` | Returns `200 application/json` with body `{"status":"ok","uptime_s":<integer seconds>}`. |

## Data schemas

| Schema | Location | Required fields | Notes |
| --- | --- | --- | --- |
| `HealthResponse` | `GET /health` | `status: "ok"`, `uptime_s: integer` | `uptime_s` is `Math.floor(process.uptime())`. |

## Commands

| Command | Purpose | Expected result |
| --- | --- | --- |
| `node --test` | Run unit tests. | Exit 0. |

## File ownership rules

| Area | Owner lane | Allowed files | Forbidden files |
| --- | --- | --- | --- |
| HTTP route | `lane-1` | `src/server.js`, `test/server.test.js` | package manager files |

## Out-of-scope for current slice

- Auth.
- Metrics libraries.
- Deployment.
- Changing `/`.

## Contract change log

| Date | Change | Approved by | Reason |
| --- | --- | --- | --- |
| `2026-06-22` | Added `GET /health` contract. | `Fable` | Required by slice S-001. |
