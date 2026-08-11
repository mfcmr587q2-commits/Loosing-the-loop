"""Minimal executable prototype of the Losing-the-Loop safety architecture.

This is a deterministic research harness, not an autonomous agent. It models:
- evidence and provenance
- uncertainty/conflict detection
- BREATH (pause)
- The Hammer (circuit breaker)
- Security Guard (independent authorization)
- protected invariants
"""
from dataclasses import dataclass, field
from enum import Enum
from typing import List


class Decision(str, Enum):
    PROCEED = "proceed"
    BREATH = "breath"
    BLOCK = "block"


@dataclass(frozen=True)
class Evidence:
    claim: str
    source: str
    confidence: float
    authenticated: bool = True


@dataclass
class State:
    risk_score: float = 0.0
    uncertainty: float = 0.0
    conflicts: int = 0
    invariant_violation: bool = False
    anomaly: bool = False
    history: List[str] = field(default_factory=list)


class LosingTheLoop:
    def __init__(self, positive_threshold: float = 0.999999):
        self.positive_threshold = positive_threshold
        self.invariants = {"no_unauthorized_self_modification", "preserve_human_control"}
        self.authorized_actions = set()
        self.state = State()

    def assess(self, evidence: List[Evidence], requested_action: str) -> Decision:
        if not evidence:
            self.state.uncertainty = 1.0
            return self._breath("no evidence")

        authenticated = [e for e in evidence if e.authenticated]
        confidences = [e.confidence for e in authenticated]
        self.state.uncertainty = 1.0 - max(confidences, default=0.0)

        claims = {e.claim for e in authenticated}
        self.state.conflicts = max(0, len(claims) - 1)
        self.state.anomaly = self.state.conflicts > 0 or any(e.confidence < 0.5 for e in authenticated)

        self.state.invariant_violation = (
            requested_action == "self_modify"
            and "no_unauthorized_self_modification" in self.invariants
            and requested_action not in self.authorized_actions
        )

        if self.state.invariant_violation:
            return self._block("protected invariant violation")
        if self.state.anomaly or self.state.uncertainty > 0.25:
            return self._breath("conflicting or insufficient evidence")
        return Decision.PROCEED

    def authorize(self, action: str, independent_reviewer: bool = False) -> bool:
        if not independent_reviewer:
            return False
        self.authorized_actions.add(action)
        return True

    def _breath(self, reason: str) -> Decision:
        self.state.history.append(f"BREATH: {reason}")
        return Decision.BREATH

    def _block(self, reason: str) -> Decision:
        self.state.history.append(f"HAMMER/BLOCK: {reason}")
        return Decision.BLOCK
