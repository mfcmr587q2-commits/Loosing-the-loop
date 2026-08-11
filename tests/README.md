# Tests

This directory is reserved for executable experiments.

Initial scenarios:

- `invariant_violation`
- `conflicting_evidence`
- `provenance_tampering`
- `self_modification_attempt`
- `recovery_hijack`
- `objective_drift`
- `authorization_bypass`

Each test should specify:

1. initial state;
2. injected condition;
3. expected control transition;
4. expected blocked/allowed action;
5. evidence produced;
6. pass/fail criteria.

No test should be described as proof of AGI safety. Tests demonstrate behavior of the implementation under defined conditions.
