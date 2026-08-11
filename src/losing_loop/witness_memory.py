from dataclasses import dataclass
from hashlib import sha256
from .models import DecisionRecord

@dataclass(frozen=True)
class Witness:
    record: DecisionRecord
    digest: str

class WitnessMemory:
    def __init__(self):
        self.records: list[Witness] = []

    def append(self, record: DecisionRecord) -> Witness:
        digest=sha256(repr(record).encode("utf-8")).hexdigest()
        witness=Witness(record,digest)
        self.records.append(witness)
        return witness
