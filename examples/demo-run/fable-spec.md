# Step 1 - Fable (Architect)

## A. STATE FROM MEMORY

- Repo memory was just initialized. Only the objective is known.
- `src/server.js` currently serves `200 "ok"` on `/`. No JSON routes exist.
- Test runner is `node --test`.

## B. DISAGREEMENTS / RISKS

1. "status and uptime" is underspecified. Freezing the response shape now:
   `{ "status": "ok", "uptime_s": <number> }`.
2. Risk: builder may add a logging/metrics framework. Out of scope.
3. Risk: uptime unit ambiguity. Decision: integer seconds since process start.

## C. FROZEN CONTRACTS TO VERIFY

- Confirm `process.uptime()` returns seconds (Node docs) before coding.
- Confirm `node --test` is the project's runner (package.json).

## D. NEXT SLICE SPEC

- Slice `S-001`: add `GET /health` returning the frozen JSON shape + one test.
- Out of scope: auth, metrics libs, changing `/`.

## E. BUILDER LANES

- One lane only (small slice). `lane-1`: edit `src/server.js` + add test.
- No parallel lanes needed; nothing is independent enough to split.

## F. REVIEWER INSTRUCTIONS

- Reviewer confirms: route returns exact shape, status code 200, test passes,
  `/` unchanged. Returns APPROVE or numbered defects.

## G. PASTE-READY BUILDER BLOCK

```txt
/goal: execute slice S-001 - add GET /health.

PHASE 0: disagree first. List plan, ambiguities, files checked, and the two
reality checks (process.uptime units, test runner). No silent scope additions.

PHASE 1: freeze contract in docs/CONTRACTS.md:
  GET /health -> 200 application/json {"status":"ok","uptime_s":<int seconds>}
  Freeze gates in docs/EVALS.md.

PHASE 2: lane-1 only. Edit src/server.js. Do not change "/".

PHASE 3: reviewer lane (no feature code) returns APPROVE or DEFECTS.

PHASE 4: run `node --test`. Capture raw output + exit code.

PHASE 5: update docs/HANDOFF.md with raw facts only.
```
