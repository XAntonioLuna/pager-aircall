import pytest
from app.models.escalation_policy import EscalationPolicy
from app.models.alert import Alert
from app.models.levels import Level
from app.models.target import Target, TargetType
from app.services.notification_service import NotificationService


@pytest.fixture()
def notification_service(mocker):
    database_adapter = mocker.Mock()
    email_adapter = mocker.Mock()
    sms_adapter = mocker.Mock()
    return NotificationService(database_adapter=database_adapter, email_adapter=email_adapter, sms_adapter=sms_adapter)


def test_notify(notification_service):
    escalation_policy = EscalationPolicy(
        escalation_id='ep1',
        name='Test escalation policy',
        levels=[
            Level(
                level_id='level1',
                name='Level 1',
                targets=[
                    Target(
                        target_id='target1',
                        type=TargetType.EMAIL,
                        contact_info='test@testing.com',
                        name='Email target'
                    ),
                    Target(
                        target_id='target1',
                        type=TargetType.SMS,
                        contact_info='+1(925)550-8877',
                        name='SMS target'
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

    notification_service.email_adapter.send.assert_called_once()
    notification_service.sms_adapter.send.assert_called_once()
    notification_service.database_adapter.insert_notification.assert_called_once()
