from .models import Claim, ValidationStatus

class Validator:
    """Validates against an independent observation; a model claim alone is insufficient."""
    def validate(self, claim: Claim, observed_hypothesis: str | None):
        if observed_hypothesis is None:
            return ValidationStatus.UNKNOWN
        return (ValidationStatus.VALIDATED if observed_hypothesis == claim.hypothesis
                else ValidationStatus.REJECTED)
