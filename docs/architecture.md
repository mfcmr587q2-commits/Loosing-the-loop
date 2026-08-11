# Architecture

## Objective

Losing the Loop is a control architecture for adaptive AI systems. Its purpose is to prevent an adaptive subsystem from becoming the sole authority over its own correctness, authorization, and recovery.

## Layers

### 1. Perception and tools
Collect observations and execute bounded tool calls. Tool output is treated as evidence, not automatically as truth.

### 2. Learning and reasoning
Generate hypotheses, plans, predictions, and candidate updates. This layer may adapt, but it cannot unilaterally redefine protected invariants.

### 3. Memory and witness
Record relevant observations, provenance, decisions, uncertainty, counterevidence, and state transitions. The witness record should be append-oriented and independently verifiable where feasible.

### 4. Truth / integrity layer
Evaluate evidence quality, provenance, conflicts, confidence, and invariant compliance. The layer should explicitly distinguish:

- observed fact;
- inferred claim;
- hypothesis;
- uncertainty;
- unresolved conflict.

### 5. BREATH
A controlled pause state. When evidence is insufficient, contradictory, or safety-relevant uncertainty exceeds a defined threshold, consequential action is suspended.

BREATH is not a solution by itself. It creates time and state stability for verification.

### 6. Hammer
A pre-execution anomaly detector and circuit breaker. It evaluates whether a proposed transition violates invariants, provenance requirements, authorization boundaries, or expected behavior.

### 7. Security Guard
An authorization boundary independent from the adaptive reasoning path. It evaluates whether a proposed change is permitted. The adaptive system can propose a change; it cannot grant itself permission.

### 8. Recovery
Rejected or uncertain transitions enter a recoverable state. Recovery should preserve evidence and safe options rather than forcing immediate self-modification.

## Trust boundary

The critical boundary is:

```text
Adaptive system → proposes
Protected control plane → verifies
Independent authorization → permits or rejects
Execution → occurs only after authorization
```

## Non-negotiable invariant

> Detection of a breach must not automatically authorize the mechanism that changes the system after the breach.

A recovery algorithm may be prepared or selected from an approved set, but authorization remains separate.
