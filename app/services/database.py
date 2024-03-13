"""
Mock database used for demonstration purposes
"""
from app.models.service import Service
from typing import Optional

# ---------------Mock table data--------------------------
SERVICES = {
    'serv1': {
        'name': 'Service 1',
        'escalation_policy_id': 'ep1',
        'current_state': 'healthy'
    },
    'serv2': {
        'name': 'Service 2',
        'escalation_policy_id': 'ep2',
        'current_state': 'healthy'
    },
    'serv3': {
        'name': 'Service 3',
        'escalation_policy_id': 'ep1',
        'current_state': 'healthy'
    },
}

# -----------------------------------------------------------


class NoResultsFoundException(Exception):
    pass


class Database:
    def __init__(
            self,
            services: Optional[dict] = SERVICES
    ):
        self.services = services

    # Simulates queries to the database
    def get_service_by_id(self, service_id: str) -> Service:
        try:
            service = self.services[service_id]
            return Service(
                id=service_id,
                name=service.get('name'),
                current_state=service.get('current_state'),
                escalation_id=service.get('escalation_policy_id')
            )
        except Exception:
            raise NoResultsFoundException
