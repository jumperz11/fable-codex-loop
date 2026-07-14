from __future__ import annotations

import sys
import tempfile
import textwrap
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))

import doctor  # noqa: E402
from gates import freeze_gate, verify_all  # noqa: E402


class JudgeLoopInvariantTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        for rel in ("docs/gates", "docs/lanes", "docs/verdicts"):
            (self.root / rel).mkdir(parents=True, exist_ok=True)
        self.write(".gitignore", ".architect/\n")

    def tearDown(self) -> None:
        self.temp.cleanup()

    def write(self, rel: str, text: str) -> None:
        path = self.root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(textwrap.dedent(text).strip() + "\n", encoding="utf-8")

    def ready_in_progress(self) -> None:
        self.write(
            "docs/HANDOFF.md",
            """
            # HANDOFF

            | Field | Value |
            | --- | --- |
            | Current slice | S-001 / add sum |
            | Frozen gate file | docs/gates/S-001.md |
            | Lane reports | docs/lanes/S-001-*.md |
            | Last updated | 2026-07-13 15:20 Africa/Tunis |
            | Judge | Fable |
            | Workers | Sol |

            | Item | Value |
            | --- | --- |
            | Slice attempted | NONE |
            | Final status | UNKNOWN |
            """,
        )
        self.write(
            "docs/CONTRACTS.md",
            """
            # CONTRACTS

            | Field | Value |
            | --- | --- |
            | Current slice | S-001 |
            | Freeze timestamp | 2026-07-13 15:20 Africa/Tunis |
            | Frozen by | Fable |
            | Can change this slice? | No |
            """,
        )
        self.write("docs/DECISIONS.md", "# DECISIONS\n\nADR-001: Fable judges; Sol works.")
        self.write(
            "docs/EVALS.md",
            """
            # EVALS

            | Field | Value |
            | --- | --- |
            | Current slice | S-001 |

            | Gate ID | Requirement | Verification | Pass condition | Status |
            | --- | --- | --- | --- | --- |
            | G-001 | sum returns 5 | npm test | exit 0 | pending |
            """,
        )
        self.write(
            "docs/NEXT_SLICE.md",
            """
            # NEXT SLICE

            | Field | Value |
            | --- | --- |
            | Slice ID | S-001 |
            | Title | Add sum |
            | Objective | Export a sum function |
            | Workers | Sol |
            | Worker engine | Example Engine |
            | Judge | Fable |
            | Human owner | Jamel |
            | Frozen gate file | docs/gates/S-001.md |

            | ID | Criteria | Evidence required |
            | --- | --- | --- |
            | AC-001 | sum returns 5 | npm test exits 0 |
            """,
        )
        self.write(
            "docs/gates/S-001.md",
            """
            # S-001 Gates

            | Gate ID | Requirement | Command | Pass condition |
            | --- | --- | --- | --- |
            | G-001 | sum returns 5 | npm test | exit 0 |
            """,
        )
        success, message = freeze_gate(self.root, "S-001")
        self.assertTrue(success, message)

    def completed_slice(self) -> None:
        self.ready_in_progress()
        self.write(
            "docs/lanes/S-001-sol.md",
            """
            # Sol Worker Report

            | Field | Value |
            | --- | --- |
            | Worker | Sol |
            | Engine | Example Engine |

            Command result: PASS, exit 0.

            STATUS: COMPLETE
            """,
        )
        self.write(
            "docs/verdicts/S-001.md",
            """
            # Fable Verdict

            | Field | Value |
            | --- | --- |
            | Slice | S-001 |
            | Judge | Fable |
            | Verdict | PASS |
            """,
        )
        self.write(
            "docs/HANDOFF.md",
            """
            # HANDOFF

            | Field | Value |
            | --- | --- |
            | Current slice | S-002 / validate input |
            | Frozen gate file | docs/gates/S-002.md |
            | Lane reports | docs/lanes/S-002-*.md |
            | Last updated | 2026-07-13 15:30 Africa/Tunis |
            | Judge | Fable |
            | Workers | Terra |

            | Item | Value |
            | --- | --- |
            | Slice attempted | S-001 |
            | Fable verdict | docs/verdicts/S-001.md |
            | Final status | PASS |
            """,
        )
        self.write(
            "docs/CONTRACTS.md",
            """
            # CONTRACTS

            | Field | Value |
            | --- | --- |
            | Current slice | S-002 |
            | Freeze timestamp | 2026-07-13 15:30 Africa/Tunis |
            | Frozen by | Fable |
            | Can change this slice? | No |
            """,
        )
        self.write(
            "docs/EVALS.md",
            """
            # EVALS

            | Field | Value |
            | --- | --- |
            | Current slice | S-002 |

            | Gate ID | Requirement | Verification | Pass condition | Status |
            | --- | --- | --- | --- | --- |
            | G-002 | reject strings | npm test | exit 0 | pending |
            """,
        )
        self.write(
            "docs/NEXT_SLICE.md",
            """
            # NEXT SLICE

            | Field | Value |
            | --- | --- |
            | Slice ID | S-002 |
            | Title | Validate input |
            | Objective | Reject string input |
            | Workers | Terra |
            | Worker engine | Example Engine |
            | Judge | Fable |
            | Human owner | Jamel |
            | Frozen gate file | docs/gates/S-002.md |

            | ID | Criteria | Evidence required |
            | --- | --- | --- |
            | AC-002 | strings throw TypeError | npm test exits 0 |
            """,
        )
        self.write(
            "docs/gates/S-002.md",
            """
            # S-002 Gates

            | Gate ID | Requirement | Command | Pass condition |
            | --- | --- | --- | --- |
            | G-002 | reject strings | npm test | exit 0 |
            """,
        )
        success, message = freeze_gate(self.root, "S-002")
        self.assertTrue(success, message)

    def problems(self) -> list[str]:
        return doctor.check(self.root, color=False)[1]

    def test_ready_in_progress_slice_passes(self) -> None:
        self.ready_in_progress()
        self.assertEqual(self.problems(), [])

    def test_verify_requires_at_least_one_gate(self) -> None:
        _, problems = verify_all(self.root)
        self.assertEqual(problems, ["no frozen slice gates found in docs/gates/"])

    def test_completed_slice_with_fable_verdict_passes(self) -> None:
        self.completed_slice()
        self.assertEqual(self.problems(), [])

    def test_worker_verdict_is_rejected(self) -> None:
        self.completed_slice()
        path = self.root / "docs/lanes/S-001-sol.md"
        path.write_text(path.read_text(encoding="utf-8") + "VERDICT: PASS\n", encoding="utf-8")
        self.assertTrue(any("illegally issues worker verdict PASS" in item for item in self.problems()))

    def test_modified_frozen_gate_is_rejected(self) -> None:
        self.ready_in_progress()
        path = self.root / "docs/gates/S-001.md"
        path.write_text(path.read_text(encoding="utf-8") + "changed after freeze\n", encoding="utf-8")
        self.assertTrue(any("frozen gate changed" in item for item in self.problems()))

    def test_slice_mismatch_is_rejected(self) -> None:
        self.ready_in_progress()
        path = self.root / "docs/CONTRACTS.md"
        path.write_text(path.read_text(encoding="utf-8").replace("S-001", "S-009"), encoding="utf-8")
        self.assertTrue(any("Current slice must match" in item for item in self.problems()))

    def test_unknown_worker_is_rejected(self) -> None:
        self.ready_in_progress()
        path = self.root / "docs/NEXT_SLICE.md"
        path.write_text(path.read_text(encoding="utf-8").replace("| Workers | Sol |", "| Workers | Atlas |"), encoding="utf-8")
        self.assertTrue(any("Workers must be a unique subset" in item for item in self.problems()))

    def test_completed_slice_requires_fable_verdict(self) -> None:
        self.completed_slice()
        (self.root / "docs/verdicts/S-001.md").unlink()
        self.assertTrue(any("missing Fable verdict" in item for item in self.problems()))

    def test_changed_lock_requires_explicit_force(self) -> None:
        self.ready_in_progress()
        path = self.root / "docs/gates/S-001.md"
        path.write_text(path.read_text(encoding="utf-8") + "approved revision\n", encoding="utf-8")
        success, message = freeze_gate(self.root, "S-001")
        self.assertFalse(success)
        self.assertIn("refusing to replace changed lock", message)
        success, message = freeze_gate(self.root, "S-001", force=True)
        self.assertTrue(success, message)
        _, problems = verify_all(self.root)
        self.assertEqual(problems, [])


if __name__ == "__main__":
    unittest.main()
