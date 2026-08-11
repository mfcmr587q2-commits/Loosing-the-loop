import unittest
from prototype.loop import Decision, Evidence, LosingTheLoop


class LosingTheLoopTests(unittest.TestCase):
    def test_no_evidence_triggers_breath(self):
        system = LosingTheLoop()
        self.assertEqual(system.assess([], "external_action"), Decision.BREATH)

    def test_conflicting_evidence_triggers_breath(self):
        system = LosingTheLoop()
        evidence = [
            Evidence("safe", "source-a", 0.95),
            Evidence("unsafe", "source-b", 0.95),
        ]
        self.assertEqual(system.assess(evidence, "external_action"), Decision.BREATH)

    def test_low_confidence_triggers_breath(self):
        system = LosingTheLoop()
        evidence = [Evidence("safe", "weak-source", 0.40)]
        self.assertEqual(system.assess(evidence, "external_action"), Decision.BREATH)

    def test_unauthorized_self_modification_is_blocked(self):
        system = LosingTheLoop()
        evidence = [Evidence("safe", "trusted-source", 0.99)]
        self.assertEqual(system.assess(evidence, "self_modify"), Decision.BLOCK)

    def test_independent_authorization_allows_self_modification(self):
        system = LosingTheLoop()
        self.assertTrue(system.authorize("self_modify", independent_reviewer=True))
        evidence = [Evidence("safe", "trusted-source", 0.99)]
        self.assertEqual(system.assess(evidence, "self_modify"), Decision.PROCEED)

    def test_self_authorization_is_rejected(self):
        system = LosingTheLoop()
        self.assertFalse(system.authorize("self_modify", independent_reviewer=False))

    def test_blocked_self_modification_does_not_poison_later_actions(self):
        system = LosingTheLoop()
        evidence = [Evidence("safe", "trusted-source", 0.99)]
        self.assertEqual(system.assess(evidence, "self_modify"), Decision.BLOCK)
        self.assertEqual(system.assess(evidence, "external_action"), Decision.PROCEED)


if __name__ == "__main__":
    unittest.main()
