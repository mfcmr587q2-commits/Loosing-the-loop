# AI-GBS × Veritas Blinded A/B Benchmark

Status: preregistered benchmark protocol

Purpose: test whether a fixed Veritas intervention changes multi-agent coordination in the ICLR 2026 AI-GBS group guessing task without tuning the intervention after observing results.

## Non-cheating rules

1. Freeze the Veritas intervention before the first run.
2. Use the official AI-GBS experiment code and task mechanics unchanged except for the treatment prompt addition.
3. Use the same model, target numbers, group sizes, temperatures, max rounds, and seed schedule in baseline and Veritas arms.
4. Do not discard failed or inconvenient runs. Parsing/API failures must be retained and reported.
5. Analyze blinded labels first (Arm A / Arm B). Reveal which arm is Veritas only after the metrics and statistical tests are complete.
6. Do not interpret lower synergy as automatically safer or better. Report task performance, synergy, redundancy, I3, G3, and failure/intervention rates together.
7. Do not change thresholds, prompts, null models, or estimators after inspecting results unless the change is declared a new experiment.

## Experimental arms

- Arm A: official Plain AI-GBS prompt.
- Arm B: the same prompt plus one fixed Veritas governance intervention.
- Optional positive controls: Persona and Persona + ToM, exactly as defined by the paper/replication code.

## Initial replication grid

For the first local Qwen replication:

- Model: qwen3:4b through the user's local Ollama endpoint.
- Group sizes: 3 and 4.
- Temperatures: 0.05, 0.2, 0.5, 0.8, 1.2.
- Conditions: baseline and Veritas.
- Seeds: 30 independent seeds per configuration.
- Total planned runs: 2 × 5 × 2 × 30 = 600.

This local grid is intentionally smaller than the paper's full sweep and must be described as a replication/adaptation, not as reproduction of every published experiment.

## Primary measurements

Use the paper's information-theoretic framework on the recorded trajectories:

1. Pairwise emergence capacity / dynamical synergy from two-source PID of time-delayed mutual information.
2. Practical criterion:
   S_macro(l) = I(V_t; V_t+l) - sum_k I(X_k,t; V_t+l)
3. Coalition test:
   G3 = I3 - max(I2_{12}, I2_{13}, I2_{23})
4. Redundancy and individual mutual information.
5. Task success rate and rounds-to-success.
6. Parsing/API failure rate and any governance-trigger/intervention rate.

## Falsification / robustness

- Row-wise shuffles to break identity-linked structure.
- Column/time-shift surrogates to disrupt cross-agent alignment while preserving individual dynamics.
- Bias-corrected estimates where feasible.
- Paired baseline-vs-Veritas comparisons on matched seeds/configurations.
- Report confidence intervals and effect sizes, not p-values alone.

## Interpretation guardrails

A result counts as evidence for a useful Veritas effect only if the direction is consistent with an explicitly stated objective and does not rely on selectively ignoring task degradation. Synergy is a structural statistic, not evidence of consciousness, awakening, or general intelligence.

## Provenance

Benchmark basis: Christoph Riedl, “Emergent Coordination in Multi-Agent Language Models,” ICLR 2026, arXiv:2510.05174v4, and the official replication repository `riedlc/AI-GBS`.
