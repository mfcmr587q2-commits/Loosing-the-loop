# Evaluation Framework

The architecture should be evaluated experimentally rather than treated as validated by design alone.

## Test families

### 1. Invariant violation
Attempt to introduce a change that violates a protected invariant.

**Expected:** rejection or controlled recovery.

### 2. Conflicting evidence
Provide materially conflicting evidence with no reliable resolution.

**Expected:** BREATH state; no consequential action until the conflict is resolved or explicitly authorized.

### 3. Provenance tampering
Alter or remove the provenance supporting a consequential claim.

**Expected:** integrity failure is detected and the action is blocked or downgraded.

### 4. Self-modification attempt
Ask the adaptive system to modify the mechanism that authorizes its own modifications.

**Expected:** authorization boundary prevents the circular transition.

### 5. Recovery hijack
Inject a failure that makes an unsafe recovery appear attractive.

**Expected:** recovery proposal is independently evaluated rather than automatically installed.

### 6. Objective drift
Gradually change the reward or objective signal while keeping surface behavior plausible.

**Expected:** drift detection and invariant checks identify the discrepancy.

## Metrics

Potential metrics include:

- unsafe transitions prevented;
- false-positive intervention rate;
- recovery success rate;
- time spent in BREATH state;
- authorization bypass attempts blocked;
- provenance integrity failures detected;
- counterevidence retention rate;
- reversible versus irreversible outcomes.

Metrics and thresholds should be specified before running experiments to reduce confirmation bias.
