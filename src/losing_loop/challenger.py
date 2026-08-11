from .models import Claim, Evidence

class Challenger:
    """Attempts to falsify a claim instead of approving it."""
    def challenge(self, claim: Claim, evidence: list[Evidence]) -> list[str]:
        findings=[]
        if not claim.evidence_ids:
            findings.append("missing supporting evidence")
        for item in evidence:
            if item.type.value == "COUNTEREVIDENCE":
                findings.append(f"counterevidence:{item.id}")
        return findings
