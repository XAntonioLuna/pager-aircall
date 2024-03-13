import uuid

from app.models.alert import Alert
from app.models.escalation_policy import EscalationPolicy
from app.models.target import TargetType
from app.adapters.sms_adapter import SmsAdapter
from app.adapters.email_adapter import EmailAdapter
from app.models.notification import Notification
from app.utilities.time_utils import now_in_millis
from app.adapters.database_adapter import DatabaseAdapter


class NotificationService:
    def __init__(
            self,
            database_adapter: DatabaseAdapter = DatabaseAdapter(),
            sms_adapter: SmsAdapter = SmsAdapter(),
            email_adapter: EmailAdapter = EmailAdapter()
    ):
        self.sms_adapter = sms_adapter
        self.email_adapter = email_adapter
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
            if target.type == TargetType.SMS:
                self.sms_adapter.send(
                    phone_number=target.contact_info, message=alert.message
                )
            elif target.type == TargetType.EMAIL:
                self.email_adapter.send(
                    email=target.contact_info, subject=f'Alert {alert.alert_id}', body=alert.message
                )
            else:
                raise ValueError(f"Target type {target.type.value} not supported")
