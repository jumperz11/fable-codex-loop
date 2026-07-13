# Lane Reports

Each worker lane writes one raw report here:

```txt
docs/lanes/S-001-sol.md
```

Reports are evidence, not verdicts. They should contain:

- files touched
- commands run
- exit codes
- raw output
- open disagreements
- blockers
- final lane status

Every report names one fixed worker (`Sol`, `Terra`, or `Luna`) and records the
engine powering that worker. Workers report evidence. Fable alone gives
protocol verdicts. The human decides whether to ship or stop.

See [`SCHEMA.md`](SCHEMA.md) for the minimal required status format.
