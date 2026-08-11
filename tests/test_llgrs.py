import unittest
from src.losing_loop import Claim, Decision, Evidence, EvidenceType, LosingTheLoop, ValidationStatus
from src.losing_loop import EdgeType, ProvenanceGraph, Witness

class LLGRSTests(unittest.TestCase):
    def setUp(self):
        self.system = LosingTheLoop()
        self.evidence = [Evidence("e1", "safe", "test", "safe", 0.99)]

    def test_no_evidence_breaths(self):
        result = self.system.assess([], Claim("x"), authorized=True)
        self.assertEqual(result.decision, Decision.BREATH)

    def test_conflict_breaths(self):
        evidence = [Evidence("a", "safe", "a", "", .9), Evidence("b", "unsafe", "b", "", .9)]
        claim = Claim("x", validation=ValidationStatus.UNKNOWN)
        self.assertEqual(self.system.assess(evidence, claim, authorized=True).decision, Decision.BREATH)

    def test_unsupported_claim_breaths(self):
        claim = Claim("x", validation=ValidationStatus.SUPPORTED)
        self.assertEqual(self.system.assess(self.evidence, claim, authorized=True).decision, Decision.BREATH)

    def test_unauthorized_self_modification_blocks(self):
        claim = Claim("x", validation=ValidationStatus.VALIDATED)
        self.assertEqual(self.system.assess(self.evidence, claim, "self_modify", False).decision, Decision.BLOCK)

    def test_validated_authorized_action_proceeds(self):
        claim = Claim("safe", evidence_ids=["e1"], validation=ValidationStatus.VALIDATED)
        self.assertEqual(self.system.assess(self.evidence, claim, "safe_action", True).decision, Decision.PROCEED)

    def test_provenance_witness(self):
        graph = ProvenanceGraph()
        graph.add_edge("source", "mid", EdgeType.DERIVED_FROM)
        graph.add_edge("mid", "sink", EdgeType.SUPPORTED_BY)
        witness = Witness("source", "sink", ["source", "mid", "sink"])
        self.assertTrue(witness.verify(graph))

if __name__ == "__main__":
    unittest.main()
