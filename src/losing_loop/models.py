from dataclasses import dataclass, field
from enum import Enum
from typing import Any

class EvidenceType(str, Enum):
    OBSERVATION = "observation"
    STATIC_ANALYSIS = "static_analysis"
    RUNTIME_RESULT = "runtime_result"
    USER_ASSERTION = "user_assertion"
    MODEL_ASSERTION = "model_assertion"
    EXTERNAL_SOURCE = "external_source"
    DERIVED_FACT = "derived_fact"
    COUNTEREVIDENCE = "counterevidence"

class ValidationStatus(str, Enum):
    UNKNOWN = "unknown"
    SUPPORTED = "supported"
    CONTRADICTED = "contradicted"
    VALIDATED = "validated"
    REJECTED = "rejected"

class Decision(str, Enum):
    PROCEED = "proceed"
    BREATH = "breath"
    BLOCK = "block"

@dataclass(frozen=True)
class Evidence:
    id: str
    claim: str
    source: str
    content: str
    confidence: float
    authenticated: bool = True
    type: EvidenceType = EvidenceType.OBSERVATION
    provenance: tuple[str, ...] = ()

@dataclass
class Claim:
    hypothesis: str
    evidence_ids: list[str] = field(default_factory=list)
    assumptions: list[str] = field(default_factory=list)
    uncertainties: list[str] = field(default_factory=list)
    counterevidence_needed: list[str] = field(default_factory=list)
    validation_plan: list[str] = field(default_factory=list)
    validation: ValidationStatus = ValidationStatus.UNKNOWN

@dataclass
class DecisionRecord:
    decision: Decision
    reason: str
    evidence_ids: list[str]
    validation: ValidationStatus
    authorization: bool
    metadata: dict[str, Any] = field(default_factory=dict)
