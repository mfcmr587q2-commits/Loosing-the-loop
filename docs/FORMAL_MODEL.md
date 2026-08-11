# Formal Model

The system is inspired by the semantic-grounding formulation in arXiv:2605.15097. The paper defines a propagation graph and step-wise grounded reasoning for vulnerability analysis; this project generalizes those ideas into a safety-oriented research prototype.

## Provenance graph

`G = (V, E, kappa, mu)`

- V: evidence/state nodes
- E: propagation relationships
- kappa: relationship type
- mu: relationship metadata

## Grounded reasoning

`S_n = Phi_theta(S_(n-1), R_n, A_n)`

- S: reasoning state
- R: grounded representation
- A: anchor/provenance metadata

## Claim object

`C = (H, E, P, U, V)`

- H: hypothesis
- E: evidence
- P: provenance
- U: uncertainty
- V: validation status

## Decision policy

BLOCK if a protected invariant is violated.

BREATH if evidence conflicts, provenance is incomplete, uncertainty is unresolved, or validation is unknown.

BLOCK if independent authorization is missing.

PROCEED only when evidence, provenance, validation, safety, and authorization requirements are satisfied.

The thresholds in the implementation are experimental parameters, not established safety constants.
