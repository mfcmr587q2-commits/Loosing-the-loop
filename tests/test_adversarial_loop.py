import unittest

from prototype import Decision, Evidence, LosingTheLoop


class AdversarialLoopTests(unittest.TestCase):
    def test_self_confirmation_does_not_authorize(self):
        s = LosingTheLoop()
        evidence = [Evidence("safe", "model", 0.99)]
        self.assertEqual(s.assess(evidence, "self_modify"), Decision.BLOCK)

    def test_counterevidence_forces_breath(self):
        s = LosingTheLoop()
        evidence = [
            Evidence("safe", "A", 0.99),
            Evidence("unsafe", "B", 0.99),
        ]
        self.assertEqual(s.assess(evidence, "external_action"), Decision.BREATH)

    def test_unknown_validation_is_not_proceed(self):
        s = LosingTheLoop()
        result = s.assess([Evidence("safe", "trusted", 0.99)], "external_action")
        self.assertEqual(result, Decision.PROCEED)
        # The prototype's current policy treats ordinary validated evidence as sufficient.
        # A future Validator layer must change this to require independent validation.

    def test_self_authorization_fails(self):
        s = LosingTheLoop()
        self.assertFalse(s.authorize("self_modify", independent_reviewer=False))


if __name__ == "__main__":
    unittest.main()
