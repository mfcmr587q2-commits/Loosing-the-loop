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

    def test_high_confidence_external_action_proceeds_in_minimal_prototype(self):
        s = LosingTheLoop()
        result = s.assess([Evidence("safe", "trusted", 0.99)], "external_action")
        self.assertEqual(result, Decision.PROCEED)
        # The minimal prototype treats authenticated high-confidence evidence as sufficient.
        # The grounded kernel separately requires independent validation and authorization.

    def test_self_authorization_fails(self):
        s = LosingTheLoop()
        self.assertFalse(s.authorize("self_modify", independent_reviewer=False))


if __name__ == "__main__":
    unittest.main()
