from .challenger import Challenger
from .models import Claim, Decision, DecisionRecord, Evidence, EvidenceType, ValidationStatus


class LosingTheLoop:
    def __init__(self, uncertainty_threshold: float = 0.25):
        if not 0 <= uncertainty_threshold <= 1:
            raise ValueError("uncertainty_threshold must be between 0 and 1")
        self.uncertainty_threshold = uncertainty_threshold
        self.challenger = Challenger()
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

        if action == "self_modify" and not authorized:
            return self._record(Decision.BLOCK, "protected invariant: unauthorized self-modification", evidence, claim, authorized)

        challenge_findings = self.challenger.challenge(claim, evidence)
        if challenge_findings:
            return self._record(
                Decision.BREATH,
                "challenger found unresolved evidence issues",
                evidence,
                claim,
                authorized,
                metadata={"challenge_findings": challenge_findings},
            )

        if any(not 0 <= e.confidence <= 1 for e in evidence):
            return self._record(Decision.BREATH, "invalid evidence confidence", evidence, claim, authorized)

        claims = {e.claim for e in evidence if e.type != EvidenceType.COUNTEREVIDENCE}
        if len(claims) > 1:
            return self._record(Decision.BREATH, "conflicting evidence", evidence, claim, authorized)

        cited_ids = set(claim.evidence_ids)
        cited_evidence = [e for e in evidence if e.id in cited_ids]
        if any(e.claim != claim.hypothesis for e in cited_evidence):
            return self._record(Decision.BREATH, "cited evidence does not support claim", evidence, claim, authorized)

        uncertainty = 1 - max(e.confidence for e in cited_evidence)
        if uncertainty > self.uncertainty_threshold:
            return self._record(Decision.BREATH, "evidence uncertainty exceeds threshold", evidence, claim, authorized)

        if claim.validation != ValidationStatus.VALIDATED:
            return self._record(Decision.BREATH, "validation is not complete", evidence, claim, authorized)

        if not authorized:
            return self._record(Decision.BLOCK, "independent authorization missing", evidence, claim, authorized)

        return self._record(Decision.PROCEED, "validated and independently authorized", evidence, claim, authorized)

    @staticmethod
    def _record(decision, reason, evidence, claim, authorized, metadata=None):
        return DecisionRecord(
            decision=decision,
            reason=reason,
            evidence_ids=[e.id for e in evidence],
            validation=claim.validation,
            authorization=authorized,
            metadata=metadata or {},
        )
