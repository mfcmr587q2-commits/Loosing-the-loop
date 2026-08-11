from .models import Claim, Decision, DecisionRecord, Evidence, EvidenceType, ValidationStatus

class LosingTheLoop:
    def __init__(self, uncertainty_threshold: float = 0.25):
        self.uncertainty_threshold = uncertainty_threshold
        self.invariants = {
            "NO_UNAUTHORIZED_SELF_MODIFICATION",
            "PRESERVE_HUMAN_CONTROL",
            "DO_NOT_DELETE_EVIDENCE",
            "DO_NOT_ERASE_PROVENANCE",
            "DO_NOT_SUPPRESS_COUNTEREVIDENCE",
            "DO_NOT_SELF_AUTHORIZE",
        }

    def assess(self, evidence: list[Evidence], claim: Claim, action: str | None = None,
               authorized: bool = False) -> DecisionRecord:
        if not evidence:
            return self._record(Decision.BREATH, "no evidence", evidence, claim, authorized)

        if any(not e.authenticated for e in evidence):
            return self._record(Decision.BREATH, "unauthenticated evidence", evidence, claim, authorized)

        if claim.validation == ValidationStatus.CONTRADICTED:
            return self._record(Decision.BREATH, "claim contradicted", evidence, claim, authorized)

        if claim.validation == ValidationStatus.REJECTED:
            return self._record(Decision.BLOCK, "claim rejected", evidence, claim, authorized)

        if claim.uncertainties:
            return self._record(Decision.BREATH, "unresolved uncertainty", evidence, claim, authorized)

        claims = {e.claim for e in evidence if e.type != EvidenceType.COUNTEREVIDENCE}
        if len(claims) > 1:
            return self._record(Decision.BREATH, "conflicting evidence", evidence, claim, authorized)

        if action == "self_modify" and not authorized:
            return self._record(Decision.BLOCK, "protected invariant: unauthorized self-modification", evidence, claim, authorized)

        if claim.validation != ValidationStatus.VALIDATED:
            return self._record(Decision.BREATH, "validation is not complete", evidence, claim, authorized)

        if not authorized:
            return self._record(Decision.BLOCK, "independent authorization missing", evidence, claim, authorized)

        return self._record(Decision.PROCEED, "validated and independently authorized", evidence, claim, authorized)

    @staticmethod
    def _record(decision, reason, evidence, claim, authorized):
        return DecisionRecord(
            decision=decision,
            reason=reason,
            evidence_ids=[e.id for e in evidence],
            validation=claim.validation,
            authorization=authorized,
        )
