import pytest
from app.models.escalation_policy import EscalationPolicy
from app.models.alert import Alert
from app.models.levels import Level
from app.models.target import TargetEmail, TargetSms
from app.services.notification_service import NotificationService


@pytest.fixture()
def notification_service(mocker):
    database_adapter = mocker.Mock()
    return NotificationService(database_adapter=database_adapter)


def test_notify(notification_service):
    escalation_policy = EscalationPolicy(
        escalation_id='ep1',
        name='Test escalation policy',
        levels=[
            Level(
                level_id='level1',
                name='Level 1',
                targets=[
                    TargetEmail(
                        target_id='target1',
                        name='Email target',
                        email='testing@testtest.com'
                    ),
                    TargetSms(
                        target_id='target1',
                        name='SMS target',
                        phone_number='+1234567890'
                    ),

                ]
            )
        ]
    )

    alert = Alert(
        alert_id='alert1',
        service_id='serv1',
        escalation_policy_id='ep1',
        message='Test message'
    )

    notification_service.notify(escalation_policy, alert)
    notification_service.database_adapter.insert_notification.assert_called_once()
