# Step 0 - Before

Project: `pingbox`, a tiny Node HTTP service. The team wants a health endpoint
for uptime checks before they wire monitoring.

## Repo state before JudgeLoop memory

```txt
pingbox/
|-- src/server.js      # starts an http server on PORT, responds 200 "ok" on /
|-- test/server.test.js
`-- package.json       # scripts: "test": "node --test"
```

## Objective (from the human)

> "Add a /health endpoint that returns JSON status and uptime, with a test."

Nothing is in `docs/` yet. First action: run `judgeloop init .`, let Fable fill
`docs/NEXT_SLICE.md` and its gate, then run `judgeloop freeze .`.
