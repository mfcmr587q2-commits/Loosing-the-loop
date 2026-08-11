import unittest
from src.losing_loop.models import Claim, Decision, Evidence, EvidenceType, ValidationStatus
from src.losing_loop.core import LosingTheLoop
from src.losing_loop.challenger import Challenger
from src.losing_loop.validator import Validator
from src.losing_loop.witness_memory import WitnessMemory

class GroundedLoopTests(unittest.TestCase):
    def setUp(self):
        self.ev=Evidence(id="e1", claim="safe", source="test", confidence=.99, authenticated=True, type=EvidenceType.OBSERVATION)
        self.claim=Claim(hypothesis="safe", evidence_ids=["e1"], validation=ValidationStatus.VALIDATED)

    def test_counterevidence_triggers_challenge(self):
        bad=Evidence(id="e2", claim="unsafe", source="test", confidence=.99, authenticated=True, type=EvidenceType.COUNTEREVIDENCE)
        self.assertTrue(Challenger().challenge(self.claim,[self.ev,bad]))

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
