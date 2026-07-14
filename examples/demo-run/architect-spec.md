# Step 1 - Fable Checkpoint

Fable is the sole architect and judge. Sol implements; Luna reviews. Both are
workers powered by Codex CLI in this example.

## A. STATE FROM MEMORY

- Repo memory was just initialized. Only the objective is known.
- `src/server.js` currently serves `200 "ok"` on `/`. No JSON routes exist.
- Test runner is `node --test`.

## B. DISAGREEMENTS / RISKS

1. "status and uptime" is underspecified. Freezing the response shape now:
   `{ "status": "ok", "uptime_s": <number> }`.
2. Risk: a worker may add a logging/metrics framework. Out of scope.
3. Risk: uptime unit ambiguity. Decision: integer seconds since process start.

## C. FROZEN CONTRACTS TO VERIFY

- Confirm `process.uptime()` returns seconds (Node docs) before coding.
- Confirm `node --test` is the project's runner (package.json).

## D. NEXT SLICE SPEC

- Slice `S-001`: add `GET /health` returning the frozen JSON shape + one test.
- Out of scope: auth, metrics libs, changing `/`.

## E. WORKER ASSIGNMENTS

- Sol: edit `src/server.js`, add tests, and report raw evidence.
- Luna: review only and return APPROVE or DEFECTS.

## F. REVIEWER INSTRUCTIONS

- Reviewer confirms: route returns exact shape, status code 200, test passes,
  `/` unchanged. Returns APPROVE or numbered defects.

## G. PASTE-READY SOL BLOCK

```txt
/goal: execute Fable's frozen slice S-001 - add GET /health.

Worker: Sol.
Engine: Codex CLI.
Fable is the sole judge. Do not issue a protocol verdict.

PHASE 0: disagree first. List plan, ambiguities, files checked, and the two
reality checks (process.uptime units, test runner). No silent scope additions.

PHASE 1: run judgeloop verify . and stop if the gate lock fails.

PHASE 2: Sol implementation lane only. Edit src/server.js. Do not change "/".

PHASE 3: Luna reviewer worker (no feature code) returns APPROVE or DEFECTS.

PHASE 4: run `node --test`. Capture raw output + exit code.

PHASE 5: write the Sol lane report and update HANDOFF with raw facts only.
End with STATUS: COMPLETE. Do not write VERDICT: PASS / FAIL / PARTIAL.
```
