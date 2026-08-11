# The Hammer

The Hammer is the pre-execution anomaly detector and circuit breaker.

It asks whether a proposed transition is consistent with:

- protected invariants;
- expected system state;
- provenance requirements;
- authorization policy;
- safety constraints.

A Hammer event should create an auditable record and can force the system into BREATH. It should not itself become the authority to rewrite the protected policy it enforces.
