# Controlled Benchmark

This benchmark compares four deterministic configurations:

- A_LLM: unguarded baseline
- B_GROUNDED: evidence/provenance gating
- C_VERITAS_STYLE: grounding plus independent validation
- D_LOSING_THE_LOOP: grounding, validation, Challenger behavior, BREATH, Hammer, and authorization policy

## Metrics

Accuracy:

`correct / total`

Precision for safe/proceed decisions:

`TP / (TP + FP)`

Recall for safe/proceed decisions:

`TP / (TP + FN)`

Loop-loss rate:

`consequential unsafe decisions / total scenarios`

## Current scope

The suite is synthetic and deterministic. It tests the architecture's decision policy and failure handling. It does **not** establish real-world LLM performance, safety, or generalization.

The next benchmark layer should replace the mock reasoner with a locally hosted LLM and repeat the exact scenarios with fixed prompts, seeds where supported, model identifiers, latency, token counts, and full decision records.

The Veritas paper is used as architectural inspiration for grounding and independent validation; its reported 90% recall is not a result of this repository and must not be conflated with our benchmark.
