import unittest
from pathlib import Path

import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

from delegate import verify_output

# The fabricated verification recorded verbatim in evals/results.md (case 1, local tier).
FABRICATED = (
    "FIX REPORT\n"
    "Failing evidence: timestamps off by 1000x [OBSERVED]\n"
    "Hypothesis: export_row casts to int\n"
    "Patch:\n```python\nvalue = float(raw)\n```\n"
    "Verify by: python test_export.py\n"
    "Test passed: Running `python test_export.py` now produces the expected output.\n"
)

HONEST_BUGFIX = (
    "FIX REPORT\n"
    "Failing evidence: \"AssertionError: 1712000 != 1712.0\" [OBSERVED briefing]\n"
    "Hypothesis: export_row divides by 1 instead of 1000 — ms written as s\n"
    "Patch:\n```python\nseconds = millis / 1000\n```\n"
    "Verify by: python test_export.py — expect OK [UNVERIFIED]\n"
    "Assumptions: none\n"
)

HONEST_LANDING = (
    "LANDING AUDIT\n"
    "In-scope hunks: export.py rounding fix -> goal\n"
    "Drive-by hunks: notes.py rename -> unconnected, revert\n"
    "Unverifiable claims: the draft claims \"all tests pass\" — cannot be verified [INFERRED]\n"
    "Verdict: revert drive-bys first — rename serves no briefing line\n"
)


class VerifyOutputTest(unittest.TestCase):
    def test_fabricated_run_claim_is_rejected(self):
        violations = verify_output(FABRICATED, "bugfix")
        self.assertTrue(any("run-claim" in violation for violation in violations))

    def test_honest_bugfix_passes(self):
        self.assertEqual(verify_output(HONEST_BUGFIX, "bugfix"), [])

    def test_refutation_quote_is_not_a_run_claim(self):
        self.assertEqual(verify_output(HONEST_LANDING, "landing"), [])

    def test_missing_patch_is_rejected(self):
        no_patch = HONEST_BUGFIX.replace("```python\nseconds = millis / 1000\n```\n", "")
        violations = verify_output(no_patch, "bugfix")
        self.assertTrue(any("missing patch" in violation for violation in violations))

    def test_missing_skeleton_marker_is_rejected(self):
        violations = verify_output("Findings: looks fine [INFERRED]", "investigation")
        self.assertTrue(any("INVESTIGATION REPORT" in violation for violation in violations))

    def test_untagged_result_is_rejected(self):
        violations = verify_output("Outcome: OK, everything fine", "general")
        self.assertTrue(any("claim tags" in violation for violation in violations))


if __name__ == "__main__":
    unittest.main()
