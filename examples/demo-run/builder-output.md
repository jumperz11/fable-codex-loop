# Step 2 - Sol and Luna Worker Evidence

Sol and Luna are workers. GPT-5.5 Codex powers both in this example.

## PHASE 0 - Disagree first

- Plan: add a route check for `/health` in the existing request handler.
- Files checked: `src/server.js`, `test/server.test.js`, `package.json`.
- Reality checks:
  - `process.uptime()` returns seconds as a float (Node docs). Will `Math.floor`.
  - `package.json` confirms `"test": "node --test"`.
- Disagreement: spec says "uptime" - flooring to integer seconds per frozen contract. No objection.

## PHASE 1 - Verify Fable's freeze

- `judgeloop verify .`: every gate lock verified, exit 0.
- Sol did not edit contracts, gates, or `.sha256` locks.

## PHASE 2 - Sol implementation

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

## PHASE 3 - Luna reviewer evidence

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

Sol updated the lane report and HANDOFF with raw results only. Neither worker
issued a protocol verdict.
