import pytest
from app.services.pager_service import PagerService
from app.models.monitored_service import MonitoredService, MonitoredServiceState
from app.models.alert import Alert


@pytest.fixture()
def pager_service(mocker):
    database_adapter = mocker.Mock()
    notification_service = mocker.Mock()
    timer_adapter = mocker.Mock()
    escalation_policy_adapter = mocker.Mock()

    return PagerService(database_adapter, notification_service, timer_adapter, escalation_policy_adapter)


def test_raise_alert(pager_service):
    service_id = "service_id"
    message = "message"

    pager_service.database_adapter.get_service_by_id.return_value = MonitoredService(
        service_id='serv_x',
        name="Service X",
        escalation_policy_id="escalation_policy_X"
    )

    pager_service.raise_alert(service_id, message)

    pager_service.database_adapter.get_service_by_id.assert_called_once_with(service_id)
    pager_service.database_adapter.update_service.assert_called_once()
    pager_service.escalation_policy_adapter.get.assert_called_once_with('escalation_policy_X')
    pager_service.database_adapter.insert_alert.assert_called_once()
    pager_service.notification_service.notify.assert_called_once()
    pager_service.timer_adapter.send_task.assert_called_once()


def test_raise_alert_for_nonexistent_service(pager_service):
    service_id = "service_id"
    message = "message"

    pager_service.database_adapter.get_service_by_id.side_effect = Exception("Not found")

    with pytest.raises(Exception) as e:
        pager_service.raise_alert(service_id, message)

    assert str(e.value) == "Not found"
    pager_service.database_adapter.get_service_by_id.assert_called_once_with(service_id)
    pager_service.database_adapter.update_service.assert_not_called()
    pager_service.escalation_policy_adapter.get.assert_not_called()
    pager_service.database_adapter.insert_alert.assert_not_called()
    pager_service.notification_service.notify.assert_not_called()
    pager_service.timer_adapter.send_task.assert_not_called()


def test_raise_alert_for_unhealthy_service(pager_service):
    service_id = "service_id"
    message = "message"

    pager_service.database_adapter.get_service_by_id.return_value = MonitoredService(
        service_id='serv_x',
        name="Service X",
        escalation_policy_id="escalation_policy_X",
        current_state=MonitoredServiceState.UNHEALTHY
    )

    alert_id = pager_service.raise_alert(service_id, message)

    assert alert_id is None
    pager_service.database_adapter.get_service_by_id.assert_called_once_with(service_id)
    pager_service.database_adapter.update_service.assert_not_called()
    pager_service.escalation_policy_adapter.get.assert_not_called()
    pager_service.database_adapter.insert_alert.assert_not_called()
    pager_service.notification_service.notify.assert_not_called()
    pager_service.timer_adapter.send_task.assert_not_called()


def test_acknowledge_alert(pager_service):
    alert_id = "test_alert_id"

    pager_service.database_adapter.get_alert.return_value = Alert(
        alert_id=alert_id,
        service_id='serv_x',
        escalation_policy_id="escalation_policy_X",
        message="test message"
    )

    pager_service.acknowledge_alert(alert_id)

    pager_service.database_adapter.get_alert.assert_called_once_with(alert_id)
    pager_service.database_adapter.insert_alert.assert_called_once()


def test_acknowledge_alert_for_nonexistent_alert(pager_service):
    alert_id = "test_alert_id"

    pager_service.database_adapter.get_alert.side_effect = Exception("Not found")

    with pytest.raises(Exception) as e:
        pager_service.acknowledge_alert(alert_id)

    assert str(e.value) == "Not found"
    pager_service.database_adapter.get_alert.assert_called_once_with(alert_id)
    pager_service.database_adapter.insert_alert.assert_not_called()


def test_acknowledge_alert_for_already_acknowledged_alert(pager_service):
    alert_id = "test_alert_id"

    alert = Alert(
        alert_id=alert_id,
        service_id='serv_x',
        escalation_policy_id="escalation_policy_X",
        message="test message",
        acknowledged=True
    )

    pager_service.database_adapter.get_alert.return_value = alert

    pager_service.acknowledge_alert(alert_id)

    pager_service.database_adapter.get_alert.assert_called_once_with(alert_id)
    pager_service.database_adapter.insert_alert.assert_not_called()
    pager_service.database_adapter.insert_notification.assert_not_called()


def test_resolve_alert(pager_service):
    alert_id = "test_alert_id"

    pager_service.database_adapter.get_alert.return_value = Alert(
        alert_id=alert_id,
        service_id='serv_x',
        escalation_policy_id="escalation_policy_X",
        message="test message"
    )

    pager_service.resolve_alert(alert_id)

    pager_service.database_adapter.get_alert.assert_called_once_with(alert_id)
    pager_service.database_adapter.insert_alert.assert_called_once()


def test_resolve_alert_for_nonexistent_alert(pager_service):
    alert_id = "test_alert_id"

    pager_service.database_adapter.get_alert.side_effect = Exception("Not found")

    with pytest.raises(Exception) as e:
        pager_service.resolve_alert(alert_id)

    assert str(e.value) == "Not found"
    pager_service.database_adapter.get_alert.assert_called_once_with(alert_id)
    pager_service.database_adapter.insert_alert.assert_not_called()


def test_resolve_alert_for_already_resolved_alert(pager_service):
    alert_id = "test_alert_id"

    alert = Alert(
        alert_id=alert_id,
        service_id='serv_x',
        escalation_policy_id="escalation_policy_X",
        message="test message",
        resolved=True
    )

    pager_service.database_adapter.get_alert.return_value = alert

    pager_service.resolve_alert(alert_id)

    pager_service.database_adapter.get_alert.assert_called_once_with(alert_id)
    pager_service.database_adapter.insert_alert.assert_not_called()
    pager_service.database_adapter.insert_notification.assert_not_called()
