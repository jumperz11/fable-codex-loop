# Step 2 - Codex (Builder)

## PHASE 0 - Disagree first

- Plan: add a route check for `/health` in the existing request handler.
- Files checked: `src/server.js`, `test/server.test.js`, `package.json`.
- Reality checks:
  - `process.uptime()` returns seconds as a float (Node docs). Will `Math.floor`.
  - `package.json` confirms `"test": "node --test"`.
- Disagreement: spec says "uptime" - flooring to integer seconds per frozen contract. No objection.

## PHASE 1 - Freeze contracts

- `docs/CONTRACTS.md`: `GET /health -> 200 JSON {"status":"ok","uptime_s":<int>}`.
- `docs/EVALS.md`: gates G-001..G-003 written. Frozen.

## PHASE 2 - Build (lane-1)

```diff
 const server = http.createServer((req, res) => {
+  if (req.url === "/health") {
+    res.writeHead(200, { "content-type": "application/json" });
+    res.end(JSON.stringify({ status: "ok", uptime_s: Math.floor(process.uptime()) }));
+    return;
+  }
   res.writeHead(200, { "content-type": "text/plain" });
   res.end("ok");
 });
```

## PHASE 3 - Reviewer lane

```txt
APPROVE
```

## PHASE 4 - Verify

```txt
$ node --test
PASS GET / still returns "ok"
PASS GET /health returns 200
PASS /health body has status=ok and integer uptime_s
# tests 3, pass 3, fail 0
exit code: 0
```

## PHASE 5 - Handoff

Updated `docs/HANDOFF.md` with raw results only (see `repo/docs/HANDOFF.md`).
