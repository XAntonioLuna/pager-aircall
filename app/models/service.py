from app.models.service_state import ServiceState


class Service:
    def __init__(self, service_id: str, name: str, current_state: ServiceState, escalation_id: str) -> None:
        self.service_id = service_id
        self.name = name
        self.current_state = current_state
        self.escalation_id = escalation_id
