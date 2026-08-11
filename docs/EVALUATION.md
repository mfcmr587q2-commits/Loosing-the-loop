# Evaluation Plan

Metrics:

- Recall = TP / (TP + FN)
- Precision = TP / (TP + FP)
- Evidence coverage = preserved required evidence / available required evidence
- Provenance integrity = verified provenance links / required provenance links
- Validation rate = validated claims / candidate claims
- Loop-loss rate = integrity-failure decisions / consequential decisions

Required ablations:

A. model alone
B. model + evidence retrieval
C. model + provenance
D. model + provenance + challenger
E. model + provenance + validator
F. full Losing-the-Loop system

Every experiment must report configuration, model, data, trial count, failures, latency, and cost where available. No safety guarantee should be inferred from a single benchmark.
