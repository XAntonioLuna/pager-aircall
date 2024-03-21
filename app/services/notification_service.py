import uuid

from app.models.alert import Alert
from app.models.escalation_policy import EscalationPolicy
from app.models.notification import Notification
from app.utilities.time_utils import now_in_millis
from app.adapters.database_adapter import DatabaseAdapter


class NotificationService:
    def __init__(
            self,
            database_adapter: DatabaseAdapter = DatabaseAdapter(),
    ):
        self.database_adapter = database_adapter

    def notify(self, escalation_policy: EscalationPolicy, alert: Alert) -> None:
        # It is possible that alerts reach levels higher than the number of levels in the escalation policy. We need
        # to make sure we don't go out of bounds
        escalation_level = min(alert.escalation_level, len(escalation_policy.levels) - 1)
        level = escalation_policy.levels[escalation_level]

        notification = Notification(
            notification_id=str(uuid.uuid4()),
            alert_id=alert.alert_id,
            level_id=level.level_id,
            sent_at=now_in_millis()
        )

        try:
            self.database_adapter.insert_notification(notification)
        except Exception as e:
            print('Error storing to database')
            raise e

        for target in level.targets:
            target.adapter.send(message=alert.message, kwargs=target.__dict__)
