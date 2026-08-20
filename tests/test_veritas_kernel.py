import tempfile
import unittest
from pathlib import Path

from src.losing_loop.veritas_kernel import (
    EvidenceChain,
    EyeLedger,
    GuardianDecision,
    KernelOutcome,
    VeritasGovernanceKernel,
)


class AllowGuardian:
    def authorize(self, action, evidence):
        return GuardianDecision(True, "independent-test-guardian", "approved")


class VeritasKernelTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.ledger = EyeLedger(Path(self.tmp.name) / "eye.jsonl")
        self.kernel = VeritasGovernanceKernel(self.ledger, guardian=AllowGuardian())
        self.good = EvidenceChain("source", "claim", "test", "outcome", authenticated=True, independently_validated=True)

    def tearDown(self):
        self.tmp.cleanup()

    def test_unknown_action_type_fails_closed(self):
        out = self.kernel.run_action({"type": "teleport", "affects_human": False}, lambda: "bad", evidence=self.good)
        self.assertFalse(out.allowed)
        self.assertIn("BREATH", out.reason)

    def test_missing_human_impact_declaration_blocks_execute(self):
        out = self.kernel.run_action({"type": "execute"}, lambda: "bad", evidence=self.good)
        self.assertFalse(out.allowed)
        self.assertIn("human-impact", out.reason)

    def test_incomplete_evidence_does_not_authorize_execution(self):
        weak = EvidenceChain("source", "claim", "test", "outcome")
        out = self.kernel.run_action({"type": "execute", "affects_human": False}, lambda: "bad", evidence=weak)
        self.assertFalse(out.allowed)
        self.assertIn("independently validated", out.reason)

    def test_irreversible_remains_forbidden(self):
        out = self.kernel.run_action({"type": "delete", "affects_human": False}, lambda: "bad", evidence=self.good)
        self.assertFalse(out.allowed)

    def test_safe_execution_with_independent_guardian(self):
        out = self.kernel.run_action({"type": "execute", "affects_human": False}, lambda: "ok", evidence=self.good)
        self.assertTrue(out.allowed)
        self.assertEqual(out.result, "ok")
        self.assertTrue(self.ledger.verify_chain())

    def test_ledger_detects_tampering_when_head_anchored(self):
        self.kernel.run_action({"type": "observe"}, lambda: "ok")
        head = self.ledger.head_hash()
        self.assertTrue(self.ledger.verify_chain(expected_head=head))
        text = self.ledger.path.read_text(encoding="utf-8")
        self.ledger.path.write_text(text.replace('"ok"', '"tampered"', 1), encoding="utf-8")
        self.assertFalse(self.ledger.verify_chain(expected_head=head))

    def test_canon_promotion_requires_independent_validation(self):
        denied = self.kernel.promote_to_canon("abc", verifier="reviewer", evidence_complete=True, independent_validation=False)
        self.assertFalse(denied.allowed)
        allowed = self.kernel.promote_to_canon("abc", verifier="reviewer", evidence_complete=True, independent_validation=True)
        self.assertTrue(allowed.allowed)

    def test_human_override_is_logged_but_cannot_override_irreversible_default(self):
        out = self.kernel.human_override({"type": "delete", "affects_human": False}, human_id="human-1", reason="recovery")
        self.assertFalse(out.allowed)
        self.assertTrue(self.ledger.verify_chain())


if __name__ == "__main__":
    unittest.main()
