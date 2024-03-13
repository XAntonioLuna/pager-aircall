from dataclasses import dataclass
from app.utilities.time_utils import now_in_millis


@dataclass
class Alert:
    alert_id: str
    service_id: str
    escalation_policy_id: str
    message: str
    created_at: int = now_in_millis()
    updated_at: int = None
    escalation_level: int = 0
    last_escalated_at: int = None
    acknowledged_at: int = None
    resolved_at: int = None
    acknowledged: bool = False
    resolved: bool = False

    def acknowledge(self) -> None:
        self.acknowledged = True
        self.acknowledged_at = now_in_millis()
        self.updated_at = self.acknowledged_at

    def resolve(self) -> None:
        self.resolved = True
        self.resolved_at = now_in_millis()
        self.updated_at = self.resolved_at

    def escalate(self) -> None:
        self.escalation_level += 1
        self.last_escalated_at = now_in_millis()
        self.updated_at = self.last_escalated_at
