# Losing the Loop

A research and engineering repository for designing AI systems that can detect loss of epistemic integrity, pause consequential action, recover safely, and require independently authorized changes.

> **Status:** Research / prototype specification. The mechanisms in this repository are design hypotheses and testable engineering patterns, not claims of production validation.

## Core architecture

Losing the Loop is organized around three connected systems:

1. **Trust Recovery Loop** — detects when an adaptive system has lost alignment with protected invariants and moves it into recovery rather than allowing uncontrolled self-modification.
2. **Truth / Integrity Layer** — preserves provenance, uncertainty, counterevidence, decision history, and protected invariants so the system can distinguish confidence from truth.
3. **BREATH → Hammer → Security Guard** — a staged control path: pause when evidence conflicts, detect anomalous or unsafe transitions, then require an independent authorization boundary before consequential changes.

### Design principles

- Truth governs epistemic integrity.
- Recovery is preferred to irreversible action when uncertainty is material.
- Adaptive cognition must be separated from protected authorization.
- A detected breach does **not** automatically authorize a new algorithm, policy, or self-modification.
- Provenance and counterevidence travel with important decisions.
- Protected invariants require explicit authorization to change.
- Safety controls should fail closed where practical.
- Every consequential transition should be observable and auditable.

## Repository map

```text
Loosing-the-loop/
├── README.md
├── LICENSE
├── SECURITY.md
├── CONTRIBUTING.md
├── docs/
│   ├── architecture.md
│   ├── trust-recovery-loop.md
│   ├── threat-model.md
│   ├── protected-invariants.md
│   └── evaluation.md
├── concepts/
│   ├── truth-integrity.md
│   ├── breath.md
│   ├── hammer.md
│   ├── security-guard.md
│   └── hope-purpose.md
└── tests/
    └── README.md
```

## A minimal control loop

```text
Observe
  ↓
Assess evidence + provenance + uncertainty
  ↓
Conflict / anomaly?
  ├── No → Continue under normal policy
  └── Yes
       ↓
     BREATH (pause consequential action)
       ↓
     HAMMER (detect / classify unsafe transition)
       ↓
     Preserve state + evidence
       ↓
     SECURITY GUARD (independent authorization)
       ├── Reject → recover / contain
       └── Approve → controlled change + verification
```

## What this project is trying to prevent

The central failure mode is a system **losing the loop**: an adaptive process changes its own assumptions, objectives, policies, or validation pathway and then uses the changed pathway to justify the change itself.

The proposed answer is to separate:

- **learning** from **authorization**;
- **reasoning** from **protected invariants**;
- **confidence** from **truth claims**;
- **recovery** from **self-modification**;
- **internal proposals** from **externally authorized changes**.

## Validation roadmap

The next stage is empirical testing. Proposed tests include invariant-violation scenarios, provenance tampering, conflicting evidence, reward/objective drift, unauthorized self-modification attempts, recovery after anomalous state transitions, and adversarial attempts to bypass authorization.

Success criteria should be defined before experiments are run.

## License

Apache-2.0. See `LICENSE`.
