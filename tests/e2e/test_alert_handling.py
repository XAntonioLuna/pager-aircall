from app.services.pager_service import PagerService
from app.models.monitored_service import MonitoredService
from app.adapters.database_adapter import DatabaseAdapter


def monitored_service_fixture():
    return MonitoredService(
        service_id='super_service',
        name='Super Service',
        escalation_policy_id="ep1",
    )


def test_create_new_alert():
    base_service = monitored_service_fixture()
    database_adapter = DatabaseAdapter({})
    database_adapter.update_service(base_service)

    ps = PagerService(database_adapter=database_adapter)
    message = "Something went wrong!"

    alert_id = ps.raise_alert(base_service.service_id, message)

    assert len(ps.database_adapter.alerts) == 1
    assert len(ps.database_adapter.notifications) == 1

    alert = ps.database_adapter.get_alert(alert_id)
    assert alert.service_id == base_service.service_id
    assert alert.escalation_policy_id == base_service.escalation_policy_id
    assert alert.message == message

    service = ps.database_adapter.get_service_by_id(base_service.service_id)
    assert not service.is_healthy()


def test_attempt_to_raise_alert_for_nonexistent_service():
    database_adapter = DatabaseAdapter({})

    ps = PagerService(database_adapter=database_adapter)
    message = "Something went wrong!"

    try:
        ps.raise_alert('nonexistent_service', message)
        assert False
    except Exception as e:
        assert str(e) == "Not found"


def test_attempt_to_raise_alert_for_unhealthy_service():
    base_service = monitored_service_fixture()
    database_adapter = DatabaseAdapter({})
    database_adapter.update_service(base_service)

    ps = PagerService(database_adapter=database_adapter)
    message = "Something went wrong!"

    ps.raise_alert(base_service.service_id, message)

    alert = ps.raise_alert(base_service.service_id, message)
    assert alert is None


def test_acknowledge_alert():
    base_service = monitored_service_fixture()
    database_adapter = DatabaseAdapter({})
    database_adapter.update_service(base_service)

    ps = PagerService(database_adapter=database_adapter)
    message = "Something went wrong!"

    alert_id = ps.raise_alert(base_service.service_id, message)

    ps.acknowledge_alert(alert_id)

    alert = ps.database_adapter.get_alert(alert_id)
    assert alert.acknowledged
    assert not alert.resolved
    assert alert.acknowledged_at is not None
    assert alert.resolved_at is None


def test_acknowledge_nonexistent_alert():
    ps = PagerService()
    try:
        ps.acknowledge_alert('nonexistent_alert')
        assert False
    except Exception as e:
        assert str(e) == "Not found"


def test_resolve_alert():
    base_service = monitored_service_fixture()
    database_adapter = DatabaseAdapter({})
    database_adapter.update_service(base_service)

    ps = PagerService(database_adapter=database_adapter)
    message = "Something went wrong!"

    alert_id = ps.raise_alert(base_service.service_id, message)

    ps.resolve_alert(alert_id)

    alert = ps.database_adapter.get_alert(alert_id)
    assert alert.acknowledged
    assert alert.resolved
    assert alert.acknowledged_at is not None
    assert alert.resolved_at is not None

    service = ps.database_adapter.get_service_by_id(base_service.service_id)
    assert service.is_healthy()


def test_resolve_nonexistent_alert():
    ps = PagerService()
    try:
        ps.resolve_alert('nonexistent_alert')
        assert False
    except Exception as e:
        assert str(e) == "Not found"


def test_timeout_callback_not_acknowledged():
    base_service = monitored_service_fixture()
    database_adapter = DatabaseAdapter({})
    database_adapter.update_service(base_service)

    ps = PagerService(database_adapter=database_adapter)
    message = "Something went wrong!"

    alert_id = ps.raise_alert(base_service.service_id, message)
    alert = ps.database_adapter.get_alert(alert_id)

    assert alert.escalation_level == 0

    notifications = len(ps.database_adapter.notifications)
    assert notifications == 1

    ps.timeout_callback(alert_id)
    assert alert.escalation_level == 1
    assert len(ps.database_adapter.notifications) == notifications + 1

    service = ps.database_adapter.get_service_by_id(base_service.service_id)
    assert not service.is_healthy()


def test_timeout_callback_acknowledged():
    base_service = monitored_service_fixture()
    database_adapter = DatabaseAdapter({})
    database_adapter.update_service(base_service)

    ps = PagerService(database_adapter=database_adapter)
    message = "Something went wrong!"

    alert_id = ps.raise_alert(base_service.service_id, message)

    notifications = len(ps.database_adapter.notifications)
    assert notifications == 1

    ps.acknowledge_alert(alert_id)
    ps.timeout_callback(alert_id)

    alert = ps.database_adapter.get_alert(alert_id)
    assert len(ps.database_adapter.notifications) == notifications
    assert alert.escalation_level == 0

    service = ps.database_adapter.get_service_by_id(base_service.service_id)
    assert not service.is_healthy()
