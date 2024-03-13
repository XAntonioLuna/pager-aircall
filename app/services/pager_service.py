import uuid

from app.adapters.database_adapter import DatabaseAdapter, NoResultsFoundException
from app.adapters.escalation_policy_adapter import EscalationPolicyAdapter
from app.adapters.timer_adapter import TimerAdapter
from app.services.notification_service import NotificationService
from app.models.alert import Alert
from typing import Optional


DATABASE = DatabaseAdapter()


class PagerService:
    def __init__(
            self,
            database_adapter: Optional[DatabaseAdapter] = DATABASE,
            notification_service: Optional[NotificationService] = None,
            timer_adapter: Optional[TimerAdapter] = TimerAdapter(),
            escalation_policy_adapter: Optional[EscalationPolicyAdapter] = EscalationPolicyAdapter()
    ):
        self.database_adapter = database_adapter
        if not notification_service:
            self.notification_service = NotificationService(database_adapter)
        else:
            self.notification_service = notification_service
        self.timer_adapter = timer_adapter
        self.escalation_policy_adapter = escalation_policy_adapter

    def raise_alert(self, service_id: str, message: str) -> Optional[str]:
        """
        Method called when a service detects an anomaly and raises an alert
        :param service_id: Service identifier
        :param message: Message containing the description of the failure
        """
        try:
            service = self.database_adapter.get_service_by_id(service_id)
        except NoResultsFoundException as e:
            print(f"Service with id {service_id} not found")
            raise e

        if not service.is_healthy():
            return None

        service.mark_as_unhealthy()
        self.database_adapter.update_service(service)
        print(f'Service {service.name} marked as unhealthy')

        try:
            escalation_policy = self.escalation_policy_adapter.get(service.escalation_policy_id)
        except Exception as e:
            print(f"Error getting escalation policy {service.escalation_policy_id} for service {service_id}")
            raise e

        alert = Alert(
            alert_id=service.service_id + '-' + str(uuid.uuid4()),
            service_id=service_id,
            escalation_policy_id=service.escalation_policy_id,
            message=message
        )
        self.database_adapter.insert_alert(alert)
        print(f'Alert {alert.alert_id} raised')

        self.notification_service.notify(escalation_policy, alert)
        self.timer_adapter.send_task(alert.alert_id)

        return alert.alert_id

    def acknowledge_alert(self, alert_id: str) -> None:
        """
        Method called when an alert is acknowledged via the web interface
        :param alert_id: Alert identifier
        """
        try:
            alert = self.database_adapter.get_alert(alert_id)
        except NoResultsFoundException as e:
            print(f"Alert with id {alert_id} not found")
            raise e

        if alert.acknowledged:
            return

        alert.acknowledge()
        self.database_adapter.insert_alert(alert)

    def resolve_alert(self, alert_id: str) -> None:
        """
        Method called when an alert is resolved via the web interface
        :param alert_id: Alert identifier
        """
        try:
            alert = self.database_adapter.get_alert(alert_id)
        except NoResultsFoundException as e:
            print(f"Alert with id {alert_id} not found")
            raise e

        if alert.resolved:
            return

        try:
            service = self.database_adapter.get_service_by_id(alert.service_id)
        except NoResultsFoundException as e:
            # This should never happen, but just in case
            print(f"Service with id {alert.service_id} not found")
            raise e

        if not alert.acknowledged:
            alert.acknowledge()
        alert.resolve()
        self.database_adapter.insert_alert(alert)

        service.mark_as_healthy()
        self.database_adapter.update_service(service)

    def timeout_callback(self, alert_id: str) -> None:
        """
        Method called when the timer service calls the callback URL to indicate a timeout
        :param alert_id: Alert identifier
        """
        try:
            alert = self.database_adapter.get_alert(alert_id)
        except NoResultsFoundException as e:
            print(f"Alert with id {alert_id} not found")
            raise e

        if alert.acknowledged or alert.resolved:
            return

        escalation_policy = self.escalation_policy_adapter.get(alert.escalation_policy_id)

        if alert.escalation_level == escalation_policy.escalation_levels():
            return

        alert.escalate()
        self.notification_service.notify(escalation_policy, alert)
        self.timer_adapter.send_task(alert.alert_id)
