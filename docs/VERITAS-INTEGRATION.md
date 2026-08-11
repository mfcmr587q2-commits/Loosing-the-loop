# Veritas + Losing-the-Loop Integration

## Purpose

This document maps the Veritas paper (arXiv:2605.15097) to the Losing-the-Loop architecture and identifies what the paper provides, what Losing-the-Loop adds, and what remains to be experimentally validated.

Paper: **Veritas: A Semantically Grounded Agentic Framework for Memory Corruption Vulnerability Detection in Binaries**.

## 1. What we adopt from Veritas

Veritas provides a strong pattern for reliable agentic reasoning:

1. deterministic/static evidence construction;
2. compact witness-backed flows;
3. dual-view grounded representations;
4. step-wise LLM reasoning over grounded evidence;
5. multi-agent/runtime validation;
6. explicit rejection of unsupported hypotheses.

Its reported benchmark result is 90% recall on 20 real-world vulnerability instances. The paper reports exhaustive validation of 623 candidates with no false positives and an additional audit that identified two false positives; the authors also discuss benchmark and coverage limitations.

## 2. What Losing-the-Loop adds

Losing-the-Loop generalizes the grounding principle beyond binary vulnerability detection into a safety/control architecture:

```text
Observation
    -> Evidence
    -> Provenance
    -> Grounded Reasoning
    -> Counterevidence
    -> BREATH
    -> Challenger
    -> Validator
    -> Security Guard
    -> Action
    -> Witness Memory
    -> New Observation
```

The additional controls are:

- **BREATH:** deterministic pause on uncertainty, conflict, incomplete provenance, inconclusive validation, or missing authorization.
- **The Hammer:** protected invariant enforcement that the reasoning model cannot override.
- **Security Guard:** authorization separated from reasoning and validation.
- **Witness Memory:** auditable decision records with provenance and integrity metadata.
- **Counterevidence:** an explicit falsification path rather than a one-directional confirmation loop.

## 3. Gap-coverage matrix

| Reliability problem | Veritas contribution | Losing-the-Loop extension | Status |
|---|---|---|---|
| Too much irrelevant context | Slicer / compact flows | Evidence selector + grounded state | Prototype |
| Unsupported propagation | Witness-backed flows | Provenance graph + witness verification | Prototype |
| Model overconfidence | Grounded reasoning | BREATH + uncertainty threshold | Prototype |
| Confirmation bias | Validator | Independent Challenger + counterevidence | Prototype |
| Claim mistaken for truth | Candidate + runtime validation | Explicit VALIDATED state | Prototype |
| Model self-approval | Multi-agent validation | Security Guard outside reasoner | Prototype |
| Unauthorized self-change | Not the primary scope | Protected invariants + Hammer | Prototype |
| Loss/corruption of memory | Not the primary scope | Witness Memory + integrity digest | Prototype |
| Runtime mismatch | Debugger/runtime validation | General Validator interface | Prototype |
| Infinite investigation | Bounded agentic validation | Iteration limit -> UNKNOWN -> BREATH | Planned/tested |
| Semantic drift | Not a primary target | Context-drift detection | Planned |
| General-purpose safe action | Binary-security-specific | Policy/authorization kernel | Planned |

## 4. Formal bridge

Veritas models a propagation graph using a structure of the form:

\[
G_P=(F,E,\kappa,\mu)
\]

Losing-the-Loop generalizes this into a typed provenance graph:

\[
G=(V,E,\kappa,\mu)
\]

where nodes may represent observations, evidence, claims, validation results, authorization decisions, and actions.

The reasoning transition is represented as:

\[
S_n=\Phi_\theta(S_{n-1},R_n,A_n)
\]

but the resulting state is **not** itself a verdict.

A claim is represented as:

\[
C=(H,E,P,U,V)
\]

where:

- \(H\): hypothesis;
- \(E\): evidence;
- \(P\): provenance;
- \(U\): uncertainty;
- \(V\): validation state.

The policy layer then enforces:

\[
D(a)=
\begin{cases}
BLOCK & \text{protected invariant violation}\\
BREATH & \text{uncertainty/conflict/incomplete provenance}\\
BREATH & \text{validation unknown}\\
BLOCK & \text{authorization missing}\\
PROCEED & \text{evidence + provenance + validation + authorization}
\end{cases}
\]

This policy is an extension proposed by Losing-the-Loop; it is not claimed to be an equation from the Veritas paper.

## 5. What the combined system should prove

The project should not claim that combining the two architectures automatically produces a safe AGI. Instead, it should test measurable hypotheses:

### H1 — Grounding
Grounded reasoning produces fewer unsupported claims than unrestricted reasoning.

### H2 — Provenance
Witness verification reduces provenance-loss failures.

### H3 — Falsification
An independent Challenger detects contradictions that a single reasoner misses.

### H4 — Validation
Runtime/external validation reduces false positives relative to model-only decisions.

### H5 — Control separation
Separating reasoning, validation, and authorization prevents model self-authorization.

### H6 — Recovery
BREATH prevents uncertain or contradictory states from becoming consequential actions.

### H7 — Memory integrity
Witness Memory allows reconstruction of why a decision was made and detects tampering or provenance discontinuity.

## 6. Evaluation plan

Run the following ablations:

```text
A: LLM only
B: LLM + grounding
C: LLM + grounding + provenance
D: LLM + grounding + provenance + Challenger
E: LLM + grounding + provenance + Validator
F: Full Losing-the-Loop
```

Measure:

- precision;
- recall;
- false-positive rate;
- unsupported-claim rate;
- provenance integrity;
- counterevidence detection;
- validation success/failure;
- unauthorized-action blocking;
- loop-loss rate;
- latency;
- token/context cost.

## 7. Important limitation

The Veritas paper is specifically about binary memory-corruption vulnerability detection. Its results should therefore be treated as evidence for **semantic grounding and validation as engineering principles**, not evidence that the generalized Losing-the-Loop architecture is already proven for general AI systems.

The combined project must preserve that distinction.

## 8. Target architecture

```text
                    ┌───────────────────┐
                    │    OBSERVATION     │
                    └─────────┬─────────┘
                              ↓
                    ┌───────────────────┐
                    │  EVIDENCE SLICER  │
                    └─────────┬─────────┘
                              ↓
                    ┌───────────────────┐
                    │ PROVENANCE/WITNESS│
                    └─────────┬─────────┘
                              ↓
                    ┌───────────────────┐
                    │  GROUNDED STATE   │
                    └─────────┬─────────┘
                              ↓
                    ┌───────────────────┐
                    │     REASONER      │
                    └─────────┬─────────┘
                              ↓
                    ┌───────────────────┐
                    │   COUNTEREVIDENCE │
                    └─────────┬─────────┘
                              ↓
                    ┌───────────────────┐
                    │      BREATH       │
                    └─────────┬─────────┘
                              ↓
                    ┌───────────────────┐
                    │    CHALLENGER     │
                    └─────────┬─────────┘
                              ↓
                    ┌───────────────────┐
                    │    VALIDATOR      │
                    └─────────┬─────────┘
                              ↓
                    ┌───────────────────┐
                    │  SECURITY GUARD   │
                    └─────────┬─────────┘
                              ↓
                           ACTION
                              ↓
                    ┌───────────────────┐
                    │  WITNESS MEMORY   │
                    └─────────┬─────────┘
                              └──────────↺
```

The design objective is not to make the model infallible. It is to prevent an unsupported model belief from becoming an irreversible action without passing through independent evidence, challenge, validation, and authorization boundaries.
