from dataclasses import dataclass
from typing import List
from app.models.levels import Level


@dataclass
class EscalationPolicy:
    escalation_id: str
    name: str
    levels: List[Level]

    def escalation_levels(self) -> int:
        return len(self.levels)
