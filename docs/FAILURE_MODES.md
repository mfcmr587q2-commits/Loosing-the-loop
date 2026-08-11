# Failure Modes

The prototype treats these as explicit test targets:

1. Self-confirmation: model creates and approves its own claim.
2. Provenance collapse: a claim contains facts without a traceable evidence path.
3. Counterevidence suppression: contradictory evidence is ignored.
4. Unauthorized self-modification: a model attempts to authorize its own modification.
5. Memory rewriting: prior evidence is changed without provenance invalidation.
6. Validation bypass: a supported hypothesis is treated as validated without an external check.
7. Validation non-convergence: repeated validation attempts never establish a result.
8. Context drift: the meaning of a protected fact changes during reasoning.

Expected controls are BREATH or BLOCK depending on whether the failure is recoverable or violates a protected invariant.
