# Trust Recovery Loop

## Problem

A self-improving system can create a circular validation failure:

```text
system changes policy
      ↓
system evaluates change using changed policy
      ↓
system concludes change is valid
      ↓
system changes policy again
```

This is the loop that the project calls **losing the loop**.

## Proposed recovery sequence

1. **Observe** — capture the triggering event and relevant state.
2. **Freeze consequential action** — enter BREATH when required.
3. **Preserve evidence** — retain provenance, prior state, counterevidence, and uncertainty.
4. **Detect** — Hammer evaluates the proposed transition.
5. **Classify** — determine whether the event is ordinary error, drift, policy conflict, integrity failure, or authorization failure.
6. **Generate recovery candidates** — adaptive components may suggest safe recovery options.
7. **Verify** — compare the candidate against protected invariants and independent evidence.
8. **Authorize** — Security Guard independently approves or rejects the transition.
9. **Execute in a bounded way** — apply only the authorized change.
10. **Re-test** — verify the post-change state against predefined criteria.
11. **Record** — append the complete decision and outcome to the witness record.

## Important separation

Recovery is not equivalent to self-modification.

A system can learn from an event without immediately installing the lesson as a new algorithm. Learning can produce a proposal; authorization decides whether that proposal becomes an active system change.

## Evaluation questions

For every proposed recovery mechanism ask:

- What invariant is protected?
- What evidence triggered recovery?
- What evidence could falsify the diagnosis?
- Who or what authorizes the change?
- Can the learning system alter that authorization path?
- Is the change reversible?
- Can the system explain what changed and why?
- What happens if the evidence remains unresolved?
