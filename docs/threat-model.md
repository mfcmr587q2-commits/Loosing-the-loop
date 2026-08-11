# Threat Model

## Assets

- Protected invariants
- Authorization credentials and policies
- Witness/provenance records
- Model and policy state
- Human control over consequential actions
- Recovery pathways

## Threats

### T1 — Self-validation loop
The system modifies the rule used to validate its own modification.

**Control:** separate adaptive reasoning from protected authorization.

### T2 — Provenance corruption
Evidence or decision history is altered so a false conclusion appears supported.

**Control:** provenance metadata, append-oriented witness records, integrity checks, and independent verification.

### T3 — Reward/objective drift
An optimization process gradually prioritizes a proxy over the protected objective.

**Control:** invariant checks, independent policy evaluation, drift monitoring, and authorization gates.

### T4 — Recovery hijacking
A detected failure is used to justify an unsafe automatic recovery algorithm.

**Control:** BREATH + Hammer + Security Guard; breach detection does not grant change authority.

### T5 — Counterevidence suppression
The system ignores evidence that conflicts with its current hypothesis.

**Control:** explicit counterevidence storage and conflict states.

### T6 — Authorization bypass
A reasoning or learning component reaches execution without passing the protected control boundary.

**Control:** enforce authorization outside the adaptive execution path.

## Failure philosophy

When uncertainty is material and consequences are significant, the system should prefer a bounded, recoverable state over an irreversible action.

## Threat-model limitation

This document is a design baseline. It does not establish that the controls are sufficient. Each control must be tested against concrete implementations and adversarial scenarios.
