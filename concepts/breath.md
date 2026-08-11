# BREATH

BREATH is the controlled pause state of the architecture.

## Trigger conditions

Examples include:

- insufficient evidence for a consequential action;
- unresolved evidence conflict;
- invariant violation;
- unexpected model or policy transition;
- provenance failure;
- authorization ambiguity.

## Behavior

When BREATH is entered, consequential execution pauses while the system preserves state, records the trigger, gathers evidence, and routes the proposed action for verification.

BREATH is deliberately simple: **when the system cannot safely establish what it should do, it stops doing the consequential thing.**
