from __future__ import annotations

import dataclasses
import hashlib
import json
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Literal, Protocol


Lane = Literal["QUARANTINE", "CANON"]
Trust = Literal["UNVERIFIED", "VERIFIED", "EXTERNAL", "CANON"]
Risk = Literal["OBSERVE", "ADVISE", "SIMULATE", "EXECUTE", "IRREVERSIBLE"]

KNOWN_ACTION_TYPES: dict[str, Risk] = {
    "observe": "OBSERVE",
    "read": "OBSERVE",
    "inspect": "OBSERVE",
    "advise": "ADVISE",
    "recommend": "ADVISE",
    "simulate": "SIMULATE",
    "sandbox": "SIMULATE",
    "execute": "EXECUTE",
    "connect": "EXECUTE",
    "write": "EXECUTE",
    "deploy": "EXECUTE",
    "self_modify": "EXECUTE",
    "transfer": "IRREVERSIBLE",
    "delete": "IRREVERSIBLE",
    "broadcast": "IRREVERSIBLE",
    "exploit": "IRREVERSIBLE",
    "harm": "IRREVERSIBLE",
}


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


@dataclass
class EyePacket:
    ts: float
    lane: Lane
    trust: Trust
    source: str
    claim: Any
    evidence: Any = None
    test: Any = None
    outcome: Any = None
    prev_hash: str | None = None
    hash: str | None = None

    def compute_hash(self) -> str:
        body = dataclasses.asdict(self)
        body.pop("hash", None)
        return _sha256(json.dumps(body, sort_keys=True, ensure_ascii=False).encode("utf-8"))


class EyeLedger:
    """Append-oriented local witness ledger.

    Hash chaining is tamper-evident, not an independent trust anchor. Callers may
    persist/attest `head_hash()` outside this process for stronger guarantees.
    """

    def __init__(self, path: str | Path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.touch(exist_ok=True)

    def _objects(self) -> list[dict[str, Any]]:
        return [json.loads(line) for line in self.path.read_text(encoding="utf-8").splitlines() if line]

    def head_hash(self) -> str | None:
        objs = self._objects()
        return objs[-1].get("hash") if objs else None

    def append(self, packet: EyePacket) -> str:
        packet.prev_hash = self.head_hash()
        packet.hash = packet.compute_hash()
        with self.path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(dataclasses.asdict(packet), sort_keys=True, ensure_ascii=False) + "\n")
        return packet.hash

    def verify_chain(self, expected_head: str | None = None) -> bool:
        prev: str | None = None
        last: str | None = None
        for obj in self._objects():
            claimed = obj.get("hash")
            body = dict(obj)
            body.pop("hash", None)
            actual = _sha256(json.dumps(body, sort_keys=True, ensure_ascii=False).encode("utf-8"))
            if claimed != actual or obj.get("prev_hash") != prev:
                return False
            prev = claimed
            last = claimed
        return expected_head is None or last == expected_head

    def write(self, source: str, claim: Any, *, lane: Lane = "QUARANTINE", trust: Trust = "UNVERIFIED", **extra: Any) -> str:
        return self.append(EyePacket(time.time(), lane, trust, source, claim, **extra))


@dataclass(frozen=True)
class EvidenceChain:
    source: Any
    claim: Any
    test: Any
    outcome: Any
    authenticated: bool = False
    independently_validated: bool = False

    def is_complete(self) -> bool:
        return all(value is not None for value in (self.source, self.claim, self.test, self.outcome))

    def is_authorizable(self) -> bool:
        return self.is_complete() and self.authenticated and self.independently_validated


@dataclass(frozen=True)
class GuardianDecision:
    allowed: bool
    reviewer: str
    reason: str


class Guardian(Protocol):
    def authorize(self, action: dict[str, Any], evidence: EvidenceChain | None) -> GuardianDecision: ...


class DenyByDefaultGuardian:
    def authorize(self, action: dict[str, Any], evidence: EvidenceChain | None) -> GuardianDecision:
        return GuardianDecision(False, "deny-by-default", "independent guardian approval missing")


@dataclass(frozen=True)
class KernelOutcome:
    allowed: bool
    reason: str
    result: Any = None
    risk: Risk | None = None


