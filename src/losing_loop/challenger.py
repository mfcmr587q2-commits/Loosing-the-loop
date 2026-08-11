from .models import Claim, Evidence, EvidenceType


class Challenger:
    """Attempts to falsify a claim instead of approving it."""

    def challenge(self, claim: Claim, evidence: list[Evidence]) -> list[str]:
        findings: list[str] = []
        if not claim.evidence_ids:
            findings.append("missing supporting evidence")

        seen_ids: set[str] = set()
        for item in evidence:
            if item.id in seen_ids:
                findings.append(f"duplicate evidence id:{item.id}")
            seen_ids.add(item.id)
            if item.type == EvidenceType.COUNTEREVIDENCE:
                findings.append(f"counterevidence:{item.id}")

        for evidence_id in claim.evidence_ids:
            if evidence_id not in seen_ids:
                findings.append(f"missing evidence:{evidence_id}")
        return findings
