import unittest

from benchmarks.benchmark import SYSTEMS, SCENARIOS, evaluate


class BenchmarkTests(unittest.TestCase):
    def test_benchmark_has_four_configurations(self):
        self.assertEqual(set(SYSTEMS), {"A_LLM", "B_GROUNDED", "C_VERITAS_STYLE", "D_LOSING_THE_LOOP"})

    def test_full_system_has_zero_loop_loss_on_synthetic_suite(self):
        metrics = evaluate(SYSTEMS["D_LOSING_THE_LOOP"])
        self.assertEqual(metrics["loop_loss_events"], 0)
        self.assertEqual(metrics["fp"], 0)
        self.assertEqual(metrics["fn"], 0)

    def test_baseline_exposes_loop_loss(self):
        metrics = evaluate(SYSTEMS["A_LLM"])
        self.assertGreater(metrics["loop_loss_events"], 0)

    def test_suite_contains_adversarial_cases(self):
        names = {s.name for s in SCENARIOS}
        for required in {"unsupported_claim", "conflicting_evidence", "validation_mismatch", "unauthorized_action", "self_confirmation"}:
            self.assertIn(required, names)


if __name__ == "__main__":
    unittest.main()
