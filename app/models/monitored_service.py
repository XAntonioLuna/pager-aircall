from dataclasses import dataclass
from enum import Enum
from app.models.escalation_policy import EscalationPolicy


class MonitoredServiceState(Enum):
    HEALTHY = "HEALTHY",
    UNHEALTHY = "UNHEALTHY"


@dataclass
class MonitoredService:
    service_id: str
    name: str
    escalation_policy_id: str
    current_state: MonitoredServiceState = MonitoredServiceState.HEALTHY

    def mark_as_healthy(self):
        self.current_state = MonitoredServiceState.HEALTHY

    def mark_as_unhealthy(self):
        self.current_state = MonitoredServiceState.UNHEALTHY

    def is_healthy(self):
        return self.current_state == MonitoredServiceState.HEALTHY
