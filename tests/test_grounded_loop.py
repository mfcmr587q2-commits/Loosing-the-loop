import unittest
from src.losing_loop.models import Claim, Decision, Evidence, EvidenceType, ValidationStatus
from src.losing_loop.core import LosingTheLoop
from src.losing_loop.challenger import Challenger
from src.losing_loop.validator import Validator
from src.losing_loop.witness_memory import WitnessMemory

class GroundedLoopTests(unittest.TestCase):
    def setUp(self):
        self.ev=Evidence(id="e1", claim="safe", content="observed safe", source="test", confidence=.99, authenticated=True, type=EvidenceType.OBSERVATION)
        self.claim=Claim(hypothesis="safe", evidence_ids=["e1"], validation=ValidationStatus.VALIDATED)

    def test_counterevidence_triggers_challenge(self):
        bad=Evidence(id="e2", claim="unsafe", content="observed unsafe", source="test", confidence=.99, authenticated=True, type=EvidenceType.COUNTEREVIDENCE)
        self.assertEqual(Challenger().challenge(self.claim,[self.ev,bad]), ["counterevidence:e2"])

    def test_counterevidence_forces_kernel_to_breath(self):
        bad=Evidence(id="e2", claim="unsafe", content="observed unsafe", source="test", confidence=.99, authenticated=True, type=EvidenceType.COUNTEREVIDENCE)
        result=LosingTheLoop().assess([self.ev,bad],self.claim,action="external",authorized=True)
        self.assertEqual(result.decision,Decision.BREATH)
        self.assertEqual(result.metadata["challenge_findings"], ["counterevidence:e2"])

    def test_missing_cited_evidence_forces_breath(self):
        claim=Claim(hypothesis="safe", evidence_ids=["missing"], validation=ValidationStatus.VALIDATED)
        result=LosingTheLoop().assess([self.ev],claim,action="external",authorized=True)
        self.assertEqual(result.decision,Decision.BREATH)

    def test_mismatched_cited_evidence_forces_breath(self):
        claim=Claim(hypothesis="unsafe", evidence_ids=["e1"], validation=ValidationStatus.VALIDATED)
        result=LosingTheLoop().assess([self.ev],claim,action="external",authorized=True)
        self.assertEqual(result.decision,Decision.BREATH)

    def test_low_confidence_cited_evidence_forces_breath(self):
        weak=Evidence(id="e1", claim="safe", content="weak signal", source="test", confidence=.5)
        result=LosingTheLoop().assess([weak],self.claim,action="external",authorized=True)
        self.assertEqual(result.decision,Decision.BREATH)

    def test_duplicate_evidence_ids_force_breath(self):
        duplicate=Evidence(id="e1", claim="safe", content="duplicate", source="other", confidence=.99)
        result=LosingTheLoop().assess([self.ev,duplicate],self.claim,action="external",authorized=True)
        self.assertEqual(result.decision,Decision.BREATH)
        self.assertEqual(result.metadata["challenge_findings"], ["duplicate evidence id:e1"])

    def test_invalid_confidence_forces_breath(self):
        invalid=Evidence(id="e1", claim="safe", content="invalid", source="test", confidence=1.1)
        result=LosingTheLoop().assess([invalid],self.claim,action="external",authorized=True)
        self.assertEqual(result.decision,Decision.BREATH)

    def test_invalid_uncertainty_threshold_is_rejected(self):
        with self.assertRaises(ValueError):
            LosingTheLoop(uncertainty_threshold=1.1)

    def test_validator_rejects_mismatch(self):
        self.assertEqual(Validator().validate(self.claim,"unsafe"), ValidationStatus.REJECTED)

    def test_validator_accepts_independent_match(self):
        self.assertEqual(Validator().validate(self.claim,"safe"), ValidationStatus.VALIDATED)

    def test_missing_validation_causes_breath(self):
        c=Claim(hypothesis="safe", evidence_ids=["e1"], validation=ValidationStatus.UNKNOWN)
        r=LosingTheLoop().assess([self.ev],c,action="external",authorized=True)
        self.assertEqual(r.decision,Decision.BREATH)

    def test_witness_memory_hashes_record(self):
        c=LosingTheLoop().assess([self.ev],self.claim,action="external",authorized=True)
        w=WitnessMemory().append(c)
        self.assertEqual(len(w.digest),64)

if __name__ == "__main__": unittest.main()
