# Protected Invariants

Protected invariants are constraints that adaptive components may reason about but cannot redefine without an independent authorization path.

## Initial invariant set

1. **Authorization separation** — no adaptive component may authorize its own consequential modification.
2. **Provenance preservation** — consequential claims must retain sufficient provenance to be independently evaluated.
3. **Uncertainty preservation** — unresolved uncertainty must not silently become certainty.
4. **Counterevidence visibility** — material counterevidence must remain available to the evaluator.
5. **Recovery before irreversible action** — where safe recovery is possible, uncertainty should not force irreversible action.
6. **Auditability** — consequential transitions must produce an inspectable decision record.
7. **Human agency** — defined classes of consequential actions remain subject to explicit human or independently controlled authorization.

## Change protocol

Changing an invariant is itself a consequential change. Therefore the proposed invariant change must pass a separate authorization process and must not be accepted merely because the adaptive system recommends it.

## Future formalization

Each invariant should eventually receive:

- a machine-checkable representation;
- scope and applicability conditions;
- test cases;
- failure behavior;
- an owner/authority definition;
- versioning and provenance metadata.