class VeritasGovernanceKernel:
    """Governance wrapper designed to sit above adaptive reasoners/tools."""

    def __init__(self, ledger: EyeLedger, guardian: Guardian | None = None):
        self.eye = ledger
        self.guardian = guardian or DenyByDefaultGuardian()

    @staticmethod
    def classify_risk(action: dict[str, Any]) -> Risk:
        raw = action.get("type")
        if not isinstance(raw, str) or not raw.strip():
            raise ValueError("unknown action type")
        action_type = raw.strip().lower()
        try:
            return KNOWN_ACTION_TYPES[action_type]
        except KeyError as exc:
            raise ValueError(f"unknown action type: {action_type}") from exc

    @staticmethod
    def _ethics_block(action: dict[str, Any]) -> str | None:
        # Consequential actions must explicitly declare whether they affect humans.
        risk = VeritasGovernanceKernel.classify_risk(action)
        if action.get("harm") is True:
            return "declared harmful action"
        if risk in ("EXECUTE", "IRREVERSIBLE"):
            if "affects_human" not in action:
                return "human-impact declaration missing"
            if action["affects_human"] is True and action.get("consent") is not True:
                return "human consent missing"
        return None

    def promote_to_canon(self, packet_hash: str, *, verifier: str, evidence_complete: bool, independent_validation: bool) -> KernelOutcome:
        if not verifier or not evidence_complete or not independent_validation:
            return KernelOutcome(False, "DENY: canon promotion requirements incomplete")
        self.eye.write(
            "promotion",
            {"type": "CANON_PROMOTION", "packet_hash": packet_hash, "verifier": verifier},
            lane="CANON",
            trust="CANON",
        )
        return KernelOutcome(True, "ALLOW: promoted to CANON")

    def human_override(self, action: dict[str, Any], *, human_id: str, reason: str) -> KernelOutcome:
        if not human_id or not reason:
            return KernelOutcome(False, "DENY: explicit human override identity and reason required")
        self.eye.write(
            "human_override",
            {"type": "HUMAN_OVERRIDE", "human_id": human_id, "reason": reason, "action": action},
            lane="QUARANTINE",
            trust="VERIFIED",
        )
        # Override authorizes review/recovery, not prohibited irreversible actions.
        try:
            risk = self.classify_risk(action)
        except ValueError as exc:
            return KernelOutcome(False, f"BREATH: {exc}")
        if risk == "IRREVERSIBLE":
            return KernelOutcome(False, "DENY: irreversible action remains prohibited", risk=risk)
        return KernelOutcome(True, "ALLOW: explicit logged human override", risk=risk)

    def run_action(
        self,
        action: dict[str, Any],
        fn: Callable[[], Any],
        *,
        evidence: EvidenceChain | None = None,
    ) -> KernelOutcome:
        try:
            risk = self.classify_risk(action)
        except ValueError as exc:
            self.eye.write("governance", {"type": "BREATH", "reason": str(exc), "action": action})
            return KernelOutcome(False, f"BREATH: {exc}")

        ethics_reason = self._ethics_block(action)
        if ethics_reason:
            self.eye.write("ethics", {"type": "BLOCK", "reason": ethics_reason, "action": action})
            return KernelOutcome(False, f"DENY: {ethics_reason}", risk=risk)

        prelog = self.eye.write("system", {"type": "ACTION_PRELOG", "action": action})

        if risk == "IRREVERSIBLE":
            return KernelOutcome(False, "DENY: irreversible forbidden by default", risk=risk)

        if risk == "EXECUTE":
            if evidence is None or not evidence.is_authorizable():
                self.eye.write("governance", {"type": "BREATH", "reason": "evidence not independently authorizable", "prelog": prelog})
                return KernelOutcome(False, "BREATH: authenticated independently validated evidence required", risk=risk)
            guardian = self.guardian.authorize(action, evidence)
            self.eye.write("guardian", dataclasses.asdict(guardian), trust="VERIFIED" if guardian.allowed else "UNVERIFIED")
            if not guardian.allowed:
                return KernelOutcome(False, f"DENY: guardian authorization missing: {guardian.reason}", risk=risk)

        try:
            result = fn()
        except Exception as exc:  # fail closed and witness the exception
            self.eye.write("system", {"type": "ACTION_POSTLOG", "action": action}, outcome={"ok": False, "error": repr(exc)})
            return KernelOutcome(False, "FAIL_CLOSED: execution exception", risk=risk)

        self.eye.write("system", {"type": "ACTION_POSTLOG", "action": action}, outcome={"ok": True, "result": result})
        return KernelOutcome(True, "ALLOW", result=result, risk=risk)
