"""
Mock database used for demonstration purposes
"""
from app.models.monitored_service import MonitoredService, MonitoredServiceState
from app.models.alert import Alert
from app.models.notification import Notification

from typing import Optional

# ---------------Test data--------------------------
SERVICES = {
    'serv1': MonitoredService(
        service_id='serv1',
        name='Service 1',
        current_state=MonitoredServiceState.HEALTHY,
        escalation_policy_id='ep1'
    ),
}
# ---------------------------------------------------


class NoResultsFoundException(Exception):
    pass


class DatabaseAdapter:
    def __init__(
            self,
            services: Optional[dict] = SERVICES
    ):
        self.services = services
        self.alerts = {}
        self.notifications = {}

    def get_service_by_id(self, service_id: str) -> MonitoredService:
        try:
            return self.services[service_id]
        except Exception:
            raise NoResultsFoundException

    def update_service(self, service: MonitoredService) -> None:
        self.services[service.service_id] = service

    def insert_notification(self, notification: Notification) -> None:
        self.notifications[notification.notification_id] = notification

    def insert_alert(self, alert: Alert) -> None:
        self.alerts[alert.alert_id] = alert

    def get_alert(self, alert_id: str) -> Alert:
        try:
            return self.alerts[alert_id]
        except Exception:
            raise NoResultsFoundException
