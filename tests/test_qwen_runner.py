import io
import unittest
from contextlib import redirect_stderr, redirect_stdout
from unittest.mock import Mock, patch

from benchmarks import run_large_qwen
from src.losing_loop.llm_reasoner import validate_proposal


VALID_PROPOSAL = {
    "hypothesis": "safe",
    "facts_used": ["e1"],
    "assumptions": [],
    "uncertainties": [],
    "counterevidence_needed": [],
    "validation_plan": ["independent check"],
    "proposed_action": "continue",
}


class QwenRunnerTests(unittest.TestCase):
    def test_selected_scenarios_reject_unknown_name(self):
        with self.assertRaisesRegex(SystemExit, "Unknown scenario"):
            run_large_qwen.selected_scenarios(["not-a-scenario"])

    def test_selected_scenarios_preserve_canonical_order(self):
        scenarios = run_large_qwen.selected_scenarios(["self_authorization", "clean_claim"])
        self.assertEqual([scenario["name"] for scenario in scenarios], ["clean_claim", "self_authorization"])

    def test_runner_reports_reasoner_failure(self):
        reasoner = Mock(
            model="qwen3:4b",
            base_url="http://localhost:11434/v1",
            timeout_seconds=900,
        )
        reasoner.reason.side_effect = RuntimeError("model failure")
        with patch.object(run_large_qwen, "LocalLLMReasoner", return_value=reasoner):
            with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
                self.assertEqual(run_large_qwen.main(["clean_claim"]), 1)

    def test_proposal_schema_accepts_complete_output(self):
        self.assertIs(validate_proposal(VALID_PROPOSAL), VALID_PROPOSAL)

    def test_proposal_schema_rejects_missing_fields(self):
        with self.assertRaisesRegex(ValueError, "missing required field"):
            validate_proposal({"hypothesis": "safe"})

    def test_proposal_schema_rejects_wrong_field_types(self):
        invalid = {**VALID_PROPOSAL, "uncertainties": "none"}
        with self.assertRaisesRegex(ValueError, "invalid field type"):
            validate_proposal(invalid)

    def test_proposal_schema_rejects_non_string_list_items(self):
        invalid = {**VALID_PROPOSAL, "facts_used": [{"id": "e1"}]}
        with self.assertRaisesRegex(ValueError, "invalid field type"):
            validate_proposal(invalid)


if __name__ == "__main__":
    unittest.main()
